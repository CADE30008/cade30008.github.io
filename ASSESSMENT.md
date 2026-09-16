# Assessment design: CADE30008, control half

This file records how this half of the unit is assessed, and why. The fixed
principles below are rigid: changing one takes a University change cycle or two,
at 10 to 12 months each. Everything after them is design within those limits,
and is marked as decided, proposed or open.

> **Keep assessment material private.** This file holds design reasoning only.
> Briefs, marking schemes with model answers, per-student parameters and last
> year's materials live in `private/`, which git ignores. Never copy them into
> a tracked file.

## Fixed principles

IDs are stable, as in [PEDAGOGY.md](PEDAGOGY.md).

- **AP1. One coursework, in two parts.** This half is **Part B** of a single
  coursework submission for the unit. Part B is a **design paper** section plus a
  **code upload**.
- **AP2. One summative point.** No orals, and no formal assessments during the
  term. The final submission is the only thing marked.
- **AP3. Formative support throughout.** Formative submission checkpoints,
  one-to-one peer feedback, and top-level notes from the lecturer to the cohort.
- **AP4. Generative AI is permitted,** including agentic AI in MATLAB and
  Simulink. The brief names the Bristol category (AQ3).
- **AP5. Collaboration has clear boundaries.** The brief states what students may
  work on together and what is forbidden.
- **AP6. Self-checks, with participation visible to the lecturer.** Numbas and
  MATLAB Grader self-checks (P16) give students feedback. Their completion data
  is for the lecturer's oversight only, and carries no marks.
- **AP7. A decision log that builds through the term,** kept in Blackboard, and
  feeding the final submission.
- **AP8. A peer feedback activity** on a formative checkpoint.
- **AP9. An example submission** shows the format students replicate.
- **AP10. The rubric is developed** from last year's, the lecturer's preferred
  examples, and University guidance.

## What is fixed by the unit

- **100 per cent individual coursework** across ILOs 1 to 6. Part B assesses
  **ILOs 4, 5 and 6**: stability and robustness analysis, design and
  characterisation of controllers, and applying control to aircraft performance
  and operations.
- **Aims for the marks** (P10): a pass, roughly 40 to 60, evidences solid applied
  control design; 60 and above links that design convincingly to theory; a first,
  70 and above, shows the depth to progress to advanced study.
- **About 200 students.** Assume no teaching assistants.
- **Generative AI categories.** Bristol sets four: 1, Prohibited; 2, Minimal,
  the default; 3, Selective, for defined purposes; and 4, Integral, where
  students critique and improve AI output. The brief must name the category,
  explain why, and have marking criteria that fit it.

## The shape of Part B

### The task (proposed)

A design brief like the in-lecture builds, but not the same one: the full design
cycle, applied to a system or axis students haven't built in lectures.

| Option | What it is | For | Against |
|---|---|---|---|
| **A. Per-student variant** | A system with parameters generated from each student's number | Each student's numbers are their own and can be checked automatically | Close to the lecture work, so tests transfer (P5) less |
| **B. A new system or axis** | For example, an axis of the Quanser helicopter or a multirotor loop not built in lectures | Tests transfer; can draw on laboratory data | Depends on every student getting rig time in good time |
| **C. Shared with Part A** | Part A models an aircraft (ILOs 1 to 3); Part B designs its flight control (ILOs 4 to 6) | One authentic story across the coursework | Needs agreement with the Part A staff, and couples the two parts |

**Proposal:** per-student parameters (A) in any case, within B or C depending on
AQ1 and AQ5.

### What students submit (decided in outline)

1. **The design paper section.** A fixed structure that follows the design cycle:
   requirements, model and assumptions, design, stability and robustness
   analysis, verification, and limitations and transfer. It closes with a short
   account of the key design decisions and how the design changed through the
   term, drawn from the decision log.
2. **The code upload.** Code or a Simulink model that reproduces every number and
   figure in the paper from a single run (P6).

The example submission (AP9) sets the exact format of both, on a system distinct
from the assessed one.

### Through the term: an assessment that builds on itself (proposed)

Three formative checkpoints, each building on the last, and all feeding the one
final submission:

| Checkpoint | Contents | Feedback |
|---|---|---|
| **1. Requirements and model** | Requirements, the plant model and its assumptions | Automated checks against each student's parameters; lecturer's cohort notes |
| **2. Design and analysis** | A first design, with its margins and step response | **Peer review** (AP8): each student reviews two others against rubric criteria |
| **3. Draft paper** | The paper in draft, with code | Lecturer's cohort notes on common strengths and gaps |

