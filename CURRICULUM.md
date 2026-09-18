# Curriculum: content scope for the control half

> Drafted with the assistance of generative AI tools.[^checked]

[^checked]: The final versions of all process and assignment documents, and of all student-facing and back-office code, will be fully checked manually.

**Status: proposal, 18 September 2026. Nothing here is committed except Lecture
1.** Every other session in the site's navigation is a placeholder (see
[CONTENT.md](CONTENT.md)). This document proposes what the unit should teach, in
what order, and where the boundaries sit, so that the week-by-week can be agreed
and then written.

It sits between [PEDAGOGY.md](PEDAGOGY.md), which says *how* we teach, and
[CONTENT.md](CONTENT.md), which says what exists. When a scope is agreed here,
CONTENT.md's rows move from **placeholder** to **scoped**.

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
the room) and for independent study (52 hours).

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

## 5. The proposed arc

Three acts (as agreed), mapped onto this year's nine control sessions.

### Act I — the loop you can build

By the end of Act I, every student has been round the whole design cycle
twice: once on hardware they watched, once properly.

| Wk | Session | Design question | Focus | System | Case | Cliffhanger |
|---|---|---|---|---|---|---|
| 1 | **The design cycle, end to end** | Can we make it fly? | Whole cycle | Quanser elevation | The open-loop flight attempt | No right answer without a goal; simulation disagrees with hardware |
| 3 | **Requirements and models you can trust** | What do we want, and what do we know? | Requirements, model validation | Quanser, then fixed-wing | Lecture 1's simulation-hardware gap | A model you trust, a requirement you can test — and a controller that still saturates |
| 4 | **PID, properly** | Why does the obvious controller usually work, and when doesn't it? | Design, implementation | Fixed-wing pitch | An actuator-limited loop; windup | It worked — but how close to the edge is it? |

*Week 2 is Flight Dynamics this year. Act I's second session is week 3.*

### Guest week

| Wk | Session | Note |
|---|---|---|
| 5 | **Guest: model-based design with agentic AI** (proposed topic) | Reading week. MathWorks' own agentic AI control demo — requirements to deployment on a rotary pendulum — maps directly onto our Quanser. Hour 2 open Q&A. The P18 chain is suspended here, by agreement |

### Act II — analysis and design that scales

| Wk | Session | Design question | Focus | System | Case | Cliffhanger |
|---|---|---|---|---|---|---|
| 6 | **Stability and margins** | How close to the edge are we? | Analysis | Fixed-wing | YF-22: rate limit and delay | Big margins, and it still went unstable — margins measure the wrong thing |
| 7 | **Robustness and trade-offs** | What happens when the model is wrong? | Analysis, requirements | Multirotor | Ingenuity flight 6 | We know what we want the loop to look like — now build it |
| 8 | **Loop shaping** | How do we design to a spec, not tune by eye? | Design | Fixed-wing | Revisit week 4's PID as a shaped loop | One loop at a time works — until the loops talk to each other |

### Act III — aircraft and modern methods

| Wk | Session | Design question | Focus | System | Case | Cliffhanger |
|---|---|---|---|---|---|---|
| 9 | **Flight control architecture** | Who is flying, and which loop is doing what? | Whole cycle, architecture | Fixed-wing | Boeing 737 MAX MCAS; Air France 447 | Loops that interact need a method that sees all the states at once |
| 10 | **State space and state feedback** | What if we could use everything the system knows? | Design | Quanser, all three axes | Why the Quanser's travel axis defeats a single PID | What sits above this course |
| 11 | **Horizon, then coursework Q&A** | What comes next — and does your design hold up? | Implementation, limits | All three | X-15 3-65-97: adaptive control | — (the unit closes) |

**Week 11 is also the buffer.** If a session is lost earlier in the term, week
11's first hour absorbs it and the horizon material moves to the handout. That
is the term's only slack, and it should be spent deliberately rather than
planned into.

### How the coursework tracks the arc

The deadline is **Thursday of week 11**. The three checkpoints (ASSESSMENT.md,
AQ2) fall at the end of each act, so each lands just after its material:

