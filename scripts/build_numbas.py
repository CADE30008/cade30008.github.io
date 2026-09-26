"""Turn a quiz written as YAML into a Numbas .exam file, and a readable draft.

    python scripts/build_numbas.py diagnostics/prerequisites.yaml

Writes <name>.exam beside the source, for upload to the Numbas editor, and
fills the question list in <name>.md between its markers, so the readable draft
and the thing students sit can't drift apart.

Two question types, which is all a diagnostic needs:

    type: choice    one correct answer from several (Numbas "1_n_2")
    type: numbers   one or more numeric answers with tolerances ("numberentry")

Every numeric answer is re-checked against python-control on each build, from
the `check` expressions in this file, so a value can't rot quietly.

The .exam format is the Numbas editor's own: a header comment, then JSON. The
editor fills in anything omitted, so this writes the fields that matter and
leaves the rest to defaults.
"""

from __future__ import annotations

import base64
import json
import re
import sys
from html import escape
from html import escape as attr
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# What each numeric answer should be, recomputed rather than trusted.
CHECKS = {
    ("wn-zeta", 0): lambda ct, np: np.sqrt(25),
    ("wn-zeta", 1): lambda ct, np: 4 / (2 * np.sqrt(25)),
    ("steady-state", 0): lambda ct, np: float(ct.dcgain(ct.tf(3, [1, 2]))),
    ("steady-state-error", 0): lambda ct, np: 1 / (1 + float(ct.dcgain(ct.tf(4, [1, 1])))),
    # Read back off the same system the figure plots, so the question, the
    # picture and the answer cannot drift apart: omega_n is where the phase
    # crosses -90 degrees, and zeta comes from the height of the peak.
    ("bode-second-order", 0): lambda ct, np: _bode_read(ct, np)[0],
    ("bode-second-order", 1): lambda ct, np: _bode_read(ct, np)[1],
}


def _bode_read(ct, np) -> tuple[float, float]:
    import sys
    sys.path.insert(0, str(ROOT))
    from models.diagnostic_bode import WN, ZETA
    G = ct.tf([WN**2], [1, 2 * ZETA * WN, WN**2])
    w = np.geomspace(0.2, 60, 20000)
    mag, ph, w = ct.frequency_response(G, w)
    wn = float(w[np.argmin(abs(ph * 180 / np.pi + 90))])       # phase crossing
    mr = float(mag.max())                                       # resonant peak
    zeta = float(np.roots([4, -4, 1 / mr**2]).min() ** 0.5)     # Mr = 1/(2 z sqrt(1-z^2))
    return round(wn, 3), round(zeta, 3)


def check_feedback(quiz: dict) -> list[str]:
    """Every option must carry feedback, right and wrong alike.

    A wrong option with nothing to say is filler, and filler makes the cohort
    results meaningless: you cannot tell a misconception from a shrug.
    """
    problems = []
    for q in quiz["questions"]:
        for i, c in enumerate(q.get("choices", []), 1):
            if not str(c.get("why", "")).strip():
                problems.append(f"{q['id']} choice {i} ({c['text'][:30]}...): no `why`")
        if not str(q.get("advice", "")).strip():
            problems.append(f"{q['id']}: no advice")
    return problems


def check_answers(quiz: dict) -> list[str]:
    try:
        import control as ct
        import numpy as np
    except ImportError:
        return ["python-control not available: numeric answers were not re-checked"]
    problems = []
    for q in quiz["questions"]:
        for i, a in enumerate(q.get("answers", [])):
            fn = CHECKS.get((q["id"], i))
            if fn is None:
                problems.append(f"{q['id']} answer {i + 1}: no check in build_numbas.py")
                continue
            want = float(fn(ct, np))
            if abs(want - float(a["value"])) > 1e-9:
                problems.append(f"{q['id']} answer {i + 1}: file says {a['value']}, computed {want:g}")
    return problems



# LaTeX is passed through untouched: \( ... \) and $$ ... $$ may contain
# characters that would otherwise be read as Markdown.
MATHS = re.compile(r"(\$\$.*?\$\$|\\\(.*?\\\))", re.S)


def emphasis(text: str) -> str:
    """Markdown emphasis to HTML, leaving maths alone.

    Numbas renders HTML, not Markdown, so **bold** and *italic* in the YAML
    would otherwise reach students as literal asterisks.

    The maths is stashed behind placeholders rather than split out and rejoined.
    Splitting looks equivalent and is not: bold that *contains* maths - which is
    most of the bold in this file - would have its opening and closing markers
    land in different chunks, so neither could pair. The orphans then paired
    with markers from elsewhere and produced <strong> tags spanning </li><li>.
    """
    stash: list[str] = []

    def keep(m: re.Match) -> str:
        stash.append(m.group(0))
        return f"\x00{len(stash) - 1}\x00"

    text = MATHS.sub(keep, text)
    # [label](url) -> a link. Numbas keeps <a>, and without this the brackets
    # reach the student literally.
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
                  r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)


