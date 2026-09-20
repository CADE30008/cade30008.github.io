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


def html(text: str) -> str:
    """The YAML is plain text with LaTeX; Numbas wants HTML."""
    text = text.strip()
    return text if text.startswith("<") else f"<p>{text}</p>"


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
        "distractors": ["" for _ in choices],
    }


def number_parts(q: dict) -> list[dict]:
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


def question(q: dict) -> dict:
    parts = [choice_part(q)] if q["type"] == "choice" else number_parts(q)
    return {
        "name": q["name"],
        "tags": [],
        "metadata": {"description": html(q.get("checks", "")), "licence": "None specified"},
        "statement": html(q["statement"]),
        "advice": html(q["advice"]),
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
                out.append(f"- {c['text'].strip()}" + ("  ← correct" if c.get("correct") else ""))
        else:
            for a in q["answers"]:
                out.append(f"- {a['label']}: **{a['value']:g}** (tolerance ±{a.get('tolerance', 0):g})")
        out += ["", f"*Checks:* {q['checks']}", "", f"*Feedback:* {q['advice'].strip()}", ""]
    return "\n".join(out).strip()


def main() -> None:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "private/diagnostic/week1-diagnostic.yaml")
    quiz = yaml.safe_load(src.read_text(encoding="utf-8"))

    problems = check_answers(quiz)
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
    print(f"\n{len(problems)} error(s); {n} questions, {marks} marks -> {out}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
