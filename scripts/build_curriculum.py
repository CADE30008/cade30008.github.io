"""Check the curriculum and generate everything derived from it.

The control half is designed to the University calendar: week n of teaching
block 1 is "Week n" on every student-facing page. Two sources:

  curriculum/weeks.yaml  what each of the eleven content weeks is: the lecture
                         weeks' full scope, the guest week, and the
                         consolidation week's recommended activities
  curriculum/term.yaml   the year, the coursework's deadline and weekly steps,
                         the laboratory window, and the workload model

Then:

  checks  that the two agree with each other and with the site: every week 1 to
          the deadline once and in order, the consolidation week lecture-free,
          folders wNN-topic with NN the week, every page, deck, sheet and nav
          entry carrying the right week and title, every ILO covered, the
          hook-and-cliffhanger chain, P19's budget, and the workload model's
          sums;
  writes  the term map and the schedule and workload tables in week 1;
          the lecture map, docs/staff/lecture-map.html; the consolidation
          week's activity table; each unwritten week's learning outcomes; and
          the home page's week table.

Run it with `npm run curriculum`. Exits non-zero if any check fails, so it can
gate the build. Warnings don't fail it.
"""

from __future__ import annotations

import html
import re
import sys
from datetime import timedelta
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
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def label(w: dict) -> str:
    return f"Week {w['week']}: {w['title']}"


# ---------------------------------------------------------------- calendar
# Content weeks and calendar weeks are the same thing until the timetable is
# disturbed. term.yaml's `schedule` records this year's disturbances, and
# everything that shows the term *as a calendar* - the term map, week 1's
# schedule table, the staff strip, STATUS.md's dates - reads the calendar built
# here rather than the week numbers. One edit in term.yaml moves them together.
#
# Week numbers keep their old meaning everywhere else: they are the sequence of
# the content, they name the folders, and they are what "Week 2" means on a
# page. The coursework steps and the laboratory window stay in calendar weeks,
# because that is what they were always about.
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def calendar(weeks: list[dict], term: dict) -> list[dict]:
    """The twelve calendar weeks, each with the control sessions it holds."""
    sched = term.get("schedule") or {}
    moved = {m["week"]: m for m in sched.get("taught", [])}
    notes = {n["calendar"]: n["why"] for n in sched.get("no_session", [])}
    rows = [{"n": n, "sessions": [], "why": notes.get(n)} for n in range(1, 13)]
    for w in weeks:
        m = moved.get(w["week"], {})
        n = m.get("calendar", w["week"])
        if not 1 <= n <= 12:
            err(f"week {w['week']}: taught in calendar week {n}, which is outside the term")
            continue
        rows[n - 1]["sessions"].append({"w": w, "day": m.get("day", term["day"]),
                                        "time": m.get("time") if m else term["time"],
                                        "room": m.get("room") if m else term["room"],
                                        "moved": bool(m)})
    for r in rows:
        r["sessions"].sort(key=lambda s: DAYS.index(s["day"]))
    return rows


def check_calendar(rows: list[dict], term: dict) -> None:
    for r in rows:
        n, ss = r["n"], r["sessions"]
        if r["why"] and ss:
            err(f"calendar week {n} is listed as having no session, but holds "
                f"{oxford([s['w']['slug'] for s in ss])}")
        days = [s["day"] for s in ss]
        if len(set(days)) != len(days):
            err(f"calendar week {n}: two sessions on the same day ({oxford(sorted(days))})")
        for s in ss:
            if s["w"]["kind"] != "consolidation" and n == term["consolidation_week"]:
                err(f"calendar week {n} is consolidation week and can hold no session")
            if n == term["revision_week"]:
                err(f"calendar week {n} is revision week and can hold no session")
    taught = {s["w"]["week"] for r in rows for s in r["sessions"]}
    for m in (term.get("schedule") or {}).get("taught", []):
        if m["week"] not in taught:
            err(f"schedule: no week {m['week']} to move")


def schedule_note(weeks: list[dict], term: dict) -> str:
    """This year's departures from the timetable, in a sentence or two.

    Empty in a year where nothing moves, which is the point of generating it:
    the note appears and disappears with term.yaml rather than being remembered
    or forgotten by hand.
    """
    cal = calendar(weeks, term)
    parts = []
    for r in cal:
        if r["why"] and not r["sessions"]:
            # term.yaml's "why" is written as two sentences, the first naming
            # the absence and the second giving the reason. Only the reason is
            # wanted here; the week number supplies the rest.
            reason = r["why"].split(". ", 1)[-1]
            parts.append(f"**There is no control session in week {r['n']}.** {reason}")
        elif len(r["sessions"]) > 1:
            days = oxford([x["day"] for x in r["sessions"]])
            parts.append(f"**Week {r['n']} runs twice**, on the {days}.")
    if not parts:
        return ""
    unconfirmed = [f"{x['day']} of week {r['n']}" for r in cal for x in r["sessions"] if not x["time"]]
    if unconfirmed:
        parts.append(f"Blackboard carries the room and the hour for the {oxford(unconfirmed)}.")
    return " ".join(parts)


def session_when(s: dict, term: dict) -> str:
    """"Tuesday", or "Thursday (time on Blackboard)" when the slot isn't confirmed."""
    if s["time"]:
        return s["day"]
    return f"{s['day']} (time on Blackboard)"


# ------------------------------------------------------------------- checks
LECTURE_FIELDS = {"week", "kind", "short", "slug", "title", "act", "question", "focus", "ilos", "capabilities",
                  "threshold", "systems", "case", "outcomes", "hook", "in_lecture", "cliffhanger",
                  "out_of_lecture", "budget", "handout_only"}
SLOT_KEYS = {"hook", "learn_a", "do_a", "learn_b", "do_b", "case"}
PART_KEYS = {"close_the_loop", "examples", "next_case"}
OTHER_FIELDS = {"guest": {"week", "kind", "short", "slug", "title", "note", "independent"},
                "consolidation": {"week", "kind", "short", "slug", "title", "purpose", "activities",
                                  "coursework", "laboratory"}}


def check_shape(weeks: list[dict]) -> None:
    """Shape first: a malformed entry makes every later check unreliable. In
    particular, unquoted text in YAML's {ilo: .., text: ..} form is split at its
    first comma, silently, which truncates the text and invents a key."""
    for w in weeks:
        tag = f"week {w.get('week', '?')}"
        kind = w.get("kind")
        need = LECTURE_FIELDS if kind == "lecture" else OTHER_FIELDS.get(kind)
        if need is None:
            err(f"{tag}: kind must be lecture, guest or consolidation, not {kind!r}")
            continue
        if missing := need - set(w):
            err(f"{tag}: missing {', '.join(sorted(missing))}")
            continue
        if kind == "lecture":
            for o in w["outcomes"]:
                if set(o) != {"ilo", "text"}:
                    err(f"{tag}: malformed outcome {o!r} — quote text containing commas")
                elif o["ilo"] not in (4, 5, 6):
                    err(f"{tag}: outcome serves ILO {o['ilo']}; this half covers 4 to 6")
            if missing := SLOT_KEYS - set(w["in_lecture"]):
                err(f"{tag}: in_lecture lacks {', '.join(sorted(missing))}")
            if missing := PART_KEYS - set(w["out_of_lecture"]):
                err(f"{tag}: out_of_lecture lacks {', '.join(sorted(missing))}")
        if kind == "consolidation":
            for a in w["activities"]:
                if set(a) != {"hours", "title", "what"}:
                    err(f"{tag}: malformed activity {a!r} — quote text containing commas")


