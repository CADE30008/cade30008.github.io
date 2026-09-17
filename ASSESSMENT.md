# Assessment design: CADE30008, control half

> Drafted with the assistance of generative AI tools.[^checked]

[^checked]: The final versions of all process and assignment documents, and of all student-facing and back-office code, will be fully checked manually.

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
  Checkpoints are expected, but can't be made compulsory.
- **AP4. Generative AI: Bristol Category 3, Selective.** AI is permitted,
  including agentic AI in MATLAB and Simulink, for the purposes the brief lists.
  The brief makes two things clear:
  - AI is **not required** to complete the assessment.
  - Using AI without understanding the fundamental principles and the design
    cycle, and without communicating that understanding, is likely to score
    poorly.
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

## Baseline: the 2025 coursework

The starting point, from last year's released brief:

- **One coursework, two sections,** A (flight dynamics) and B (control), 50 marks
  each and assessed separately. Submitted as a single PDF of up to 20 pages, 10
  per section, plus a single `.zip` of code that runs on a University MATLAB
  computer and outputs all data and figures used.
- **Question-based.** Section B was a sequence of set questions, not a design
  paper.
- **Rubric:** three criteria, benchmarked against the University's level 6
  marking criteria on the 21-point scale: methodological approach and accuracy
  (40%), argument and critique (30%), and explanation and communication (30%).
- **AI:** Category 2, Minimal.
- **Timing:** released in the middle of the term, due near its end.

What carries forward: the single PDF and code `.zip`, 10 pages for Part B, code
that regenerates every result, and level 6 benchmarking. What changes: a design
paper in place of set questions, Category 3 AI use, a rubric built on the design
cycle, and an assessment that builds through the term, which needs the brief
released much earlier (AQ2).

## The shape of Part B

### The task (proposed)

A design brief like the in-lecture builds, but not the same one: the full design
cycle, applied to a system or axis students haven't built in lectures.

| Option | What it is | For | Against |
|---|---|---|---|
| **A. Per-student variant** | A system with parameters generated from each student's number | Each student's numbers are their own and can be checked automatically | Close to the lecture work, so tests transfer (P5) less |
| **B. A new system or axis** | For example, an axis of the Quanser helicopter or a multirotor loop not built in lectures | Tests transfer; can draw on laboratory data | Depends on every student getting rig time in good time |
| **C. Shared with Part A** | Part A models an aircraft (ILOs 1 to 3); Part B designs its flight control (ILOs 4 to 6) | One authentic story across the coursework | Needs agreement with the Part A staff, and couples the two parts |

**Proposal: integrated but separate (C, with A inside it).** Parts A and B stay
separate sections, taught, marked and weighted separately, but tell one story.
Part A characterises an aircraft and delivers a model package in an agreed
format. Part B validates that model against data from a shared virtual flight
test, then designs and flight-tests a controller to fix the deficiencies Part A
identified. A reference model means no student is penalised in Part B for errors
in Part A, and no skill is assessed in both parts. The case study is Tom's
choice: any fixed-wing aircraft works. A proposal note for Tom, with comparable
draft rubrics for both parts, is in `private/assessment/drafts/`.

### What students submit (decided in outline)

1. **The design paper section.** A fixed structure that follows the design cycle:
   requirements, model and assumptions, design, stability and robustness
   analysis, verification, and limitations and transfer. It closes with a short
   account of the key design decisions and how the design changed through the
   term, drawn from the decision log.
2. **The code upload.** Code or a Simulink model that reproduces every number and
   figure in the paper from a single run (P6).

The example submission (AP9) sets the exact format of both, on a system distinct
from the assessed one. Proposal: a multirotor altitude-hold design, one of the
course's three systems, written once the brief and rubric settle, and built with
the same reproducible pipeline as the course materials, so that its numbers and
figures are generated rather than typed. It should be good but not perfect: a
paper in the 60s, whose annotated weaknesses give students something to find
when they mark it against the rubric.

### Through the term: an assessment that builds on itself (proposed)

Three checkpoints, each building on the last, and all feeding the one final
submission. A checkpoint is a point where students are expected, but can't be
required, to submit interim work. Every checkpoint submission gets automated,
individual verification and feedback, and every checkpoint is followed by
general feedback to the cohort. Nothing is marked: grades are awarded only
against the final submission.

| Checkpoint | Contents | Feedback |
|---|---|---|
| **1. Requirements and model** | Requirements, the plant model and its assumptions | Automated checks against each student's parameters; lecturer's cohort notes |
| **2. Design and analysis** | A first design, with its margins and step response | Automated checks; **peer review** (AP8), in which each student reviews two others against rubric criteria |
| **3. Draft paper** | The paper in draft, with code | Automated checks; lecturer's cohort notes on common strengths and gaps |

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

### Marking criteria (draft v1, AP10)

v1 re-scopes criterion 1 to model validation and requirements, since deriving
the model is assessed in Part A, and adds a comparable Part A rubric in the same
shape.