def html(text: str) -> str:
    """The YAML is plain text with LaTeX; Numbas wants HTML.

    A blank line starts a new paragraph, and a block whose first line begins
    "- " becomes a numbered list, so advice can set out steps rather than one
    dense block. Emphasis is converted per block, after the structure is
    decided, so an unclosed marker can never reach past its own paragraph or
    list item.

    A list item may wrap onto further lines, which are folded back into it.
    Testing every line for "- " instead, as this did first, meant one wrapped
    item turned the whole list into a paragraph with the dashes left in the
    middle of the prose - no error, just a run-on sentence in the worked
    solution.
    """
    text = str(text).strip()
    if text.startswith("<"):
        return text
    out = []
    for block in re.split(r"\n\s*\n", text):
        lines = [ln.strip() for ln in block.strip().splitlines() if ln.strip()]
        if not lines:
            continue
        if lines[0].startswith("- "):
            items: list[str] = []
            for ln in lines:
                if ln.startswith("- "):
                    items.append(ln[2:])
                else:
                    items[-1] += " " + ln          # a wrapped item, not a new one
            out.append("<ol>" + "".join(f"<li>{emphasis(i)}</li>" for i in items) + "</ol>")
        else:
            out.append(f"<p>{emphasis(' '.join(lines))}</p>")
    return "".join(out)


def choice_part(q: dict) -> dict:
    choices = q["choices"]
    return {
        "type": "1_n_2",
        "marks": 1,
        "showCorrectAnswer": True,
        "showFeedbackIcon": True,
        "minMarks": 0,
        "maxMarks": 0,
        "shuffleChoices": False,          # AP11: everyone sees the same thing
        "displayType": "radiogroup",
        "displayColumns": 0,
        "showCellAnswerState": True,
        "choices": [html(c["text"]) for c in choices],
        "matrix": ["1" if c.get("correct") else "0" for c in choices],
        # Per-choice feedback. Every option carries one, right and wrong alike:
        # a student who guessed correctly learns why it was right, and a student
        # who missed it is told which misconception they have rather than only
        # that they are wrong. Each wrong option is chosen to be a real error
        # someone makes, not filler.
        "distractors": [html(c["why"]) for c in choices],
    }


def number_parts(q: dict) -> list[dict]:
    """Numeric parts have no per-choice feedback, so the common wrong values are
    folded into the shared advice instead (see `advice_html`)."""
    parts = []
    for a in q["answers"]:
        value, tol = float(a["value"]), float(a.get("tolerance", 0))
        parts.append({
            "type": "numberentry",
            "marks": 1,
            "showCorrectAnswer": True,
            "showFeedbackIcon": True,
            "prompt": html(a["label"]),
            "minValue": f"{value - tol:g}",
            "maxValue": f"{value + tol:g}",
            "correctAnswerFraction": False,
            "allowFractions": False,
            "mustBeReduced": False,
            "notationStyles": ["plain", "en", "si-en"],
        })
    return parts


def embed_image(qid: str, rel: str, alt: str) -> str:
    """A figure, base64'd into the .exam rather than linked.

    A link would need somewhere to host it, would break the moment that moved,
    and would leave the quiz depending on something outside the file we hand
    over. Embedding costs 60-90 kB a figure, which against a 30 kB exam is a
    lot proportionally and nothing absolutely.
    """
    src = ROOT / rel
    if not src.exists():
        raise SystemExit(f"{qid}: image {rel} not found")
    if not alt.strip():
        raise SystemExit(f"{qid}: {rel} needs alt text, or it is unusable to a screen reader")
    b64 = base64.b64encode(src.read_bytes()).decode()
    # Escape the alt text. Describing a figure means quoting the labels on it,
    # and an unescaped " closes the attribute early: the rest of the sentence
    # becomes junk attributes and Numbas fails the whole question with
    # "SyntaxError: The string did not match the expected pattern".
    return (f'<p><img src="data:image/png;base64,{b64}" alt="{attr(alt, quote=True)}" '
            f'style="max-width:100%;height:auto"></p>')


