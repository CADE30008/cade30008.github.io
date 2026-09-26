"""Turn the diagnostic YAML into things Blackboard Ultra will accept.

    python scripts/build_blackboard.py diagnostics/prerequisites.yaml

Writes three things into diagnostics/blackboard/, in the order you should try
them:

    PROBE.zip                 eight small questions, each isolating one thing
                              we do not know about this institution's Ultra.
                              Import first; it takes two minutes to read.
    prerequisites-qti.zip     the whole diagnostic as a QTI 2.1 package, for
                              import as a question bank.
    prerequisites-upload.txt  the whole diagnostic as Ultra's tab-delimited
                              question upload. No feedback and no images, but
                              it goes straight into a test and cannot fail on
                              anything subtle.

Ultra takes questions by two routes and they are not equivalent.

  Question upload, a tab-delimited .txt, goes straight into a test. It carries
  every question type we need, including NUM. It carries no feedback at all and
  the documentation says images are not supported.

  A QTI 2.1 package goes into a question bank, not a test. Anthology's
  documentation lists only Multiple Choice, True/False, Fill in the Blank and
  Essay as supported on import, and says questions "using the optional QTI
  response processing are skipped". So the numeric questions may well not
  arrive; they are written out anyway, because a question that is skipped costs
  nothing and the documentation is the kind that is worth checking.

Three things about Ultra decide whether this route is usable at all, and none
can be settled from the documentation. PROBE.zip settles them:

  1. Does \\( ... \\) render? Ultra renders LaTeX through MathJax, but that is
     an institution-level setting rather than something always on. If it is
     off, every question here is unreadable and the maths has to go through the
     WIRIS editor by hand, one equation at a time.
  2. Does per-answer feedback survive a QTI import? Ultra has the feature - and
     it is mutually exclusive with question-level feedback, which is why the
     worked route is appended to every option below rather than set once. But
     nothing says whether an imported package can populate it.
  3. Do the figures arrive? Three questions have one, and two of those are
     unanswerable without it.

The generated HTML is parsed as XML before it is written, so a stray < in the
prose - "\\( \\zeta < 0.707 \\)" is in there - fails the build rather than the
import.
"""

from __future__ import annotations

import base64
import re
import sys
import zipfile
from html import escape
from pathlib import Path
from xml.etree import ElementTree

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_numbas import html as md_html  # noqa: E402  the same Markdown-ish subset

OUT = ROOT / "diagnostics" / "blackboard"

QTI_NS = "http://www.imsglobal.org/xsd/imsqti_v2p1"
CP_NS = "http://www.imsglobal.org/xsd/imscp_v1p1"


# ---------------------------------------------------------------- text


def xhtml(text: str) -> str:
    """The YAML's text as the XHTML subset QTI allows.

    Escaping happens before the Markdown conversion, not after, so the tags
    this adds are the only ones in the result. Doing it the other way round
    would escape the tags too.
    """
    return md_html(escape(str(text), quote=False))


def inline(text: str) -> str:
    """The same conversion, for somewhere a <p> would be wrong: a list item,
    a label, a run of prose inside a sentence."""
    out = xhtml(text)
    return out[3:-4] if out.startswith("<p>") and out.count("<p>") == 1 else out


def img(rel: str, alt: str, *, embed: bool) -> tuple[str, str | None]:
    """A figure, either as a file in the package or inlined as a data URI.

    Which of the two Blackboard keeps is one of the things PROBE.zip asks, so
    both are generated and the answer decides which the real package uses.
    Returns the markup and the file to add to the package, if any.
    """
    src = ROOT / rel
    if not src.exists():
        raise SystemExit(f"image {rel} not found")
    if not alt.strip():
        raise SystemExit(f"{rel} needs alt text, or it is unusable to a screen reader")
    a = escape(alt, quote=True)
    if embed:
        b64 = base64.b64encode(src.read_bytes()).decode()
        return f'<p><img src="data:image/png;base64,{b64}" alt="{a}"/></p>', None
    name = Path(rel).name
    return f'<p><img src="{name}" alt="{a}"/></p>', rel


# ---------------------------------------------------------------- QTI items


ITEM = """<?xml version="1.0" encoding="UTF-8"?>
<assessmentItem xmlns="{qti}"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="{qti} http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1.xsd"
    identifier="{ident}" title="{title}" adaptive="false" timeDependent="false">
{body}
</assessmentItem>
"""


