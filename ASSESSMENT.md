# Assessment design: CADE30008, control half

**Status: draft proposal for discussion.** Nothing here is decided. Decisions
move into this file as they are made, as in [PEDAGOGY.md](PEDAGOGY.md).

> **Keep assessment material private.** This file holds design reasoning only.
> Briefs, marking schemes with model answers, exemplars and per-student
> parameters must not appear in any public copy of this repository. See AQ8.

## What is fixed

- The unit is assessed by **100 per cent individual coursework**, across ILOs 1
  to 6. This half assesses **ILOs 4, 5 and 6**: stability and robustness
  analysis, design and characterisation of controllers, and applying control to
  aircraft performance and operations.
- **Aims for the marks** (P10): a pass, roughly 40 to 60, evidences solid applied
  control design; 60 and above links that design convincingly to theory; a first,
  70 and above, shows the depth to progress to advanced study.
- **About 200 students**, marked by the lecturer. Assume no teaching assistants.
- Eight lectures build week on week to a full design cycle (P8). Students have
  two two-hour Quanser laboratory sittings, and a formative challenge each week
  (P16).
- Bristol sets four categories for generative AI use in assessment: 1,
  Prohibited; 2, Minimal, which is the default; 3, Selective, for defined
  purposes; and 4, Integral, where students critique and improve AI output. The
  brief must name the category, explain why it was chosen, and have marking
  criteria that fit it.

## Design goals

- **G1. Authentic.** The task is real control design, of the kind practised in
  lectures, not a test of recall (P10).
- **G2. Aligned.** Every criterion traces to an ILO and to a lecture activity
  that rehearsed it (constructive alignment).
- **G3. Discriminates at the right boundaries.** The descriptors separate 40,
  60 and 70 on what matters: working design, theory linked to it, and critical
  depth. The SOLO taxonomy gives the language.
- **G4. Individual, and robust to AI.** The evidence shows the student's own
  judgement, not only a product that a generative AI tool could produce.
- **G5. Markable by one person.** Structure and automation carry everything that
  doesn't need judgement, so marking time goes on judgement.
- **G6. Feedback that gets used.** At least one point in the term where feedback
  can still change the final submission.

## Proposed shape

### The task

A design brief like the in-lecture builds, but not the same one: the same design
cycle, applied to a system or axis students haven't built in lectures. Three
ways to set it:

| Option | What it is | For | Against |
|---|---|---|---|
| **A. Per-student variant** | A lecture system with parameters generated from each student's number | Results can be checked automatically; copying and shortcuts are harder | Close to the lecture work, so transfer (P5) is tested less |
| **B. A new system or axis** | For example, an axis of the Quanser helicopter or a multirotor loop not built in lectures | Tests transfer; can use data from the student's own laboratory session | Depends on laboratory timing, and on every student getting rig time before the deadline |
| **C. Integrated with the other half** | The other half's coursework models an aircraft (ILOs 1 to 3); this half designs its flight control (ILOs 4 to 6) | One authentic story across the unit, matching how aircraft are actually developed | Needs agreement with the other staff, and couples the two halves' deadlines |

**Recommendation:** C, if the other half agrees, with per-student parameters (A)
inside it. Otherwise A, with B available as an extension for those aiming high.

### What students submit

1. **A design report** with a fixed structure that follows the design cycle:
   requirements, model and assumptions, design, stability and robustness analysis,
   verification in simulation, and limitations and transfer. Page-limited.
2. **Runnable code or a Simulink model** that reproduces every number and figure
   in the report (P6). This makes the work auditable, and lets results be checked
   automatically.
3. **A design log.** Short entries kept through the term, recording each design
   decision, the alternatives considered, and why. It evidences process, which is
   individual and hard to produce convincingly after the fact.

Possible, depending on AQ3:

4. **A short recorded explanation**, about three minutes, of one design decision
   chosen by the marker from the log.

### Staging

- **A checkpoint after reading week.** Requirements, model and a first design.
  Formative. Feedback comes three ways, none needing teaching assistants:
  automated checks on the code, peer review through FeedbackFruits (which Bristol
  supports), and one whole-cohort feedback summary from the lecturer. Peer review
  also builds students' own judgement of quality.
- **The final submission.** Date to be set within the unit's assessment rules
  (AQ2).

### Marking criteria

Criteria, each tagged with the ILO it evidences. Weights to be set.

| Criterion | ILO | Carries the boundary at |
|---|---|---|
| Requirements and modelling | 6 | 40 |
| Design | 5 | 40 |
| Stability and robustness analysis | 4 | 50 |
| Verification | 5, 6 | 50 |
| Design linked to theory | 4, 5 | **60** |
| Limitations, assumptions and transfer | 4, 5, 6 | **70** |
| Communication and reproducibility | all | all |

Band descriptors, mapped onto SOLO levels:

| Mark | In short | SOLO |
|---|---|---|
| Below 40 | The design doesn't work, isn't evidenced, or misapplies the procedure | Prestructural |
| 40 to 49 | A working design with gaps in requirements, verification or evidence; little justification | Unistructural |
| 50 to 59 | A sound design that meets its requirements and is verified in simulation; the procedure is described correctly, but justification is descriptive | Multistructural |
| 60 to 69 | Design choices explained through theory, for example margins to transient response and system type to steady-state error, with trade-offs made explicit | Relational |
| 70 to 79 | Assumptions and limits analysed critically; results generalised beyond the case; alternatives compared | Extended abstract |
| 80 and above | An original extension with real depth, such as a modern-control comparison, rigorous robustness analysis, or insight from hardware validation, at a level suited to advanced study or research | Extended abstract |

