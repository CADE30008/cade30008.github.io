# Pedagogical principles: CADE30008, control half

This file records how we want these materials to teach, so that decisions are
made once and applied consistently. It grows: add principles as we settle them.

**Principle IDs are stable.** Reviews, commit messages and review notes cite
them (`P3`, `P7`). Never renumber. If a principle is dropped, mark it
withdrawn and leave its number in place.

Two kinds of entry appear below. Unmarked principles are agreed. Those marked
**(proposed)** are suggestions awaiting a decision.

## The unit

[Flight Dynamics and Advanced Control (CADE30008)](https://www.bris.ac.uk/unit-programme-catalogue/UnitDetails.jsa?ayrCode=26%2F27&unitCode=CADE30008),
20 credits, level H/6, teaching block 1, weeks 1 to 12. Assessment is 100 per
cent individual coursework across all six intended learning outcomes. A 20
credit unit is about 200 hours of student effort in total.

This half of the unit covers **ILOs 4, 5 and 6**, paraphrased:

| ILO | In short |
|---|---|
| 4 | Analyse stability and robustness of negative-feedback control systems |
| 5 | Design and characterise control algorithms, classical and modern |
| 6 | Apply control theory to achieve aircraft performance and operations |

ILOs 1 to 3 cover rigid-body equations of motion, flight balance, stability and
the aircraft modes, and the reading of flight data against handling qualities.
They are delivered in parallel by other staff. The catalogue holds the
authoritative wording; the table above is a working paraphrase.

**Delivery.** Nine two-hour lectures. Each is a lectured element followed by
students implementing what was covered, individually or in pairs or threes,
building week on week towards a complete design cycle. Students also have about
four hours of laboratory time on a Quanser 3-DoF helicopter.

**Preferred text.** Dorf and Bishop, *Modern Control Systems*, chiefly for its
framing of the control design cycle.

## Aims

**A1. Insight into the design cycle.** Students understand the control design
cycle and how each tool we teach serves a design goal, rather than meeting a
sequence of techniques with no stated purpose.

**A2. Practice tied to theory.** Students connect what they do to the theory
that underpins it, through accessible descriptions, figures and interactive
demonstrations, with extensions for those confident in the mathematics.

The measure of success: a graduate of this half can *do* credible aerospace
control design, and can say why it works.

## Principles

### P1. The design cycle is the spine

Every lecture states where it sits in the design cycle, and which design
question the week's tool answers.

- Each handout opens by locating itself in the cycle.
- A tool is introduced by the goal it serves, never as technique for its own sake.
- **Review check:** can you name, for each lecture, the design question it answers?

### P2. Examples and demos first, theory hung off them

Start with something concrete that matters, then explain it. The example is the
hook the theory hangs on.

- Open with a system misbehaving, a demo, or a design that fails, before any derivation.
- Theory arrives as the explanation of something already seen.
- **Review check:** does the section's first screen or slide show a concrete case, not a definition?

### P3. Mathematical barriers are mitigated, not lowered

Top-level understanding takes precedence. A student whose grasp of the
underlying mathematics is shaky should still reach a correct working
understanding, and should be shown the route to the deeper version.

- State results plainly first; derive after, or in an aside.
- Link explicitly to prior and parallel learning rather than assuming it.
- Never require a derivation to follow the design argument.
- **Review check:** can the section be followed without the derivations? Are the links to deeper treatment present?

### P4. Information overload is managed

Core concepts come through cleanly on a first pass. Depth is available on the
second.

- Main line carries the core argument. Extensions, derivations and caveats go in collapsible asides.
- One idea per slide; the handout carries the full argument.
- **Review check:** read only the main line. Is it coherent and complete? Read only the asides. Are they genuinely optional?

### P5. Transfer is designed for

Students will apply this elsewhere, on systems we never show them. So the
boundary of each example is made explicit.

- Name the assumptions an example relies on, and what breaks when they fail.
- Separate what is general from what is specific to this aircraft or this rig.
- **Review check:** does each worked example state its limitations?

### P6. Every plot and interactive is reproducible, without getting in the way

Students can see and re-run the code behind anything we show, but it does not
clutter the argument.

- Figure and applet code is available, folded away or linked to source.
- Ideally in Python and MATLAB or Octave. The mechanism is an open question (Q1).
- **Review check:** for each figure, can a student reach the code that made it?

### P7. Code students are meant to run is prominent

The opposite of P6. Where the task is for the student to run, edit or extend
code, it is shown plainly in the flow of the material, not hidden.

- Student-facing code appears in full, in Python and MATLAB tabs.
- It is runnable as given, and has been run.
- **Review check:** is every snippet either clearly "yours to run" or clearly "how the figure was made"?

### P8. Two-hour rhythm: taught, then built

Each session is a lectured element and then supervised implementation, alone or
in small groups. The week's build is a step of the full design cycle.

- Every lecture has a defined activity with a deliverable a student can finish or take away.
- Activities compound: week *n* consumes the output of week *n* − 1.
- **Review check:** does the lecture have an activity, and does it use last week's result?

### P9. Three systems, revisited

We return to a small set of systems so that familiarity compounds and
comparisons are possible: a **fixed-wing** aircraft, a **multirotor**, and the
**Quanser 3-DoF helicopter** used in the laboratory.

- A new technique is shown on a system students already know.
- The same design goal is compared across systems where it is instructive.
- **Review check:** does the lecture use one of the three, and say why that one?

### P10. Assessment mirrors the practice

The coursework is a design task of the same kind as the in-lecture builds, with
room for extension.

- Pass, roughly 40 to 60 per cent: solid applied control design, evidenced.
- Excel, 60 per cent and above: that design linked convincingly to the theory.
- Nothing is assessed that was not practised; nothing is practised that leads nowhere.
- **Review check:** for each assessment criterion, which lecture activity rehearses it?

### P11 (proposed). Each lecture opens by retrieving the last

A few minutes of recall or prediction on the previous week, before new material.
Spacing and retrieval are among the best evidenced effects in learning, and this
course's week-on-week build gives them for free.

### P12 (proposed). Demos follow predict, observe, explain

Ask for a prediction before running a demo, then show the result, then explain
the gap. A demo that is merely watched teaches much less than one that has been
bet on.

### P13 (proposed). Misconceptions are named

Where students reliably go wrong, say so explicitly rather than only stating the
correct version. Candidates: margins as a safety guarantee, derivative action as
noise-free prediction, cancelling a plant pole, linearisation valid far from trim.

### P14 (proposed). Accessible by construction

Figures carry meaningful alternative text, colour is never the only channel of
information, applets are operable from the keyboard, and every figure's meaning
survives in the printed PDF.

## Models we are drawing on

Named here so we can write about this later, and so choices are defensible.

- **Four-component instructional design (van Merriënboer).** The overarching
  fit: complex skills are learned through whole tasks of increasing complexity,
  supported by just-in-time information and part-task practice. Our week-on-week
  build to a full design cycle is precisely this. Supports A1, P8.
- **Cognitive load theory (Sweller).** The constraint behind P3 and P4. Keep
  extraneous load down, and stage intrinsic load deliberately.
- **Worked example effect, and the expertise reversal effect (Kalyuga).** Start
  with fully worked designs, then completion problems, then open design. What
  helps a novice hinders an expert, so support fades week by week.
- **Constructive alignment (Biggs).** ILOs, activities and assessment stated in
  the same terms. Supports P10.
- **SOLO taxonomy (Biggs and Collis).** A defensible language for the pass and
  excellence split in P10: applying a procedure correctly is one level, relating
  it to the theory that justifies it is the next.
- **Variation theory (Marton).** Understanding comes from what is varied against
  a fixed background. Revisiting three systems (P9) is what makes the invariant
  principles visible.
- **Predict, observe, explain (White and Gunstone).** Behind P12.
- **Peer instruction (Mazur).** For the in-lecture activity in pairs and threes.
- **Productive failure (Kapur).** Letting students attempt a design before being
  given the tool can prepare them to learn it. A candidate for the opening of
  some lectures.
- **Threshold concepts (Meyer and Land).** Some ideas are gateways and are worth
  dwelling on: feedback itself, stability margin as robustness, the cost of
  bandwidth.

## Reviewing content against these principles

Mechanical consistency is already checked by `npm run check`. This review is the
judgement part, and is done by reading.

**When.** When a lecture first reaches draft; before the week it is taught;
and once across the whole course each time the principles change.

**How.** Read the handout, then the deck, then the example sheet, against the
principles above. Flag mismatches. Do not silently rewrite: the point is to
surface disagreements, some of which will be the principle's fault.

**Where findings go.** `reviews/<date>-<scope>.md`, for example
`reviews/2026-09-20-l02.md`:

```markdown
# Review: Lecture 2, 20 September 2026

| Principle | Where | Finding | Proposed action |
|---|---|---|---|
| P2 | l02 #derivative | Opens with the transfer function, no motivating case | Lead with the derivative-kick demo |
| P5 | l02 #pid-tuning | No statement of where the design assumptions fail | Add a limitations note |

Not a finding, but noted: ...
```

An AI assistant asked to review reports in exactly this form, cites principle
IDs, and changes nothing until a person agrees.

## Open questions

Recorded so they are not lost. Numbered for reference in discussion.

- **Q1. Two languages, one web page.** How to offer MATLAB alongside Python for
  runnable code, given that a browser cannot run MATLAB.
- **Q2. Assessment design.** Structure, artefacts, timing and rubric for the
  coursework, and how the control half combines with the other half's mark.
- **Q3. In-lecture activities.** Room, kit, class size and teaching support, all
  of which constrain what the activity can be.
- **Q4. Quanser resources.** The existing MATLAB, Simulink and PDF materials,
  and how laboratory time is scheduled against the lecture sequence.
- **Q5. Prior knowledge.** What year 2 covered exactly, and what the parallel
  half will have covered by each week of ours.
- **Q6. Shared system models.** Whether the three systems get one shared
  definition under `models/`, used by every lecture.