The full draft is in `private/assessment/drafts/`, as a spreadsheet and a
Markdown copy generated from one script. It follows the structure of the
EMATM0055 dissertation workbook: weighted criteria with descriptions and what to
look for, band descriptors as numbered points on the University's level 6 bands,
a mapping of every numbered point to a row of the University's level 6 criteria,
and a bank of example feedback statements for marking at scale.

| Criterion | Weight | Assesses | ILOs |
|---|---|---|---|
| 1. Model validation and requirements | 20% | Requirements; model validation; uncertainty and assumptions | 6, 5, 4 |
| 2. Control design and analysis | 35% | Design method; stability and robustness; verification, including of AI-generated work | 5, 4, 6 |
| 3. Theory, argument and critique | 30% | Explanation through theory; decisions and argument; limitations and transfer | 4, 5, 6 |
| 4. Communication and reproducibility | 15% | Structure and writing; figures and referencing; code and statements | All |

**Why this shape.** Criteria 1, 2 and 4 reward applied design and its evidence,
so sound applied work passes (P10). Criterion 3 rewards understanding, so it
separates the 50s from the 60s and 70s, and it is where output without
understanding, from AI or otherwise, earns little. Illustrative profiles, as
criterion marks and weighted total:

| Profile | 1 | 2 | 3 | 4 | Total |
|---|---|---|---|---|---|
| Sound design, explanation only descriptive | 55 | 55 | 45 | 55 | 52 |
| AI-generated design, unverified and little understood | 50 | 45 | 30 | 50 | 42 |
| Good design, theory well linked | 62 | 65 | 68 | 62 | 65 |
| First-class | 72 | 75 | 75 | 68 | 73 |

SOLO levels sit alongside the University bands: unistructural at 40 to 49,
multistructural at 50 to 59, relational at 60 to 69, and extended abstract at 70
and above.

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
7. **Detection where it exists.** Turnitin on the paper: Bristol uses its
   similarity report and AI-writing indicator as flags for a person to weigh.
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

## Individual inputs, marking and feedback (proposed)

The full proposal is in `private/assessment/drafts/`, as Markdown and PDF. In
short:

- **Individual inputs** are generated deterministically from each username and a
  cohort secret, and checked across the whole cohort for solvability and similar
  difficulty before release. Students reach them through one MATLAB toolbox: their
  inputs, the virtual flight test, a formative self-check, and submission
  validation. Everything it returns carries a fingerprint of the student's variant.
- **A submission contract** makes checking automatic: the paper, a `run_all.m`
  that runs unattended, a results file to a fixed schema, and numbered figures.
  Students can run the same checks before they submit.
- **Formative and assessment pipelines,** both code-assisted, with no generative
  AI. Formative pipelines run on checkpoint submissions and return individual
  reports and cohort statistics. The assessment pipeline runs on the final
  submission and supports marking. Between them:
  intake, reproduction in an isolated environment, independent recomputation,
  cross-checks between the paper and its results, integrity signals, a marker
  sheet, and release. Automation finds facts, and suggests bands only for
  evidence-based rubric points. Criterion B3 and every other judgement stays with
  the marker. Grades are awarded only against the summative submission.
  Formative pipelines can support an integrity review by showing how a design
  developed, but never lower a mark by themselves, and not submitting at a
  checkpoint is never a flag.
- **Feedback** is assembled from structured marking records: comment codes, a few
  sentences from the marker, individual PDF reports, a gradebook upload, and
  cohort notes drawn from the marking data.
- **LLM support is not used in marking in 2026/27** (decided). Instead, subject
  to approval, it is trialled on already-marked, pseudonymised work after the
  relevant exam boards, so the trial can't affect any student's mark or feedback.
  Students are told in the brief before they submit. The trial tests evidence
  location, claim extraction, feedback drafting, consistency prompts and cohort
  themes against the real marking records, and decides whether any of it is
  adopted in later years. It never awards or suggests bands, and never judges
  whether text was written by AI.
- **Policy.** At Bristol, summative coursework with formative feedback on drafts is
  exempt from anonymous first marking, but moderation should still be anonymous,
  so the pipeline uses pseudonymous IDs. Moderation samples at least eight scripts
  or 10 per cent. Live marking uses no generative AI. Bristol uses Turnitin's
  similarity report and AI-writing indicator as flags for a person to weigh. The
  trial on marked work needs agreement from the School and Faculty Education
  Directors and the central AI team, and students must be told about it before
  they submit.

## Where this stands, 17 September 2026

Assessment design is parked here while curriculum and learning design are worked
on. The state of it:

**Out for comment.** Three v0.1 documents were sent to unit colleagues on 17
September: the Part B brief, *Parts A and B as one story*, and *Individual
inputs, code-assisted marking and efficient feedback*. Sources are in
`private/assessment/drafts/`. They are consistent with each other; a scripted
check covers criterion names, paper sections, checkpoint names, toolbox
functions, the AI category, marks and the page limit. Nothing moves until Tom
and colleagues reply (AQ1).

