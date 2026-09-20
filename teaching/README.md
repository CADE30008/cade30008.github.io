# Run sheets

One file per lecture week, named like its folder (`w01-design-cycle.md`),
written for the person standing at the front. Not student-facing, and not built
into the site.

A run sheet is derived from four things and holds nothing that belongs in any
of them:

- **[curriculum/weeks.yaml](../curriculum/weeks.yaml)** gives the
  lecture's outcomes, what goes in each of P17's slots, its case, its hook and
  its cliffhanger. The run sheet turns those into timings and logistics.
- **[PEDAGOGY.md](../PEDAGOGY.md)** gives the session's shape (P17's slots), how
  the case runs (P18), and the reasoning behind any lecture with a plan of its
  own, such as week 1.
- **The handout** (`docs/<lesson>/index.md`) is authoritative for every fact,
  number and equation. A run sheet never restates one; it points at the section.
- **The deck** (`slides/<lesson>/index.md`) gives the slide order.

Which *week* a lecture falls in is not in the run sheet: it changes between years, and lives in `curriculum/term.yaml`.

So a run sheet answers only: what happens, when, with what in front of you, and
what to do when it goes wrong. If you find yourself writing content into one,
it belongs in the handout.

## The template

Every run sheet has these headings, in this order.

```markdown
# Lecture N: <title> — run sheet

**In advance** — everything that has to be true before you walk in.
**In the room** — set-up, in the order you do it, with times.
**Files** — every file needed, with its path, and where students get theirs.
**Hook** — where the last session left off, and how this one grabs them.
**The plan** — a table of P17's slots: minutes, what happens, what's on screen.
**Cliffhanger** — what the session ends on, and what resolves it next week.
**If it goes wrong** — the two or three failures that are actually likely.
**After** — what to collect, post or check before next week.
```

## Rules

- **Times are cumulative as well as per-slot,** so you can tell at a glance
  whether you are behind.
- **Every file is named with a full path,** including student-facing ones and
  where students get them.
- **The contingencies are real ones.** Three likely failures beat a dozen
  hypothetical ones; a run sheet nobody reads under pressure is useless.
- **Update it the same day you teach it.** What actually took 20 minutes rather
  than 15 is the most valuable thing in the file, and it is also P19 evidence:
  a session that reliably overruns is over budget.
- **Hook and cliffhanger are not the same thing,** and the words are not
  interchangeable. A session opens on its hook and closes on its cliffhanger,
  and week *n*'s cliffhanger is week *n* + 1's hook. P18 defines both.
- **Check the chain.** Session *n*'s Cliffhanger and session *n* + 1's Hook
  should describe the same gap. If they don't, one of the two sessions has
  moved and nobody updated the other.

## The recurring processes

| File | When | What it's for |
|---|---|---|
| [weekly-review.md](weekly-review.md) | Straight after each lecture, then Sunday. | Five lines on what went wrong while it's still obvious, then ten minutes to fix what's cheap and park what isn't. |
| [announcements.md](announcements.md) | Sunday evening | What to post on Blackboard, ready to paste. |
| [matlab-drive.md](matlab-drive.md) | When a session hands out or takes in files, and every year. | The Drive layout, what is shared with whom, and how to test it from a student account. |
| [annual-update.md](annual-update.md) | Before each cohort | Everything with a date or a number in it, then a content review built from the term's weekly notes. |

The three are a loop: the weekly review feeds the annual update, and the annual
update resets the announcements. Skipping the weekly one doesn't cost anything
until August, which is exactly why it gets skipped.