def choice_item(ident: str, title: str, stem: str, options: list[dict],
                *, feedback: str = "inline") -> str:
    """One multiple-choice item, with feedback on every option.

    `feedback` picks where the per-option text is written. QTI has two places
    for it and Blackboard documents neither, so the probe tries both:

        inline   a <feedbackInline> inside each <simpleChoice>
        modal    a <modalFeedback> per choice, after the body
        both     both at once
        none     no feedback, as a control

    The response processing is the standard match_correct template rather than
    rules written out, because Blackboard skips questions that carry their own.
    """
    correct = next(o for o in options if o.get("correct"))
    decls = [
        f'  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">',
        f'    <correctResponse><value>{correct["id"]}</value></correctResponse>',
        f'  </responseDeclaration>',
        f'  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">',
        f'    <defaultValue><value>0</value></defaultValue>',
        f'  </outcomeDeclaration>',
    ]
    if feedback in ("inline", "modal", "both"):
        decls.append('  <outcomeDeclaration identifier="FEEDBACK" cardinality="single"'
                     ' baseType="identifier"/>')

    choices, modals = [], []
    for o in options:
        inner = o["text"]
        if feedback in ("inline", "both"):
            inner += (f'<feedbackInline outcomeIdentifier="FEEDBACK" identifier="{o["id"]}"'
                      f' showHide="show">{o["why"]}</feedbackInline>')
        choices.append(f'        <simpleChoice identifier="{o["id"]}">{inner}</simpleChoice>')
        if feedback in ("modal", "both"):
            modals.append(f'  <modalFeedback outcomeIdentifier="FEEDBACK"'
                          f' identifier="{o["id"]}" showHide="show">{o["why"]}</modalFeedback>')

    body = "\n".join([
        *decls,
        "  <itemBody>",
        f"    {stem}",
        '    <choiceInteraction responseIdentifier="RESPONSE" shuffle="false" maxChoices="1">',
        *choices,
        "    </choiceInteraction>",
        "  </itemBody>",
        '  <responseProcessing template="http://www.imsglobal.org/question/qti_v2p1'
        '/rptemplates/match_correct.xml"/>',
        *modals,
    ])
    return ITEM.format(qti=QTI_NS, ident=ident, title=escape(title, quote=True), body=body)


def numeric_item(ident: str, title: str, stem: str, value: float, tol: float) -> str:
    """One numeric item, which the documentation says will probably be skipped.

    Written as the plainest numeric item QTI 2.1 allows: a float response, the
    standard match_correct template, and the tolerance carried in the stem
    rather than in a mapping, since a mapping is response processing of the
    kind Blackboard skips. If Blackboard drops it we lose nothing; if it keeps
    it, the numeric questions need no rewriting.
    """
    body = "\n".join([
        '  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="float">',
        f'    <correctResponse><value>{value:g}</value></correctResponse>',
        '  </responseDeclaration>',
        '  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">',
        '    <defaultValue><value>0</value></defaultValue>',
        '  </outcomeDeclaration>',
        '  <itemBody>',
        f'    {stem}',
        '    <p><textEntryInteraction responseIdentifier="RESPONSE" expectedLength="8"/></p>',
        '  </itemBody>',
        '  <responseProcessing template="http://www.imsglobal.org/question/qti_v2p1'
        '/rptemplates/match_correct.xml"/>',
    ])
    body = "\n".join(ln for ln in body.splitlines() if ln.strip())
    return ITEM.format(qti=QTI_NS, ident=ident, title=escape(title, quote=True), body=body)


def package(path: Path, items: dict[str, str], assets: dict[str, Path]) -> None:
    """Zip the items and their figures with a manifest, checking the XML first.

    A resource declares the figures that item refers to and no others, found by
    reading the item back rather than tracked alongside it, so the two cannot
    disagree.
    """
    for name, text in items.items():
        try:
            ElementTree.fromstring(text)
        except ElementTree.ParseError as e:
            raise SystemExit(f"{name}: not well-formed XML - {e}")

    resources = []
    for name, text in items.items():
        ident = Path(name).stem
        used = [a for a in assets if f'src="{a}"' in text]
        files = "".join(f'<file href="{a}"/>' for a in used)
        resources.append(
            f'    <resource identifier="res-{ident}" type="imsqti_item_xmlv2p1" href="{name}">\n'
            f'      <file href="{name}"/>{files}\n'
            f'    </resource>')
    manifest = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<manifest xmlns="{CP_NS}"\n'
        '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
        f'    xsi:schemaLocation="{CP_NS}'
        ' http://www.imsglobal.org/xsd/qti/qtiv2p1/imscp_v1p2_v1p0.xsd"\n'
        f'    identifier="{path.stem}">\n'
        '  <organizations/>\n'
        '  <resources>\n' + "\n".join(resources) + '\n  </resources>\n'
        '</manifest>\n')
    ElementTree.fromstring(manifest)

    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("imsmanifest.xml", manifest)
        for name, text in items.items():
            z.writestr(name, text)
        for name, src in assets.items():
            z.write(src, name)
    print(f"  {path.relative_to(ROOT)}  ({len(items)} items, {len(assets)} figures,"
          f" {path.stat().st_size // 1024} kB)")