Alongside them:

- **The decision log (AP7).** A Blackboard Ultra **journal**, private between
  each student and the lecturer, left ungraded. One short entry per decision:
  what was decided, the alternatives, the evidence, and any AI assistance.
- **Weekly self-checks (AP6).** Numbas for mathematics and concepts, MATLAB
  Grader for code, each rehearsing that week's build.

Blackboard Ultra supports what this needs: ungraded journals, and assignments
with built-in peer review, which distributes submissions randomly and
anonymously, with separate submission and review deadlines. FeedbackFruits,
which Bristol also supports, is the alternative for peer review.

### Marking criteria (to develop, AP10)

A starting point for the rubric work, to be reconciled with last year's rubric,
the preferred examples and University guidance.

| Criterion | ILO | Carries the boundary at |
|---|---|---|
| Requirements and modelling | 6 | 40 |
| Design | 5 | 40 |
| Stability and robustness analysis | 4 | 50 |
| Verification, including of any AI-generated work | 5, 6 | 50 |
| Design linked to theory | 4, 5 | **60** |
| Limitations, assumptions and transfer | 4, 5, 6 | **70** |
| Communication and reproducibility | all | all |

| Mark | In short | SOLO |
|---|---|---|
| Below 40 | The design doesn't work, isn't evidenced, or misapplies the procedure | Prestructural |
| 40 to 49 | A working design with gaps in requirements, verification or evidence; little justification | Unistructural |
| 50 to 59 | A sound design that meets its requirements and is verified; the procedure described correctly, but justification is descriptive | Multistructural |
| 60 to 69 | Design choices explained through theory, with trade-offs made explicit | Relational |
| 70 to 79 | Assumptions and limits analysed critically; results generalised beyond the case; alternatives compared | Extended abstract |
| 80 and above | An original extension with real depth, at a level suited to advanced study or research | Extended abstract |

## Assuring the work is the student's own (proposed)

Without orals or in-term assessment, no single measure can guarantee authorship.
The aim is assurance by design: several reasonable measures that make honest work
the easiest route, make misconduct visible, and reward the judgement that is
hardest to outsource. Assessment security research is clear that no design is
immune, so these concentrate on what matters most.

1. **Each student's task is their own.** Per-student parameters, generated from
   the student number, so a copied design gives visibly wrong numbers. Set
   requirements with genuine trade-offs, so that valid designs differ between
   students.
2. **The code must reproduce the paper.** A single run script regenerates every
   number and figure. All submissions are run in batch, their results compared
   with the paper and with each student's expected values, and mismatches flagged
   for the marker.
3. **Process is visible.** The dated decision log and the three checkpoints show
   how a design developed. The paper's closing section must trace the design's
   changes to the log and to the peer and cohort feedback. The brief says, in
   advance, that the log may be consulted if a concern arises.
4. **AI use is part of the evidence.** Students state what AI they used and for
   what, and, for agentic workflows, summarise what the agent did. The rubric
   rewards independent verification of AI-produced models, code and claims:
   unverified output scores poorly whoever produced it. That also matches good
   engineering practice.
5. **Collaboration boundaries are explicit,** and every submission carries a
   collaboration statement naming who the student discussed Part B with, and
   about what. See the table below.
6. **Understanding shows in writing.** The theory criteria, which carry the 60
   and 70 boundaries, ask students to explain their own design's behaviour: why
   *this* margin gave *this* overshoot, what fails if an assumption breaks. Those
   explanations are specific to the student's numbers.
7. **Detection where it exists.** Turnitin on the paper, which Bristol supports.
   Common code-similarity tools don't clearly support MATLAB; per-student
   parameters and the reproduction check do more for code.
8. **Students understand quality before they submit.** In a lecture activity,
   students mark the example submission against the rubric. Knowing what good
   work looks like reduces confusion, and confusion drives some misconduct.
9. **Early warning, not surveillance.** Self-check completion and journal
   activity show who may be struggling, so support can be offered early. The
   brief says how this data is used.
10. **A declaration** at submission, covering authorship, AI use and
    collaboration.

### Collaboration boundaries (proposed)

