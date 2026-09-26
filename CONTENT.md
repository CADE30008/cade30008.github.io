# Content notes

Why each week is where it is: decisions, dependencies and the things that will
bite. The site looks complete and is not, and this says what is behind each
page that the navigation does not.

**State is not here.** Every file carries its own, written and checked by
`npm run track`, and [STATUS.md](STATUS.md) collects it. This file used to keep
a status column of its own, in a fourth vocabulary; by the morning after the
first lecture it said that week was `scoped` with nothing written, while the
handout said `written` and STATUS.md said `published`. Three records of one
fact, and the hand-typed one lost.

Update the notes here in the same change as the content they describe.

## Weeks

Eleven weeks of content, designed to the University calendar and **scoped** —
titles, outcomes, activities, cases, hooks and cliffhangers — in
[curriculum/weeks.yaml](curriculum/weeks.yaml). The reasoning is in
[CURRICULUM.md](CURRICULUM.md). Scoped means agreed in outline and awaiting
Steve's review; it does not mean written.

| Week | Title | Folder | Notes |
|---|---|---|---|
| 1 | The design cycle, end to end. | `w01-design-cycle` | Written, taught on 22 September and published. Run sheet in `teaching/w01-design-cycle.md`, retrospective in `teaching/weekly-review.md`. It overran at the front, so the fitting and tuning were set as work between sessions. |
| 2 | Requirements and models you can trust. | `w02-requirements-and-models` | Back in the plan now week 2 has cover. |
| 3 | PID, properly | `w03-pid-control` | The only written lecture. Its content predates P8, P11–P19 and the scope; redraft to P17's shape rather than edit. Its sync state needs re-accepting (see below). |
| 4 | Stability and margins | `w04-stability-margins` | Moved into act I, 19 September, so the consolidation week closes an act. |
| 5 | Guest lecture | `w05-guest-lecture` | Speaker and topic unconfirmed. |
| 6 | Consolidation week | `w06-consolidation` | No lecture. Page written; its activity table is generated. The consolidation challenge in Numbas and MATLAB Grader is still to build. |
| 7 | Robustness and trade-offs | `w07-robustness` | |
| 8 | Loop shaping | `w08-loop-shaping` | |
| 9 | Flight control architecture | `w09-flight-control-architecture` | MCAS and AF447 still need primary sources. |
| 10 | State space and state feedback. | `w10-state-space` | Over P19's budget unless scoped hard. **Steve to work through it when we reach it**. |
| 11 | What comes next | `w11-beyond-this-course` | One hour, then coursework Q&A; the term's buffer. |

**Folders** are `wNN-topic`, NN the week. **Retired 18 September:** the
"Longitudinal dynamics" and "Lateral-directional dynamics" placeholders, which
were ILOs 1–3 and Part A's material, and "Autopilot modes", merged into week 9.

**Sync state after the renames.** `sync.lock.json` is keyed by folder, so the
PID lecture's accepted state is still recorded under its original name,
`l02-pid-control` (it is now `w03-pid-control`), and the check reports its
sections as not yet accepted. Its content is unchanged. A person should check it
and run `npm run sync:accept`, which rewrites the lock under the new names —
and, as a side effect, accepts the placeholders as a baseline, which is what F10
of the 17 September review asked for.

## Other material

| What | Status | Notes |
|---|---|---|
| Glossary | drafted | ~80 terms, deliberately ahead of the lectures. |
| Preparing for Control | **ready to publish** | Listed in `publish.yaml`. MATLAB first; long scripts in scrolling boxes; certificate upload and diagnostic described. Device checks pass, including the browser runner on the live build. Steve to run through before week 1. |
| Blackboard: Before week 1 | **build sheet ready** | `teaching/blackboard.md`: learning module, links, certificate assignment, diagnostic test, and a check to run in student preview. Not yet built in Blackboard. |
| Prerequisite diagnostic | **drafted** | Eleven questions in `diagnostics/prerequisites.yaml`; `npm run numbas` builds the `.exam` for upload and re-checks every numeric answer. Not yet uploaded or tested in Numbas. |
| Diagnostic in Blackboard Ultra | **on hold** | `npm run bb` builds a probe package, a QTI 2.1 package and a question-upload file from the same YAML. Whether Ultra can carry the diagnostic turns on two things neither documented nor tested: whether this installation renders LaTeX, and whether per-option feedback survives a QTI import. On hold from 21 Sep 2026: Ultra cannot do item-by-item feedback in-quiz, which is the mechanism the question set is built on. Kept buildable. Protocol in `diagnostics/blackboard/README.md`. |
| Live site | **ready, not deployed** | `npm run preview:live` shows it. Deploys on push once the `cade30008` organisation and repository exist. |
| Run sheets | 1 of 8 | Only `teaching/w01-design-cycle.md`. The pattern is unproven on a normal session. |
| Applets | 1 | The PID tuner, tested against `models/pitch_numbers.json`. |
| `models/` | 1 lecture | `pitch.py` and its MATLAB check. 41/41 numbers agree. |
| Example sheets | 1 real | Week 3's, written as about an hour, which fits the budget. The rest are scaffolds. |
| Weekly challenges (P16) | none | Numbas and MATLAB Grader integrations not yet set up. |
| Week 1 build items | none | Student Live Script, measured data, MATLAB Drive folders, gain filter, selection tool. All prerequisites for week 1. |

## What this means in practice

- **One lecture week of nine is written,** and it needs re-drafting to P17's shape
  rather than editing.
- **Every week is now scoped, but none except week 1 has an agreed plan.**
  The scope is a proposal for review.
- **Week 1 has hard dependencies that do not exist yet** — the last row of the
  table above. Those are the real critical path, not the lectures.

## The AI page

`docs/ai.md`, linked from About and summarised in week 1. Revised by Steve on
19 September, with the agreed fixes applied the same day: his own caveat on
Schneier's "work" written in, the Tao and Fields Medallists' declaration leading
into the work-or-gym test, Tao's ChatGPT conversation dated 20 July 2026, and
the GitHub issues link pointing at the `cade30008.github.io` repository. Week 1's
handout section and three slides were brought into line the same day.

## The About page and the repository

The About page no longer carries the repository and planning links, or the
build instructions; those are in the README. Its licence section links to
`LICENSE.md` at `github.com/CADE30008/cade30008.github.io`, the repository the
site publishes from.

## Student workload

Modelled in `curriculum/term.yaml`, 19 September: 6 hours in every week from
1 to 11 — in week 6, 4 hours of recommended consolidation in place of the
lecture and independent learning — plus 4 hours of laboratory, 70 hours planned
against a notional 100. Drawn at the top of the lecture map and written into
week 1's "your week" table by `npm run curriculum`. Example sheets must now be sized to
about an hour, and the handout's core to about 45 minutes' rereading.

<!-- tracking: status=draft version=0 -->