# ---------------------------------------------------------------- the probe

# Each probe asks one question of Ultra and nothing else, so that a single
# import tells you which parts of the real package will survive. Every stem
# says what to look for and every option's feedback names what it proves, so
# the findings can be read straight off the screen without this file open.

PROBE_OPTIONS = [
    {"id": "yes", "text": "Yes", "correct": True},
    {"id": "no", "text": "No"},
]


def probe_options(proof: str) -> list[dict]:
    """The two options. `proof` is block-level HTML, so a probe can put a
    figure or a list in the feedback rather than only a sentence."""
    yes = dict(PROBE_OPTIONS[0], why=f"<p><strong>Per-option feedback works.</strong></p>{proof}")
    no = dict(PROBE_OPTIONS[1], why="<p>You picked No, and this text is the feedback attached "
                                    "to that option alone. If you can read it, per-option "
                                    "feedback survived the import.</p>")
    return [yes, no]


MATHML = ('<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mn>1</mn>'
          '<mrow><mi>s</mi><mo>+</mo><mn>2</mn></mrow></mfrac></math>')


RICH_FEEDBACK = "".join([
    '<p><strong>Structure survived.</strong> Check each of these against what you '
    'wrote in the file:</p>',
    '<ol><li>A numbered list, with <strong>bold</strong> and <em>italic</em> inside it.</li>',
    '<li>Maths in a list item: \\( \\zeta = 0.4 \\) gives about 25% overshoot.</li>',
    '<li>A link to the '
    '<a href="https://cade30008.github.io/notation/" target="_blank" '
    'rel="noopener">notation page</a>.</li></ol>',
    '<p style="font-weight:700">Try it in MATLAB</p>',
    '<p style="font-family:ui-monospace,Menlo,monospace;white-space:pre">s  = tf(\'s\');</p>',
    '<p style="font-family:ui-monospace,Menlo,monospace;white-space:pre">'
    'G  = 10/(s + 10);</p>',
    '<p style="font-family:ui-monospace,Menlo,monospace;white-space:pre">bode(G), grid on</p>',
])


