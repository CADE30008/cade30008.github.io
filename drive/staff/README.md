<!-- version: 2026.4 (2026-09-22) -->

# Laboratory pass — 40 minutes

Two jobs, and they need the rig for different reasons.

| Folder | What it is for | Needs the rig? |
|---|---|---|
| `rig-characterisation/` | Measuring the machine, so the model and the envelope describe *this* rig | Yes, all of it |
| `student-code-test/` | Checking that what students are handed actually runs | Only at the end |

**Do them interleaved, not in sequence.** The rig work has long waits in it
(the arm takes about a minute to settle between runs), and the student code
runs unattended in half a minute. Start a recording, run the checker while you
wait.

## The 40 minutes

Ordered so that if you run out of time, what you lose is the least important
thing. The first two are five minutes together and both block the lecture.

| At | For | Do |
|---|---|---|
| 0 | 5 | Amplifier on, open `m_part1.slx`, build |
| 5 | 2 | **Q1: the derivative question.** `rig-characterisation/README.md` §1 |
| 7 | 2 | **Q2: what holds it level?** §2 |
| 9 | 6 | **Record the step at the level datum.** §3. While it settles and runs, start the student checker below |
| 15 | 1 | `student-code-test/` → `run_all_student_code` (32 s, unattended) |
| 16 | 8 | **Three more recordings at different trims.** §4 |
| 24 | 4 | Fit them all: `t1_fit_this_rig`, then `rig_trim_sweep` |
| 28 | 6 | **Fly four sets of gains.** §5 |
| 34 | 4 | Student code by hand: the two interactive bits. `student-code-test/README.md` |
| 38 | 2 | Back row sight line, and locate both switches |

## If you only get twenty minutes

Q1, Q2, one step recording, and `run_all_student_code`. That is enough to know
the session works. Everything else improves it.

## What I need back

Each section ends with **SEND ME**. The short version, in priority order:

1. Derivative on the measurement, or on the error? One word.
2. The voltage that holds the arm level.
3. K, wn, zeta from your recording.
4. Whether `run_all_student_code` printed anything in red.
5. The trim table, if you got that far.
