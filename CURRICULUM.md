# Curriculum: content scope for the control half

> Drafted with the assistance of generative AI tools.[^checked]

[^checked]: The final versions of all process and assignment documents, and of all student-facing and back-office code, will be fully checked manually.

**Status, 18 September 2026: option B agreed** (§7). The nine lectures are
scoped — titles, learning outcomes, activities, cases — in
[curriculum/lectures.yaml](curriculum/lectures.yaml), and mapped onto this
year's twelve weeks in
[curriculum/schedule-2026-27.yaml](curriculum/schedule-2026-27.yaml). The scope
is a proposal for Steve's review; only Lecture 1's plan was agreed first. No
lecture content is written except Lecture 3's, which predates all of this.

This document holds the *reasoning*: the constraint, the capabilities, the
concept tiers, the benchmarks, the options, and the decisions. It does not
repeat the per-lecture detail, which lives in the YAML and is rendered by
`npm run curriculum` as the lecture map, `docs/planning/lecture-map.html`, which the site serves at `/planning/lecture-map.html`.

It sits between [PEDAGOGY.md](PEDAGOGY.md), which says *how* we teach, and
[CONTENT.md](CONTENT.md), which says what exists.

**Lectures and weeks are decoupled.** A lecture has a stable number and a
folder `lNN-topic` carrying that number. Which week it falls in belongs to a year's schedule. So
this document refers to lectures by number (L1 to L9), never by week, except
where it is talking about this particular year.

---

## 1. The constraint that shapes everything

Under P17, each session has **two 15-minute taught blocks**. Across eight
content sessions that is **eight hours of lecturing**.

