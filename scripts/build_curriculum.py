"""Check the curriculum and generate everything derived from it.

Reads curriculum/lectures.yaml (what each lecture is) and
curriculum/schedule-<year>.yaml (which week it falls in), then:

  checks   that the two agree with each other and with the site: every
           lecture scheduled exactly once, none in reading or revision week,
           a folder for every lecture and no orphan folders, the handout, deck,
           example sheet and solutions all carrying the right number and title, the nav matching, every ILO covered,
           the cliffhanger chain unbroken, and P19's budget respected;
  writes   docs/design-cycle/figures/term-map.svg — the term map in Lecture 1;
           planning/lecture-map.html — the planning diagram (not built into
           the site); and the lecture table on the home page, between its
           markers.

Run it with `npm run curriculum`. Exits non-zero if any check fails, so it can
gate the build. Warnings don't fail it.

    python scripts/build_curriculum.py [--year 2026-27]
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CUR = ROOT / "curriculum"
DOCS = ROOT / "docs"
SLIDES = ROOT / "slides"

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


# ------------------------------------------------------------------- checks
def check(lectures: list[dict], schedule: dict) -> dict[int, list[int]]:
    """Validate, and return lecture number -> list of weeks it is scheduled in."""
    # Shape first: a malformed entry makes every later check unreliable. In
    # particular, unquoted text in YAML's {ilo: .., text: ..} form is split at
    # its first comma, silently, which truncates the outcome and invents a key.
    required = {"number", "slug", "title", "act", "question", "focus", "ilos", "capabilities", "threshold",
                "systems", "case", "outcomes", "hook", "in_lecture", "cliffhanger", "out_of_lecture", "budget", "handout_only"}
    slots = {"hook", "block_a", "do_a", "block_b", "do_b", "case"}
    parts = {"close_the_loop", "examples", "next_case"}
    for L in lectures:
        tag = f"lecture {L.get('number', '?')}"
        if missing := required - set(L):
            err(f"{tag}: missing {', '.join(sorted(missing))}")
            continue
        for o in L["outcomes"]:
            if set(o) != {"ilo", "text"}:
                err(f"{tag}: malformed outcome {o!r} — quote text containing commas")
            elif o["ilo"] not in (4, 5, 6):
                err(f"{tag}: outcome serves ILO {o['ilo']}; this half covers 4 to 6")
        if missing := slots - set(L["in_lecture"]):
            err(f"{tag}: in_lecture lacks {', '.join(sorted(missing))}")
        if missing := parts - set(L["out_of_lecture"]):
            err(f"{tag}: out_of_lecture lacks {', '.join(sorted(missing))}")
    if errors:
        return {}

    by_num = {L["number"]: L for L in lectures}
    nums = [L["number"] for L in lectures]
    if nums != list(range(1, len(nums) + 1)):
        err(f"lecture numbers must run 1..N without gaps, in order; got {nums}")

    weeks_of: dict[int, list[int]] = {n: [] for n in nums}
    for w in schedule["weeks"]:
        kind = w["kind"]
        if kind in ("reading", "revision") and w.get("lectures"):
            err(f"week {w['week']}: no lecture may be held in {kind} week")
        if kind == "guest" and w.get("lectures"):
            err(f"week {w['week']}: a guest week holds no numbered lecture")
        for n in w.get("lectures", []):
            if n not in by_num:
                err(f"week {w['week']}: schedules lecture {n}, which lectures.yaml doesn't define")
            else:
                weeks_of[n].append(w["week"])
        if len(w.get("lectures", [])) > 1:
            warn(f"week {w['week']}: {len(w['lectures'])} lectures in one session "
                 f"({', '.join(map(str, w['lectures']))}) — P19 load")
    if [w["week"] for w in schedule["weeks"]] != list(range(1, 13)):
        err("the schedule must list weeks 1 to 12, once each, in order")

    for n, ws in weeks_of.items():
        if not ws:
            err(f"lecture {n} ({by_num[n]['title']}) is not scheduled")
        elif len(ws) > 1:
            err(f"lecture {n} is scheduled in more than one week: {ws}")
    order = [(ws[0], n) for n, ws in weeks_of.items() if ws]
    if [n for _, n in sorted(order)] != sorted(n for _, n in order):
        err("lectures are not scheduled in number order")

    # Folders: one per lecture, and no orphans.
    slugs = {L["slug"] for L in lectures}
    for L in lectures:
        for base in (DOCS, SLIDES):
            if not (base / L["slug"] / "index.md").exists():
                err(f"lecture {L['number']}: no {base.name}/{L['slug']}/index.md")
    for d in SLIDES.iterdir():
        if d.is_dir() and d.name not in slugs:
            err(f"slides/{d.name} is not a lecture in lectures.yaml")

    # Labels: handout, deck and nav must carry the number and title.
    nav = (ROOT / "zensical.toml").read_text(encoding="utf-8")
    for L in lectures:
        label = f"Lecture {L['number']}: {L['title']}"
        h = DOCS / L["slug"] / "index.md"
        d = SLIDES / L["slug"] / "index.md"
        if h.exists():
            fm = front_matter(h)
            if fm.get("title") != label:
                err(f"docs/{L['slug']}/index.md: title is {fm.get('title')!r}, expected {label!r}")
            if fm.get("order") != L["number"]:
                err(f"docs/{L['slug']}/index.md: order is {fm.get('order')!r}, expected {L['number']}")
            if f"# {label}" not in h.read_text(encoding="utf-8"):
                err(f"docs/{L['slug']}/index.md: first heading should be '# {label}'")
        if d.exists():
            fm = front_matter(d)
            if fm.get("title") != label:
                err(f"slides/{L['slug']}/index.md: title is {fm.get('title')!r}, expected {label!r}")
            if f"Lecture {L['number']}" not in str(fm.get("footer", "")):
                err(f"slides/{L['slug']}/index.md: footer should name Lecture {L['number']}")
        for kind, word, head in (("example-sheet", "example sheet", "Example sheet"), ("solutions", "solutions", "Solutions")):
            f = DOCS / L["slug"] / f"{kind}.md"
            if not f.exists():
                err(f"lecture {L['number']}: no docs/{L['slug']}/{kind}.md")
                continue
            want = f"Lecture {L['number']} {word}: {L['title']}"
            got = front_matter(f).get("title")
            if got != want:
                err(f"docs/{L['slug']}/{kind}.md: title is {got!r}, expected {want!r}")
            if f"# {head}: {L['title']}" not in f.read_text(encoding="utf-8"):
                err(f"docs/{L['slug']}/{kind}.md: first heading should be '# {head}: {L['title']}'")
        if f'"{label}"' not in nav:
            err(f"zensical.toml nav has no entry {label!r}")

    # Coverage: every ILO served by at least two lectures' outcomes.
    for ilo in (4, 5, 6):
        serving = sorted({L["number"] for L in lectures for o in L["outcomes"] if o["ilo"] == ilo})
        if len(serving) < 2:
            err(f"ILO {ilo} is served by lectures {serving}; want at least two")

    # The chain: each lecture's hook resolves the one before.
    for L in lectures[1:]:
        prev = L["number"] - 1
        if f"Lecture {prev}" not in L["in_lecture"]["hook"]:
            warn(f"lecture {L['number']}: its hook doesn't name Lecture {prev}'s cliffhanger")

    # P19: two concepts, one tool, one notation, in the taught blocks.
    for L in lectures:
        b = L["budget"]
        over = []
        if len(b["concepts"]) > 2: over.append(f"{len(b['concepts'])} concepts")
        if len(b["tool"]) > 1: over.append(f"{len(b['tool'])} tools")
        if len(b["notation"]) > 1: over.append(f"{len(b['notation'])} notations")
        if over:
            warn(f"lecture {L['number']}: over P19's budget ({', '.join(over)}); verdict recorded: {b['verdict']}")

    # Coursework: a step every week up to the deadline, and a lecture that week.
    cw = schedule["coursework"]
    dl = cw["deadline"]["week"]
    have = sorted(s["week"] for s in cw["steps"])
    if have != list(range(1, dl + 1)):
        warn(f"coursework steps cover weeks {have}; expected every week 1 to {dl}")
    return weeks_of


# ----------------------------------------------------------- term map (SVG)
RED, RED_TINT, INK, MUTED, RULE, GREY = "#b01c2e", "#f6e3e5", "#1a1a1a", "#5a5a5a", "#bfbfbf", "#eeeeee"


def term_map_svg(lectures: list[dict], schedule: dict) -> str:
    """The twelve weeks, for Lecture 1's deck and handout. Light, print-safe."""
    by_num = {L["number"]: L for L in lectures}
    cw = {s["week"]: s for s in schedule["coursework"]["steps"]}
    lab = schedule["laboratory"]
    W, row, top, x_wk, x_act, x_ses, w_ses, x_cw, w_cw, x_lab, w_lab = 1000, 34, 58, 22, 86, 128, 496, 640, 190, 846, 124
    H = top + 12 * row + 64
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Trebuchet MS, Arial, sans-serif" role="img" '
         f'aria-labelledby="t d"><title id="t">The control half, week by week, {schedule["year"]}</title>'
         f'<desc id="d">Twelve weeks down the page. Each row gives the week, the act, what happens in the Tuesday session, '
         f'the coursework event if any, and the open-access laboratory window.</desc>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         '<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<line x1="0" y1="0" x2="0" y2="6" stroke="#e4e4e4" stroke-width="1.5"/></pattern></defs>']
    hdr = f'font-size="15" font-weight="700" fill="{INK}"'
    o += [f'<text x="{x_wk + 24}" y="36" {hdr} text-anchor="middle">Week</text>',
          f'<text x="{x_act}" y="36" {hdr} text-anchor="middle">Act</text>',
          f'<text x="{x_ses}" y="36" {hdr}>Tuesday session</text>',
          f'<text x="{x_cw}" y="36" {hdr}>Coursework</text>',
          f'<text x="{x_lab}" y="36" {hdr}>Laboratory</text>',
          f'<line x1="20" y1="46" x2="{W - 20}" y2="46" stroke="{RED}" stroke-width="2"/>']

    # Laboratory window: a dashed bracket over its weeks.
    y0 = top + (lab["from_week"] - 1) * row + 3
    y1 = top + lab["to_week"] * row - 3
    o.append(f'<rect x="{x_lab}" y="{y0}" width="{w_lab}" height="{y1 - y0}" rx="6" fill="#fff" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="5 4"/>')
    o.append(f'<text x="{x_lab + w_lab / 2}" y="{(y0 + y1) / 2 - 4}" font-size="14" font-weight="700" fill="{INK}" text-anchor="middle">Quanser</text>')
    o.append(f'<text x="{x_lab + w_lab / 2}" y="{(y0 + y1) / 2 + 14}" font-size="13" fill="{MUTED}" text-anchor="middle">open access</text>')

    act_first: dict[int, int] = {}
    for i, w in enumerate(schedule["weeks"]):
        y = top + i * row
        cy = y + row / 2 + 5
        o.append(f'<text x="{x_wk + 24}" y="{cy}" font-size="15" font-weight="700" fill="{INK}" text-anchor="middle">{w["week"]}</text>')
        kind = w["kind"]
        if kind == "lecture":
            ls = [by_num[n] for n in w["lectures"]]
            label = " + ".join(f'L{L["number"]} {L["title"]}' for L in ls)
            if len(ls) > 1:
                label = " + ".join(f'L{L["number"]} {L["title"].split(" and ")[0]}' for L in ls)
            if w.get("second_hour"):
                label += f' · then {w["second_hour"]}'
            for L in ls:
                act_first.setdefault(L["act"], i)
            fill, stroke, colour, weight = RED_TINT, RED, INK, "400"
        elif kind == "guest":
            label, fill, stroke, colour, weight = w["label"], "#fff", RED, INK, "400"
        else:
            label, fill, stroke, colour, weight = w.get("label", kind.title()), "url(#hatch)", RULE, MUTED, "400"
        o.append(f'<rect x="{x_ses}" y="{y + 4}" width="{w_ses}" height="{row - 8}" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
        o.append(f'<text x="{x_ses + 12}" y="{cy}" font-size="14" font-weight="{weight}" fill="{colour}" '
                 f'stroke="{"#fff" if kind not in ("lecture",) else "none"}" stroke-width="5" paint-order="stroke">{html.escape(label)}</text>')
        step = cw.get(w["week"], {})
        if step.get("event"):
            deadline = step["event"] == "Deadline"
            ev = f'Due {schedule["coursework"]["deadline"]["day"]}' if deadline else step["event"]
            o.append(f'<rect x="{x_cw}" y="{y + 5}" width="{w_cw}" height="{row - 10}" rx="12" fill="{RED if deadline else "#fff"}" stroke="{RED}" stroke-width="1.2"/>')
            o.append(f'<text x="{x_cw + w_cw / 2}" y="{cy - 1}" font-size="13" font-weight="700" fill="{"#fff" if deadline else RED}" text-anchor="middle">{html.escape(ev)}</text>')

    # Acts: a label at each act's first week, and a rule down its span.
    spans: dict[int, list[int]] = {}
    for i, w in enumerate(schedule["weeks"]):
        for n in w.get("lectures", []):
            spans.setdefault(by_num[n]["act"], []).append(i)
    for act, idx in spans.items():
        a, b = min(idx), max(idx)
        o.append(f'<line x1="{x_ses - 10}" y1="{top + a * row + 6}" x2="{x_ses - 10}" y2="{top + (b + 1) * row - 6}" stroke="{RED}" stroke-width="2"/>')
        o.append(f'<text x="{x_act}" y="{top + a * row + row / 2 + 5}" font-size="15" font-weight="700" fill="{RED}" text-anchor="middle">{"I" * act if act < 4 else act}</text>')

    ly = top + 12 * row + 30
    items = [(RED_TINT, RED, "Our lecture"), ("#fff", RED, "Guest lecture"), ("url(#hatch)", RULE, "No control lecture")]
    x = x_ses
    for fill, stroke, text in items:
        o.append(f'<rect x="{x}" y="{ly - 13}" width="18" height="18" rx="4" fill="{fill}" stroke="{stroke}"/>')
        o.append(f'<text x="{x + 26}" y="{ly + 1}" font-size="13" fill="{MUTED}">{text}</text>')
        x += 190
    o.append(f'<text x="{W - 20}" y="{ly + 1}" font-size="13" fill="{MUTED}" text-anchor="end">L = lecture. Coursework due {schedule["coursework"]["deadline"]["day"]} of week {schedule["coursework"]["deadline"]["week"]}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


# ------------------------------------------------ planning diagram (HTML)
SLOTS = [("hook", "Hook and recall", 5), ("block_a", "Block A", 15), ("do_a", "Do A", 10),
         ("block_b", "Block B", 15), ("do_b", "Do B", 10), (None, "Changeover", 5),
         ("case", "Case brief, build, converge", 40), ("cliffhanger", "Cliffhanger", 10)]
PARTS = [("close_the_loop", "1. Close the loop", "1.5 h"), ("examples", "2. Work the examples", "2 h"),
         ("feed", "3. Feed the design", "2 h"), ("next_case", "4. Meet next week's case", "0.25 h")]


def e(s) -> str:
    return html.escape(str(s))


def planning_html(lectures: list[dict], schedule: dict, weeks_of: dict[int, list[int]]) -> str:
    cw = {s["week"]: s for s in schedule["coursework"]["steps"]}
    wk = {w["week"]: w for w in schedule["weeks"]}
    acts = {1: "Act I — the loop you can build", 2: "Act II — analysis and design that scale", 3: "Act III — aircraft and modern methods"}

    # Term strip
    strip = []
    for w in schedule["weeks"]:
        k = w["kind"]
        body = " + ".join(f'L{n}' for n in w.get("lectures", [])) or {"guest": "Guest", "reading": "Reading", "revision": "Revision"}.get(k, w.get("label", ""))
        ev = cw.get(w["week"], {}).get("event", "")
        lab = schedule["laboratory"]["from_week"] <= w["week"] <= schedule["laboratory"]["to_week"]
        strip.append(f'<div class="wk k-{k}{" two" if len(w.get("lectures", [])) > 1 else ""}"><b>{w["week"]}</b><span>{e(body)}</span>'
                     f'{f"<i>{e(ev)}</i>" if ev else ""}{"<u></u>" if lab else ""}</div>')

    # ILO matrix
    mat = ['<table class="mx"><tr><th></th>' + "".join(f"<th>L{L['number']}</th>" for L in lectures) + "</tr>"]
    for ilo, name in ((4, "ILO 4 — stability and robustness"), (5, "ILO 5 — design, classical and modern"), (6, "ILO 6 — aircraft application")):
        cells = []
        for L in lectures:
            c = sum(1 for o in L["outcomes"] if o["ilo"] == ilo)
            cells.append(f'<td class="c{min(c, 3)}">{c or ""}</td>')
        mat.append(f"<tr><th>{name}</th>{''.join(cells)}</tr>")
    mat.append("</table>")

    cards = []
    for i, L in enumerate(lectures):
        n = L["number"]
        weeks = weeks_of.get(n, [])
        w = weeks[0] if weeks else None
        shared = [m for m in (wk[w].get("lectures", []) if w else []) if m != n]
        when = f"Week {w}" + (f" · with L{shared[0]}" if shared else "") if w else "Unscheduled"
        if w and wk[w].get("second_hour"):
            when += f" · hour 2: {wk[w]['second_hour']}"
        if i == 0 or L["act"] != lectures[i - 1]["act"]:
            cards.append(f'<h2 class="act">{e(acts.get(L["act"], L["act"]))}</h2>')
        slot_rows = []
        for key, name, mins in SLOTS:
            if key is None:
                continue
            text = L["cliffhanger"] if key == "cliffhanger" else L["in_lecture"].get(key, "")
            slot_rows.append(f'<tr><td class="sl">{name}<small>{mins} min</small></td><td>{e(text)}</td></tr>')
        bar = "".join(f'<span class="s s-{(k or "gap").replace("_", "")}" style="flex:{m}" title="{e(nm)}, {m} min"></span>' for k, nm, m in SLOTS)
        part_rows = []
        for key, name, hrs in PARTS:
            text = (cw.get(w, {}).get("step", "") if key == "feed" else L["out_of_lecture"].get(key, ""))
            part_rows.append(f'<tr><td class="sl">{name}<small>{hrs}</small></td><td>{e(text)}</td></tr>')
        outs = "".join(f'<li><span class="ilo i{o["ilo"]}">{o["ilo"]}</span>{e(o["text"])}</li>' for o in L["outcomes"])
        b = L["budget"]
        verdict = b["verdict"]
        vclass = "ok" if verdict == "fits" else ("na" if verdict.startswith("awareness") else "warn")
        chips = "".join(f'<span class="chip">{e(t)}</span>' for t in L["threshold"]) or '<span class="muted">none new</span>'
        cards.append(f"""
<section class="card" id="L{n}">
  <header>
    <div class="num">L{n}</div>
    <div class="tt"><h3>{e(L['title'])}</h3><p class="q">{e(L['question'])}</p></div>
    <div class="when">{e(when)}</div>
  </header>
  <div class="grid">
    <div class="col id">
      <dl>
        <dt>Focus</dt><dd>{e(L['focus'])}</dd>
        <dt>Threshold</dt><dd>{chips}</dd>
        <dt>System</dt><dd>{e(', '.join(L['systems']))}</dd>
        <dt>Case</dt><dd>{e(L['case'])}</dd>
        <dt>P19 budget</dt><dd><span class="v {vclass}">{e(verdict)}</span><br><small>{e(', '.join(b['concepts']) or '—')} · {e(', '.join(b['tool']) or '—')} · {e(', '.join(b['notation']) or '—')}</small></dd>
        <dt>Handout only</dt><dd><small>{e('; '.join(L['handout_only']))}</small></dd>
      </dl>
    </div>
    <div class="col">
      <h4>Learning outcomes</h4><ul class="lo">{outs}</ul>
      <p class="hk"><b>Hook</b> {e(L['hook'])}</p>
    </div>
    <div class="col">
      <h4>In the room <small>110 min</small></h4>
      <div class="bar">{bar}</div>
      <table class="sl-t">{''.join(slot_rows)}</table>
    </div>
    <div class="col">
      <h4>Between sessions <small>about 7 h</small></h4>
      <table class="sl-t">{''.join(part_rows)}</table>
      {f'<p class="note">{e(L["notes"])}</p>' if L.get('notes') else ''}
    </div>
  </div>
</section>""")
        if i + 1 < len(lectures):
            cards.append(f'<div class="chain"><span>cliffhanger</span> {e(L["cliffhanger"])} <span>→ hook of L{n + 1}</span></div>')

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lecture map — CADE30008 control half, {e(schedule['year'])}</title>
<style>
:root{{--red:#b01c2e;--tint:#f6e3e5;--ink:#1a1a1a;--mut:#5f5f5f;--rule:#d9d9d9;--bg:#fafafa;--card:#fff;--i4:#534ab7;--i5:#0f6e56;--i6:#993c1d}}
@media (prefers-color-scheme:dark){{:root{{--tint:#3a1a1e;--ink:#ececec;--mut:#a8a8a8;--rule:#3a3a40;--bg:#17171b;--card:#1f1f24;--i4:#afa9ec;--i5:#5dcaa5;--i6:#f0997b}}}}
*{{box-sizing:border-box}}body{{margin:0;padding:24px clamp(16px,3vw,40px) 60px;font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:var(--bg)}}
h1{{font-size:22px;margin:0 0 4px}}.sub{{color:var(--mut);margin:0 0 18px;max-width:80ch}}
h2.act{{font-size:15px;color:var(--red);border-bottom:2px solid var(--red);padding-bottom:4px;margin:28px 0 12px}}
.strip{{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:4px;margin:8px 0 18px}}
.wk{{background:var(--card);border:1px solid var(--rule);border-radius:6px;padding:6px 4px 8px;text-align:center;position:relative;min-height:74px}}
.wk b{{display:block;font-size:12px;color:var(--mut)}}.wk span{{display:block;font-weight:600;font-size:13px;margin-top:2px;overflow-wrap:anywhere}}
.wk i{{display:block;font-style:normal;font-size:11px;color:var(--red);margin-top:3px;font-weight:600}}
.wk u{{position:absolute;left:6px;right:6px;bottom:3px;border-bottom:2px dashed var(--mut)}}
.k-lecture{{background:var(--tint);border-color:var(--red)}}.k-lecture.two{{outline:2px solid var(--red);outline-offset:1px}}
.k-reading,.k-revision,.k-other{{background:repeating-linear-gradient(45deg,transparent 0 5px,var(--rule) 5px 6px);color:var(--mut)}}
.legend{{font-size:12px;color:var(--mut);margin:-10px 0 18px}}
.mxw{{overflow-x:auto;margin-bottom:8px}}.mx{{border-collapse:collapse;font-size:12px}}.mx th,.mx td{{border:1px solid var(--rule);padding:4px 8px;text-align:center}}.mx th:first-child{{text-align:left;font-weight:500}}
.mx .c1{{background:color-mix(in srgb,var(--red) 18%,transparent)}}.mx .c2{{background:color-mix(in srgb,var(--red) 38%,transparent)}}.mx .c3{{background:color-mix(in srgb,var(--red) 60%,transparent);color:#fff}}
.card{{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:14px 16px;margin:0}}
.card header{{display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap;border-bottom:1px solid var(--rule);padding-bottom:10px;margin-bottom:10px}}
.num{{background:var(--red);color:#fff;font-weight:700;border-radius:6px;padding:4px 9px;font-size:15px}}
.tt{{flex:1;min-width:220px}}.tt h3{{margin:0;font-size:17px}}.q{{margin:2px 0 0;color:var(--mut);font-style:italic}}
.when{{font-size:12px;color:var(--red);font-weight:600;white-space:nowrap}}
.grid{{display:grid;grid-template-columns:1fr 1.25fr 1.5fr 1.25fr;gap:16px}}
@media (max-width:1100px){{.grid{{grid-template-columns:1fr 1fr}}}}@media (max-width:640px){{.grid{{grid-template-columns:1fr}}.strip{{grid-template-columns:repeat(4,minmax(0,1fr))}}.wk span{{font-size:12px}}}}
h4{{font-size:12px;text-transform:none;margin:0 0 6px;color:var(--mut);font-weight:600}}h4 small{{font-weight:400}}
dl{{margin:0;display:grid;grid-template-columns:auto 1fr;gap:4px 10px;font-size:12.5px}}dt{{color:var(--mut)}}dd{{margin:0}}
.chip{{display:inline-block;background:var(--tint);border:1px solid var(--red);border-radius:10px;padding:0 7px;margin:0 3px 3px 0;font-size:11.5px}}
.muted{{color:var(--mut)}}.v{{font-weight:600;font-size:12px}}.v.ok{{color:var(--i5)}}.v.warn{{color:var(--red)}}.v.na{{color:var(--mut)}}
ul.lo{{list-style:none;margin:0;padding:0}}ul.lo li{{display:flex;gap:7px;margin-bottom:5px;font-size:12.5px}}
.ilo{{flex:none;font-size:10.5px;font-weight:700;border-radius:4px;padding:1px 5px;height:fit-content;color:#fff}}.i4{{background:var(--i4)}}.i5{{background:var(--i5)}}.i6{{background:var(--i6)}}
.hk{{font-size:12.5px;margin:8px 0 0;padding:6px 8px;border-left:3px solid var(--red);background:var(--tint)}}
.bar{{display:flex;height:10px;border-radius:3px;overflow:hidden;margin-bottom:6px;border:1px solid var(--rule)}}
.s{{display:block}}.s-hook{{background:var(--red)}}.s-blocka,.s-blockb{{background:var(--i4)}}.s-doa,.s-dob{{background:var(--i5)}}.s-gap{{background:var(--rule)}}.s-case{{background:var(--i6)}}.s-cliffhanger{{background:var(--red)}}
table.sl-t{{border-collapse:collapse;width:100%;font-size:12.5px}}.sl-t td{{border-top:1px solid var(--rule);padding:4px 4px;vertical-align:top}}
.sl{{width:36%;color:var(--mut);font-weight:600}}.sl small{{display:block;font-weight:400}}
.note{{font-size:12px;color:var(--mut);border-top:1px dashed var(--rule);margin-top:8px;padding-top:6px}}
.chain{{margin:6px 0 6px 22px;padding:4px 0 4px 14px;border-left:2px dashed var(--red);font-size:12.5px;font-style:italic}}.chain span{{font-style:normal;font-weight:600;color:var(--red);font-size:11.5px}}
footer{{margin-top:28px;font-size:12px;color:var(--mut)}}
@media print{{body{{background:#fff}}.card{{break-inside:avoid}}}}
</style></head><body>
<h1>Lecture map — the control half, {e(schedule['year'])}</h1>
<p class="sub">Planning view, not student-facing. Generated by <code>scripts/build_curriculum.py</code> from <code>curriculum/lectures.yaml</code> and <code>curriculum/schedule-{e(schedule['year'].replace('/', '-'))}.yaml</code>; edit those, not this. Scope is a proposal (option B, CURRICULUM.md) awaiting review.</p>
<div class="strip">{''.join(strip)}</div>
<p class="legend">Red: our lectures (outlined where two share a week). Hatched: no control lecture. Red text: coursework. Dashed underline: the laboratory window.</p>
<div class="mxw">{''.join(mat)}</div>
<p class="legend">Learning outcomes per lecture per ILO. Colour bar in each card: hook and cliffhanger in red, taught blocks purple, pair work green, the case hour orange, to scale over 110 minutes.</p>
{''.join(cards)}
<footer>CADE30008 · Steve Bullock · generated from the curriculum sources. Teaching material CC BY 4.0.</footer>
</body></html>
"""


# ------------------------------------------------------- home page table
def home_table(lectures: list[dict], schedule: dict, weeks_of: dict[int, list[int]]) -> str:
    rows = ["| Lecture | Topic | Materials |", "|---|---|---|"]
    for L in lectures:
        s = L["slug"]
        rows.append(f"| {L['number']} | {L['title']} | [Handout]({s}/index.md) · [Slides](slides/{s}/index.html) · "
                    f"[Example sheet]({s}/example-sheet.md) · [Solutions]({s}/solutions.md) |")
    return "\n".join(rows)


def schedule_table(lectures: list[dict], schedule: dict) -> str:
    """This year's weeks as a table, for Lecture 1's handout: the text version of the term map."""
    by_num = {L["number"]: L for L in lectures}
    cw = {s["week"]: s for s in schedule["coursework"]["steps"]}
    rows = [f"*{schedule['year']}. Lectures are on {schedule['day']}s.*", "",
            "| Week | Tuesday session | Coursework |", "|---|---|---|"]
    for w in schedule["weeks"]:
        if w["kind"] == "lecture":
            what = " and ".join(f"[Lecture {n}: {by_num[n]['title']}](../{by_num[n]['slug']}/index.md)" for n in w["lectures"])
            if w.get("second_hour"):
                what += f"; then {w['second_hour'][0].lower() + w['second_hour'][1:]}"
        else:
            what = f"*{w.get('label', w['kind'].title())}*"
        ev = cw.get(w["week"], {}).get("event", "")
        if ev == "Deadline":
            d = schedule["coursework"]["deadline"]
            ev = f"**Due {d['day']} of week {d['week']}**"
        rows.append(f"| {w['week']} | {what} | {ev} |")
    lab = schedule["laboratory"]
    rows += ["", f"The Quanser laboratory is open access from week {lab['from_week']} to week "
                 f"{lab['to_week']}: you choose when to go."]
    return "\n".join(rows)


def outcomes_block(L: dict) -> str:
    """The learning-outcomes admonition for a lecture's handout."""
    items = [f"    - {o['text'][0].lower() + o['text'][1:]};" for o in L["outcomes"]]
    items[-1] = items[-1][:-1] + "."
    return '!!! abstract "Learning outcomes"\n    By the end of this lecture you should be able to:\n\n' + "\n".join(items)


def replace_between(text: str, start: str, end: str, new: str) -> str:
    i, j = text.find(start), text.find(end)
    if i < 0 or j < 0:
        raise SystemExit(f"markers {start} … {end} not found")
    return text[: i + len(start)] + "\n" + new + "\n" + text[j:]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", default="2026-27")
    args = ap.parse_args()
    lectures = yaml.safe_load((CUR / "lectures.yaml").read_text(encoding="utf-8"))["lectures"]
    schedule = yaml.safe_load((CUR / f"schedule-{args.year}.yaml").read_text(encoding="utf-8"))

    weeks_of = check(lectures, schedule)
    if not weeks_of:
        for x in errors:
            print(f"error    {x}")
        sys.exit(1)

    fig = DOCS / "design-cycle" / "figures"
    fig.mkdir(parents=True, exist_ok=True)
    (fig / "term-map.svg").write_text(term_map_svg(lectures, schedule), encoding="utf-8")
    (ROOT / "planning").mkdir(exist_ok=True)
    (ROOT / "planning" / "lecture-map.html").write_text(planning_html(lectures, schedule, weeks_of), encoding="utf-8")
    home = DOCS / "index.md"
    home.write_text(replace_between(home.read_text(encoding="utf-8"), "<!-- lectures:start -->", "<!-- lectures:end -->",
                                    home_table(lectures, schedule, weeks_of)), encoding="utf-8")

    for L in lectures:
        h = DOCS / L["slug"] / "index.md"
        text = h.read_text(encoding="utf-8")
        if "<!-- outcomes:start -->" in text:
            h.write_text(replace_between(text, "<!-- outcomes:start -->", "<!-- outcomes:end -->", outcomes_block(L)), encoding="utf-8")
        else:
            warn(f"lecture {L['number']}: handout keeps its own outcomes, not generated from lectures.yaml")

    l1 = DOCS / "design-cycle" / "index.md"
    l1.write_text(replace_between(l1.read_text(encoding="utf-8"), "<!-- schedule:start -->", "<!-- schedule:end -->",
                                  schedule_table(lectures, schedule)), encoding="utf-8")

    for w in warnings:
        print(f"warning  {w}")
    for x in errors:
        print(f"error    {x}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s); {len(lectures)} lectures, "
          f"wrote the term map and schedule in Lecture 1, planning/lecture-map.html, and the home table")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
