# Pedagogical principles: CADE30008, control half

> Drafted with the assistance of generative AI tools.[^checked]

[^checked]: The final versions of all process and assignment documents, and of all student-facing and back-office code, will be fully checked manually.

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

**Naming.** The course site calls this *Flight Dynamics & Control*. For control,
this unit is the introduction; a separate advanced unit at year 4 master's level
is planned, and "advanced" is kept for that.

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

**Delivery.** The unit runs for 12 weeks. Week 6 is reading week and week 12 is
revision week, leaving 10 teaching weeks. This half has eight two-hour lectures,
which leaves room for some guest lectures for flavour. Each session runs to a
fixed shape (P17): a taught hour, then a 50-minute case hour in which students
deploy what was covered, individually or in pairs or threes. The timetabled
second hour is 50 minutes, not 60. Students also have about four hours of
laboratory time on a Quanser 3-DoF helicopter, likely in two two-hour sittings.

**Student effort between lectures.** Two hours a week for a mid-range student,
with up to two more available for those who want them. The first two hours are
the expectation and everything assessed depends only on them; the extension
hours are genuine depth, not catch-up for people who were slower in the room.
See P17 for how those hours are divided.

**Lecture 1** introduces the Quanser helicopter in person and runs the whole
design cycle once, so it departs from the standard shape: there is no previous
week to retrieve, and the case hour is built round the hardware. Its plan is
under "Lecture 1: the Quanser session" below. The Quanser can come back into the
lecture for demonstrations in later weeks.

**In the room.** Most students bring laptops; those who don't share with those
who do. Assume no teaching assistants, although some may join.

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
control design, and can say why it works. A first-class graduate will also have
the deeper theoretical and mathematical underpinning to progress to an advanced
course or a PhD.

## Course themes

Threads that run through the lectures, alongside the principles below.

- **Model-based design.** Introduced early, as the industrial form of the design
  cycle (P1): requirements, models, simulation, verification and implementation
  worked from the same models. A guest lecture from MathWorks is likely to focus
  on it.
- **AI-assisted engineering.** Students may use AI throughout, including
  MathWorks' copilots in MATLAB and Simulink, and agentic workflows through the
  MATLAB MCP Server and the MATLAB and Simulink agentic toolkits. Verifying what
  an AI tool produces is taught as part of good design practice, and assessed
  (see [ASSESSMENT.md](ASSESSMENT.md)).

## Principles

### P1. The design cycle is the spine

Every lecture states where it sits in the design cycle, and which design
question the week's tool answers.

- Each handout opens by locating itself in the cycle.
- A tool is introduced by the goal it serves, never as technique for its own sake.
- **A week focuses on one part of the cycle; it does not stop there.** Where it
  can be afforded, a week runs the whole cycle and changes only which part is
  examined closely. A week that is purely analysis, or purely modelling, leaves
  students with nothing that flies, and a term of such weeks is disjointed. What
  varies week to week is the focus, not the presence of the other stages.
- **Review check:** can you name, for each lecture, the design question it
  answers, and what the students had working by the end of it?

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
- Python, runnable in the browser where that helps. MATLAB as an accompanying
  Live Script or code to paste, and Simulink models shared from MATLAB Drive.
  Delivery details are still open (Q1).
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

- **A floor.** Every activity has a first result that every student, or every
  pair, can definitely reach in the time available.
- **A feedback moment at the floor.** Students check their result with a
  neighbour, and a sample is shared with the room, for example through
  Mentimeter.
- **A ceiling above it.** The rest of the build and its extensions continue past
  the floor. Quicker students stretch themselves in the session; others finish
  afterwards. Not finishing in the room is expected, not a failure.
- **Unblockable without staff.** With no teaching assistants assumed, instructions,
  starter code and checkpoints must let students get themselves and each other
  unstuck.
- Activities compound: week *n* consumes the output of week *n* − 1.
- **Review check:** what is the floor, can every student reach it in the time, and does the activity use last week's result?

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

### P11. Each lecture opens by retrieving the last

A few minutes of recall or prediction on earlier weeks, before new material.
Retrieval and spacing are among the best evidenced effects in learning, and this
course's week-on-week build gives them for free.

- Open with two or three questions that students answer before any answer is shown.
- Prefer questions that ask for prediction or reasoning over recall of definitions.
- Reach back beyond the previous week at times, so that practice is spaced.
- **Review check:** does the lecture open with questions students answer, and do some reach further back than last week?

### P12. Demos follow predict, observe, explain

Ask for a prediction before running a demo, then show the result, then explain
the gap. A demo that is merely watched teaches much less than one that has been
bet on.

- Students commit to a prediction first: a show of hands, a vote, or a sentence written down.
- The explanation addresses the gap between what was predicted and what happened.
- In the handout, pose the prediction as a question and fold the result away beneath it.
- **Review check:** is there a prediction prompt before every demo and applet experiment?

### P13. Misconceptions are named

Where students reliably go wrong, say so explicitly rather than only stating the
correct version. Explanations that confront a misconception teach better than
those that only present the right answer.