def check(weeks: list[dict], term: dict) -> None:
    lectures = [w for w in weeks if w["kind"] == "lecture"]
    deadline = term["coursework"]["deadline"]["week"]
    nums = [w["week"] for w in weeks]
    if nums != list(range(1, deadline + 1)):
        err(f"weeks must run 1 to {deadline}, the coursework deadline, once each and in order; got {nums}")
    for w in weeks:
        if w["week"] == term["consolidation_week"] and w["kind"] != "consolidation":
            err(f"week {w['week']} is the consolidation week and can hold no lecture")
        if w["kind"] == "consolidation" and w["week"] != term["consolidation_week"]:
            err(f"week {w['week']}: only week {term['consolidation_week']} is the consolidation week")
        if w["week"] == term["revision_week"]:
            err(f"week {w['week']} is revision week and carries no content")
        if not w["slug"].startswith(f"w{w['week']:02d}-"):
            err(f"week {w['week']}: folder {w['slug']!r} should start 'w{w['week']:02d}-'")

    # Folders: a page for every week; decks and sheets for lecture weeks; no orphans.
    slugs = {w["slug"] for w in weeks}
    lecture_slugs = {w["slug"] for w in lectures}
    for w in weeks:
        if not (DOCS / w["slug"] / "index.md").exists():
            err(f"week {w['week']}: no docs/{w['slug']}/index.md")
    for w in lectures:
        if not (SLIDES / w["slug"] / "index.md").exists():
            err(f"week {w['week']}: no slides/{w['slug']}/index.md")
    for d in SLIDES.iterdir():
        if d.is_dir() and d.name not in lecture_slugs:
            err(f"slides/{d.name} is not a lecture week in weeks.yaml")
    # "figures" holds the term map and the week graphic outside any week
    # folder, because published pages point at them and the live build
    # removes unpublished weeks wholesale. Written at the end of this
    # script, which is why its absence from this list only showed up on the
    # second run.
    # "laboratory" is the open-access Quanser material, which spans the whole
    # term rather than sitting in one week's folder.
    known = {"applets", "assets", "downloads", "figures", "includes", "javascripts",
             "laboratory", "preparing", "slides", "staff", "stylesheets"}
    for d in DOCS.iterdir():
        if d.is_dir() and d.name not in slugs | known:
            err(f"docs/{d.name}/ is neither a week in weeks.yaml nor a known site folder — a leftover?")

    # Labels: every page, deck, sheet and nav entry names its week.
    nav = (ROOT / "zensical.toml").read_text(encoding="utf-8")
    for w in weeks:
        lab = label(w)
        h = DOCS / w["slug"] / "index.md"
        if h.exists():
            fm = front_matter(h)
            if fm.get("title") != lab:
                err(f"docs/{w['slug']}/index.md: title is {fm.get('title')!r}, expected {lab!r}")
            if fm.get("order") != w["week"]:
                err(f"docs/{w['slug']}/index.md: order is {fm.get('order')!r}, expected {w['week']}")
            if f"# {lab}" not in h.read_text(encoding="utf-8"):
                err(f"docs/{w['slug']}/index.md: first heading should be '# {lab}'")
        if f'"{lab}"' not in nav:
            err(f"zensical.toml nav has no entry {lab!r}")
        if w["kind"] != "lecture":
            continue
        d = SLIDES / w["slug"] / "index.md"
        if d.exists():
            fm = front_matter(d)
            if fm.get("title") != lab:
                err(f"slides/{w['slug']}/index.md: title is {fm.get('title')!r}, expected {lab!r}")
            if f"Week {w['week']}" not in str(fm.get("footer", "")):
                err(f"slides/{w['slug']}/index.md: footer should name Week {w['week']}")
        for kind, word, head in (("example-sheet", "example sheet", "Example sheet"), ("solutions", "solutions", "Solutions")):
            f = DOCS / w["slug"] / f"{kind}.md"
            if not f.exists():
                err(f"week {w['week']}: no docs/{w['slug']}/{kind}.md")
                continue
            want = f"Week {w['week']} {word}: {w['title']}"
            if (got := front_matter(f).get("title")) != want:
                err(f"docs/{w['slug']}/{kind}.md: title is {got!r}, expected {want!r}")
            if f"# {head}: {w['title']}" not in f.read_text(encoding="utf-8"):
                err(f"docs/{w['slug']}/{kind}.md: first heading should be '# {head}: {w['title']}'")

    # Coverage: every ILO served by at least two weeks' outcomes.
    for ilo in (4, 5, 6):
        serving = sorted({w["week"] for w in lectures for o in w["outcomes"] if o["ilo"] == ilo})
        if len(serving) < 2:
            err(f"ILO {ilo} is served by weeks {serving}; want at least two")

    # The chain: each lecture week's hook resolves the previous lecture week's cliffhanger.
    for prev, w in zip(lectures, lectures[1:]):
        if f"week {prev['week']}" not in w["in_lecture"]["hook"]:
            warn(f"week {w['week']}: its hook doesn't name week {prev['week']}'s cliffhanger")

    # P19: two concepts, one tool, one notation, in the Learn slots.
    for w in lectures:
        b = w["budget"]
        over = [f"{len(b[k])} {n}" for k, n, lim in (("concepts", "concepts", 2), ("tool", "tools", 1), ("notation", "notations", 1))
                if len(b[k]) > lim]
        if over:
            warn(f"week {w['week']}: over P19's budget ({', '.join(over)}); verdict recorded: {b['verdict']}")

    steps = sorted(s["week"] for s in term["coursework"]["steps"])
    if steps != list(range(1, deadline + 1)):
        warn(f"coursework steps cover weeks {steps}; expected every week 1 to {deadline}")


# ------------------------------------------------------------ workload model
CATS = ("lecture", "independent", "consolidation", "coursework")


def hrs(h: float) -> str:
    """0.75 -> '45 min', 1.0 -> '1 h'."""
    return f"{round(h * 60)} min" if h < 1 else f"{h:g} h"


def workload(weeks: list[dict], term: dict) -> dict:
    m = term["workload"]
    by_kind = m["by_kind"]
    parts = m["independent_parts"]
    if abs(sum(parts.values()) - by_kind["lecture"]["independent"]) > 1e-9:
        err(f"workload: independent parts sum to {sum(parts.values()):g} h, not a lecture week's "
            f"{by_kind['lecture']['independent']:g} h")
    for w in weeks:
        if w["kind"] == "consolidation":
            got = sum(a["hours"] for a in w["activities"])
            want = by_kind["consolidation"]["consolidation"]
            if abs(got - want) > 1e-9:
                err(f"week {w['week']}: consolidation activities sum to {got:g} h, not the model's {want:g} h")
    kind_of = {w["week"]: w["kind"] for w in weeks}
    deadline = term["coursework"]["deadline"]["week"]
    lab = term["laboratory"]
    rows = []
    for n in range(1, 13):
        kind = kind_of.get(n, "revision" if n == term["revision_week"] else "none")
        hours = by_kind.get(kind, {})
        r = {"week": n, "kind": kind, **{c: hours.get(c, 0) for c in CATS}}
        if n > deadline:
            r["coursework"] = 0
        r["total"] = sum(r[c] for c in CATS)
        r["lab_window"] = lab["from_week"] <= n <= lab["to_week"]
        rows.append(r)
    tot = {c: sum(r[c] for r in rows) for c in CATS}
    tot["laboratory"] = m["laboratory"]
    lw = by_kind["lecture"]
    share = m["working_week"] / m["units_at_once"] * m["share_of_unit"]
    if sum(lw.values()) > share + 0.5:
        warn(f"workload: a lecture week plans {sum(lw.values()):g} h, above this half's share of a "
             f"{m['working_week']:g} h week ({share:.1f} h)")
    return {"share": share, "working_week": m["working_week"], "units_at_once": m["units_at_once"], "rows": rows, "totals": tot, "planned": sum(tot.values()), "notional": m["notional"],
            "lecture_week": lw, "typical": sum(lw.values()), "consolidation": by_kind["consolidation"],
            "parts": {**parts, "feed": lw["coursework"]}, "lab": lab, "laboratory": m["laboratory"]}


# ----------------------------------------------------------- term map (SVG)
RED, RED_TINT, INK, MUTED, RULE = "#b01c2e", "#f6e3e5", "#1a1a1a", "#5a5a5a", "#bfbfbf"


def e(s) -> str:
    return html.escape(str(s))


def session_label(s: dict, term: dict, with_day: bool) -> str:
    w = s["w"]
    if w["kind"] == "consolidation":
        return "Consolidation week · no lecture"
    text = w["title"]
    if w.get("second_hour"):
        text += f" · then {w['second_hour']}"
    return f"{session_when(s, term)} · {text}" if with_day else text