| Course | Taught hours | Shape |
|---|---|---|
| [MIT 16.30](https://ocw.mit.edu/courses/16-30-feedback-control-systems-fall-2010/pages/calendar/) Feedback Control Systems | 24 | 24 one-hour lectures |
| [Caltech CDS 110](https://murray.cds.caltech.edu/CDS_110/ChE_105,_Spring_2024) Introduction to Feedback Control | ~30 | Ten weeks, Åström and Murray |
| [MIT 16.06](https://ocw.mit.edu/courses/16-06-principles-of-automatic-control-fall-2012/pages/syllabus/) Principles of Automatic Control | ~39 | Three lectures and a recitation a week |
| **This unit, control half** | **8** | Eight sessions of two 15-minute blocks |

We have a third of MIT 16.30's lecturing and a quarter of Caltech's. That is not
a problem to solve by talking faster. It is a design choice P17 already made:
the unit trades lecture time for application time (6.7 hours of case work in
the room) and for independent study and coursework (18 and 22 hours).

So the question this document answers is **not** "how do we fit a controls
syllabus into eight hours". It is:

> **What must a student hear from a person, in the room, that they cannot get
> as well from the handout?**

The working answer: **threshold concepts** (Meyer and Land) — the ideas that,
once grasped, reorganise everything else, and that students reliably fail to
grasp from reading. The handout carries the full argument (AGENTS.md already
says so); the taught blocks unlock the threshold; the case hour makes it
operational. Everything this document proposes follows from that division.

**Consequence for P19.** The per-session budget — two new concepts, one tool,
one notation — applies to the *taught blocks*. The handout can hold more,
provided it is marked as the handout's rather than the lecture's.

---

## 2. What a graduate of this half should be able to do

Written as capabilities, not topics, and mapped to the unit's ILOs. These are
what the assessment tests (P10), so everything taught must serve at least one.

| # | Capability | ILO |
|---|---|---|
| C1 | Turn a vague need ("it should feel responsive") into measurable requirements, and justify them from the vehicle's role and handling qualities | 6 |
| C2 | Get a model — from physics, from data, or from someone else — and say how far to trust it | 4, 6 |
| C3 | Design a feedback controller that meets stated requirements, classically, and explain why it works in both the time and frequency domains | 5 |
| C4 | Establish that a loop is stable, and how stable, and say what that does and does not guarantee | 4 |
| C5 | Reason about the fundamental trade-offs — bandwidth against noise against actuator effort — and say which one a design is making | 4, 5 |
| C6 | Design a state-feedback controller for a small multi-state system, and say what it buys over a classical design | 5 |
| C7 | Place a controller within an aircraft's flight control architecture — SAS, autopilot, modes, pilot — and say what each layer is responsible for | 6 |
| C8 | Verify a design against every requirement, including with realistic effects the model left out | 4, 5, 6 |
| C9 | Use MATLAB and Simulink, including their AI tools, to do all of the above, and check what those tools produce | all |

**What distinguishes a first** (P10, the aims): the same capabilities, plus the
ability to say *why* — to connect a design decision to the theory that justifies
it, and to predict where it will break.

---

## 3. Concept inventory

Every concept the half needs, tiered by how much taught time it deserves.

**Tier 0 — assumed from CADE20002.** Revisited by retrieval (P11), never
re-taught. Laplace transform; transfer function; poles and zeros; block
diagrams; step-response specifications; Bode plots as a picture; closed-loop
transfer function; basic PID.

The prerequisite is covered "lightly", in three sessions at the end of year 2
(Q5), and non-aerospace cohorts vary. So tier 0 is **assumed but checked**: the
week 1 diagnostic (P16) says who needs the Preparing for Control material.

**Tier 1 — threshold concepts. Taught in the room.** The eight or so ideas the
unit exists to unlock:

| Concept | Why it is a threshold |
|---|---|
| **Feedback as a trade**, not a fix | Students arrive thinking feedback removes error. It moves it: S + T = 1 |
| **A requirement is a design input** | Until this lands, tuning is guessing. Lecture 1's cliffhanger |
| **A model is a claim with a range of validity** | Separates people who design from people who tune. Lecture 1's other cliffhanger |
| **Loop gain is where the design lives** | Reorganises the Bode plot from a thing you draw into a thing you shape |
| **Stability margin is distance, not safety** | The misconception P13 already names |
| **Bandwidth costs something** | Noise, actuator effort, unmodelled dynamics. Every design is a choice about it |
| **State is what the system remembers** | The door into modern control; without it, state space is just matrices |
| **Control is layered** | Inner and outer loops, modes, the pilot. How an aircraft's control actually works |

**Tier 2 — taught tools.** Introduced in the taught blocks, practised in the
case hour, fully treated in the handout: system identification by fit; PID
terms, derivative filtering, anti-windup; Nyquist criterion; gain, phase and
delay margins; sensitivity and complementary sensitivity; lead and lag
compensation; loop shaping; pole placement; LQR as a tuning knob; SAS and
autopilot loop structure.

**Tier 3 — handout and extension only.** Real, correct, and not lectured:
root locus in detail; Ziegler–Nichols; the Bode sensitivity integral;
controllability and observability tests; observer design; Kalman filtering;
discretisation and zero-order hold; gain scheduling.

**Tier 4 — awareness.** Named, located, and left for year 4, in the horizon
session: MPC; adaptive control; robust control proper (H∞, μ); nonlinear
control; reinforcement learning and learned control; certification of
flight control software.

---

## 4. Benchmarks: what comparable courses teach, and in what order

| Course | Order | What it tells us |
|---|---|---|
| **MIT 16.30** | Root locus → frequency response → Bode design → **twelve lectures of state space** (controllability, pole placement, estimators, LQR, LQG) → digital → nonlinear → anti-windup | A full semester, and half of it is state space. We cannot and should not attempt this |
| **Caltech CDS 110** | Modelling → linear systems → **state feedback** → estimation → trajectory generation and MPC → *then* frequency domain → robustness → PID last | Modern-first. Elegant, and matches Åström and Murray, but assumes students arrive fresher than ours |
| **MIT 16.06** | Feedback properties → performance measures → stability → root locus → Nyquist → frequency design → state space | Classical-first, aerospace framing. The closest in spirit to us |
| **TU Delft AE4301** (MSc) | PID, MPC, adaptive, robust; Nyquist, Bode, Lyapunov; GNC; sensors | Where Bristol's planned year 4 unit sits, not us |
| **Michigan AEROSP 341** | Equations of motion → linearisation → modes → linear systems → simulation | What Tom's half does. Confirms lectures 4 and 5 are the wrong half |

**Conclusions.**

- **Classical-first is right for us.** Our students know Bode from year 2, not
  state space; P2 wants concrete first; and the coursework is classical in
  flavour. Caltech's modern-first order is better mathematics and worse
  pedagogy for this cohort.
- **State space gets one session, deliberately scoped.** Every benchmark spends
  far more. We are teaching the door, not the building (§6).
- **PID placement is the real disagreement.** Caltech puts it last, as the
  practical synthesis. We put it first because Lecture 1 needs it and the
  Quanser demands it — which is P2 working as intended — but it means PID must
  be *revisited* after loop shaping, not just taught once.
- **Nobody benchmarked teaches flight control architecture** (SAS, modes,
  handling qualities) at this level. That is our aerospace differentiator and
  ILO 6's whole job. It deserves a full session.

---

## 5. The arc

Three acts, nine lectures. Each lecture's design question, outcomes, activities,
case, hook and cliffhanger are in `curriculum/lectures.yaml`; the planning
diagram shows them together.

| Act | Lectures | By the end of the act |
|---|---|---|
| **I — the loop you can build** | L1 The design cycle, end to end · L2 Requirements and models you can trust · L3 PID, properly | Every student has been round the whole cycle twice: once on hardware they watched, once properly |
| **II — analysis and design that scale** | L4 Stability and margins · L5 Robustness and trade-offs · L6 Loop shaping | They can say how stable a loop is, what that does and doesn't guarantee, and design to a specification rather than tune |
| **III — aircraft and modern methods** | L7 Flight control architecture · L8 State space and state feedback · L9 What comes next | They can place a controller in an aircraft's architecture, design by state feedback, and see what lies beyond the unit |

The guest lecture is unnumbered, sits outside the acts, and is proposed as
MathWorks on agentic AI for model-based design: their own demonstration takes
a rotary pendulum from requirements to deployment, which maps directly onto the
Quanser.

### This year: one lecture over

2026/27 has room for eight lectures, not nine: week 2 is given to Flight
Dynamics, week 5 has the guest lecture, week 6 is reading week, and week 11's
second hour is coursework Q&A. Options, **for Steve to decide**:

| | Option | Costs | Keeps |
|---|---|---|---|
| **R1** | **L5 and L6 in one session, week 8** (proposed) | Each gets half a session. The P19 budget holds only because block A carries S and T and block B carries shaping — which is P17's idea-then-method structure exactly | State space keeps a full session in week 10, before the deadline; L9 keeps week 11; nothing is cut |
| R2 | L9 becomes a handout page | State space moves to week 11's single hour, two days before the deadline — the most overloaded lecture in the thinnest slot | L5 and L6 separate |
| R3 | Use week 12, if the Tuesday slot exists | Revision week, after submission, when attendance will be thin and students are revising for exams in other units. State space or L9 would fall after the deadline | Nothing cut. Needs the timetable checked |
| R4 | L4 and L5 together | Two threshold concepts — margin as distance, and feedback as a trade — in one session. Over budget | L6 separate |

**Recommendation: R1.** It costs least and fits P17 unusually well. From
2027/28, with week 2 back, nine lectures fit with half a session to spare.

### How the coursework tracks the arc

The deadline is **Thursday of week 11**. The three checkpoints (ASSESSMENT.md,
AQ2) fall at the end of each act, so each lands just after its material:

| Checkpoint | Week | After | Paper sections |
|---|---|---|---|
| 1. Requirements and model | end of 4 | Act I | 1–2 |
| 2. Design and analysis | end of 8 | Act II | 3–4, plus peer review |
| 3. Draft paper | end of 9 | Architecture | All |

**State space in the coursework — decided for now.** L8 is taught after the last
checkpoint and just before the deadline, so a state-space design is **optional
and rewarded** under criterion B2, not required (AQ15). It may leave the
coursework entirely. Either way it stays in the lectures, as the foundation the
year 4 advanced unit builds on.

### Where things land

**The three systems (P9).** Each has a job, and each appears in more than one
act, which is what makes comparison possible (variation theory):

| System | Lectures | Why there |
|---|---|---|
| Quanser 3-DoF | L1, L2, L4, L8, and the laboratory | Real hardware, really unstable open loop. Genuinely multi-axis, which makes it the natural state-space case |
| Fixed-wing | L2, L3, L4, L6, L7 | The coursework plant. Carries the aircraft-specific material |
| Multirotor | L5, and example sheets throughout | Fast, open-loop unstable, easy to reason about. Robustness bites visibly |

**The real-world cases (P15).** One per lecture where the lesson is precise;
none where it would be decoration:

| Case | Lecture | The control lesson, stated precisely |
|---|---|---|
| YF-22 (1992) | L4 | Rate limiting and loop delay produce a PIO that linear margins don't predict |
| Ingenuity flight 6 (2021) | L5 | Margins and robustness bought survival when the model's assumptions broke |
| 737 MAX MCAS | L7 | Authority, sensing redundancy, and the pilot as a loop element — **to find** a primary source |
| Air France 447 | L7 | Automation handing back a degraded aircraft — **to find** a primary source |
| X-15 3-65-97 (1967) | L9 | An adaptive system entering a limit cycle; why adaptive and learned control are hard to certify |

MCAS and AF447 both land on L7, the architecture lecture, which is where they
are most instructive. Both still need primary sources (P15, kept as agreed).

**Emerging trends.**

| Trend | Where | How much |
|---|---|---|
| **Agentic AI for model-based design** — Simulink Agentic Toolkit, MATLAB MCP server | The guest lecture; a theme throughout (PEDAGOGY's course themes); permitted in the coursework (Category 3) | A thread, not a topic. Students *use* it, and verification of its output is taught and assessed |
| **Model-based design** | Every case hour; L1's live demonstration is model-based design in miniature | A thread |
| **Reinforcement learning and learned control** | L9 | About ten minutes. Framed by the X-15: what it is, where it is genuinely used, and why certification is the hard part — the aerospace-specific insight a general machine-learning course won't give |
| **Digital implementation** | L3's handout; L9 | Enough to know that what runs is discrete, and what that costs |

---

## 6. Loading: does each lecture fit P19's budget?

Two new concepts, one new tool, one new notation, **in the taught blocks**.
The counts live in each lecture's `budget` in `lectures.yaml`, and
`npm run curriculum` checks them, so this section records only the verdicts and
what to do about them. At present it warns on four things:

| Lecture | Verdict | What to do |
|---|---|---|
| L4 Stability and margins | Borderline: two notations, $L(j\omega)$ and encirclement | $L(j\omega)$ is tier 0 in principle. Check the week 1 diagnostic before deciding |
| L5 Robustness | Fits only if S and T are taught as one idea | Teach them as a pair from the start — "the two ways a loop responds". That is also the better way: S + T = 1 *is* the threshold |
| L8 State space | At budget only because observers and controllability are handout-only; two tools, pole placement and LQR | See below. **Steve to spend time on this lecture when we reach it** |
| This year's week 8 | Two lectures in one session (R1) | Block A carries S and T, block B carries shaping |

**L8 is the problem**, and it is the one every benchmark agrees on: state space
is big. Three ways to fit it:

1. **Scope it hard (current).** Teach *state* and *state feedback by pole
   placement*, with LQR introduced as "a tuning knob instead of choosing poles
   by hand". Observers, controllability and observability move to the handout
   (tier 3). Every student can then design a state-feedback controller on a
   model with all states measured, which is what C6 asks. The Quanser's second
   laboratory material already covers LQR, so the laboratory carries it too.
2. **Two sessions.** Possible from 2027/28, with the half-session to spare.
3. **Introduce state earlier and thinner,** in L2 alongside models, so L8 builds
   rather than starts. Better learning, but L2 is already full.

---

## 7. Options on the boundaries

**Option B was agreed on 18 September.** The others are recorded because the
classical–modern balance is to be reviewed again (see below).

| | Option | What changes | Buys | Costs |
|---|---|---|---|---|
| A | Classical only | State space drops to L9 | Depth. Two full lectures on design | **Fails ILO 5**, which says "classical and modern". Not viable without a catalogue change |
| **B** | **Balanced — agreed** | As §5. One scoped state-space lecture | Covers every ILO; aircraft architecture gets a full lecture | State space is thin — the door, not the building |
| C | Modern-first (Caltech's order) | State space in Act I, frequency domain in Act II | Mathematically cleaner; state space properly taught | Fights the prerequisite, fights P2, and fights the classical coursework |
| D | Depth over coverage | Six topics, two lectures each on the hardest | Real mastery of margins and state space | Architecture (ILO 6) becomes reading only — the one thing no benchmark teaches, and our differentiator |

**To review in future: the classical–modern balance.** Option B gives modern
control one lecture of nine. That is defensible for an introductory unit that
feeds a year 4 advanced one, but it should be revisited once both units exist,
with three questions: is one lecture enough for the advanced unit to build on;
should state space stay in the coursework at all (AQ15); and whether L2 should
introduce *state* early so L8 has less to do.

**On student loading.** Independent learning is 2 hours a week in a week with a
lecture — 45 minutes back over the handout and the challenge, an hour on the
example sheet, a quarter of an hour on next week's case — and coursework another
2 (the workload model in PEDAGOGY.md). That is tight, and it changes what §1's
division of labour can ask of the handout: the handout still carries the full
argument, but a student has about 45 minutes a week to go back over it. So
handouts must put the core first and fold the rest away (P4), and anything that
can't be read in that time is an aside, not an expectation.

If even that proves too much in practice (watch P16's completion data from
week 3):

| Lever | What gives | Keep |
|---|---|---|
| **1. Example sheets** | Trim to the questions that rehearse the coursework; mark the rest as extension | The weekly challenge, which is the retrieval |
| **2. Handout asides** | Fold more away as optional | The threshold concepts |
| **3. Part 4 pre-reading** | Drop it in the heaviest weeks | The cliffhanger itself, which is in the room |
| **Never** | The coursework step, or the case hour | They are what the assessment rests on |

---|---|---|
| **1. Example sheets** | Cut from ~2 hours to ~1. Mark the rest as extension | The weekly challenge, which is the retrieval |
| **2. Tier 3 handout material** | Fold it away as optional | The threshold concepts |
| **3. Part 4 pre-reading** | Drop it in the heaviest weeks | The cliffhanger itself, which is in the room |
| **Never** | The coursework step (P17 part 3), or the case hour | They are what the assessment rests on |

---

## 8. What to cut first, if a session is lost

In order. Decided now so it is not decided in a panic mid-term. This year is
already one over, so the first line of this list is already spent (§5, R1).

1. **L5 and L6 share a session** — this year's resolution, already applied.
2. **L9 becomes a handout page.** Its hour then holds whatever slipped.
3. **L2's second half.** Model validation is essential; requirements from
   handling qualities can be carried by L7.

**Never cut:** L1; L4, margins; L7, architecture. Those carry ILO 4, ILO 6, and
the unit's reason for existing.

---

## 9. Decisions

| # | Decision | Status |
|---|---|---|
| D1 | Option A to D | **B, agreed 18 September** |
| D2 | L8 state space: scope hard, two sessions, or earlier? | **Deferred** — Steve to work through it when we reach it. Scoped hard for now |
| D2a | Does Part B require state space? (AQ15) | **Optional and rewarded, for now.** May be removed from the coursework; stays in the lectures |
| D3 | Guest lecture topic: agentic AI for model-based design? | Open. Recommended, if MathWorks can do it |
| D4 | Reinforcement learning | Open. Recommended in, briefly, in L9 |
| D5 | The two flight-dynamics placeholders | **Retired, 18 September** |
| D7 | This year's one-over: R1 to R4 | **Open.** R1 recommended, and applied provisionally in the schedule |
| D8 | Classical–modern balance | **To review in future**, once the year 4 unit exists |

## Sources

- MIT OpenCourseWare. [16.30 Feedback Control Systems, calendar](https://ocw.mit.edu/courses/16-30-feedback-control-systems-fall-2010/pages/calendar/), fall 2010.
- MIT OpenCourseWare. [16.06 Principles of Automatic Control, syllabus](https://ocw.mit.edu/courses/16-06-principles-of-automatic-control-fall-2012/pages/syllabus/), fall 2012.
- Murray, R. M. [CDS 110 / ChE 105, Spring 2024](https://murray.cds.caltech.edu/CDS_110/ChE_105,_Spring_2024). Caltech.
- Åström, K. J. and Murray, R. M. (2021). *Feedback Systems: An Introduction for Scientists and Engineers*, 2nd edition. Princeton University Press. [Free online](https://fbswiki.org/).
- TU Delft. [MSc Control and Simulation courses](https://cs.lr.tudelft.nl/education/msc-courses/), including AE4301 Automatic Flight Control System Design.
- University of Michigan. [Aerospace Engineering course bulletin](https://bulletin.engin.umich.edu/courses/aero/), AEROSP 341 Aircraft Dynamics.
- MathWorks. [Agentic AI with MATLAB and Simulink](https://www.mathworks.com/products/matlab/agentic-ai.html); [Simulink Agentic Toolkit](https://github.com/matlab/simulink-agentic-toolkit); [Using Agentic AI to Design and Deploy a Control System](https://www.mathworks.com/videos/using-agentic-ai-to-design-and-deploy-a-control-system-1781868278531.html).
- Meyer, J. H. F. and Land, R. (2005). Threshold concepts and troublesome knowledge (2). *Higher Education*, 49(3), 373–388. [doi:10.1007/s10734-004-6779-5](https://doi.org/10.1007/s10734-004-6779-5).
- Engineering Council. [AHEP fourth edition: defining characteristics and learning outcomes](http://www.engc.org.uk/media/1bvlh55m/defining-characteristics-and-learning-outcomes-aaqa-first-edition-and-ahep-fourth-edition.pdf). The UK accreditation standard for engineering degrees. Not yet mapped against this unit; worth doing if the programme's accreditation review asks for it.