- State the misconception, show why it is tempting, then show where it fails.
- Keep a list per lecture. Candidates so far: margins as a safety guarantee,
  derivative action as noise-free prediction, cancelling a plant pole,
  linearisation valid far from trim.
- **Review check:** are the lecture's known misconceptions named and confronted?

### P14. Accessible by construction

Figures carry meaningful alternative text, colour is never the only channel of
information, applets are operable from the keyboard, and every figure's meaning
survives in the printed PDF.

- Alternative text says what a figure shows, not only what it is.
- Lines are distinguished by style, marker or direct label, not by colour alone.
- Applets work from the keyboard and expose their controls to screen readers.
- Video carries captions.
- **Review check:** could a student using a screen reader, or a greyscale printout, follow the lecture?

### P15. Real-world context shows why it matters

Anchor the material in real aerospace systems and events, so that students see
why a technique exists, what it made possible, and what happened when it was
missing or misapplied. Wider engineering examples are welcome where they make
the point better.

- Each lecture uses at least one real system, programme or incident to show the stakes of its topic.
- Describe incidents from primary sources, such as investigation reports and agency accounts. State the control lesson precisely, and don't overstate it.
- People died in several of these events. Treat them with care, and keep the focus on the engineering lesson.
- **Review check:** does the lecture show a real case that makes its topic matter, and cite a source for it?

Candidate cases. The first three have been checked in outline against the
sources linked; all need checking against the primary report before teaching.

