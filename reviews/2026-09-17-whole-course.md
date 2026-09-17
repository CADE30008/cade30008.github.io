# Review: whole course and processes, 17 September 2026

Scope: everything. `PEDAGOGY.md`, `ASSESSMENT.md`, `AGENTS.md`, `README.md`,
`teaching/`, `docs/`, `slides/`, `models/`, `scripts/`, the site build and the
repository's own checks, against the principles as they stand after P17, P18
and P19 (`556d209`, `0e2afb9`).

Run because the principles changed, which PEDAGOGY.md requires, and because the
course is about to be chunked into weeks — the point at which structural
mistakes get expensive.

## Start here tomorrow

In this order. The first three block the week-by-week plan; the rest don't.

1. **F1, the effort budget.** 44 of about 100 hours are accounted for. Decide
   where the other 56 live before deciding what goes in a week, because the
   answer changes whether 2 hours of independent work a week is right.
2. **F2, no slack in the term.** Eight lectures plus two guest weeks is exactly
   the ten teaching weeks. One cancellation and something is cut.
3. **F5, lectures 4 and 5 are Part A's material.** Two of eight control
   lectures are currently pointed at flight dynamics.
4. **F7, re-review Lecture 2.** The only written lecture, reviewed against six
   principles when thirteen more now exist.
5. Then the concept inventory and the week-by-week.

## Health of the build

Everything mechanical passes.

| Check | Result |
|---|---|
| `zensical build` | No issues |
| `npm run check` | 0 errors, 35 warnings, all "not yet accepted as in sync" on scaffolds |
| `npm test` | Applet maths passes |
| `npm run models` | 41/41 numbers agree between Python and MATLAB |
| Internal links in tracked Markdown | 0 broken |

## Findings

| ID | Principle | Where | Finding | Proposed action |
|---|---|---|---|---|
| F1 | P17, P8 | PEDAGOGY "Delivery" | The effort budget doesn't close. 20 credits is about 200 hours; this half is about 100. Contact is 24 (eight sessions, two guest weeks, four laboratory hours) and core independent work is 20, so 44 are accounted for and **56 are not**. Either the weekly independent hours are set too low, or there is a large unnamed coursework endgame, or the 50/50 split with Part A is wrong | Decide which, and write the resulting budget into PEDAGOGY. If the endgame really is ~50 hours, say so and put it in the term plan, because students will plan around whatever we publish |
| F2 | P17, Q7 | PEDAGOGY "Delivery", Q7 | Eight lectures plus two whole guest weeks is exactly the ten teaching weeks. There is no slack for a cancelled session, an overrun, or a guest pulling out | Either accept and write down what gets cut first, or make one guest week a half. Decide before the grid, not during the term |
| F3 | P18 | Q7, P18 | A guest week breaks the case chain: a cliffhanger set in week *n* is resolved in week *n* + 2, with an unrelated week between. P18 says every cliffhanger is paid off in the next session's hook | Place guest weeks at act boundaries, where a cliffhanger is closing anyway; or have the guest week carry a light standing task. Needs deciding with the grid |
| F4 | P16 | P16, Q7 | Eight challenges plus a week 1 diagnostic across ten weeks leaves the two guest weeks without one. Probably right, but unstated | State it in P16, and decide whether guest weeks are deliberately lighter (P19) |
| F5 | P1, P10 | `docs/l04-*`, `docs/l05-*` | Lectures 4 and 5 are "Longitudinal dynamics and modes" and "Lateral-directional dynamics and modes" — ILOs 1 to 3, taught by Tom. Two of eight control lectures spent re-teaching flight dynamics, against ILOs 4 to 6 | Repoint both at control topics that *use* those dynamics. Settled by the concept inventory |
| F6 | P1 | `docs/l01-*`, `zensical.toml` | Lecture 1 is titled "Course introduction and aircraft models" everywhere on the site, but its plan is the Quanser session running a whole design cycle | Retitle with the grid |
| F7 | all | `docs/l02-*`, `slides/l02-*` | The one written lecture was reviewed on 16 September against P1 to P10 as they then stood. P11 to P19 did not exist. It is still structured as a 50-minute lecture plus a separate example sheet, which P17 replaced | Re-review against the full set once the grid exists. Its existing findings from `2026-09-16-l02.md` are still open |
| F8 | P17 | all eight `docs/l0*/index.md` | Front matter said `duration: 50 min`, from the pre-P17 brief | **Fixed:** all eight now say 110 min |
| F9 | P19 | PEDAGOGY, `teaching/l01.md` | Lecture 1's operational plan existed in both files and had already begun to drift — Steve's run-sheet edits on the technician and the e-stop were not in PEDAGOGY | **Fixed:** PEDAGOGY keeps the reasoning only and points at the run sheet; the two statements are reconciled. 48 lines removed |
| F10 | — | `sync.lock.json` | All 35 check warnings are scaffolds never accepted. The check currently carries no signal: real drift will hide among them | Accept the scaffolds as a baseline, or teach the check to ignore `status: draft`. Otherwise the check is decorative |
| F11 | — | `zensical.toml` | The footer's About link was not rewritten per page and was broken on every nested page | **Fixed:** root-relative, with a comment about the sub-path assumption |
| F12 | — | repository | Nothing runs the checks automatically. All four rely on someone remembering | Add CI once there is a remote. The repository has no git remote yet |
| F13 | — | `package.json` | The Marp theme is taken from a sibling folder, `../flightlab-marp-template`, which is not published. Nobody else can build the slides, and neither can CI | Publish the theme, then switch the dependency, as the README already notes |
| F14 | P19 | `docs/includes/glossary-abbr.md` | On the one written lecture, 62 tooltips, 15 of them on "phase margin" — the lecture's own subject | **Fixed:** terms that are the subject of a lecture removed. 62 → 28 on that page |