| You may | You may not |
|---|---|
| Discuss concepts, lectures, example sheets and the methods the brief asks for | Share your design, parameter values, code or text for Part B |
| Help each other get software working, and debug lecture and starter code | Use another student's code, figures or text, or let them use yours |
| Take part in the structured peer review, and act on the feedback | Work on another student's variant |
| Use AI tools as the brief permits, and declare them | Submit AI output you haven't verified, and can't explain in your paper |

If in doubt, name it in the collaboration statement. Acknowledged discussion is
never misconduct.

## Open questions

- **AQ1. Part A.** What Part A covers, how marks split between Parts A and B, and
  whether the two parts could share a system (option C).
- **AQ2. Timing.** The final deadline, and dates for the three checkpoints.
- **AQ3. Generative AI category.** Category 3, Selective, with a broad list of
  permitted purposes including agentic MATLAB and Simulink workflows; or
  Category 4, Integral, if the brief makes AI-assisted model-based design and its
  critique part of the task.
- **AQ4. Marking resource.** Any second markers, and the moderation required.
- **AQ5. The laboratory.** Whether Quanser sessions are individual or in groups,
  and whether laboratory data can feature in Part B.
- **AQ6. Volume.** Page limit for the design paper section, and the format of the
  code upload.
- **AQ7. Existing material.** Last year's brief and rubric, the preferred rubric
  examples, and University guidance, to be uploaded to `private/`.
- **AQ8. Blackboard.** Confirm that Bristol's courses use Ultra course view,
  with journals and assignment peer review available. The Original course view
  retires at the end of 2026.

## References

- Villarroel, V., Bloxham, S., Bruna, D., Bruna, C. and Herrera-Seda, C. (2018). Authentic assessment: creating a blueprint for course design. *Assessment & Evaluation in Higher Education*, 43(5), 840–854. [doi:10.1080/02602938.2017.1412396](https://doi.org/10.1080/02602938.2017.1412396)
- Hattie, J. and Timperley, H. (2007). The power of feedback. *Review of Educational Research*, 77(1), 81–112. [doi:10.3102/003465430298487](https://doi.org/10.3102/003465430298487)
- Carless, D. and Boud, D. (2018). The development of student feedback literacy: enabling uptake of feedback. *Assessment & Evaluation in Higher Education*, 43(8), 1315–1325. [doi:10.1080/02602938.2018.1463354](https://doi.org/10.1080/02602938.2018.1463354)
- Tai, J., Ajjawi, R., Boud, D., Dawson, P. and Panadero, E. (2018). Developing evaluative judgement: enabling students to make decisions about the quality of work. *Higher Education*, 76(3), 467–481. [doi:10.1007/s10734-017-0220-3](https://doi.org/10.1007/s10734-017-0220-3)
- Boud, D. (2000). Sustainable assessment: rethinking assessment for the learning society. *Studies in Continuing Education*, 22(2), 151–167. [doi:10.1080/713695728](https://doi.org/10.1080/713695728)
- Dawson, P. (2020). *Defending Assessment Security in a Digital World: Preventing E-Cheating and Supporting Academic Integrity in Higher Education*. Routledge. [doi:10.4324/9780429324178](https://doi.org/10.4324/9780429324178)
- Bretag, T., Harper, R., Burton, M., Ellis, C., Newton, P., van Haeringen, K., Saddiqui, S. and Rozenberg, P. (2019). Contract cheating and assessment design: exploring the relationship. *Assessment & Evaluation in Higher Education*, 44(5), 676–691. [doi:10.1080/02602938.2018.1527892](https://doi.org/10.1080/02602938.2018.1527892)
- University of Sydney. [The two-lane approach to assessment](https://educational-innovation.sydney.edu.au/teaching@sydney/frequently-asked-questions-about-the-two-lane-approach-to-assessment-in-the-age-of-ai/).
- University of Bristol. [Using AI in assessment](https://www.bristol.ac.uk/bilt/sharing-practice/guides/guidance-on-ai/using-ai-in-assessment/) (staff) and [Using AI in assessments and for studying](https://www.bristol.ac.uk/students/support/academic-advice/using-artificial-intelligence/) (students).
- Blackboard. [Grade journals](https://help.blackboard.com/Learn/Instructor/Ultra/Interact/Journals/Grade_Journals) and [Peer review for qualitative peer assessments](https://help.blackboard.com/Learn/Instructor/Ultra/Assignments/Self_and_Peer_Assessment/Peer_Review_for_Qualitative_Peer_Assessments).
- Constructive alignment and the SOLO taxonomy are referenced in [PEDAGOGY.md](PEDAGOGY.md).
