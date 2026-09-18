# Review: structure and processes, 18 September 2026

Scope: everything except the content of individual lectures, which is all
placeholder bar Lecture 1's plan (CONTENT.md). Run after Steve's corrections of
18 September — the calendar, the effort budget, open-access laboratory, staff
roles, one guest lecture — to find what those corrections made stale, and to
check the new content scope (CURRICULUM.md) against the principles.

Follows [2026-09-17-whole-course.md](2026-09-17-whole-course.md).

## Health of the build

| Check | Result |
|---|---|
| `zensical build` | No issues |
| `npm run check` | 0 errors, 35 warnings, all scaffolds (unchanged; see F10 of the previous review) |
| `npm test` | All applet checks pass |
| `npm run models` | 41/41 |
| Internal links, all tracked Markdown | 0 broken |

## What the corrections changed

The previous review's three blocking findings are all resolved:

| Previous finding | Now |
|---|---|
| F1, effort budget doesn't close | **Closed.** 20 contact, 4 laboratory, 24 coursework, 52 independent. Q9 |
| F2, no slack in the term | **Superseded.** Nine control sessions for eight lectures; week 11 is the buffer |
| F3, guest weeks break the case chain | **Accepted,** knowingly. Q7 |

## Findings

| ID | Principle | Where | Finding | Action |
|---|---|---|---|---|
| S1 | — | PEDAGOGY, calendar | Reading week was recorded as week 6 throughout. It is week 5 | **Fixed** everywhere, including the laboratory arithmetic |
| S2 | P17 | P17's between-session table | Built for a 2-hour week; the budget is now about 7 (5 independent, 2 coursework) | **Fixed.** Four parts plus an unallocated 1.25 hours, which is deliberate slack |
| S3 | — | PEDAGOGY, run sheet | Technical services, TAs and "technician" were conflated; the run sheet had "TA/Technician" as one role | **Fixed.** Three roles, stated as not interchangeable. The run sheet books technical services for the rig and a TA for the room |
| S4 | — | laboratory section | Modelled as booked slots; it is open access and self-scheduled | **Fixed.** Recomputed in station-hours. The failure mode changes from matching to queueing, which is noted along with a cheap mitigation |
| S5 | P16 | P16 | Challenge count assumed two guest weeks | **Fixed.** Eight challenges plus the diagnostic |
| S6 | Q7 | guest lectures page | Two placeholder guest slots | **Fixed.** One, week 5 |
| S7 | P10 | CURRICULUM week 10; ASSESSMENT | **State space is taught in week 10, one week before a Thursday-week-11 deadline, and after the last checkpoint.** If Part B requires it, students meet it too late | Recorded as **AQ15**. Recommendation: optional and rewarded under B2 |
| S8 | P10 | ASSESSMENT AQ2 | Deadline now known; checkpoints still undated | **Proposed:** end of weeks 4, 8 and 9, one per act, in AQ2 and CURRICULUM |
| S9 | Q10 | week 5 | The one guest lecture is booked in reading week | Flagged as **Q10** for Steve to confirm. Not changed |
| S10 | P19 | CURRICULUM §6 | Checked every proposed session against P19's budget. Week 10 is over by two or three concepts; week 7 is over unless S and T are taught as one idea | Both recorded with options in CURRICULUM. Recommendation for week 10: scope hard, and let the laboratory carry LQR |
| S11 | Q6 | `models/` | CURRICULUM uses each of the three systems in three or more sessions. Q6 — one shared definition per system — was a nicety; it is now close to a necessity, or the same aircraft will drift between lectures | Raise Q6's priority. Decide before the second lecture is written |
| S12 | — | `package.json` | Theme still from `file:../flightlab-marp-template` | Answered in README: pin to a release tag once published. Nothing to change until then |
| S13 | — | licence | CC BY for everything was a poor fit for code | **Fixed.** Teaching material CC BY 4.0, software MIT. Both attribute; MIT carries it in the retained notice |

## Load and complexity (P19)

**Removed in this pass**

| What | Why |
|---|---|
| The second guest-lecture placeholder | Dropped for this year |
| The footer's exclusion list | Moved to the About page; the footer now points there |
| "Two guest weeks" reasoning in Q7 | Superseded by the corrected calendar. Q7 rewritten shorter |

**Named, not removed**

| Candidate | Why not yet |
|---|---|
| The laboratory section of PEDAGOGY, about 70 lines | It is capacity planning, not pedagogy. It belongs in a planning document of its own once there is a second thing to put there. Not worth a file yet |
| "Live feedback in lectures" | Unchanged since the last review; Q3 still open |

**The unit as a whole** now has a load model it didn't have yesterday. Two
checks it makes possible, once content exists:

- Every week's example sheet should take a mid-range student about two hours
  (P17 part 2). That is testable, by timing a TA or a student through it.
- P16's completion data from weeks 3 and 4 will show whether five hours of
  independent study is actually happening. If it isn't, CURRICULUM §7 lists what
  gives first.

## Processes

**Improved since yesterday.** Content status is now explicit (CONTENT.md): the
site no longer silently implies eight finished lectures to anyone reading the
repository. The scope has a home (CURRICULUM.md) separate from both the
principles and the status, so each of the three documents has one job.

**Unchanged, and still worth fixing:** the sync check's 35 warnings carry no
signal; nothing runs the checks automatically; the theme can't be built outside
Steve's machine. All three were raised yesterday.

**New:** three planning documents now reference each other — PEDAGOGY,
CURRICULUM, CONTENT — plus ASSESSMENT. A decision made in one (the deadline,
say) has to be propagated to the others by hand, and this pass found four places
where yesterday's facts had survived today's corrections. That will keep
happening. The mitigation is the one already in AGENTS.md — update in the same
change — plus this: **when a fact about the calendar changes, grep for the old
value.** That is how S1 was found.