| Checkpoint | Week | After | Paper sections |
|---|---|---|---|
| 1. Requirements and model | end of 4 | Act I | 1–2 |
| 2. Design and analysis | end of 8 | Act II | 3–4, plus peer review |
| 3. Draft paper | end of 9 | Architecture | All |

**One collision to resolve.** State space (week 10) is taught *after* the last
checkpoint and one week before the deadline. If Part B *requires* a
state-space design, students meet it too late to use well. Recommendation:
make it **optional and rewarded** — a route to higher marks under criterion B2,
not a requirement. Recorded as AQ15 in ASSESSMENT.md.

### Where things land

**The three systems (P9).** Each has a job, and each appears in more than one
act, which is what makes comparison possible (variation theory):

| System | Where | Why there |
|---|---|---|
| Quanser 3-DoF | 1, 3, 10, laboratory | Real hardware, really unstable open loop. Genuinely multi-axis, which makes it the natural state-space case |
| Fixed-wing | 3, 4, 6, 8, 9 | The coursework plant. Carries the aircraft-specific material |
| Multirotor | 7, and example sheets throughout | Fast, open-loop unstable, easy to reason about. Robustness bites visibly |

**The real-world cases (P15).** One per session where the lesson is precise;
none where it would be decoration:

| Case | Session | The control lesson, stated precisely |
|---|---|---|
| YF-22 (1992) | 6 | Rate limiting and loop delay produce a PIO that linear margins don't predict |
| Ingenuity flight 6 (2021) | 7 | Margins and robustness bought survival when the model's assumptions broke |
| 737 MAX MCAS | 9 | Authority, sensing redundancy, and the pilot as a loop element — **to find** a primary source |
| Air France 447 | 9 | Automation handing back a degraded aircraft — **to find** a primary source |
| X-15 3-65-97 (1967) | 11 | An adaptive system entering a limit cycle; why adaptive and learned control are hard to certify |

MCAS and AF447 both land on week 9 — the architecture session — which is where
they are most instructive. Both still need primary sources (P15, as agreed).

**Emerging trends.**

