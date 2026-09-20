# Blackboard build sheet

What to build in the unit's Blackboard Ultra course, and how to check it.
Lecturer-facing. Build it by hand from this list, then run the check at the end.

`npm run live` checks every `https://cade30008.github.io/…` link on this page
against the live site, and fails if one doesn't exist. So when a page moves or is
unpublished, this sheet is flagged, not the students.

**Status: before week 1 only.** Later weeks are added here as each is
published, following the pattern under "Each week, from week 1".

## How the course is laid out

- **Progress tracking on.** In the course settings, turn on progress tracking.
  Students then see a circle beside each item, which fills when they open it,
  submit it, or tick it themselves; you can see who has done what per item.
- **One learning module per week**, in order: *Before week 1*, *Week 1*, …
  *Week 11*. A learning module keeps a week's items together and in sequence,
  and shows the student's progress through it. Don't force sequence: students
  should be able to go back and forth.
- **Release each module when its week is published** on the site, not before.
- **Links go to the live site**, `https://cade30008.github.io`, which is the
  single source for content. Blackboard holds only what has to be there:
  assignments, tests, the journal, and anything specific to this cohort.

## Before week 1

Learning module title: **Before week 1**

Module description, to paste:

>  **One thing to do before Tuesday: check your device runs the course code.**
> It takes a few minutes, and it means the first lecture goes on control rather
> than on installing software. Bring a laptop if you have one.
>
> Everything else here — the Onramp courses and the diagnostic quiz — is useful
> whenever you get to it. Do it now if you have time, or alongside the unit as
> each part becomes relevant. It is not a gate, and week 1 assumes none of it.
> None of it contributes to your grade: it is here so you can find your own
> gaps, and so I know where to spend time in the first weeks.

Items, in this order:

| # | Type | Title | Content or settings |
|---|---|---|---|
| 1 | Link | **Start here: Preparing for Control**. | `https://cade30008.github.io/preparing/` — Description: "What to install, how to check your device, and what to do before week 1.". |
| 2 | Link | **Check your device** | `https://cade30008.github.io/preparing/#check` — Description: "Run the check in your browser or on your computer. It should report a phase margin of 43.21°.". |
| 3 | Text | **About the Onramp courses** | See the wording below. Goes *above* the three links. |
| 4 | Link | **Control Design Onramp with Simulink** — *recommended* | `https://matlabacademy.mathworks.com/details/control-design-onramp-with-simulink/controls` — Description: "30 minutes, and the one most worth doing. Designing a feedback controller in Simulink.". |
| 5 | Link | **MATLAB Onramp** — *if you want the practice* | `https://matlabacademy.mathworks.com/details/matlab-onramp/gettingstarted` — Description: "2 hours. Sign in with your University email address.". |
| 6 | Link | **Simulink Onramp** — *if you want the practice* | `https://matlabacademy.mathworks.com/details/simulink-onramp/simulink` — Description: "2 hours. Blocks, and simulating models built from them.". |
| 7 | Assignment | **Onramp certificates** | See below |
| 8 | Numbas activity | **Diagnostic quiz** | See below. Questions in `diagnostics/prerequisites.md` |
| 9 | Link | **How this unit uses AI**. | `https://cade30008.github.io/ai/` — Description: "What you may and may not use AI for, and why.". |

### Item 3: About the Onramp courses (text)

Most of this cohort has already used MATLAB and Simulink for control work, so
the three courses are not equally useful. Say so, rather than listing three
things of which two are revision.

> **Text, to paste:** "Most of you have used MATLAB and Simulink before,
> including for control. So of the three Onramp courses, the one worth your
> time is **Control Design Onramp with Simulink** — about 30 minutes, and it
> covers designing a feedback controller, which is what we build on.
>
> The MATLAB and Simulink Onramps are each about two hours. If you've done them
> before, you don't need to repeat them. If you haven't, or you'd like the
> practice, they're good and they're free.
>
> **Already done any of these, in this unit or another?** Upload that
> certificate — an older version is fine. Nothing here contributes to your
> grade; it tells me how the cohort is placed so I can pitch the software side
> of each session accordingly."

### Item 7: Onramp certificates (assignment)

- **Instructions, to paste:** "If you finish an Onramp course, upload its
  certificate here — and if you already hold one from a previous year or
  another unit, upload that: an older version of the course counts. MATLAB Academy gives you one as a PDF when you finish.
  There's no deadline and it isn't marked — it tells me how the cohort is
  placed, so I can pitch the software side of each session accordingly. Partial
  is fine and useful: upload one, or two, as you go."