def probe_items() -> tuple[dict[str, str], dict[str, Path]]:
    items: dict[str, str] = {}
    assets: dict[str, Path] = {}
    packaged, src = img("diagnostics/figures/first-order-lag.png",
                        "Bode plot of a first-order lag, used here only to test whether an "
                        "image survives import.", embed=False)
    assets[Path(src).name] = ROOT / src
    embedded, _ = img("diagnostics/figures/overshoot-vs-damping.png",
                      "Overshoot against damping ratio, used here only to test whether a "
                      "base64 image survives import.", embed=True)

    def add(n: int, title: str, stem: str, proof: str, **kw) -> None:
        items[f"probe-{n:02d}.xml"] = choice_item(
            f"probe-{n:02d}", f"{n}. {title}", stem, probe_options(proof), **kw)

    add(1, "Inline LaTeX",
        '<p>Does the next line show a fraction, or backslashes and braces?</p>'
        '<p>A first-order lag is \\( G(s) = \\dfrac{1}{1 + s/\\omega_\\mathrm{c}} \\), '
        'with its corner at \\( \\omega_\\mathrm{c} \\).</p>'
        '<p><strong>Answer Yes if it is a typeset fraction.</strong></p>',
        '<p>MathJax is on, and every \\( ... \\) in the diagnostic will render. '
        'Feedback maths too: \\( -3 \\) dB and \\( -45^\\circ \\).</p>')

    add(2, "Display LaTeX",
        '<p>Does the next line sit centred on its own, as an equation?</p>'
        '<p>$$ M_\\mathrm{p} = e^{-\\pi\\zeta/\\sqrt{1-\\zeta^2}} $$</p>'
        '<p><strong>Answer Yes if it is typeset and centred.</strong></p>',
        '<p>Display maths works, so the worked routes can set equations out on their '
        'own line.</p>')

    add(3, "MathML",
        f'<p>Does the next line show a fraction?</p><p>{MATHML}</p>'
        '<p><strong>Answer Yes if it is a typeset fraction.</strong></p>'
        '<p>This is the fallback if question 1 failed: MathML is what the WIRIS editor '
        'built into Ultra produces, so it should render whatever MathJax is set to.</p>',
        '<p>MathML renders. If question 1 failed and this one worked, the build can emit '
        'MathML instead of LaTeX.</p>')

    add(4, "Figure, as a file in the package",
        '<p>Is there a Bode plot below this line?</p>' + packaged +
        '<p><strong>Answer Yes if you can see the plot.</strong></p>',
        '<p>Figures referenced as files in the package survive, which is the cheaper of '
        'the two ways: one file, however many questions point at it.</p>')

    add(5, "Figure, inlined as a data URI",
        '<p>Is there a plot of overshoot against damping below this line?</p>' + embedded +
        '<p><strong>Answer Yes if you can see the plot.</strong></p>',
        '<p>Inlined figures survive, so the package needs no separate files.</p>')

    add(6, "Per-option feedback, written inline",
        '<p>This question carries its feedback as a <em>feedbackInline</em> element inside '
        'each option. Answer either way, submit, and see whether you get back the text '
        'belonging to the option you picked.</p>',
        '<p>The inline form is the one to use.</p>', feedback="inline")

    add(7, "Per-option feedback, written as modal feedback",
        '<p>The same thing again, written the other way QTI allows: a <em>modalFeedback</em> '
        'element per option. Answer either way and compare what comes back with question 6.</p>',
        '<p>The modal form is the one to use.</p>', feedback="modal")

    items["probe-08.xml"] = choice_item(
        "probe-08", "8. Rich feedback",
        '<p>The worked routes are not one paragraph. They have headings, numbered steps, '
        'bold, links and a MATLAB snippet in them. Answer either way and see how much of '
        'that structure comes back.</p>',
        [{"id": "yes", "text": "Yes", "correct": True, "why": RICH_FEEDBACK},
         {"id": "no", "text": "No", "why": RICH_FEEDBACK}])

    add(9, "Figure inside feedback",
        '<p>Three of the worked routes are carried by a figure rather than by prose. '
        'Answer either way; the feedback should contain a Bode plot.</p>',
        '<p>A figure in the feedback survives.</p>' + packaged)

    items["probe-10.xml"] = numeric_item(
        "probe-10", "10. A numeric question",
        '<p>The documentation lists only multiple choice, true/false, fill in the blank and '
        'essay as supported on import, so this question may simply not be here. If it is, '
        'four questions in the diagnostic can stay numeric instead of becoming '
        'multiple choice.</p><p>What is \\( 3/2 \\)? Answer to within 0.01.</p>',
        1.5, 0.01)
    return items, assets


# ---------------------------------------------------------------- the real thing


def worked_route(q: dict, assets: dict[str, Path]) -> str:
    """The method, the figure, the common wrong values and the working.

    The same material Numbas puts behind "Show steps". Ultra has no equivalent:
    nothing is shown during an attempt, so this can only arrive afterwards.

    It is appended to every option's feedback rather than set once at question
    level, because Ultra's two kinds of feedback are mutually exclusive and
    per-option is the one carrying the diagnosis. The cost is that the file
    repeats itself four times over; nobody reads the file.
    """
    parts = [xhtml(q["advice"])]
    if q.get("steps_image"):
        markup, src = img(q["steps_image"], q.get("steps_image_alt", ""), embed=False)
        assets[Path(src).name] = ROOT / src
        parts.append(markup)
    if q.get("common_errors"):
        rows = "".join(f"<li><strong>{inline(e['value'])}</strong>: "
                       f"{inline(e['why'])}</li>" for e in q["common_errors"])
        parts.append(f"<p>If you got one of these:</p><ol>{rows}</ol>")
    if q.get("worked"):
        parts.append('<p><strong>Working, step by step</strong></p>' + xhtml(q["worked"]))
    if q.get("code"):
        caption = escape(q.get("code_caption", "Try it in MATLAB"))
        rows = "".join(
            f'<p style="font-family:ui-monospace,Menlo,monospace;white-space:pre">'
            f'{escape(ln) if ln.strip() else "&#160;"}</p>'
            for ln in q["code"].rstrip().split("\n"))
        parts.append(f'<p><strong>{caption}</strong></p>{rows}')
    return ('<p><strong>The worked route</strong></p>' + "".join(parts))