| Case | What it shows | Source |
|---|---|---|
| Ingenuity Mars helicopter, flight 6 (2021) | A lost navigation image corrupted timestamps and caused large oscillations. The controller's stability margins let it land safely anyway. Robustness, ILO 4 | [NASA](https://science.nasa.gov/blog/surviving-an-in-flight-anomaly-what-happened-on-ingenuitys-sixth-flight/) |
| X-15 flight 3-65-97 (1967) | The MH-96 adaptive flight control system entered diverging pitch and roll oscillations on re-entry. The aircraft broke up and Michael Adams was killed. Adaptive control, limit cycles | [Summary](https://en.wikipedia.org/wiki/X-15_Flight_3-65-97), [NASA NESC analysis](https://nescacademy.nasa.gov/video/afbbfa1bb74243aeab139db4c110c2021d) |
| YF-22 (1992) | Pilot-induced oscillation with the stabilator at its software rate limit, and over half a second of lag round the pilot loop. Actuator limits and delay | [Aviation Safety Network](https://aviation-safety.net/wikibase/46043) |
| Boeing 737 MAX, MCAS (2018, 2019) | Automatic trim commanded from a single angle-of-attack sensor. Sensing, control authority and the pilot in the loop | To find |
| Air France 447 (2009) | Pitot icing, autopilot disconnection and degraded control laws. What happens when automation hands the aircraft back | To find |

### P16. A short challenge each week

A low-stakes, automatically marked challenge each week, open for a set window: a
diagnostic in week 1, then one challenge per lecture that rehearses that week's
build. It gives spaced retrieval (P11) outside the lecture, and tells students
and staff early who is struggling.

- Mathematics and concept questions in Numbas, which Bristol supports through
  Blackboard, with randomised values so that each student works their own
  numbers.
- Code challenges in MATLAB Grader. The University's licence covers it; its
  Blackboard integration needs the licence administrator to set it up.
- Formative: feedback rather than marks, unless the assessment design (Q2) says
  otherwise.
- **Review check:** does each lecture have a challenge, and does it rehearse something the coursework assesses?

### P17. One shape every week

Every session runs to the same named slots, in the same order, so that students
always know what kind of work the next fifteen minutes asks of them. The
predictability is the point: it removes a cognitive cost (P4) that carries no
teaching value, and it lets the material vary without the format varying.

| Slot | Min | What happens | Serves |
|---|---|---|---|
| **Recall and resolve** | 5 | Two or three questions on earlier weeks, answered before any answer is shown; then the resolution of last week's hook | P11, P18 |
| **Block A** | 15 | Taught: the idea, opened on something concrete | P2, P4 |
| **Do A** | 10 | Pairs: the smallest real use of the idea. Floor result, sampled to the room | P8 |
| **Block B** | 15 | Taught: the method or tool that acts on the idea | P2, P4 |
| **Do B** | 10 | Pairs: apply it. Floor result | P8 |
| *Changeover* | 5 | | |
| **Case brief** | 5 | The artifact arrives. What do we see, what matters here | P18 |
| **Case build** | 25 | Deploy the week's work on the case. Floor, then ceiling | P8, P18 |
| **Converge** | 10 | Sample results to the room, name the disagreement, resolve it | P8, P18 |
| **The hook** | 10 | What this week's tool cannot do. Students name what they would need; the independent work is set | P18, P15 |

- **Practice is interleaved, not banked.** Two taught blocks back to back, with
  the practice afterwards, lets block A decay before it is used and hides a
  failed block A until it is too late to change block B.
- **The session ends on the hook, never on the build.** The build will always
  want the extra ten minutes. It does not get them.
- **Slot names are printed in the deck and the handout.** Students should be able
  to name the slot they are in.
- **Lectures may deviate, and say so.** Lecture 1 does. A guest lecture may take
  the case hour (Q7). Deviating silently is the thing to avoid.

Between sessions, three parts in the same order every week, two hours for a
mid-range student and up to two more for those who want them:

| Part | Core | Extension | What it is |
|---|---|---|---|
| **1. Close the loop** | 45 min | +30 min | Finish the ceiling of the in-lecture build; that week's challenge in Numbas and MATLAB Grader (P16) |
| **2. Feed the design** | 60 min | +75 min | The coursework step for the week, and a decision-log entry |
| **3. Meet next week's case** | 15 min | +15 min | One small artifact to read or watch before the next session (P18) |

- **The core two hours are sufficient.** Nothing assessed requires the extension,
  and the extension is depth rather than catch-up (P8's ceiling, not its floor).
- **Part 3 stays small.** Compliance with pre-reading falls away sharply past
  about twenty minutes. The next session's opener should reward having done it
  without punishing not having.
- **Review check:** does the week's material fit these slots and these hours, and
  would a student who did only the core two hours be able to do everything
  assessed?

### P18. A case runs the week, not the hour

Each week is organised round one case: a situation with evidence attached, which
the week's work is used on. The case cycle is spread across the whole week
rather than compressed into the case hour, because the part of it that needs
independent study cannot happen in a lecture theatre.

This is an adaptation of case-based learning as the University's Vet School runs
it. See "Case-based learning" below for what was changed and why.

| Step, in the Vet School's form | Where it happens here |
|---|---|
| 1–2. Read the case, define terms, identify its key aspects | Case brief, 5 min |
| 3. Share what you already know | Case build in pairs and threes, 25 min |
| 4. Arrange explanations, identify gaps | Converge, 10 min |
| 5. Establish learning objectives | **The hook**, 10 min: the case is built so the week's tool takes students most of the way, and the residual gap is next week's topic, which they name themselves |
| 6. Independent study | The week's independent work, all three parts |
| 7. Share and reflect | Recall and resolve, at the start of the next session |

- **A case opens with evidence, not a problem statement.** A telemetry trace, a
  pilot's complaint, a page of an investigation report, a requirements document
  with a contradiction in it, a video of a rig misbehaving. Not "design a
  controller such that $\zeta \ge 0.7$": that is an exercise, and it belongs in
  the example sheet.
- **Two grains of case, kept distinct.** The *running case* is the design thread
  on our three systems (P9); it compounds week on week and is what the coursework
  rehearses (P10). The *incident case* is a short real one (P15), used for the
  hook and for critique and transfer, which is where the higher marks live.
- **Every hook is paid off** in the next session's opener. One unpaid hook and
  students stop investing in them.
- **The gap must be real.** Test each case by asking whether a practising
  engineer would actually reach for the new tool here. A manufactured gap, where
  the week's tool would have worked and something was hidden, reads as a trick.
- **Not every week needs to hurt.** The hard form, where students genuinely fail
  before being given the tool, is expensive in time and dispiriting if
  unrelieved. Three or four weeks of eight; the rest get a softer "here is where
  this stops working".
- **Review check:** what is the week's artifact, what is the gap it ends on, and
  which session resolves it?

## Case-based learning

Steve's Q8 asked whether the Vet School's case-based learning transfers to this
unit. The answer adopted in P18 is: its mechanisms do, its timetable does not.

**What the Vet School does.** Seven steps — read the case and define terms;
define its key aspects; share what you know; arrange explanations and identify
gaps; establish and review learning objectives; independent study; share and
reflect — run by small facilitated groups over about a week per cycle. The
engine is step 5: students derive their own learning objectives and then go and
meet them. The structure descends from the Maastricht "seven jump" of
problem-based learning.

**Why the standard form does not transfer here.**

1. **No facilitators.** Each Vet School group has a tutor keeping steps 3 to 5
   honest. With about 200 students and no teaching assistants assumed (Q3),
   unfacilitated groups will set vague or wrong learning objectives and nobody
   will catch it.
2. **Control's knowledge is deep and sequential, not broad and branching.** A
   student who has not met the Nyquist criterion cannot identify that it is what
   they need. Veterinary medicine's knowledge space lets a naive learner name
   useful gaps; ours largely does not, and the prior-knowledge spread (Q5) makes
   this worse.
3. **The clock.** A cycle takes the Vet School a week. Fifty minutes cannot hold
   seven steps, and compressing them produces a worksheet in a case-based
   learning costume.

**What we changed.** The cycle is distributed across the week, so the lecture
holds steps 1 to 5 and the independent work holds step 6, with step 7 opening the
next session. Step 5 is scaffolded rather than free: the gap is chosen by us,
through the design of the case, and discovered by the students. That keeps the
motivational force of deriving your own learning objective while removing the
part that needs a tutor per group.

**This may be novel, and is worth writing up.** Not a priority for 2026/27, but
worth building so that it could be. What the literature looks like at present:

- Case-based learning's evidence base is medical, veterinary and health
  professions education. Engineering has a case-study tradition, but it is mostly
  cases as illustration rather than cases as the driver of learning objectives.
- **Steve to review:** the *Case Studies in Engineering* chapter of the Cambridge
  Handbook of Engineering Education Research, which is the nearest thing to a
  survey of the engineering end.
- Reguera et al. (2008), in Steve's Q8 note, is case-based **reasoning** — an
  artificial-intelligence technique that retrieves previous students' attempts to
  advise the current one — not case-based **learning**. Useful for its remote
  laboratory and system-identification material; not evidence for the method.
- Wei (2024), also in Q8, is a four-page position piece in a new journal with no
  evaluation data. Not citable.

So the claim available to us is a reasonable one: case-based learning adapted
from the health professions to a large, unfacilitated engineering cohort, by
distributing the cycle across the week and scaffolding the learning-objective
step. If we want to make that claim, we should collect something while teaching
it — hook-to-resolution attendance, the quality of the objectives students
name at the hook, and the weekly challenge results (P16).

**To read when we engage with the pedagogy properly.** Not now.

- Schmidt, H. G. (1983). Problem-based learning: rationale and description.
  *Medical Education*, 17(1), 11–16.
  [doi:10.1111/j.1365-2923.1983.tb01086.x](https://doi.org/10.1111/j.1365-2923.1983.tb01086.x).
  The Maastricht seven-jump, from the school that built it.
- Wood, D. F. (2003). Problem based learning. *BMJ*, 326(7384), 328–330.
  [doi:10.1136/bmj.326.7384.328](https://doi.org/10.1136/bmj.326.7384.328). Two
  pages, and the quickest route in.
- University of Bristol Vet School,
  [case-based learning](https://www.bristol.ac.uk/vet-school/study/undergraduate/key-information/case-based-learning/).
- *Case Studies in Engineering*, chapter 9 of the
  [Cambridge Handbook of Engineering Education Research](https://www.cambridge.org/core/books/abs/cambridge-handbook-of-engineering-education-research/case-studies-in-engineering/35D1BCA038FA98353E8820FEDFF3489A).
- Reguera, P., Fuertes, J. J., Domínguez, M. and García, R. (2008). Case-based
  reasoning and system identification for control engineering learning. *IEEE
  Transactions on Education*, 51(2), 271–281.
  [doi:10.1109/TE.2007.909361](https://doi.org/10.1109/TE.2007.909361).
- Wei, M. (2024). Enhancing student engagement and intellectual development
  through case-based instruction in modern control theory. *International Journal
  of Education and Social Development*, 1(2), 30–33.
  [doi:10.54097/8csbk196](https://doi.org/10.54097/8csbk196). Recorded for
  completeness; see the caution above.

## Models we are drawing on

Named here so we can write about this later, and so choices are defensible. Each
has an accessible summary and an original source.

- **Four-component instructional design (van Merriënboer).** The overarching
  fit: complex skills are learned through whole tasks of increasing complexity,
  supported by just-in-time information and part-task practice. Our week-on-week
  build to a full design cycle is precisely this. Supports A1, P8.
  - Summary: [4C/ID](https://www.4cid.org/)
  - Original: van Merriënboer, J. J. G., Clark, R. E. and de Croock, M. B. M. (2002). Blueprints for complex learning: the 4C/ID-model. *Educational Technology Research and Development*, 50(2), 39–61. [doi:10.1007/BF02504993](https://doi.org/10.1007/BF02504993)
- **Cognitive load theory (Sweller).** The constraint behind P3 and P4. Keep
  extraneous load down, and stage intrinsic load deliberately.
  - Summary: [Cognitive load](https://en.wikipedia.org/wiki/Cognitive_load)
  - Original: Sweller, J. (1988). Cognitive load during problem solving: effects on learning. *Cognitive Science*, 12(2), 257–285. [doi:10.1207/s15516709cog1202_4](https://doi.org/10.1207/s15516709cog1202_4)
  - Further: Sweller, J., van Merriënboer, J. J. G. and Paas, F. (1998). Cognitive architecture and instructional design. *Educational Psychology Review*, 10(3), 251–296. [doi:10.1023/A:1022193728205](https://doi.org/10.1023/A:1022193728205)
- **Worked example effect, and the expertise reversal effect (Kalyuga).** Start
  with fully worked designs, then completion problems, then open design. What
  helps a novice hinders an expert, so support fades week by week.
  - Summaries: [Worked-example effect](https://en.wikipedia.org/wiki/Worked-example_effect), [Expertise reversal effect](https://en.wikipedia.org/wiki/Expertise_reversal_effect)
  - Originals: Sweller, J. and Cooper, G. A. (1985). The use of worked examples as a substitute for problem solving in learning algebra. *Cognition and Instruction*, 2(1), 59–89. [doi:10.1207/s1532690xci0201_3](https://doi.org/10.1207/s1532690xci0201_3). Kalyuga, S., Ayres, P., Chandler, P. and Sweller, J. (2003). The expertise reversal effect. *Educational Psychologist*, 38(1), 23–31. [doi:10.1207/S15326985EP3801_4](https://doi.org/10.1207/S15326985EP3801_4)
  - On fading support: Renkl, A. and Atkinson, R. K. (2003). Structuring the transition from example study to problem solving in cognitive skill acquisition. *Educational Psychologist*, 38(1), 15–22. [doi:10.1207/S15326985EP3801_3](https://doi.org/10.1207/S15326985EP3801_3)
- **Constructive alignment (Biggs).** ILOs, activities and assessment stated in
  the same terms. Supports P10.
  - Summary: [Constructive alignment](https://en.wikipedia.org/wiki/Constructive_alignment)
  - Original: Biggs, J. (1996). Enhancing teaching through constructive alignment. *Higher Education*, 32(3), 347–364. [doi:10.1007/BF00138871](https://doi.org/10.1007/BF00138871)
- **SOLO taxonomy (Biggs and Collis).** A defensible language for the pass and
  excellence split in P10: applying a procedure correctly is one level, relating
  it to the theory that justifies it is the next.
  - Summary: [Structure of observed learning outcome](https://en.wikipedia.org/wiki/Structure_of_observed_learning_outcome)
  - Original: Biggs, J. B. and Collis, K. F. (1982). *Evaluating the Quality of Learning: The SOLO Taxonomy*. Academic Press. [doi:10.1016/C2013-0-10375-3](https://doi.org/10.1016/C2013-0-10375-3)
- **Variation theory (Marton).** Understanding comes from what is varied against
  a fixed background. Revisiting three systems (P9) is what makes the invariant
  principles visible.
  - Summary: [Phenomenography](https://en.wikipedia.org/wiki/Phenomenography), from which variation theory grew
  - Original: Marton, F. and Pang, M. F. (2006). On some necessary conditions of learning. *Journal of the Learning Sciences*, 15(2), 193–220. [doi:10.1207/s15327809jls1502_2](https://doi.org/10.1207/s15327809jls1502_2)
- **Predict, observe, explain (White and Gunstone).** Behind P12.
  - Summary: [Predict, Observe, Explain (NZCER)](https://arbs.nzcer.org.nz/predict-observe-explain-poe)
  - Original: White, R. and Gunstone, R. (1992). *Probing Understanding*. Falmer Press; reissued by Routledge, 2014. [doi:10.4324/9780203761342](https://doi.org/10.4324/9780203761342)
- **Peer instruction (Mazur).** For the in-lecture activity in pairs and threes.
  - Summary: [Peer instruction](https://en.wikipedia.org/wiki/Peer_instruction)
  - Original: Crouch, C. H. and Mazur, E. (2001). Peer Instruction: ten years of experience and results. *American Journal of Physics*, 69(9), 970–977. [doi:10.1119/1.1374249](https://doi.org/10.1119/1.1374249)
- **Productive failure (Kapur).** Letting students attempt a design before being
  given the tool can prepare them to learn it. A candidate for the opening of
  some lectures.
  - Summary: [Manu Kapur](https://www.manukapur.com/)
  - Original: Kapur, M. (2008). Productive failure. *Cognition and Instruction*, 26(3), 379–424. [doi:10.1080/07370000802212669](https://doi.org/10.1080/07370000802212669)
  - Further: Kapur, M. (2016). Examining productive failure, productive success, unproductive failure, and unproductive success in learning. *Educational Psychologist*, 51(2), 289–299. [doi:10.1080/00461520.2016.1155457](https://doi.org/10.1080/00461520.2016.1155457)
- **Threshold concepts (Meyer and Land).** Some ideas are gateways and are worth
  dwelling on: feedback itself, stability margin as robustness, the cost of
  bandwidth.
  - Summary: [Threshold knowledge](https://en.wikipedia.org/wiki/Threshold_knowledge)
  - Original: Meyer, J. H. F. and Land, R. (2005). Threshold concepts and troublesome knowledge (2). *Higher Education*, 49(3), 373–388. [doi:10.1007/s10734-004-6779-5](https://doi.org/10.1007/s10734-004-6779-5)
- **Retrieval practice and spacing.** Behind P11.
  - Summaries: [Testing effect](https://en.wikipedia.org/wiki/Testing_effect), [Spacing effect](https://en.wikipedia.org/wiki/Spacing_effect)
  - Originals: Roediger, H. L. and Butler, A. C. (2011). The critical role of retrieval practice in long-term retention. *Trends in Cognitive Sciences*, 15(1), 20–27. [doi:10.1016/j.tics.2010.09.003](https://doi.org/10.1016/j.tics.2010.09.003). Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T. and Rothstein, T. (2006). Distributed practice in verbal recall tasks. *Psychological Bulletin*, 132(3), 354–380. [doi:10.1037/0033-2909.132.3.354](https://doi.org/10.1037/0033-2909.132.3.354)
- **Conceptual change, and teaching through misconceptions.** Behind P13.
  - Summary: [Conceptual change](https://en.wikipedia.org/wiki/Conceptual_change)
  - Originals: Posner, G. J., Strike, K. A., Hewson, P. W. and Gertzog, W. A. (1982). Accommodation of a scientific conception. *Science Education*, 66(2), 211–227. [doi:10.1002/sce.3730660207](https://doi.org/10.1002/sce.3730660207). Muller, D. A., Bewes, J., Sharma, M. D. and Reimann, P. (2008). Saying the wrong thing: improving learning with multimedia by including misconceptions. *Journal of Computer Assisted Learning*, 24(2), 144–155. [doi:10.1111/j.1365-2729.2007.00248.x](https://doi.org/10.1111/j.1365-2729.2007.00248.x)
- **Authentic learning and situated cognition.** Behind P15: knowledge learned in
  the context where it is used transfers better than knowledge learned abstractly.
  - Summaries: [Authentic learning](https://en.wikipedia.org/wiki/Authentic_learning), [Situated cognition](https://en.wikipedia.org/wiki/Situated_cognition)
  - Originals: Brown, J. S., Collins, A. and Duguid, P. (1989). Situated cognition and the culture of learning. *Educational Researcher*, 18(1), 32–42. [doi:10.3102/0013189X018001032](https://doi.org/10.3102/0013189X018001032). Herrington, J. and Oliver, R. (2000). An instructional design framework for authentic learning environments. *Educational Technology Research and Development*, 48(3), 23–48. [doi:10.1007/BF02319856](https://doi.org/10.1007/BF02319856)
- **Low floor, high ceiling, wide walls (Papert, Resnick).** Behind P8: an
  activity everyone can start and reach a result in, with room for the quickest
  to go much further, and more than one route through it.
  - Summary: [Designing for wide walls (Resnick)](https://mres.medium.com/designing-for-wide-walls-323bdb4e7277)
  - Originals: Papert, S. (1980). *Mindstorms: Children, Computers, and Powerful Ideas*. Basic Books. Resnick, M. and Silverman, B. (2005). Some reflections on designing construction kits for kids. *Proceedings of the 2005 Conference on Interaction Design and Children*, 117–122. [doi:10.1145/1109540.1109556](https://doi.org/10.1145/1109540.1109556)
- **Multimedia learning (Mayer).** How words and figures are best combined.
  Supports P4 and P14.
  - Original: Mayer, R. E. (2009). *Multimedia Learning*, 2nd edition. Cambridge University Press. [doi:10.1017/CBO9780511811678](https://doi.org/10.1017/CBO9780511811678)
- **Universal design for learning, and web accessibility.** Behind P14.
  - Summaries: [Universal Design for Learning](https://en.wikipedia.org/wiki/Universal_Design_for_Learning), [CAST UDL guidelines](https://udlguidelines.cast.org/)
  - Standard: [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/)

## Preparation before Lecture 1

Students complete these before the first lecture. The course site's
[Preparing for Control](docs/preparing/index.md) page lists them and checks each
student's set-up.

- **A device check.** Scripts confirming that Python, MATLAB and Simulink work,
  with the same expected numbers in each, and Python that runs in the browser
  for tablets and Chromebooks.
- **MathWorks Onramps:** MATLAB Onramp, Simulink Onramp, and Control Design
  Onramp with Simulink. Free and self-paced.
- **A diagnostic** on the prerequisite mathematics and control (P16).

MathWorks online courses and MATLAB Grader both integrate with Blackboard through
LTI 1.3 and report progress back. Both need a suitable MathWorks licence, a
Campus-Wide Licence in MATLAB Grader's case, and the licence administrator to set
up the integration. The University's licence is campus-wide, and includes the
Control System Toolbox, the Aerospace Toolbox and most other toolboxes, so the
licence requirement is met; the integration still needs the licence
administrator.

MATLAB Online and Simulink Online are not supported on tablets. Tablet users can
run the Python material in the browser, but need a laptop, or a partner's, for
MATLAB and Simulink.

## Live feedback in lectures (open question)

Undecided; see Q3. One candidate is Mentimeter, which Bristol supports, run
alongside the slide deck. It has two formats that do different jobs, and only one
of them can be summarised by AI:

| Format | Use it for | AI grouping and summary |
|---|---|---|
| **Q&A, switched on for every slide** | The live chat. Students post questions whenever they arise, anonymously, and upvote each other's, so the most wanted rise to the top | No |
| **Open Ended slides**, at planned moments | Anything you want summarised: results at an activity's floor, what's still unclear, explanations after a prediction | Yes, on request |

A lecture's rhythm then runs:

1. **Opening (P11).** A short quiz or multiple-choice question on earlier weeks.
2. **Throughout.** Q&A open on every slide. Don't read it while lecturing; take
   the top-voted questions at each break and at the wrap-up.
3. **Before a demo (P12).** A multiple-choice prediction.
4. **At the activity's floor (P8).** An Open Ended slide where pairs post their
   result or sticking point. Group the responses with AI, show the themes, and
   address the largest.
5. **Wrap-up.** An Open Ended "muddiest point" slide, summarised with AI, which
   also shapes the opening of the next lecture.

The deck shows the Mentimeter joining code in its header, so students can join
at any point, and each planned Mentimeter moment has a matching slide in the
deck.

Microsoft Teams with Copilot can also summarise a chat, but needs a Microsoft
365 Copilot licence and a Team for the unit, and fits a lecture theatre less
naturally. Padlet has AI features for creating boards, but none confirmed for
summarising posts.

## Lecture 1: the Quanser session

Lecture 1 runs the whole design cycle once, on the Quanser 3-DoF helicopter's
elevation axis, in front of the room. Everything after it is that cycle done
properly. It deviates from P17's shape, which is stated to students.

**The narrative.** Not "here is a control system", but "here is a machine that
cannot be flown without one". Controller selection is deliberately skipped: we
use PID because it is what everyone reaches for first, and we say plainly that
we will spend a later week finding out when that is the wrong answer. Naming the
omission is better than hiding it, and it is the first hook (P18).

**Hour 1.**

1. Why control exists, and the design cycle as the spine of the unit (P1).
2. The rig: what it is, how it is driven, how it is made safe.
3. **The open-loop flight attempt.** A student volunteer flies the elevation axis
   open loop, with direct control of each motor on two joysticks. They will not
   be able to hold it. This is the demonstration the whole unit hangs off, and it
   follows predict-observe-explain (P12): the room votes first on how long they
   will last.
4. What a requirement is, and the requirement we will design to today.

**Hour 2, the case hour.** The artifact is the recording of the open-loop
attempt, plus a clean measured response from the rig.

| Min | What |
|---|---|
| 10 | **System identification** from the measured response, in a MATLAB Live Script |
| 15 | **Tune a PID** in simulation against the stated requirement, and submit gains |
| 15 | **Fly the submitted gains** on the real rig, in three rounds |
| 10 | **The hook** |

**System identification.** The elevation axis is lightly damped and second
order, so a manual fit is genuinely readable: the oscillation period gives the
damped frequency, the ratio of successive peaks gives the damping ratio, and the
steady state gives the gain. That is the floor, reachable by everyone. The
ceiling is `tfest`, in the same Live Script, for those who can. The Live Script
offers both routes; the measured data is distributed through MATLAB Drive.
`private/quanser/Quanser Lab/Quanser Lab 1 - System ID and PID/` already holds a
system-identification Live Script and matching data from the existing
laboratory, which is the thing to adapt rather than write fresh. It models the
axis as second order with a damping ratio near 0.06, and carries two
alternative fits from different rigs, which is a ready-made illustration that
two honest engineers get two different models.

**Getting gains back.** Students drop a small results file into a shared MATLAB
Drive folder, one per student or pair, written by the Live Script so the format
is fixed and the file is named from their username. This is better than a
free-text poll: the values arrive as numbers, they can be read straight into
MATLAB, and it rehearses the coursework's submission contract in miniature.

**Flying the gains, in three rounds.** The rounds are the teaching, not the
spectacle:

1. **A few individual sets, chosen to be extreme.** A small selection tool picks
   submissions from the edges of the cohort's spread: the most aggressive, the
   most sluggish, the one with the most integral. Students see the shape of
   cause and effect before they see a good answer.
2. **The cohort average.** Rarely the best, and occasionally worse than most of
   its parts, which is a point worth making.
3. **A few of the best.** Best against the stated requirement, which is the
   setup for the hook.

**Safety.** A student is flying an unstable machine in a room of 200. An e-stop
on the amplifier, in Steve's hand, is the primary measure. The submitted gains
are filtered before anything reaches the hardware: anything predicted unstable,
or demanding more than the actuators can give, is rejected by the selection tool
and not flown. Guarding, tethering and the rig's own limits apply as in the
laboratory. Sight lines matter too: 200 seats need a camera on the rig with the
feed on the main screen.

**The hook.** Two gaps, both real:

- **There is no right answer until you say what you want.** The three rounds are
  ranked differently under different requirements. Change the requirement and
  the winner changes. This motivates the whole of the requirements strand and
  the coursework's first criterion.
- **Simulation and hardware disagree.** Gains that won in simulation will not
  behave the same on the rig, because of what the model left out: noise,
  saturation, delay, unmodelled dynamics. That is the model-validation strand
  and the coursework's virtual flight test.

**A quote for the PID week.** Åström and Murray open their PID chapter with
"PID control is by far the most common way of using feedback", above an epigraph
reporting that a Honeywell survey of over eleven thousand controllers in the
refining, chemicals, and pulp and paper industries found 97 per cent of
regulatory controllers using PID feedback.

- Åström, K. J. and Murray, R. M. *Feedback Systems: An Introduction for
  Scientists and Engineers*, chapter 10.
  [Free PDF](https://www.cds.caltech.edu/~murray/books/AM08/pdf/am06-pid_16Sep06.pdf).
  Check the wording against the current edition before printing it.
- The survey it cites: Desborough, L. and Miller, R. (2002). Increasing customer
  value of industrial control performance monitoring: Honeywell's experience.
  *AIChE Symposium Series*, 326, 153–186.
- A line from Arthur Richards would sit better in a Bristol lecture than a
  textbook epigraph. Worth asking him for one, with permission to use it.

## Demonstrations

The lecture theatre takes 200 students and has room for large demonstrations.

- **This year:** the Quanser 3-DoF helicopter, from Lecture 1 onwards.
- **Future years,** once the first lectures are solid: Crazyflie nano
  quadcopters, and a propeller and motor on a balance beam, which needs designing
  and building.

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

**The glossary is reviewed at the same time.** [docs/glossary.md](docs/glossary.md)
is the single place a term is defined, and lectures use its wording. Every
review of a lecture also asks:

- Which terms does this lecture introduce that the glossary does not hold? Add
  them, in the glossary's plain style.
- Does the lecture define a term differently from the glossary? One of the two
  is wrong; decide which, and change that one.
- Is anything in the glossary now unused, or defined before it is needed?

A lecture is not finished until its terms are in the glossary. Glossary changes
go in the same commit as the lecture change that prompted them, so the review
note can cite both.

## Open questions

Recorded so they are not lost. Numbered for reference in discussion.

- **Q1. Two languages, one web page.**
  - *Python* runs in the browser through [Pyodide](https://pyodide.org/): the
    standard Python interpreter compiled to WebAssembly, which fetches NumPy,
    SciPy and Matplotlib from a CDN and installs python-control from PyPI.
    Tested on 16 September 2026: Pyodide 314.0.7 with python-control 0.10.2
    reproduces Lecture 2's margins exactly, with about four seconds of set-up
    after the first download, which the browser then caches.
  - *MATLAB* cannot run in a page. Offer an accompanying Live Script or code to
    paste, with an "Open in MATLAB Online" link where useful.
  - *Simulink* models are shared publicly from MATLAB Drive.
  - Still open: whether runnable Python appears as a Run button on code in the
    page or as linked notebooks, and whether slides run Python live or keep to
    the JavaScript applets.
- **Q2. Assessment design.** Being designed in [ASSESSMENT.md](ASSESSMENT.md),
  including the tension between P10's two bands and the aims' first-class
  graduate, which the draft resolves with SOLO-mapped descriptors at 40, 60 and
  70.
- **Q3. In-lecture activities and feedback.** About 200 students in a large
  lecture theatre, most with laptops, and no teaching assistants assumed. Which
  live feedback tool and format to use is undecided; a candidate pattern is under
  "Live feedback in lectures". Also open: whether the
  AI features are enabled on Bristol's Mentimeter account (Mentimeter includes
  them for all users from January 2026; confirm with Digital Education), and
  whether data protection allows student responses to be processed by them.
- **Q4. Quanser resources.** The existing MATLAB, Simulink and PDF materials, to
  be uploaded, and how the two laboratory sittings are scheduled against the
  lecture sequence.
- **Q5. Prior knowledge.**
  - Aerospace undergraduates have [CADE20002 Dynamics and Control of Linear
    Systems](https://www.bris.ac.uk/unit-programme-catalogue/UnitDetails.jsa?ayrCode=26%2F27&unitCode=CADE20002)
    as a prerequisite. Its outcomes include feedback stability and
    single-input single-output controller design, with MATLAB and Simulink
    laboratories, but control and PID come at the end in three sessions and are
    covered lightly.
  - Other cohorts take this unit too: aerospace MSc, Engineering Design and
    Study Abroad students, and possibly others. Their backgrounds vary, and may
    be weaker or stronger.
  - This gives P3 real weight. The plan: a diagnostic in week 1 (P16), the
    MathWorks Onramps and the Preparing for Control page before Lecture 1, and
    links back to prerequisite material throughout.
  - Still open: what the parallel half covers, week by week.
- **Q6. Shared system models.** Whether the three systems get one shared
  definition under `models/`, used by every lecture.
- **Q7. Where guest lectures go.** The site has eight lectures and a separate
  Guest lectures page. Two options:
  - *Separate slots.* Guests take two of the ten teaching weeks on their own.
    The eight-lecture build is untouched.
  - *Second-half slots.* Guests take the second half of two lectures, in place of
    that week's activity. That frees two weeks, but those two weeks' builds need
    another home, such as a take-home step, or P8 is broken for them.
  Topics for all eight lectures are still placeholders, and are settled when
  sketching the course.
- **Q8. Case-based learning**, after
  [Bristol Vet School](https://www.bristol.ac.uk/vet-school/study/undergraduate/key-information/case-based-learning/).
  Largely settled: adopted in adapted form as P18, with the reasoning and the
  reading list under "Case-based learning" above. What remains open:
  - Steve to review the Cambridge Handbook's *Case Studies in Engineering*
    chapter, which may change how novel the adaptation is.
  - Whether to collect evidence while teaching it, with a view to writing it up.
    Not a priority for 2026/27, but what to collect has to be decided before
    teaching starts, not after.
  - How the case grain interacts with the guest lectures (Q7), since a guest
    taking the case hour breaks that week's cycle.