- **Due:** no due date. Setting one implies a gate that this isn't.
- **Attempts:** unlimited, so students can add certificates as they finish.
- **Grading:** complete/incomplete, or not counted towards the grade. It must
  not look as though it counts — it is formative (ASSESSMENT.md, "Formative and
  summative").
- **Files:** allow PDF and image files.

*Next year:* use the integrated MathWorks Onramp courses through Blackboard's
LTI link instead, which report completion automatically, once IT have set up
the integration (PEDAGOGY.md, "Preparation before week 1").

### Item 8: Diagnostic quiz (Numbas)

- **Description, to paste:** "Ten questions on the mathematics and control this
  unit builds on, about 20 minutes. It's formative: it doesn't contribute to
  your grade, but it does tell you where you're solid and where to brush up, and
  tells me what to spend time on in the first weeks. Do it on your own and
  without looking things up. You'll get feedback on every question."
- **Upload the ready-made quiz.** `npm run numbas` writes
  `diagnostics/prerequisites.exam` — **the `.exam`, not the `.md`
  beside it**, which is the readable draft and will be rejected with "Didn't
  parse all input at line 1". It is built from the questions in
  `prerequisites.yaml`. Upload that to the Numbas editor, check it there —
  [numbas.mathcentre.ac.uk](https://numbas.mathcentre.ac.uk) is a good place to
  try it — then publish it and add it through the Numbas link in Blackboard,
  whose integration is active. If the editor won't take the file, the question
  list in `prerequisites.md` is the same content to type in by hand.
- **Settings:** one attempt; no time limit; feedback and the correct answer
  after each question; not counted towards the grade, or the column hidden.
- **No randomisation** (AP11): every student gets the same questions, and they
  may work through them together.
- **Questions:** build from `diagnostics/prerequisites.md`, with its
  feedback text and numerical tolerances. Number entry for the numeric
  questions, multiple choice for the rest.
- **Before the week 2 lecture:** read the results against the table at the end
  of that file.

## Each week, from week 1

When a week is published on the site, add a learning module *Week n: title*
with, in this order:

| Type | Title | Content |
|---|---|---|
| Link | **Handout** | the week's page on the live site. |
| Link | **Slides** | the deck on the live site. |
| Link | **Example sheet** | on the live site. |
| Numbas activity or link | **This week's challenge** | Numbas, which is integrated; or MATLAB Grader for code, once its integration is set up. |
| Link | **Solutions** | on the live site; release when the week's sheet is due, if held back. |
| Text | **Coursework this week** | the step for the week from `curriculum/term.yaml`, pasted. |

A week that hands out files or takes work in also needs its two **MATLAB
Drive** links, with these titles, in this order, every week — so students learn
where to look once:

| Item | Type | Points at |
|---|---|---|
| **Files for this session** | Link | that week's `data/` view-only link. |
| **Submit your work** | Link | that week's `submit/` edit link. |

The layout, the sharing rules and how to test the links are in
[matlab-drive.md](matlab-drive.md). **Test every link from a student account,
never signed in as yourself** — as the owner every link works, so testing as
yourself tells you nothing. Week 1 needs both; a week with no hand-out and no
submission needs neither.

## Checking it

Run this after building a module, and again whenever a week is added. Use
**Student preview**, so you see what a student sees.

- [ ] Progress tracking is on, and a circle shows beside every item.
- [ ] Each link opens the right page, on `cade30008.github.io`, not the local
      preview.
- [ ] Every MATLAB Drive link opens, and the `submit/` one actually accepts a
      file. Upload one from the student account, confirm it lands, delete it.
- [ ] Opening a link fills its circle, or ticking it does.
- [ ] The assignment accepts a PDF upload, and allows more than one attempt.
- [ ] The Numbas quiz opens from Blackboard, submits once, and gives feedback
      on each question.
- [ ] Neither the assignment nor the quiz counts towards the student's grade,
      and neither is described to students as "marked".
- [ ] The module is released, or scheduled to release, when intended.
- [ ] Nothing in Blackboard duplicates content that lives on the site.

Record the check here:

| Module | Checked by | Date | Notes |
|---|---|---|---|
| Before week 1 | | | |