**Decided and not to be reopened without reason.** Category 3 Selective; 50
marks and roughly 10 pages for Part B; integrated-but-separate Parts A and B
with a reference model, so neither part's mark depends on the other; per-student
variants; the submission contract; no generative AI in live marking in 2026/27;
checkpoints never compulsory and never a flag.

**Outstanding, in the order they will bite.**

1. **Tom's answers (AQ1),** which unblock the case study, the model package and
   the shared virtual flight test. Everything else waits on these.
2. **Dates (AQ2).** Part B's design problem must be released in week 1 or 2 for
   the term-long build to work, so this is needed before teaching starts.
3. **Checkpoint incentives (AQ13),** below. The current brief wording is usable
   but is the weakest part of the draft.
4. **Placeholders in the brief (AQ14),** below.
5. **Build work.** The variant generator, reference model, virtual flight test
   and `cade30008` toolbox, tested on University MATLAB machines. Independent of
   the case study, so it can start once the interfaces are agreed.
6. **Approvals.** Running student code at scale (AQ10), the LLM trial (AQ12),
   and Blackboard and MATLAB Grader integrations (AQ8, and the licence
   administrator in [PEDAGOGY.md](PEDAGOGY.md)).

Curriculum work touches assessment at two points, and should not drift from it:
the weekly challenge (P16) is the same machinery as the formative pipelines, and
the in-lecture build (P8) is what P10 says the coursework must mirror.

## Open questions

- **AQ13. What makes a checkpoint worth submitting.** Checkpoints are not
  compulsory, so they must pay. Cohort-level feedback alone permits loafing, and
  non-submission must never read as suspicion. Ideas raised but not adopted:
  hold-out validation data or unseen flight-test conditions released only through
  a checkpoint report; an indicative band without a mark; a personal rather than
  cohort report; limiting what the local `check` returns so the checkpoint gives
  something the student cannot get alone. Each needs testing against AP-level
  fairness for students who cannot submit on the day. The brief's current wording
  says checkpoint work "may be looked at if questions arise", which is honest but
  sits awkwardly beside "not submitting is never held against you".
- **AQ14. Placeholders in the Part B brief.** The aircraft and control task, the
  criterion weights, the page limit, the `run_all.m` run-time limit, the
  permitted AI purposes, and the opt-out wording for the LLM trial.
- **AQ1. Part A.** Taught and assessed by Tom. The integrated-but-separate
  proposal puts these questions to him: the case study; whether Part A produces a
  linear model at trim; Part A's deficiencies as Part B's requirements; a
  modelling checkpoint in week 4 or 5; per-student variants shared by both parts;
  and using the virtual flight test in Part A.
- **AQ2. Timing.** The release date, the final deadline, and dates for the three
  checkpoints. In 2025 the brief was released mid-term; an assessment that builds
  from early lectures needs Part B's brief, or at least its design problem,
  released in the first week or two.
- **AQ3. Generative AI category.** Decided: Category 3, Selective (AP4). Still
  to write: the brief's list of permitted purposes.
- **AQ4. Marking resource.** Any second markers, and the moderation required.
- **AQ5. The laboratory.** In 2025 the Quanser lab was formative and
  unsupervised: system identification and PID control of the elevation axis, in
  pairs, over two one-hour sessions on four stations, with support ending at
  coursework release. Its handout said the summative assessment may build on it.
  Each station's dynamics differ slightly, which gives natural variation between
  identified models. A second set of materials covers state feedback and LQR on
  elevation and travel. Open: whether this year's two two-hour sessions stay in
  pairs, and whether Part B uses each student's own laboratory data, which would
  need individual analysis of data gathered as a pair.
- **AQ6. Volume.** Likely 10 pages for Part B, as in 2025. Whether the
  statements and references sit outside that limit.
- **AQ7. Existing material.** Received in `private/assessment/`: the 2025 brief
  and rubric, the EMATM0055 dissertation rubric workbook, and the University's
  level 6 marking criteria. A draft Part B brief is in
  `private/assessment/drafts/`.
- **AQ8. Blackboard.** Confirm that Bristol's courses use Ultra course view,
  with journals and assignment peer review available. The Original course view
  retires at the end of 2026.

- **AQ9. Part A rubric.** A comparable Part A rubric is proposed; Tom may prefer
  a more granular, criteria-based one. Also whether the two parts' briefs are
  released together.
- **AQ10. Running student code.** Where the pipeline can run untrusted student
  code at scale: a dedicated University machine or virtual machine with MATLAB,
  no network access, and time limits.
- **AQ11. Returning feedback.** Bristol's Blackboard set-up permits bulk upload of
  feedback files (confirmed), alongside marks and text feedback by gradebook
  upload. Still open: how submissions, including checkpoint submissions, appear in
  a bulk download.
- **AQ12. The LLM trial.** Approval from the School and Faculty Education
  Directors and the central AI team; whether a notice with an opt-out is enough
  or consent is needed; and whether to seek ethics approval now, in case the
  results are written up. All must be settled before this year's submission.
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