def statement_html(q: dict) -> str:
    """The question text, with its figure embedded if it has one."""
    out = html(q["statement"])
    if q.get("image"):
        out += embed_image(q["id"], q["image"], q.get("image_alt", ""))
    return out


def steps_html(q: dict) -> str:
    """Everything beyond the per-option feedback: the method, then the working.

    One channel, not two. The question-level `advice` is left empty. It renders
    only in review mode, at the foot of the page and a long way from the
    question it explains, so the same words do more work here, where a student
    can open them while the question is still in front of them.

    Order follows the way it is read: the method first, then the common wrong
    values for numeric questions, which have no per-choice feedback to carry
    them, and the step-by-step working last because it is the longest.
    """
    parts = [html(q["advice"])]
    # A figure belongs with the explanation it illustrates, before the working.
    if q.get("steps_image"):
        parts.append(embed_image(q["id"], q["steps_image"], q.get("steps_image_alt", "")))
    if q.get("common_errors"):
        rows = "".join(f"<li><strong>{emphasis(e['value'])}</strong>: {emphasis(e['why'])}</li>"
                       for e in q["common_errors"])
        parts.append(f"<p>If you got one of these:</p><ul>{rows}</ul>")
    if q.get("worked"):
        parts.append('<p style="font-weight:700">Working, step by step</p>')
        parts.append(html(q["worked"]))
    if q.get("code"):
        parts.append(code_html(q["code"], q.get("code_caption", "Try it in MATLAB")))
    return "".join(parts)


MONO = ("font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:0.92em;"
        "margin:0.1em 0;white-space:pre")


def code_html(lines: str, caption: str) -> str:
    """A runnable snippet, built only from tags Numbas is known to keep.

    No <pre> or <code>: neither is on the list confirmed to survive its
    sanitiser, and a silently stripped tag here would run the whole snippet
    together on one line. A run of <p> with a monospace inline style is ugly in
    source and reliable in the browser, which is the right way round.
    """
    rows = "".join(f'<p style="{MONO}">{escape(ln) if ln.strip() else "&nbsp;"}</p>'
                   for ln in lines.rstrip().split("\n"))
    return (f'<hr style="border:0;border-top:1px solid #d9dcdb;margin:1em 0">'
            f'<p style="font-weight:700">{caption}</p>{rows}')


def steps_for(q: dict) -> list[dict]:
    """The steps block: one information part, revealed by "Show steps".

    stepsPenalty is zero, so it costs the student nothing. It sits *above* the
    answer options and can be opened before answering; for a formative quiz
    with no marks and no randomisation that is an acceptable trade.
    """
    return [{
        "type": "information",
        "marks": 0,
        "prompt": steps_html(q),
    }]


def question(q: dict) -> dict:
    parts = [choice_part(q)] if q["type"] == "choice" else number_parts(q)
    # Attach the working to the first part; a question has one worked solution.
    parts[0]["steps"] = steps_for(q)
    parts[0]["stepsPenalty"] = 0
    return {
        "name": q["name"],
        "tags": [],
        "metadata": {"description": html(q.get("checks", "")), "licence": "None specified"},
        "statement": statement_html(q),
        "advice": "",   # see steps_html: one channel, and this is not it
        "rulesets": {},
        "extensions": [],
        "builtin_constants": {},
        "constants": [],
        "variables": {},
        "variablesTest": {"condition": "", "maxRuns": 100},
        "ungrouped_variables": [],
        "variable_groups": [],
        "functions": {},
        "preamble": {"js": "", "css": ""},
        "parts": parts,
    }


