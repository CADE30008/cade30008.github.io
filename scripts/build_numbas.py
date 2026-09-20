"""Turn a quiz written as YAML into a Numbas .exam file, and a readable draft.

    python scripts/build_numbas.py private/diagnostic/week1-diagnostic.yaml

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

import json
import re
import sys
from pathlib import Path

import yaml

# What each numeric answer should be, recomputed rather than trusted.
CHECKS = {
    ("wn-zeta", 0): lambda ct, np: np.sqrt(25),
    ("wn-zeta", 1): lambda ct, np: 4 / (2 * np.sqrt(25)),
    ("steady-state", 0): lambda ct, np: float(ct.dcgain(ct.tf(3, [1, 2]))),
    ("steady-state-error", 0): lambda ct, np: 1 / (1 + float(ct.dcgain(ct.tf(4, [1, 1])))),
}


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
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)


def html(text: str) -> str:
    """The YAML is plain text with LaTeX; Numbas wants HTML.

    A blank line starts a new paragraph, and a run of lines beginning "- "
    becomes a numbered list, so advice can set out steps rather than one dense
    block. Emphasis is converted per block, after the structure is decided, so
    an unclosed marker can never reach past its own paragraph or list item.
    """
    text = str(text).strip()
    if text.startswith("<"):
        return text
    out = []
    for block in re.split(r"\n\s*\n", text):
        lines = [ln.strip() for ln in block.strip().splitlines() if ln.strip()]
        if not lines:
            continue
        if all(ln.startswith("- ") for ln in lines):
            out.append("<ol>" + "".join(f"<li>{emphasis(ln[2:])}</li>" for ln in lines) + "</ol>")
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


def advice_html(q: dict) -> str:
    """The worked route, shown to everyone.

    Numbas shows `advice` regardless of whether the answer was right, which is
    what makes it the place for the method: the student who got it right sees
    the reasoning they should have used, and the student who did not sees how to
    get there. Common wrong values are appended for numeric questions, where
    there is no per-choice feedback to carry them.
    """
    parts = [html(q["advice"])]
    if q.get("common_errors"):
        rows = "".join(f"<li><strong>{emphasis(e['value'])}</strong> — {emphasis(e['why'])}</li>"
                       for e in q["common_errors"])
        parts.append(f"<p>If you got one of these:</p><ul>{rows}</ul>")
    return "".join(parts)


def question(q: dict) -> dict:
    parts = [choice_part(q)] if q["type"] == "choice" else number_parts(q)
    return {
        "name": q["name"],
        "tags": [],
        "metadata": {"description": html(q.get("checks", "")), "licence": "None specified"},
        "statement": html(q["statement"]),
        "advice": advice_html(q),
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
    body = {
        "name": quiz["name"],
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
            "showactualmark": True,
            "showtotalmark": True,
            "showanswerstate": True,
            "allowrevealanswer": True,
            "advicethreshold": 0,
            "intro": html(quiz["description"]),
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
    return "\n".join(out).strip()


def main() -> None:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "private/diagnostic/week1-diagnostic.yaml")
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
    print(f"  upload to Numbas:  {out}")
    if md.exists():
        print(f"  read, don't upload: {md}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