def full_package(quiz: dict, path: Path, feedback: str) -> None:
    items: dict[str, str] = {}
    assets: dict[str, Path] = {}
    skipped: list[str] = []

    for n, q in enumerate(quiz["questions"], 1):
        stem = xhtml(q["statement"])
        if q.get("image"):
            markup, src = img(q["image"], q.get("image_alt", ""), embed=False)
            assets[Path(src).name] = ROOT / src
            stem += markup
        route = worked_route(q, assets)

        if q["type"] == "choice":
            options = [{"id": f"opt{i}", "text": xhtml(c["text"]),
                        "correct": bool(c.get("correct")),
                        "why": xhtml(c["why"]) + route}
                       for i, c in enumerate(q["choices"], 1)]
            items[f"q{n:02d}-{q['id']}.xml"] = choice_item(
                f"q{n:02d}-{q['id']}", f"{n}. {q['name']}", stem, options, feedback=feedback)
        else:
            # One item per answer: QTI has no two-box numeric question, and
            # Ultra's own numeric type takes a single value too.
            for j, a in enumerate(q["answers"], 1):
                tol = float(a.get("tolerance", 0))
                label = inline(a["label"])
                suffix = f" ({j} of {len(q['answers'])})" if len(q["answers"]) > 1 else ""
                items[f"q{n:02d}-{q['id']}-{j}.xml"] = numeric_item(
                    f"q{n:02d}-{q['id']}-{j}", f"{n}. {q['name']}{suffix}",
                    stem + f"<p>Give {label}, to within {tol:g}.</p>",
                    float(a["value"]), tol)
            skipped.append(q["id"])

    package(path, items, assets)
    if skipped:
        print(f"    numeric, and likely dropped on import: {', '.join(skipped)}")


# ---------------------------------------------------------------- question upload


def plain(text: str) -> str:
    """Strip the text back to one line of characters a tab-delimited file can hold.

    The upload file has no HTML and no images, so the markup goes and the maths
    is left as LaTeX: it either renders through MathJax or it does not, which is
    the same question probe 1 asks. Tabs and newlines would end the field early.
    """
    # Only real tags, named. "<[^>]+>" looks equivalent and eats the prose
    # between a less-than in the maths and the next greater-than: "\\( \\zeta <
    # 0.707 \\) and \\( \\omega > 1 \\)" came out as "\\( \\zeta 1 \\)".
    text = re.sub(r"</?(?:p|strong|em|b|i|a|ol|ul|li|br|img|hr)\b[^>]*>", "", str(text))
    text = re.sub(r"\*{1,2}(.+?)\*{1,2}", r"\1", text)      # bold and italic markers
    return re.sub(r"\s+", " ", text).strip()


def upload_txt(quiz: dict, path: Path) -> None:
    rows = []
    for q in quiz["questions"]:
        stem = plain(q["statement"])
        if q.get("image"):
            stem += "  [FIGURE: add by hand - the upload file cannot carry images]"
        if q["type"] == "choice":
            fields = ["MC", stem]
            for c in q["choices"]:
                fields += [plain(c["text"]), "correct" if c.get("correct") else "incorrect"]
            rows.append(fields)
        else:
            for a in q["answers"]:
                label = plain(a["label"])
                rows.append(["NUM", f"{stem} Give {label}.",
                             f"{float(a['value']):g}", f"{float(a.get('tolerance', 0)):g}"])
    path.write_text("\n".join("\t".join(f) for f in rows) + "\n", encoding="utf-8")
    print(f"  {path.relative_to(ROOT)}  ({len(rows)} questions, no feedback, no figures)")


def main() -> None:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "diagnostics/prerequisites.yaml")
    quiz = yaml.safe_load((ROOT / src).read_text(encoding="utf-8"))
    feedback = next((a.split("=", 1)[1] for a in sys.argv[2:]
                     if a.startswith("--feedback=")), "both")

    print("Blackboard Ultra:")
    items, assets = probe_items()
    package(OUT / "PROBE.zip", items, assets)
    full_package(quiz, OUT / "prerequisites-qti.zip", feedback)
    upload_txt(quiz, OUT / "prerequisites-upload.txt")


if __name__ == "__main__":
    main()

# tracking: status=draft version=0