## Load and complexity (P19)

The first pass under the new principle. Per-session counting waits for content;
this is the course-level pass.

**Removed in this review**

| What | Why | Size |
|---|---|---|
| Lecture 1's operational plan in PEDAGOGY.md | Duplicated `teaching/l01.md` and had drifted (F9) | 48 lines |
| Five glossary abbreviations | Subjects of their own lectures; a tooltip on every occurrence is noise (F14) | 5 terms, 34 tooltips on one page |
| `_converted/`, `_converted/coursework-2025/` | Empty leftovers from the PDF conversion work | 2 directories |

**Named, not removed**

| Candidate | Why not yet |
|---|---|
| "Live feedback in lectures", about 30 lines on Mentimeter formats | Q3 is unresolved, so the detail is still doing work. Compress to a decision and a pointer as soon as Q3 closes |
| P15's candidate-incident table, five cases for eight lectures, two marked "To find" | Cheap to keep, but "To find" has been open since the principle was written. Either source MCAS and AF447 properly or cut them to three cases |
| 42 glossary terms not yet appearing in any lecture | Not bloat: seven of eight lectures are scaffolds, so the glossary is deliberately ahead. **Recheck once the lectures are written** — recorded here so it isn't re-argued from scratch |
| ASSESSMENT.md's summary of the private drafts | Some duplication with `private/assessment/drafts/`, but the tracked file has to stand alone for anyone without `private/` |

**Not counted yet.** P19's per-session budget — two new concepts, one new tool,
one new notation — cannot be applied until the concept inventory exists. That
inventory should be built with the budget in view, not checked against it
afterwards.

## Processes: what is working, and what isn't

**Working.** The numbers pipeline is genuinely sound: 41 of 41 agree across
Python and MATLAB, and it costs nothing to rerun. The private/tracked boundary
has held — no assessment material has leaked into a tracked file. The
principle-ID discipline is doing its job; every finding above cites one.

**Not working yet.**

- **The sync check has no signal** (F10). Thirty-five warnings that are all
  expected is the same as no warnings.
- **Nothing is automated** (F12). Four good checks that depend on memory.
- **The review cadence has no trigger.** PEDAGOGY says reviews happen when a
  lecture reaches draft, before it is taught, and when the principles change.
  Nothing enforces it, and the principles have now changed three times in two
  days. This review exists because it was asked for, not because anything
  required it.
- **Run sheets have one instance.** The pattern is only proven on Lecture 1,
  which is the least typical session in the unit.

## Not findings, but noted

- The decision to distribute the case cycle across the week (P18) resolves a
  genuine conflict — the laboratory's order-independence against P8's
  compounding — that would otherwise have surfaced mid-term.
- The laboratory arithmetic is the most valuable thing recorded this week. It
  turns "we might need more Quansers" into a dated constraint with a number
  attached.
- P19 immediately paid for itself: three removals in its first pass, two of
  which were active problems rather than tidying.
- The glossary is ahead of the content, which is the right way round. Writing a
  lecture against an existing definition is easier than reconciling one after.