| Trend | Where | How much |
|---|---|---|
| **Agentic AI for model-based design** — Simulink Agentic Toolkit, MATLAB MCP server | Guest week 5; a theme throughout (PEDAGOGY's course themes); permitted in the coursework (Category 3) | A thread, not a topic. Students *use* it, and verification of its output is taught and assessed |
| **Model-based design** | Every session's case hour; Lecture 1's live demo is MBD in miniature | A thread |
| **Reinforcement learning and learned control** | Week 11, horizon | About ten minutes. Framed by the X-15: what it is, where it is genuinely used, and why the certification story is the hard part. That framing is the aerospace-specific insight a general ML course won't give |
| **Digital implementation** | Week 4's handout; week 11 | Enough to know that what runs is discrete, and what that costs |

---

## 6. Loading: does each session fit P19's budget?

Two new concepts, one new tool, one new notation, **in the taught blocks**.

| Wk | New concepts | New tool | New notation | Verdict |
|---|---|---|---|---|
| 1 | Feedback as a trade; requirement as design input | Manual second-order fit | — | **Fits** |
| 3 | Model validity; requirement from handling qualities | Model-vs-data comparison | — | **Fits** |
| 4 | Derivative filtering; windup | Anti-windup | $K_p, K_i, K_d$ in frequency form | **Fits.** Tier 0 PID is retrieval, not new |
| 6 | Nyquist stability; margin as distance | Nyquist plot | $L(j\omega)$, encirclement | **Borderline** on notation |
| 7 | S and T; the waterbed | Sensitivity plots | $S$, $T$ | **Over** unless S and T are taught as one idea — "the two ways a loop responds" — with the waterbed as the second concept |
| 8 | Loop gain is the design | Lead–lag | — | **Fits** |
| 9 | Layered control; handling qualities as requirements | Loop architecture diagrams | — | **Fits** |
| 10 | State; state feedback; *observer*; *controllability*; *LQR* | Pole placement; LQR | $\dot x = Ax + Bu$ | **Over by two or three.** See below |
| 11 | — | — | — | Horizon: awareness only, budget doesn't apply |

**Week 10 is the problem**, and it is the one every benchmark agrees on: state
space is big. Three ways to fit it:

1. **Scope it hard (recommended).** Teach *state* and *state feedback by pole
   placement*, with LQR introduced as "a tuning knob instead of choosing poles
   by hand". Observers, controllability and observability move to the handout
   (tier 3). Every student can then design a state-feedback controller on a
   model with all states measured, which is what C6 asks. The Quanser's second
   laboratory material already covers LQR, so the laboratory carries it too.
2. **Two sessions.** Take week 11's first hour. Costs the term's only buffer.
3. **Move it earlier and thinner.** Introduce state in week 3 alongside models,
   so week 10 builds rather than starts. Better learning, but week 3 is already
   full.

**Week 7** fits if S and T are taught as a pair from the start. That is also
the better way to teach them: the identity S + T = 1 *is* the threshold concept.

---

## 7. Options on the boundaries

The recommended arc is **B** below. The others are real alternatives, each with
a cost.

| | Option | What changes | Buys | Costs |
|---|---|---|---|---|
| **A** | **Classical only** | State space drops to the horizon session. Week 10 becomes a second design session | Depth. Two full sessions on design | **Fails ILO 5**, which says "classical and modern". Not viable without a catalogue change |
| **B** | **Balanced (recommended)** | As §5. One scoped state-space session | Covers every ILO; aircraft architecture gets a full session | State space is thin — the door, not the building |
| **C** | **Modern-first** (Caltech order) | State space in Act I, frequency domain in Act II | Mathematically cleaner; state space properly taught | Fights the prerequisite, fights P2, and fights the classical coursework. Students arrive knowing Bode, not $\dot x = Ax + Bu$ |
| **D** | **Depth over coverage** | Six topics, two sessions each on the hardest | Real mastery of margins and state space | Drops a whole session. Architecture (ILO 6) becomes reading only — the one thing no benchmark teaches, and our differentiator |

**On student loading** — independent study is 52 hours, about five a week. If
that proves too much in practice (watch P16's completion data from week 3):

| Lever | What gives | Keep |
|---|---|---|
| **1. Example sheets** | Cut from ~2 hours to ~1. Mark the rest as extension | The weekly challenge, which is the retrieval |
| **2. Tier 3 handout material** | Fold it away as optional | The threshold concepts |
| **3. Part 4 pre-reading** | Drop it in the heaviest weeks | The cliffhanger itself, which is in the room |
| **Never** | The coursework step (P17 part 3), or the case hour | They are what the assessment rests on |

---

## 8. What to cut first, if a session is lost

In order. Decided now so it is not decided in a panic in week 8.

1. **Week 11's horizon hour.** It becomes a handout page. That is what the
   buffer is for.
2. **Week 8, loop shaping.** Fold its core — "loop gain is the design" — into
   week 6's second block. Lead–lag moves to the handout.
3. **Week 3's second half.** Model validation is essential; requirements from
   handling qualities can be carried by week 9's architecture session.

**Never cut:** Lecture 1; margins (week 6); architecture (week 9). Those carry
ILO 4, ILO 6, and the unit's reason for existing.

---

## 9. Decisions needed

| # | Decision | Recommendation |
|---|---|---|
| D1 | Which option, A to D? | **B** |
| D2 | Week 10 state space: scope hard, two sessions, or earlier? | **Scope hard**; laboratory carries LQR |
| D2a | Does Part B require state space, given it is taught in week 10? (AQ15) | **Optional and rewarded**, not required |
| D3 | Guest week 5 topic: agentic AI for MBD? | **Yes**, if MathWorks can do it — it maps onto our rig |
| D4 | Reinforcement learning: in or out? | **In, briefly**, in week 11, framed by certification |
| D5 | Lectures 4 and 5 placeholders | **Retire both.** Their slots become weeks 6 and 7 above |
| D6 | Week 2 next year, when it returns | Hold for now. The obvious use is splitting week 10, which option B leaves tight |

Once D1 and D2 are agreed, the site's navigation, lesson folders and titles can
be regenerated to match, and CONTENT.md's rows move to **scoped**.

---

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
