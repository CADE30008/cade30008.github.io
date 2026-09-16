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
which leaves room for some guest lectures for flavour. Each lecture is a lectured
element followed by students implementing what was covered, individually or in
pairs or threes, building week on week towards a complete design cycle. Students
also have about four hours of laboratory time on a Quanser 3-DoF helicopter,
likely in two two-hour sittings.

**Lecture 1** introduces the Quanser helicopter in person, so it runs to a fixed
plan: about 30 minutes of taught introduction, a 5-minute break, 30 minutes
demonstrating the Quanser and showing students how to use it, a 5-minute break,
30 minutes of students working examples on their laptops, and 20 minutes to wrap
up and look ahead. The Quanser can come back into the lecture for demonstrations
in later weeks.

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