def term_map_svg(weeks: list[dict], term: dict, acts: dict) -> str:
    """The twelve weeks, for week 1's deck and handout. Light and print-safe.

    Rows are a calendar week each and are sized to what the week holds, so a
    week with two sessions is twice as tall and a week with none still occupies
    its place. Every y here comes from `y_of`/`h_of` rather than from n * row,
    which is what lets that vary without the act brackets and the laboratory
    window sliding off.
    """
    cal = calendar(weeks, term)
    cw = {s["week"]: s for s in term["coursework"]["steps"]}
    lab = term["laboratory"]
    W, row, top, x_wk, x_act, x_ses, w_ses, x_cw, w_cw, x_lab, w_lab = 1000, 34, 58, 22, 86, 128, 496, 640, 190, 846, 124
    h_of = {r["n"]: row * max(1, len(r["sessions"])) for r in cal}
    y_of, y = {}, top
    for n in range(1, 13):
        y_of[n] = y
        y += h_of[n]
    H = y + 64
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Trebuchet MS, Arial, sans-serif" role="img" '
         f'aria-labelledby="t d"><title id="t">The control half, week by week, {term["year"]}</title>'
         f'<desc id="d">Twelve weeks down the page. Each row gives the week, the act, what happens that week, '
         f'the coursework event if any, and the open-access laboratory window.</desc>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         '<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<line x1="0" y1="0" x2="0" y2="6" stroke="#e4e4e4" stroke-width="1.5"/></pattern></defs>']
    hdr = f'font-size="15" font-weight="700" fill="{INK}"'
    o += [f'<text x="{x_wk + 24}" y="36" {hdr} text-anchor="middle">Week</text>',
          f'<text x="{x_act}" y="36" {hdr} text-anchor="middle">Act</text>',
          f'<text x="{x_ses}" y="36" {hdr}>This week</text>',
          f'<text x="{x_cw}" y="36" {hdr}>Coursework</text>',
          f'<text x="{x_lab}" y="36" {hdr}>Laboratory</text>',
          f'<line x1="20" y1="46" x2="{W - 20}" y2="46" stroke="{RED}" stroke-width="2"/>']
    y0 = y_of[lab["from_week"]] + 3
    y1 = y_of[lab["to_week"]] + h_of[lab["to_week"]] - 3
    o += [f'<rect x="{x_lab}" y="{y0}" width="{w_lab}" height="{y1 - y0}" rx="6" fill="#fff" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="5 4"/>',
          f'<text x="{x_lab + w_lab / 2}" y="{(y0 + y1) / 2 - 4}" font-size="14" font-weight="700" fill="{INK}" text-anchor="middle">Quanser</text>',
          f'<text x="{x_lab + w_lab / 2}" y="{(y0 + y1) / 2 + 14}" font-size="13" fill="{MUTED}" text-anchor="middle">open access</text>']
    styles = {"lecture": (RED_TINT, RED, INK, ""), "guest": ("#fff", RED, INK, ""),
              "consolidation": ("#fff", RED, INK, ' stroke-dasharray="5 3"'), None: ("url(#hatch)", RULE, MUTED, "")}
    for r in cal:
        n, ss = r["n"], r["sessions"]
        y = y_of[n]
        o.append(f'<text x="{x_wk + 24}" y="{y + row / 2 + 5}" font-size="15" font-weight="700" fill="{INK}" text-anchor="middle">{n}</text>')
        # An empty week still gets a box, so the eye reads "nothing here" rather
        # than skipping the row: hatched for revision, and named for a week the
        # timetable took away.
        boxes = ss or [None]
        for i, sn in enumerate(boxes):
            by = y + i * row
            fill, stroke, colour, dash = styles[sn["w"]["kind"] if sn else None]
            text = session_label(sn, term, len(ss) > 1 or sn["moved"]) if sn else (r["why"] or ("Revision week" if n == term["revision_week"] else ""))
            o.append(f'<rect x="{x_ses}" y="{by + 4}" width="{w_ses}" height="{row - 8}" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="1"{dash}/>')
            o.append(f'<text x="{x_ses + 12}" y="{by + row / 2 + 5}" font-size="{14 if sn else 13}" fill="{colour}" stroke="{"#fff" if not sn else "none"}" '
                     f'stroke-width="5" paint-order="stroke">{e(text)}</text>')
        ev = cw.get(n, {}).get("event")
        if ev:
            deadline = ev == "Deadline"
            text = f'Due {term["coursework"]["deadline"]["day"]}' if deadline else ev
            o.append(f'<rect x="{x_cw}" y="{y + 5}" width="{w_cw}" height="{row - 10}" rx="12" fill="{RED if deadline else "#fff"}" stroke="{RED}" stroke-width="1.2"/>')
            o.append(f'<text x="{x_cw + w_cw / 2}" y="{y + row / 2 + 4}" font-size="13" font-weight="700" fill="{"#fff" if deadline else RED}" text-anchor="middle">{e(text)}</text>')
    # Acts bracket calendar weeks, so an act that straddles a doubled week has
    # to be measured in pixels rather than counted in rows.
    cal_of = {s["w"]["week"]: r["n"] for r in cal for s in r["sessions"]}
    for act in sorted(acts):
        ns = [cal_of[w["week"]] for w in weeks if w.get("act") == act and w["week"] in cal_of]
        a, b = min(ns), max(ns)
        o.append(f'<line x1="{x_ses - 10}" y1="{y_of[a] + 6}" x2="{x_ses - 10}" y2="{y_of[b] + h_of[b] - 6}" stroke="{RED}" stroke-width="2"/>')
        o.append(f'<text x="{x_act}" y="{(y_of[a] + y_of[b] + h_of[b]) / 2 + 5}" font-size="15" font-weight="700" fill="{RED}" text-anchor="middle">{"I" * act}</text>')
    ly = y_of[12] + h_of[12] + 30
    x = x_ses
    for fill, stroke, dash, text in ((RED_TINT, RED, "", "Lecture"), ("#fff", RED, "", "Guest lecture"),
                                     ("#fff", RED, ' stroke-dasharray="4 2"', "Consolidation"), ("url(#hatch)", RULE, "", "No session")):
        o.append(f'<rect x="{x}" y="{ly - 13}" width="18" height="18" rx="4" fill="{fill}" stroke="{stroke}"{dash}/>')
        o.append(f'<text x="{x + 26}" y="{ly + 1}" font-size="13" fill="{MUTED}">{text}</text>')
        x += 150
    d = term["coursework"]["deadline"]
    o.append(f'<text x="{W - 20}" y="{ly + 1}" font-size="13" fill="{MUTED}" text-anchor="end">Coursework due {d["day"]} of week {d["week"]}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


# ------------------------------------------------------------ lecture map
SLOTS = [("hook", "Hook and recall", 5), ("learn_a", "Learn A", 15), ("do_a", "Do A", 10),
         ("learn_b", "Learn B", 15), ("do_b", "Do B", 10), (None, "Changeover", 5),
         ("case", "Case brief, build, converge", 40), ("cliffhanger", "Cliffhanger", 10)]
PART_NAMES = [("close_the_loop", "1. Close the loop"), ("examples", "2. Work the examples"),
              ("feed", "3. Feed the design"), ("next_case", "4. Meet next week's case")]
COLOURS = {"lecture": "var(--red)", "independent": "var(--i5)", "consolidation": "var(--i6)", "coursework": "var(--i4)"}


def workload_html(wl: dict) -> str:
    t, lw, cons = wl["totals"], wl["lecture_week"], wl["consolidation"]
    top = max(r["total"] for r in wl["rows"]) or 1
    cols = []
    for r in wl["rows"]:
        segs = "".join(f'<i style="height:{r[c] / top * 84:.1f}px;background:{COLOURS[c]}" title="{c}, {r[c]:g} h"></i>'
                       for c in reversed(CATS) if r[c])
        cols.append(f'<div class="wcol"><b>{r["total"]:g}</b><div class="stack">{segs}</div>'
                    f'<span>{r["week"]}</span>{"<u></u>" if r["lab_window"] else ""}</div>')
    keys = " ".join(f'<span class="key" style="background:{COLOURS[c]}"></span>{c}' for c in CATS)
    return f"""<h2 class="act">Student workload</h2>
<div class="tiles">
  <div class="tile"><div class="big">{wl["typical"]:g} h</div><div>a lecture week: {lw["lecture"]:g} lecture · {lw["independent"]:g} independent · {lw["coursework"]:g} coursework. Consolidation week: {cons["consolidation"]:g} consolidation · {cons["coursework"]:g} coursework</div></div>
  <div class="tile"><div class="big">+{wl["laboratory"]:g} h</div><div>Quanser laboratory, in total, on top — self-scheduled in weeks {wl["lab"]["from_week"]} to {wl["lab"]["to_week"]}</div></div>
  <div class="tile"><div class="big">{wl["planned"]:g} h</div><div>planned over the term: {t["lecture"]:g} lecture, {t["independent"]:g} independent, {t["consolidation"]:g} consolidation, {t["coursework"]:g} coursework, {t["laboratory"]:g} laboratory</div></div>
  <div class="tile warnt"><div class="big">{wl["notional"]:g} h</div><div>notional for 10 credits. The {wl["notional"] - wl["planned"]:g} h difference is a deliberate compromise, for a sustainable week</div></div>
</div>
<div class="wchart">{''.join(cols)}</div>
<p class="legend wl"><b>Why six hours:</b> a ~{wl["working_week"]:g} h working week across {wl["units_at_once"]} units of 20 credits is just under {wl["working_week"] / wl["units_at_once"]:.0f} h per unit, so about {wl["share"]:.0f} h for this half. The 10-hours-a-credit total doesn't fit a twelve-week teaching block, with week 12 lost to revision.</p>
<p class="legend wl">{keys} — hours per week, to scale. Dashed underline: laboratory window. Coursework is advised in-week; expect many students to back-load it towards the deadline, which the checkpoints and the consolidation week exist to pull forward.</p>"""


def lecture_card(w: dict, term: dict, wl: dict, sources: dict, when_of: dict) -> str:
    cw = {s["week"]: s for s in term["coursework"]["steps"]}
    slot_rows = "".join(f'<tr><td class="sl">{name}<small>{mins} min</small></td>'
                        f'<td>{e(w["cliffhanger"] if key == "cliffhanger" else w["in_lecture"][key])}</td></tr>'
                        for key, name, mins in SLOTS if key)
    bar = "".join(f'<span class="s s-{(k or "gap").replace("_", "")}" style="flex:{m}" title="{e(nm)}, {m} min"></span>'
                  for k, nm, m in SLOTS)
    part_rows = "".join(f'<tr><td class="sl">{name}<small>{hrs(wl["parts"][key])}</small></td>'
                        f'<td>{e(cw.get(w["week"], {}).get("step", "") if key == "feed" else w["out_of_lecture"][key])}</td></tr>'
                        for key, name in PART_NAMES)
    outs = "".join(f'<li><span class="ilo i{o["ilo"]}">{o["ilo"]}</span>{e(o["text"])}</li>' for o in w["outcomes"])
    b = w["budget"]
    vclass = "ok" if b["verdict"] == "fits" else ("na" if b["verdict"].startswith("awareness") else "warn")
    chips = "".join(f'<span class="chip">{e(t)}</span>' for t in w["threshold"]) or '<span class="muted">none new</span>'
    slot = when_of.get(w["week"], term["day"])
    when = f"{slot} · hour 2: {w['second_hour']}" if w.get("second_hour") else slot
    lw = wl["lecture_week"]
    reading = "".join(f"<li>{e(reading_line(r, sources))}</li>" for r in w.get("reading", [])) or '<li class="muted">none yet</li>'
    return f"""
<section class="card" id="W{w['week']}">
  <header><div class="num">W{w['week']}</div>
    <div class="tt"><h3>{e(w['title'])}</h3><p class="q">{e(w['question'])}</p></div><div class="when">{e(when)}</div></header>
  <div class="grid">
    <div class="col id"><dl>
      <dt>Focus</dt><dd>{e(w['focus'])}</dd>
      <dt>Threshold</dt><dd>{chips}</dd>
      <dt>System</dt><dd>{e(', '.join(w['systems']))}</dd>
      <dt>Case</dt><dd>{e(w['case'])}</dd>
      <dt>P19 budget</dt><dd><span class="v {vclass}">{e(b['verdict'])}</span><br><small>{e(', '.join(b['concepts']) or '—')} · {e(', '.join(b['tool']) or '—')} · {e(', '.join(b['notation']) or '—')}</small></dd>
      <dt>Handout only</dt><dd><small>{e('; '.join(w['handout_only']))}</small></dd>
      <dt>Reading</dt><dd><ul class="rd">{reading}</ul></dd>
    </dl></div>
    <div class="col"><h4>Learning outcomes</h4><ul class="lo">{outs}</ul><p class="hk"><b>Hook</b> {e(w['hook'])}</p></div>
    <div class="col"><h4>In the room <small>110 min</small></h4><div class="bar">{bar}</div><table class="sl-t">{slot_rows}</table></div>
    <div class="col"><h4>Between sessions <small>{hrs(lw["independent"])} independent + {hrs(lw["coursework"])} coursework</small></h4>
      <table class="sl-t">{part_rows}</table>{f'<p class="note">{e(w["notes"])}</p>' if w.get('notes') else ''}</div>
  </div>
</section>"""


def other_card(w: dict, term: dict, wl: dict) -> str:
    cw = {s["week"]: s for s in term["coursework"]["steps"]}
    if w["kind"] == "guest":
        lw = wl["lecture_week"]
        body = f"""<div class="grid g2">
    <div class="col"><h4>The session</h4><p>{e(w['note'])}</p></div>
    <div class="col"><h4>Between sessions <small>{hrs(lw["independent"])} independent + {hrs(lw["coursework"])} coursework</small></h4>
      <table class="sl-t"><tr><td class="sl">Independent<small>{hrs(lw["independent"])}</small></td><td>{e(w['independent'])}</td></tr>
      <tr><td class="sl">3. Feed the design<small>{hrs(lw["coursework"])}</small></td><td>{e(cw.get(w['week'], {}).get('step', ''))}</td></tr></table></div></div>"""
    else:
        cons = wl["consolidation"]
        acts = "".join(f'<tr><td class="sl">{e(a["title"])}<small>{hrs(a["hours"])}</small></td><td>{e(a["what"])}</td></tr>'
                       for a in w["activities"])
        body = f"""<div class="grid g2">
    <div class="col"><h4>Purpose</h4><p>{e(w['purpose'])}</p><p class="hk"><b>Laboratory</b> {e(w['laboratory'])}</p></div>
    <div class="col"><h4>Recommended activities <small>{hrs(cons["consolidation"])} consolidation + {hrs(cons["coursework"])} coursework</small></h4>
      <table class="sl-t">{acts}<tr><td class="sl">Coursework<small>{hrs(cons["coursework"])}</small></td><td>{e(w['coursework'])}</td></tr></table></div></div>"""
    return f"""
<section class="card other" id="W{w['week']}">
  <header><div class="num alt">W{w['week']}</div><div class="tt"><h3>{e(w['title'])}</h3></div>
    <div class="when">{"No lecture" if w["kind"] == "consolidation" else "Tuesday · unnumbered guest"}</div></header>
  {body}
</section>"""


def lecture_map(weeks: list[dict], term: dict, acts: dict, wl: dict, sources: dict) -> str:
    cw = {s["week"]: s for s in term["coursework"]["steps"]}
    lectures = [w for w in weeks if w["kind"] == "lecture"]
    when_of = {x["w"]["week"]: x["day"] for r in calendar(weeks, term) for x in r["sessions"]}
    strip = []
    for r in calendar(weeks, term):
        n, ss = r["n"], r["sessions"]
        k = ss[0]["w"]["kind"] if len(ss) == 1 else ("none" if not ss else "lecture")
        if ss:
            name = " · ".join(f'{x["day"][:3]} {x["w"]["short"]}' if len(ss) > 1 or x["moved"]
                                   else x["w"]["short"] for x in ss)
        else:
            name = "No session" if r["why"] else ("Revision" if n == term["revision_week"] else "")
        ev = cw.get(n, {}).get("event", "")
        lab = term["laboratory"]["from_week"] <= n <= term["laboratory"]["to_week"]
        strip.append(f'<div class="wk k-{k}"><b>Week {n}</b><span>{e(name)}</span>'
                     f'{f"<i>{e(ev)}</i>" if ev else ""}{"<u></u>" if lab else ""}</div>')
    mat = ['<table class="mx"><tr><th></th>' + "".join(f"<th>W{w['week']}</th>" for w in lectures) + "</tr>"]
    for ilo, name in ((4, "ILO 4 — stability and robustness"), (5, "ILO 5 — design, classical and modern"), (6, "ILO 6 — aircraft application")):
        cells = "".join(f'<td class="c{min(c, 3)}">{c or ""}</td>'
                        for c in (sum(1 for o in w["outcomes"] if o["ilo"] == ilo) for w in lectures))
        mat.append(f"<tr><th>{name}</th>{cells}</tr>")
    mat.append("</table>")
    cards, prev_lecture, prev_act = [], None, None
    for w in weeks:
        if w["kind"] == "lecture":
            if w["act"] != prev_act:
                cards.append(f'<h2 class="act">{e(acts[w["act"]])}</h2>')
                prev_act = w["act"]
            if prev_lecture:
                gap = w["week"] - prev_lecture["week"] > 1
                cards.append(f'<div class="chain"><span>cliffhanger, week {prev_lecture["week"]}</span> {e(prev_lecture["cliffhanger"])} '
                             f'<span>→ hook of week {w["week"]}{" (across the break)" if gap else ""}</span></div>')
            cards.append(lecture_card(w, term, wl, sources, when_of))
            prev_lecture = w
        else:
            cards.append(other_card(w, term, wl))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lecture map — CADE30008 control half, {e(term['year'])}</title>
<style>
:root{{--red:#b01c2e;--tint:#f6e3e5;--ink:#1a1a1a;--mut:#5f5f5f;--rule:#d9d9d9;--bg:#fafafa;--card:#fff;--i4:#534ab7;--i5:#0f6e56;--i6:#b35a1f}}
@media (prefers-color-scheme:dark){{:root{{--tint:#3a1a1e;--ink:#ececec;--mut:#a8a8a8;--rule:#3a3a40;--bg:#17171b;--card:#1f1f24;--i4:#afa9ec;--i5:#5dcaa5;--i6:#f0997b}}}}
*{{box-sizing:border-box}}body{{margin:0;padding:24px clamp(16px,3vw,40px) 60px;font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:var(--bg)}}
h1{{font-size:22px;margin:0 0 4px}}.sub{{color:var(--mut);margin:0 0 18px;max-width:80ch}}
h2.act{{font-size:15px;color:var(--red);border-bottom:2px solid var(--red);padding-bottom:4px;margin:28px 0 12px}}
.strip{{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:4px;margin:8px 0 18px}}
.wk{{background:var(--card);border:1px solid var(--rule);border-radius:6px;padding:6px 4px 8px;text-align:center;position:relative;min-height:78px}}
.wk b{{display:block;font-size:11.5px;color:var(--mut);font-weight:600}}.wk span{{display:block;font-weight:600;font-size:12.5px;margin-top:2px;overflow-wrap:anywhere}}
.wk i{{display:block;font-style:normal;font-size:11px;color:var(--red);margin-top:3px;font-weight:600}}
.wk u{{position:absolute;left:6px;right:6px;bottom:3px;border-bottom:2px dashed var(--mut)}}
.k-lecture{{background:var(--tint);border-color:var(--red)}}.k-guest{{border-color:var(--red)}}.k-consolidation{{border:1.5px dashed var(--red)}}
.k-none{{background:repeating-linear-gradient(45deg,transparent 0 5px,var(--rule) 5px 6px);color:var(--mut)}}
.legend{{font-size:12px;color:var(--mut);margin:-10px 0 18px}}
.mxw{{overflow-x:auto;margin-bottom:8px}}.mx{{border-collapse:collapse;font-size:12px}}.mx th,.mx td{{border:1px solid var(--rule);padding:4px 8px;text-align:center}}.mx th:first-child{{text-align:left;font-weight:500}}
.mx .c1{{background:color-mix(in srgb,var(--red) 18%,transparent)}}.mx .c2{{background:color-mix(in srgb,var(--red) 38%,transparent)}}.mx .c3{{background:color-mix(in srgb,var(--red) 60%,transparent);color:#fff}}
.card{{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:14px 16px;margin:0}}.card.other{{border-style:dashed;border-color:var(--red);margin:12px 0}}
.card header{{display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap;border-bottom:1px solid var(--rule);padding-bottom:10px;margin-bottom:10px}}
.num{{background:var(--red);color:#fff;font-weight:700;border-radius:6px;padding:4px 9px;font-size:15px}}.num.alt{{background:var(--card);color:var(--red);border:1.5px solid var(--red)}}
.tt{{flex:1;min-width:220px}}.tt h3{{margin:0;font-size:17px}}.q{{margin:2px 0 0;color:var(--mut);font-style:italic}}
.when{{font-size:12px;color:var(--red);font-weight:600;white-space:nowrap}}
.grid{{display:grid;grid-template-columns:1fr 1.25fr 1.5fr 1.25fr;gap:16px}}.grid.g2{{grid-template-columns:1fr 2fr}}
@media (max-width:1100px){{.grid{{grid-template-columns:1fr 1fr}}}}@media (max-width:640px){{.grid,.grid.g2{{grid-template-columns:1fr}}.strip{{grid-template-columns:repeat(4,minmax(0,1fr))}}}}
h4{{font-size:12px;margin:0 0 6px;color:var(--mut);font-weight:600}}h4 small{{font-weight:400}}
.col p{{font-size:12.5px;margin:0 0 6px}}
dl{{margin:0;display:grid;grid-template-columns:auto 1fr;gap:4px 10px;font-size:12.5px}}dt{{color:var(--mut)}}dd{{margin:0}}
.chip{{display:inline-block;background:var(--tint);border:1px solid var(--red);border-radius:10px;padding:0 7px;margin:0 3px 3px 0;font-size:11.5px}}
.muted{{color:var(--mut)}}.v{{font-weight:600;font-size:12px}}.v.ok{{color:var(--i5)}}.v.warn{{color:var(--red)}}.v.na{{color:var(--mut)}}
ul.lo{{list-style:none;margin:0;padding:0}}ul.lo li{{display:flex;gap:7px;margin-bottom:5px;font-size:12.5px}}
.ilo{{flex:none;font-size:10.5px;font-weight:700;border-radius:4px;padding:1px 5px;height:fit-content;color:#fff}}.i4{{background:var(--i4)}}.i5{{background:var(--i5)}}.i6{{background:var(--i6)}}
.hk{{font-size:12.5px;margin:8px 0 0;padding:6px 8px;border-left:3px solid var(--red);background:var(--tint)}}
.bar{{display:flex;height:10px;border-radius:3px;overflow:hidden;margin-bottom:6px;border:1px solid var(--rule)}}
.s{{display:block}}.s-hook,.s-cliffhanger{{background:var(--red)}}.s-learna,.s-learnb{{background:var(--i4)}}.s-doa,.s-dob{{background:var(--i5)}}.s-gap{{background:var(--rule)}}.s-case{{background:var(--i6)}}
table.sl-t{{border-collapse:collapse;width:100%;font-size:12.5px}}.sl-t td{{border-top:1px solid var(--rule);padding:4px 4px;vertical-align:top}}
.sl{{width:36%;color:var(--mut);font-weight:600}}.sl small{{display:block;font-weight:400}}
ul.rd{{margin:0;padding-left:14px;font-size:12px}}ul.rd li{{margin-bottom:2px}}
.note{{font-size:12px;color:var(--mut);border-top:1px dashed var(--rule);margin-top:8px;padding-top:6px}}
.chain{{margin:6px 0 6px 22px;padding:4px 0 4px 14px;border-left:2px dashed var(--red);font-size:12.5px;font-style:italic}}.chain span{{font-style:normal;font-weight:600;color:var(--red);font-size:11.5px}}
.tiles{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:6px 0 14px}}
.tile{{background:var(--card);border:1px solid var(--rule);border-radius:8px;padding:10px 12px;font-size:12.5px;color:var(--mut)}}
.tile .big{{font-size:22px;font-weight:700;color:var(--ink);margin-bottom:2px}}.tile.warnt{{border-color:var(--red)}}
.wchart{{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:6px;align-items:end;margin-bottom:6px}}
.wcol{{text-align:center;font-size:12px;position:relative;padding-bottom:6px}}.wcol b{{display:block;font-size:12px}}.wcol span{{color:var(--mut)}}
.stack{{display:flex;flex-direction:column;justify-content:flex-end;height:86px;border-bottom:1px solid var(--rule)}}
.stack i{{display:block;width:70%;margin:0 auto 1px}}.wcol u{{position:absolute;left:8%;right:8%;bottom:0;border-bottom:2px dashed var(--mut)}}
.legend.wl{{margin:10px 0 18px}}.key{{display:inline-block;width:11px;height:11px;border-radius:2px;vertical-align:-1px;margin:0 3px 0 8px}}
@media (max-width:900px){{.tiles{{grid-template-columns:1fr 1fr}}}}
footer{{margin-top:28px;font-size:12px;color:var(--mut)}}
@media print{{body{{background:#fff}}.card{{break-inside:avoid}}}}
</style></head><body>
<h1>Lecture map — the control half, {e(term['year'])}</h1>
<p class="sub">A lecturer-facing planning view: what each week does, how the term fits together, and what it asks of students. Generated by <code>scripts/build_curriculum.py</code> from <code>curriculum/weeks.yaml</code> and <code>curriculum/term.yaml</code>; edit those, not this. Scope is agreed in outline (option B, CURRICULUM.md), for review.</p>
{workload_html(wl)}
<h2 class="act">The term</h2>
<div class="strip">{''.join(strip)}</div>
<p class="legend">Solid red: a lecture week. Outlined: the guest lecture. Dashed: the consolidation week. Hatched: no session. Red text: coursework. Dashed underline: the laboratory window.</p>
<div class="mxw">{''.join(mat)}</div>
<p class="legend">Learning outcomes per lecture week per ILO. Colour bar in each card: hook and cliffhanger red, Learn slots purple, Do slots green, the case hour orange, to scale over 110 minutes.</p>
{''.join(cards)}
<footer>CADE30008 · Steve Bullock · generated from the curriculum sources. Teaching material CC BY 4.0.</footer>
</body></html>
"""


# ------------------------------------------------------- generated blocks
def home_table(weeks: list[dict]) -> str:
    rows = ["| Week | Topic | Materials |", "|---|---|---|"]
    for w in weeks:
        s = w["slug"]
        if w["kind"] == "lecture":
            links = (f"[Handout]({s}/index.md) · [Slides](slides/{s}/index.html) · "
                     f"[Example sheet]({s}/example-sheet.md) · [Solutions]({s}/solutions.md)")
        elif w["kind"] == "guest":
            links = f"[Details]({s}/index.md)"
        else:
            links = f"[Recommended activities]({s}/index.md)"
        rows.append(f"| {w['week']} | {w['title']} | {links} |")
    return "\n".join(rows)


def session_cell(s: dict, term: dict, prefix_day: bool) -> str:
    """One session in a calendar table: the link, and the day when it isn't the usual one."""
    w = s["w"]
    if w["kind"] == "consolidation":
        return f"[Consolidation week](../{w['slug']}/index.md): no lecture; recommended activities."
    what = f"[{w['title']}](../{w['slug']}/index.md)"
    if w.get("second_hour"):
        what += f"; then {w['second_hour'][0].lower() + w['second_hour'][1:]}."
    if prefix_day or s["moved"]:
        what = f"**{session_when(s, term)}:** {what}"
    return what


def schedule_table(weeks: list[dict], term: dict) -> str:
    """The twelve weeks as a table, for week 1's handout: the text version of the term map."""
    cal = calendar(weeks, term)
    cw = {s["week"]: s for s in term["coursework"]["steps"]}
    rows = [f"*{term['year']}. Lectures are on {term['day']}s unless a week below says otherwise.*", ""]
    if note := schedule_note(weeks, term):
        rows += [note, ""]
    rows += ["| Week | This week | Coursework |", "|---|---|---|"]
    for r in cal:
        n, ss = r["n"], r["sessions"]
        if r["why"]:
            what = f"*{r['why']}*"
        elif not ss:
            what = "*Revision week*" if n == term["revision_week"] else ""
        else:
            what = "<br>".join(session_cell(s, term, len(ss) > 1) for s in ss)
        ev = cw.get(n, {}).get("event", "")
        if ev == "Deadline":
            d = term["coursework"]["deadline"]
            ev = f"**Due {d['day']} of week {d['week']}**"
        rows.append(f"| {n} | {what} | {ev} |")
    lab = term["laboratory"]
    rows += ["", f"The Quanser laboratory is open access from week {lab['from_week']} to week "
                 f"{lab['to_week']}: you choose when to go, but the slots are booked. "
                 f"You work in {lab['group_size']}, and **one of you books for the "
                 f"group**: {lab['booking'][0].lower()}{lab['booking'][1:]}. Do it "
                 f"early rather than late: the window closes at the end of week "
                 f"{lab['to_week']}, which is before the coursework gets hard."]
    return "\n".join(rows)


def workload_block(wl: dict) -> str:
    """Week 1's 'your week' table: the student-facing view of the workload model."""
    lw, cons, t, parts = wl["lecture_week"], wl["consolidation"], wl["totals"], wl["parts"]
    return "\n".join([
        "| In a week with a lecture | Hours |", "|---|---|",
        f"| The lecture, on Tuesday | {lw['lecture']:g} |",
        f"| Independent learning: go back over the handout and do the week's challenge ({hrs(parts['close_the_loop'])}), "
        f"work the example sheet ({hrs(parts['examples'])}), and look at next week's case ({hrs(parts['next_case'])}). | {lw['independent']:g} |",
        f"| Coursework | {lw['coursework']:g} |",
        f"| **Total** | **{wl['typical']:g}** |", "",
        f"**Consolidation week** has no lecture. Instead, {cons['consolidation']:g} hours of recommended activities that "
        f"cement what you've done so far, plus the usual {cons['coursework']:g} hours of coursework.", "",
        f"Why six? A full-time working week is about {wl['working_week']:g} hours, and you take "
        f"{['one', 'two', 'three', 'four', 'five'][wl['units_at_once'] - 1]} "
        f"units at once, so each gets just under {wl['working_week'] / wl['units_at_once']:.0f} hours a week — and this "
        f"is half of one.", "",
        f"On top of that, **{wl['laboratory']:g} hours in the Quanser laboratory**, at times you choose between week "
        f"{wl['lab']['from_week']} and week {wl['lab']['to_week']}. Over the term that comes to about {wl['planned']:g} hours: "
        f"{t['lecture']:g} in lectures, {t['independent']:g} of independent learning, {t['consolidation']:g} of consolidation, "
        f"{t['coursework']:g} of coursework and {t['laboratory']:g} in the laboratory.",
    ])


def activities_block(w: dict, wl: dict) -> str:
    cons = wl["consolidation"]
    rows = ["| Activity | Time | What to do |", "|---|---|---|"]
    rows += [f"| **{a['title']}** | {hrs(a['hours'])} | {stop(a['what'])} |" for a in w["activities"]]
    rows += [f"| **Coursework** | {hrs(cons['coursework'])} | {stop(w['coursework'])} |",
             f"| **Total** | {hrs(cons['consolidation'] + cons['coursework'])} | |"]
    return "\n".join(rows)


def outcomes_block(w: dict) -> str:
    items = [f"    - {o['text'][0].lower() + o['text'][1:]};" for o in w["outcomes"]]
    items[-1] = items[-1][:-1] + "."
    return '!!! abstract "Learning outcomes"\n    By the end of this week you should be able to:\n\n' + "\n".join(items)


def reading_line(r: dict, sources: dict) -> str:
    src = sources[r["source"]]
    if r.get("sections"):
        plural = any(c in r["sections"] for c in ",-")
        where = f"section{'s' if plural else ''} {r['sections']}"
    else:
        where = f"chapter {r['chapter']}"
    note = f" — {r['note']}" if r.get("note") else ""
    return f"{src['short']}, {where}: {r['title']}{note}"


def reading_block(w: dict, sources: dict) -> str:
    """A lecture week's further reading, for its handout."""
    if not w.get("reading"):
        return "Further reading for this week is still to be chosen."
    lines = [f"- {reading_line(r, sources)}." for r in w["reading"]]
    used = sorted({r["source"] for r in w["reading"]})
    for k in used:
        src = sources[k]
        eds = src.get("editions")
        where = (f" Section numbers are the same in the {oxford([f'{e}th' for e in sorted(eds)])} editions; "
                 f"only the page numbers differ." if eds else "")
        lines += ["", f"{src['cite']}{where} It is [in the library](../reading.md), "
                      f"and is {src.get('note', 'further reading')}."]
    return "\n".join(lines)


def oxford(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def reading_page(weeks: list[dict], sources: dict) -> str:
    """The recommended-reading page: what the library has, and which sections go with which part of the unit."""
    src = sources["dorf"]
    rows = ["| Edition | Year | Print copies | eBook copies |", "|---|---|---|---|"]
    rows += [f"| {a['edition']}th | {a['year']} | {a['print']} | {a['ebook'] or '—'} |" for a in src["availability"]]
    tips = "\n".join(f"- {t}" for t in src["library"]["etiquette"])
    mapping = ["| Week | What it covers | Sections in Dorf and Bishop |", "|---|---|---|"]
    for w in weeks:
        if w["kind"] != "lecture":
            continue
        # One section group per line. A run-on cell of four groups separated by
        # semicolons is unreadable, and this is a table people scan, not read.
        cells = "<br>".join(f"**{r['sections']}** {r['title']}" for r in w.get("reading", [])) or "*No chapter covers this; a flight-control text is needed*"
        mapping.append(f"| [{w['week']}]({w['slug']}/index.md) | {w['title']} | {cells} |")
    return "\n".join([
        "### What the library has", "",
        f"{src['cite']} Earlier editions than the {min(src['editions'])}th are not mapped here.", "",
        *rows, "",
        src["library"]["search"], "", tips, "",
        "### Which sections go with which week", "",
        f"**Section numbers are the same in the {oxford([f'{e}th' for e in sorted(src['editions'])])} editions**, "
        "so any of them works. Only the page numbers differ.", "",
        *mapping,
    ])


def textbook_block(sources: dict, cohort: int) -> str:
    """Week 1's textbook paragraph: what the library has, and how to share it.

    Generated from the same availability data as the textbook page, so the copy
    counts in the first lecture can't drift from the ones students see later.
    The etiquette matters because the numbers are small: a cohort this size can
    empty the shelf and lock every eBook licence in an afternoon.
    """
    src = sources["dorf"]
    a = src["availability"]
    print_n, ebook_n = sum(x["print"] for x in a), sum(x["ebook"] for x in a)
    tips = "\n".join(f"    - {t}" for t in src["library"]["etiquette"])
    return "\n".join([
        "You don't have to buy a book. Each week's handout is the authoritative",
        "version of what you need, and it stands on its own. One is worth knowing",
        f"about, though: **{src['short']}'s *{src['title']}***. Use it **for additional",
        "study and consolidation** — a second explanation when the handout's doesn't",
        "land, and more worked examples — not as a substitute for the handout.",
        "",
        '!!! tip "Share the library copies"',
        f"    There are **{print_n} print copies and {ebook_n} eBook licences** between",
        f"    about {cohort} of you, so the book only works if everyone takes their turn.",
        "",
        tips,
        "",
        "    So: **download the chapter you want and get out**. Don't leave an eBook",
        "    open in a tab overnight, and don't download the whole book unless you",
        "    really need all of it — that takes a copy away from someone else for a",
        "    day. If everything is out, come back in an hour; it usually isn't for long.",
        "",
        "Which sections go with which part of the unit, and what the library",
        "holds, are on [Recommended reading](../reading.md).",
    ])


def curriculum_page(weeks: list[dict], term: dict, acts: dict, wl: dict) -> str:
    """docs/curriculum.md: the shape of the unit, for students.

    The staff lecture map and this page come from the same data and answer
    different questions. That one says *why* a week is built the way it is:
    threshold concepts, ILO tags, P-numbers, per-session budgets. This one says
    what the unit asks of you and when, which is what a student actually needs
    in week 1 and comes back to in week 7.

    Everything here is in week numbers rather than dates. The weeks are a
    property of the unit and survive a change of year; the dates belong on
    Blackboard, and putting them here would make the page wrong every autumn.
    """
    by_kind = wl["lecture_week"]
    per_week = wl["typical"]
    lab = term["laboratory"]
    cw = term["coursework"]
    planned = wl["planned"]

    rows = ["| Week | | What it covers |", "|---|---|---|"]
    for w in weeks:
        act = f"Act {w['act']}" if w.get("act") else ""
        if w["kind"] == "lecture":
            rows.append(f"| **{w['week']}** | {act} | [{w['title']}]({w['slug']}/index.md) |")
        elif w["kind"] == "consolidation":
            rows.append(f"| **{w['week']}** | {act} | *Consolidation week. No lecture: "
                        f"time to catch up, use the laboratory, and act on feedback.* |")
        else:
            rows.append(f"| **{w['week']}** | {act} | *{w['title']}* |")
    rows.append(f"| **{term['revision_week']}** | | *Revision week. Nothing new.* |")

    spine = ["| Week | What the coursework asks of you |", "|---|---|"]
    for s in cw["steps"]:
        event = f"**{s['event']}.** " if s.get("event") else ""
        spine.append(f"| {s['week']} | {event}{s['step']} |")

    return "\n".join([
        "---",
        # Both quoted: an unquoted value containing a colon is not valid YAML,
        # and the failure surfaces as a build error about byte offsets.
        'title: "How this unit runs"',
        'description: "What each week covers, what you are expected to put into a '
        'week, how the coursework builds, and when the laboratory is open."',
        "---", "",
        "# How this unit runs", "",
        "This page is the shape of the unit in one place: the weeks, what you are",
        "expected to put into one, how the coursework builds, and when the laboratory",
        "is open. It is written in **week numbers**, because those are a property of the",
        "unit. Dates, rooms and deadlines live on Blackboard, which is the version to",
        "trust when the two disagree.", "",
        "## The term at a glance", "",
        f"Eleven weeks of content in {len(acts)} acts, then revision.", "",
        *([note, ""] if (note := schedule_note(weeks, term)) else []),
        # The same figure week 1 carries. Both are written by this script in one
        # run, from these weeks, so the picture and the table cannot disagree.
        "![The control half week by week: what happens each week, the three acts, "
        "the coursework checkpoints and deadline, and the laboratory window]"
        "(figures/term-map.svg){ width=\"100%\" }", "",
        "The same thing as a table, if you would rather read it or follow a link:", "",
        *rows, "",
        "## What you are expected to invest", "",
        f"**About {per_week:g} hours in a lecture week**, including the lecture itself:", "",
        f"- **{by_kind['lecture']:g} h** in the room with us;",
        f"- **{by_kind['independent']:g} h** independent: closing the loop on the last session, "
        "the example sheet, and a look ahead at the next case;",
        f"- **{by_kind['coursework']:g} h** on the coursework, which is designed to be done "
        "a little each week rather than in a block at the end.", "",
        f"Plus **{wl['laboratory']:g} hours of laboratory** in total, across the open window below.", "",
        "![Your week: two hours in the lecture, two on your own and two on the "
        "coursework, six in total. The two independent hours are 45 minutes on the "
        "handout and the week's challenge, an hour on the example sheet and 15 minutes "
        "on next week's case. The consolidation week replaces the lecture and "
        "independent hours with four hours of recommended activities. On top of all "
        "of it, four hours in the Quanser laboratory at times you choose]"
        "(figures/your-week.svg){ width=\"100%\" }", "",
        '!!! info "Why that adds up to less than the credit says"',
        f"    Ten credits is {wl['notional']:g} notional hours. What is planned above comes to",
        f"    roughly **{planned:g} hours** across the term,",
        "    and the gap is deliberate rather than an accounting error.",
        "",
        "    Two reasons. Some of it is slack: a week where the example sheet takes",
        "    longer than it should, or the coursework needs a second attempt, and a",
        "    plan with no slack in it is a plan that fails in week 5. The rest is",
        "    **room to go further**, which is what the remaining time is actually for.",
        "    Dorf and Bishop's worked examples, the reading list on Blackboard, and",
        "    the video series on it are all there for people who want to push past",
        "    what the handouts cover. See [Recommended reading](reading.md).",
        "",
        f"    A {wl['working_week']:g}-hour working week across {wl['units_at_once']} units at once is the",
        "    assumption behind all of it. If a week is taking far more than this,",
        "    that is worth telling us about rather than absorbing.", "",
        "## How the coursework builds", "",
        f"One brief, released in week {cw['steps'][0]['week']} and due in week {cw['deadline']['week']}, "
        f"on the {cw['deadline']['day']}. It is designed to be built a piece",
        "at a time, and the checkpoints exist so that you find out whether you are on",
        "track while there is still time to do something about it.", "",
        *spine, "",
        "## The laboratory", "",
        f"**Open access across weeks {lab['from_week']} to {lab['to_week']}**, self-scheduled, "
        f"about {wl['laboratory']:g} hours in total.", "",
        f"You work at the rig in **{lab['group_size']}**, and **one of you books for",
        "the group** rather than everybody booking separately: the window would fill",
        "three times over otherwise.", "",
        f"There is no timetabled slot, so {lab['booking'][0].lower()}{lab['booking'][1:]},",
        "and treat that as something to do in the first week rather than the first",
        "time you need the rig.", "",
        "The window closes at the end of the consolidation week, not at the end of",
        "term, which is the part people miss: by the time the coursework gets",
        "difficult, the laboratory has shut. Slots also fill from the back, so the",
        "people who book late get the worst of both.", "",
    ])


def status_file(weeks: list[dict], term: dict, pages: set[str]) -> str:
    """STATUS.md: one screen saying where this half of the unit actually is.

    Written for ../steve-todo, which schedules Steve's commitments across units
    and is told not to duplicate the plans of record. A hand-written summary
    there goes stale within days — it already had this repo as "never pushed"
    the morning after it was pushed. So the facts are generated here, from the
    same sources as the site, and that file links to this one.

    Deliberately chunk-level: one row per week, plus the things a week can't run
    without. Granular tasks belong in the repo, not in a scheduler.
    """
    def state(w: dict) -> str:
        page = DOCS / w["slug"] / "index.md"
        if not page.exists():
            return "missing"
        if front_matter(page).get("status") == "draft":
            return "draft"
        return "published" if f"{w['slug']}/index.md" in pages else "written"

    rows = ["| Week | Taught | Session | State | Live |", "|---|---|---|---|---|"]
    for r in calendar(weeks, term):
        for sn in r["sessions"]:
            w = sn["w"]
            st = state(w)
            rows.append(f"| {w['week']} | {session_date(r['n'], sn['day'], term)} | {w['title']} "
                        f"| {st} | {'yes' if st == 'published' else 'no'} |")

    needs = []
    for w in weeks:
        for n in w.get("needs", []):
            if not n.get("done"):
                who = "**Steve**" if n["who"] == "steve" else "can be built"
                needs.append(f"| {w['week']} | {stop(n['what'])} | {who} |")
    blockers = (["| Week | What's missing | Who |", "|---|---|---|", *needs] if needs
                else ["Nothing outstanding is recorded."])

    drafts = sum(1 for w in weeks if state(w) == "draft")
    return "\n".join([
        "# CADE30008 control half: where it is",
        "",
        "<!-- Generated by scripts/build_curriculum.py (`npm run curriculum`). Don't edit by hand. -->",
        "",
        "The plans of record are [PLAN.md](PLAN.md), [CURRICULUM.md](CURRICULUM.md) and",
        "`curriculum/*.yaml`; the authoring rules are [AGENTS.md](AGENTS.md). This page",
        "is the one-screen summary, for scheduling elsewhere. It is generated, so it",
        "can't drift from the site.",
        "",
        "## Fixed points",
        "",
        f"- **Lectures:** {term['day']}s {term['time']}, {term['room']}.",
        f"- **Cohort:** about {term['cohort']}.",
        f"- **Coursework due:** {term['coursework']['deadline']['day']} of week "
        f"{term['coursework']['deadline']['week']}. Checkpoints in weeks "
        f"{oxford([str(s['week']) for s in term['coursework']['steps'] if str(s.get('event', '')).startswith('Checkpoint')])}.",
        f"- **Consolidation week:** {term['consolidation_week']}, no lectures. "
        f"**Revision week:** {term['revision_week']}, nothing planned.",
        f"- **Laboratory:** open access, weeks {term['laboratory']['from_week']} to "
        f"{term['laboratory']['to_week']}, self-scheduled.",
        "",
        "## Weeks",
        "",
        "`draft` is scaffolding only and is skipped by the sync check. `written` means",
        "there is real content; `published` means it is on the live site. "
        f"**{drafts} of {len(weeks)} weeks are still draft.**",
        "",
        *rows,
        "",
        "## What a week can't run without",
        "",
        *blockers,
        "",
        "## Published to the live site",
        "",
        *[f"- `{p}`" for p in sorted(pages)],
    ])


def session_date(cal_week: int, day: str, term: dict) -> str:
    """The date of a session, counted forward from week 1's lecture (term.yaml).

    week1_date is the timetabled day of calendar week 1, so the offset to any
    other day is the difference in weekday, which keeps a Thursday session in
    the week it belongs to rather than a week later.
    """
    d = (term["week1_date"] + timedelta(weeks=cal_week - 1)
         + timedelta(days=DAYS.index(day) - DAYS.index(term["day"])))
    return d.strftime("%a %-d %b")



def week_svg(wl: dict, term: dict) -> str:
    """"Your week", as a picture: where six hours a week actually go.

    A table of hours is read as bookkeeping. The point week 1 has to land is
    that the week is *already designed* and it is not heroic - so the shape of
    it, seen at a glance, does more work than the numbers. Three equal blocks,
    with the independent hours opened up to show they are specified rather than
    vague, and the laboratory sitting outside the bar because it is on top.

    Generated from term.yaml's workload model, so it cannot drift from the
    table beside it or from the lecture map.
    """
    m = term["workload"]
    lec, con = m["by_kind"]["lecture"], m["by_kind"]["consolidation"]
    parts = m["independent_parts"]
    total = sum(lec.values())
    labels = {"close_the_loop": "Handout and the week's challenge",
              "examples": "Example sheet", "next_case": "Next week's case"}

    # Height is computed, not chosen: the laboratory strip is the last thing on
    # the canvas and a fixed viewBox clipped it.
    W, x0, bar_w, bar_h = 1000, 150, 760, 54
    y_bar, y_parts = 62, 62 + bar_h + 34
    y_con = y_parts + bar_h + 32
    y_lab = y_con + bar_h + 30
    H = y_lab + 38 + 22
    px = bar_w / total                                   # pixels per hour
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="Trebuchet MS, Arial, sans-serif" role="img" aria-labelledby="t d">'
         f'<title id="t">Your week: {total:g} hours</title>'
         f'<desc id="d">A week with a lecture is {lec["lecture"]:g} hours of lecture, '
         f'{lec["independent"]:g} of independent learning and {lec["coursework"]:g} of coursework, '
         f'{total:g} in total. The independent hours are '
         + ", ".join(f"{v:g} h {labels[k].lower()}" for k, v in parts.items())
         + f'. Consolidation week replaces the lecture and independent hours with '
         f'{con["consolidation"]:g} hours of recommended activities. On top of all of it, '
         f'{m["laboratory"]:g} hours in the Quanser laboratory, at times you choose.</desc>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']

    def bar(y, segs, label, sub=""):
        out = [f'<text x="{x0 - 16}" y="{y + bar_h / 2 + 1}" font-size="15" font-weight="700" '
               f'fill="{INK}" text-anchor="end">{e(label)}</text>']
        if sub:
            out.append(f'<text x="{x0 - 16}" y="{y + bar_h / 2 + 19}" font-size="12.5" '
                       f'fill="{MUTED}" text-anchor="end">{e(sub)}</text>')
        x = x0
        for hours, text, fill, ink in segs:
            w = hours * px
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{bar_h}" '
                       f'fill="{fill}" stroke="{RED}" stroke-width="1.4"/>')
            out.append(f'<text x="{x + w / 2:.1f}" y="{y + 22}" font-size="14" font-weight="700" '
                       f'fill="{ink}" text-anchor="middle">{hours:g} h</text>')
            out.append(f'<text x="{x + w / 2:.1f}" y="{y + 40}" font-size="12.5" fill="{ink}" '
                       f'text-anchor="middle">{e(text)}</text>')
            x += w
        return out

    o += [f'<text x="{x0}" y="30" font-size="17" font-weight="700" fill="{INK}">'
          f'Your week, every week from 1 to {term["coursework"]["deadline"]["week"]}</text>',
          f'<line x1="{x0}" y1="40" x2="{x0 + bar_w}" y2="40" stroke="{RED}" stroke-width="2"/>']

    y = y_bar
    o += bar(y, [(lec["lecture"], "In the lecture", RED, "#fff"),
                 (lec["independent"], "On your own", RED_TINT, INK),
                 (lec["coursework"], "Coursework", "#fff", INK)],
             "A lecture week", f"{total:g} hours")

    # Open up the independent hours: they are specified, not "do some reading".
    y2 = y_parts
    o.append(f'<path d="M {x0 + lec["lecture"] * px:.1f} {y + bar_h} L {x0} {y2} '
             f'M {x0 + (lec["lecture"] + lec["independent"]) * px:.1f} {y + bar_h} '
             f'L {x0 + bar_w} {y2}" stroke="{RULE}" stroke-width="1.2" fill="none"/>')
    px2 = bar_w / lec["independent"]
    x = x0
    o.append(f'<text x="{x0 - 16}" y="{y2 + 26}" font-size="13.5" fill="{MUTED}" '
             f'text-anchor="end">which is</text>')
    for k, v in parts.items():
        w = v * px2
        # A narrow segment cannot hold its caption at full size. Shrink the
        # caption to fit rather than letting it spill over its neighbours.
        cap = min(11.5, max(8.0, (w - 8) / (0.52 * len(labels[k]))))
        o += [f'<rect x="{x:.1f}" y="{y2}" width="{w:.1f}" height="{bar_h - 10}" fill="{RED_TINT}" '
              f'stroke="{RED}" stroke-width="1.1" stroke-dasharray="4 3"/>',
              f'<text x="{x + w / 2:.1f}" y="{y2 + 19}" font-size="13" font-weight="700" fill="{INK}" '
              f'text-anchor="middle">{v * 60:g} min</text>',
              f'<text x="{x + w / 2:.1f}" y="{y2 + 35}" font-size="{cap:.1f}" fill="{MUTED}" '
              f'text-anchor="middle">{e(labels[k])}</text>']
        x += w

    y3 = y_con
    o += bar(y3, [(con["consolidation"], "Recommended activities", RED_TINT, INK),
                  (con["coursework"], "Coursework", "#fff", INK)],
             f"Week {term['consolidation_week']}", "no lecture")

    y4 = y_lab
    o += [f'<rect x="{x0}" y="{y4}" width="{m["laboratory"] * px:.1f}" height="38" rx="6" fill="#fff" '
          f'stroke="{MUTED}" stroke-width="1.3" stroke-dasharray="5 4"/>',
          f'<text x="{x0 + m["laboratory"] * px / 2:.1f}" y="{y4 + 24}" font-size="13.5" '
          f'font-weight="700" fill="{INK}" text-anchor="middle">{m["laboratory"]:g} h Quanser lab</text>',
          f'<text x="{x0 - 16}" y="{y4 + 24}" font-size="15" font-weight="700" fill="{INK}" '
          f'text-anchor="end">On top</text>',
          f'<text x="{x0 + m["laboratory"] * px + 16:.1f}" y="{y4 + 24}" font-size="13" fill="{MUTED}">'
          f'in total, whenever you like, weeks {term["laboratory"]["from_week"]} to {term["laboratory"]["to_week"]}</text>']
    return "\n".join(o) + "\n</svg>\n"



def stop(text: str) -> str:
    """End a sentence-shaped string with a full stop, per the house style.

    Only for cells and bullets that are prose. A week's *title* is a name and
    never takes one, which is why this is applied at each site rather than to
    every generated string.
    """
    t = text.rstrip()
    return t if not t or t[-1] in ".!?:;" else t + "."


def replace_between(path: Path, start: str, end: str, new: str) -> bool:
    text = path.read_text(encoding="utf-8")
    i, j = text.find(start), text.find(end)
    if i < 0 or j < 0:
        return False
    path.write_text(text[: i + len(start)] + "\n" + new + "\n" + text[j:], encoding="utf-8")
    return True


def main() -> None:
    src = yaml.safe_load((CUR / "weeks.yaml").read_text(encoding="utf-8"))
    weeks, acts, sources = src["weeks"], src["acts"], src.get("sources", {})
    term = yaml.safe_load((CUR / "term.yaml").read_text(encoding="utf-8"))

    check_shape(weeks)
    if errors:
        for x in errors:
            print(f"error    {x}")
        sys.exit(1)
    check(weeks, term)
    check_calendar(calendar(weeks, term), term)
    wl = workload(weeks, term)

    first = next(w for w in weeks if w["kind"] == "lecture")
    fig = DOCS / first["slug"] / "figures"
    fig.mkdir(parents=True, exist_ok=True)
    (fig / "term-map.svg").write_text(term_map_svg(weeks, term, acts), encoding="utf-8")
    (fig / "your-week.svg").write_text(week_svg(wl, term), encoding="utf-8")
    # And again outside the week folders, for pages that are published while
    # week 1 is not: the live build removes unpublished weeks, figures included.
    shared = DOCS / "figures"
    shared.mkdir(parents=True, exist_ok=True)
    (shared / "term-map.svg").write_text(term_map_svg(weeks, term, acts), encoding="utf-8")
    (shared / "your-week.svg").write_text(week_svg(wl, term), encoding="utf-8")
    (DOCS / "staff").mkdir(exist_ok=True)
    (DOCS / "staff" / "lecture-map.html").write_text(lecture_map(weeks, term, acts, wl, sources), encoding="utf-8")
    (DOCS / "curriculum.md").write_text(curriculum_page(weeks, term, acts, wl) + "\n", encoding="utf-8")
    if not replace_between(DOCS / "index.md", "<!-- weeks:start -->", "<!-- weeks:end -->", home_table(weeks)):
        err("docs/index.md has no weeks markers")
    published = set(yaml.safe_load((ROOT / "publish.yaml").read_text(encoding="utf-8"))["pages"])
    (ROOT / "STATUS.md").write_text(status_file(weeks, term, published) + "\n", encoding="utf-8")
    reading_md = DOCS / "reading.md"
    if reading_md.exists() and not replace_between(reading_md, "<!-- reading:start -->", "<!-- reading:end -->", reading_page(weeks, sources)):
        err("docs/reading.md has no reading markers")

    l1 = DOCS / first["slug"] / "index.md"
    for tag, block in (("schedule", schedule_table(weeks, term)),
                       ("workload", workload_block(wl)),
                       ("textbook", textbook_block(sources, term["cohort"]))):
        if not replace_between(l1, f"<!-- {tag}:start -->", f"<!-- {tag}:end -->", block):
            warn(f"week 1's handout has no {tag} markers")
    for w in weeks:
        page = DOCS / w["slug"] / "index.md"
        if not page.exists():
            continue
        if w["kind"] == "lecture" and not replace_between(page, "<!-- outcomes:start -->", "<!-- outcomes:end -->", outcomes_block(w)):
            warn(f"week {w['week']}: handout keeps its own outcomes, not generated from weeks.yaml")
        if w["kind"] == "lecture":
            if not w.get("reading"):
                warn(f"week {w['week']}: no further reading yet")
            for r in w.get("reading", []):
                if r["source"] not in sources:
                    err(f"week {w['week']}: reading cites unknown source {r['source']!r}")
            replace_between(page, "<!-- reading:start -->", "<!-- reading:end -->", reading_block(w, sources))
        if w["kind"] == "consolidation" and not replace_between(page, "<!-- activities:start -->", "<!-- activities:end -->", activities_block(w, wl)):
            err(f"week {w['week']}: page has no activities markers")

    for x in warnings:
        print(f"warning  {x}")
    for x in errors:
        print(f"error    {x}")
    t = wl["totals"]
    print(f"\nworkload: {wl['typical']:g} h in a lecture week; {wl['planned']:g} h planned of {wl['notional']:g} notional "
          f"({t['lecture']:g} lecture, {t['independent']:g} independent, {t['consolidation']:g} consolidation, "
          f"{t['coursework']:g} coursework, {t['laboratory']:g} laboratory)")
    lectures = [w for w in weeks if w["kind"] == "lecture"]
    draft = [w["week"] for w in lectures if front_matter(DOCS / w["slug"] / "index.md").get("status") == "draft"]
    written = f"; {len(lectures) - len(draft)} written, {len(draft)} still draft" if draft else ""
    print(f"{len(errors)} error(s), {len(warnings)} warning(s); {len(weeks)} weeks, {len(lectures)} with lectures{written}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