def exam(quiz: dict) -> str:
    # Uploading an .exam duplicates rather than replaces, so a run of review
    # drafts becomes a list of identically-named exams and the wrong one gets
    # linked from Blackboard. `draft:` in the YAML suffixes the name; clear it
    # for the version that goes live.
    name = quiz["name"] + (f"  (draft {quiz['draft']})" if quiz.get("draft") else "")
    body = {
        "name": name,
        "metadata": {"description": html(quiz["description"]), "licence": "None specified"},
        "duration": 0,                                   # no time limit
        "percentPass": 0,
        "showQuestionGroupNames": False,
        "showstudentname": True,
        "allowPrinting": True,
        "navigation": {
            "allowregen": False,                         # AP11: no reroll
            "reverse": True,
            "browse": True,
            "allowsteps": True,
            "showfrontpage": True,
            "showresultspage": "oncompletion",
            "navigatemode": "sequence",
            "onleave": {"action": "none", "message": ""},
            "preventleave": True,
            "startpassword": "",
        },
        "timing": {"allowPause": True, "timeout": {"action": "none", "message": ""},
                   "timedwarning": {"action": "none", "message": ""}},
        "feedback": {
            # Numbas replaced the old booleans with a timing per kind of
            # feedback: "always", "oncompletion", "inreview" or "never". We
            # were writing the deprecated keys, so everything not named here
            # fell back to its default of "inreview" - which is why the advice
            # never appeared during an attempt.
            #
            # This is formative, so everything that can be immediate is.
            "showactualmarkwhen": "always",
            "showtotalmarkwhen": "always",
            "showanswerstatewhen": "always",
            "showpartfeedbackmessageswhen": "always",
            # These two accept only "inreview" or "never" - Numbas has no
            # setting that shows them mid-attempt. Hence the worked solution
            # living in each part's `steps` instead, which is available on
            # demand. `enterreviewmodeimmediately` then makes the advice
            # visible the moment the quiz is ended, rather than never.
            "showexpectedanswerswhen": "inreview",
            "showadvicewhen": "never",
            "enterreviewmodeimmediately": True,
            # No "Reveal answers" button. Numbas's MultipleResponsePart
            # .revealAnswer() loops over every option unconditionally and posts
            # all of their feedback, so revealing dumps four contradictory
            # paragraphs and repeats the one already shown on submit. The
            # marking algorithm itself is fine: it checks what was chosen.
            #
            # Nothing is lost by removing it. The steps carry the full working,
            # including the answer, at no penalty - which Reveal is not, since
            # it zeroes the score and blocks a re-attempt.
            "allowrevealanswer": False,
            "intro": html(quiz["description"]),
            "end_message": "",
            "results_options": {"printquestions": True, "printadvice": True},
            "feedbackmessages": [],
        },
        "rulesets": {},
        "question_groups": [{
            "name": "",
            "pickingStrategy": "all-ordered",            # AP11: same order for everyone
            "questions": [question(q) for q in quiz["questions"]],
        }],
    }
    return "// Numbas version: exam_results_page_options\n" + json.dumps(body, indent=2, ensure_ascii=False) + "\n"


def markdown(quiz: dict) -> str:
    """The readable version, for checking the wording before it is built."""
    out = []
    for n, q in enumerate(quiz["questions"], 1):
        out += [f"### {n}. {q['name']}", "", q["statement"].strip(), ""]
        if q["type"] == "choice":
            for c in q["choices"]:
                mark = " **← correct**" if c.get("correct") else ""
                out += [f"- {c['text'].strip()}{mark}",
                        f"    <br>*Shown if chosen:* {' '.join(str(c.get('why', '')).split())}"]
        else:
            for a in q["answers"]:
                out.append(f"- {a['label']}: **{a['value']:g}** (tolerance ±{a.get('tolerance', 0):g})")
            for e in q.get("common_errors", []):
                out.append(f"- *Common error* {e['value']}: {' '.join(str(e['why']).split())}")
        out += ["", f"*Checks:* {q['checks']}", "",
                "*Worked route, shown to everyone:*", "", q["advice"].strip(), ""]
        if q.get("worked"):
            out += ["<details><summary><em>Full working, folded away in the quiz</em></summary>", "",
                    q["worked"].strip(), "", "</details>", ""]
    return "\n".join(out).strip()


def main() -> None:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "diagnostics/prerequisites.yaml")
    quiz = yaml.safe_load(src.read_text(encoding="utf-8"))

    problems = check_answers(quiz) + check_feedback(quiz)
    for p in problems:
        print(f"error    {p}")

    out = src.with_suffix(".exam")
    out.write_text(exam(quiz), encoding="utf-8")

    md = src.with_suffix(".md")
    if md.exists():
        text = md.read_text(encoding="utf-8")
        start, end = "<!-- questions:start -->", "<!-- questions:end -->"
        if start in text and end in text:
            i, j = text.index(start), text.index(end)
            md.write_text(text[: i + len(start)] + "\n" + markdown(quiz) + "\n" + text[j:], encoding="utf-8")
        else:
            print(f"warning  {md.name} has no questions markers; its question list was not updated")

    n = len(quiz["questions"])
    marks = sum(len(q.get("answers", [])) or 1 for q in quiz["questions"])
    print(f"\n{len(problems)} error(s); {n} questions, {marks} marks")
    if quiz.get("draft"):
        print(f'  NOTE: name carries "(draft {quiz["draft"]})" — clear `draft:` in the YAML before the live upload')
    print(f"  upload to Numbas:  {out}")
    if md.exists():
        print(f"  read, don't upload: {md}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()

# tracking: status=draft version=0