### Marking 200 submissions alone

At 15 minutes a submission, marking takes 50 hours; at 25 minutes, 83. The
levers:

- **Automated checks.** Per-student parameters give each student's expected
  results. A script, or MATLAB Grader, checks that a submitted design meets its
  specification, and the marker sees the outcome rather than recomputing it.
- **A fixed report structure and page limit,** so each section is read against
  its criterion.
- **A rubric with a comment bank** in Blackboard.
- **Calibration and moderation.** Second-mark a sample, following the
  University's moderation rules.
- **Peer review at the checkpoint,** in place of individual staff feedback.

### Generative AI

The brief must name one of Bristol's four categories and give the reason. Three
realistic choices:

- **Category 2, Minimal (the default).** Spelling and grammar help only. Rely on
  the design log and per-student parameters to make other use evident. Hard to
  enforce, and increasingly out of step with how engineers work.
- **Category 3, Selective.** AI permitted for defined purposes, such as help with
  code and language, and declared. Pair it with a secure check of individual
  understanding, following the "two-lane" idea: the recorded explanation, or
  short orals for a random sample and for borderline cases.
- **Category 4, Integral,** for one part of the task. For example, students are
  given, or generate, an AI-proposed controller for their system, then verify it,
  find where it fails, and improve it. That is authentic practice, since engineers
  increasingly check machine-generated designs, and critique of that kind is
  exactly the judgement the 70 boundary asks for.

**Recommendation:** Category 3 for the coursework as a whole, with the theory
link, which carries the 60 and 70 boundaries, secured through the recorded
explanation or sample orals. Consider a Category 4 critique task as the route to
the highest marks.

## Alignment map

To complete once the course is sketched: each ILO, the criteria that evidence
it, and the lecture activities and weekly challenges that rehearse them.

| ILO | Criteria | Rehearsed in |
|---|---|---|
| 4 | Stability and robustness analysis; design linked to theory | To map |
| 5 | Design; verification; design linked to theory | To map |
| 6 | Requirements and modelling; verification | To map |

## Open questions

- **AQ1. The other half.** How is the unit mark split between the halves? Is one
  integrated brief (option C) possible?
- **AQ2. Timing.** When can a checkpoint and a final submission fall, within the
  unit's assessment rules?
- **AQ3. Generative AI.** Which of Bristol's four categories: 2, the default, or
  3, Selective, perhaps with a Category 4 critique task? Is there appetite for
  recorded explanations, or orals for a sample?
- **AQ4. Marking resource.** Are there any second markers? What moderation is
  required?
- **AQ5. The laboratory.** Are Quanser sessions individual or in groups? Can
  laboratory data be assessed? Does every student get rig time before the
  deadline?
- **AQ6. Volume.** Page or word limits, and the University's expectations for the
  amount of coursework in half of a 20-credit unit.
- **AQ7. What exists.** Last year's brief and marking scheme, to build from
  rather than replace.
- **AQ8. Privacy.** Where assessment documents live, given that this repository
  may become public.

## References

- Villarroel, V., Bloxham, S., Bruna, D., Bruna, C. and Herrera-Seda, C. (2018). Authentic assessment: creating a blueprint for course design. *Assessment & Evaluation in Higher Education*, 43(5), 840–854. [doi:10.1080/02602938.2017.1412396](https://doi.org/10.1080/02602938.2017.1412396)
- Hattie, J. and Timperley, H. (2007). The power of feedback. *Review of Educational Research*, 77(1), 81–112. [doi:10.3102/003465430298487](https://doi.org/10.3102/003465430298487)
- Carless, D. and Boud, D. (2018). The development of student feedback literacy: enabling uptake of feedback. *Assessment & Evaluation in Higher Education*, 43(8), 1315–1325. [doi:10.1080/02602938.2018.1463354](https://doi.org/10.1080/02602938.2018.1463354)
- Tai, J., Ajjawi, R., Boud, D., Dawson, P. and Panadero, E. (2018). Developing evaluative judgement: enabling students to make decisions about the quality of work. *Higher Education*, 76(3), 467–481. [doi:10.1007/s10734-017-0220-3](https://doi.org/10.1007/s10734-017-0220-3)
- Boud, D. (2000). Sustainable assessment: rethinking assessment for the learning society. *Studies in Continuing Education*, 22(2), 151–167. [doi:10.1080/713695728](https://doi.org/10.1080/713695728)
- University of Sydney. [The two-lane approach to assessment](https://educational-innovation.sydney.edu.au/teaching@sydney/frequently-asked-questions-about-the-two-lane-approach-to-assessment-in-the-age-of-ai/).
- University of Bristol. [Using AI in assessment](https://www.bristol.ac.uk/bilt/sharing-practice/guides/guidance-on-ai/using-ai-in-assessment/) (staff) and [Using AI in assessments and for studying](https://www.bristol.ac.uk/students/support/academic-advice/using-artificial-intelligence/) (students).
- Constructive alignment and the SOLO taxonomy are referenced in [PEDAGOGY.md](PEDAGOGY.md).
