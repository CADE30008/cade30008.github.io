---
title: "Week 1: The design cycle, end to end"
description: "Placeholder. Scoped in curriculum/weeks.yaml; content not yet written."
lesson: w01-design-cycle
order: 1
duration: 2 x 50 min
status: draft
---

# Week 1: The design cycle, end to end

<div class="lesson-links" markdown>
[Slides](../slides/w01-design-cycle/index.html)
[Example sheet](example-sheet.md)
[Solutions](solutions.md)
</div>

!!! warning "Not yet written"
    This week is scoped but not written. Its title, learning outcomes and
    place in the unit are set; the sections below are placeholders, there so
    that the navigation, the slide deck and the example sheet exist in their
    final shape.

One paragraph saying what this lecture does, and how it follows from the last one.

<!-- outcomes:start -->
!!! abstract "Learning outcomes"
    By the end of this week you should be able to:

    - describe the control design cycle, and say where in it a given design activity sits;
    - identify a second-order model from a measured response, by reading its damping ratio, natural frequency and gain;
    - tune a PID controller in simulation to meet a stated requirement;
    - explain why a design that meets its requirement in simulation may not meet it on hardware.
<!-- outcomes:end -->

## Where we are {#recap}

What the student already knows that this lecture builds on, and where it came from.

## First idea {#idea-one}

The first main idea, developed from what the recap established.

## Second idea {#idea-two}

The second main idea, and how it changes the picture.

## Worked example {#worked-example}

A worked example carrying the ideas above through to numbers. Numbers belong in
a script under `models/`, not typed in here.

## Summary {#summary}

The few things to take away.

## How the unit runs {#schedule}

Eleven weeks of content, in three acts, alongside a coursework that builds
through the term and an open-access laboratory. Lectures are on Tuesdays. Week
5 is a guest lecture. Week 6 is consolidation week: there is no lecture, and
instead a set of recommended activities to make weeks 1 to 4 solid before week 7
builds on them.

<figure markdown="span">
  ![The control half week by week: what happens each week, the three acts, the coursework checkpoints and deadline, and the laboratory window](figures/term-map.svg){ width="100%" }
</figure>

<!-- schedule:start -->
*2026/27. Lectures are on Tuesdays.*

| Week | This week | Coursework |
|---|---|---|
| 1 | [The design cycle, end to end](../w01-design-cycle/index.md) | Brief released |
| 2 | [Requirements and models you can trust](../w02-requirements-and-models/index.md) |  |
| 3 | [PID, properly](../w03-pid-control/index.md) |  |
| 4 | [Stability and margins](../w04-stability-margins/index.md) | Checkpoint 1 |
| 5 | [Guest lecture](../w05-guest-lecture/index.md) |  |
| 6 | [Consolidation week](../w06-consolidation/index.md): no lecture; recommended activities. |  |
| 7 | [Robustness and trade-offs](../w07-robustness/index.md) |  |
| 8 | [Loop shaping](../w08-loop-shaping/index.md) | Checkpoint 2 |
| 9 | [Flight control architecture](../w09-flight-control-architecture/index.md) | Checkpoint 3 |
| 10 | [State space and state feedback](../w10-state-space/index.md) |  |
| 11 | [What comes next](../w11-beyond-this-course/index.md); then coursework Q&A. | **Due Thursday of week 11** |
| 12 | *Revision week* |  |

The Quanser laboratory is open access from week 1 to week 6: you choose when to go.
<!-- schedule:end -->

## How you're assessed {#assessment}

One piece of work carries your grade for this half of the unit: **the
coursework, due on the Thursday of week 11**. That is the *summative*
assessment, and it comes back with individual written feedback against the
marking rubric.

Everything else is *formative*. It doesn't contribute to your grade directly —
**but it is how the coursework gets built**, so "directly" is doing a lot of
work in that sentence.

| Through the term | Contributes to your grade | What you get back |
|---|---|---|
| The diagnostic, before week 1 | Not directly. | Automatic feedback on each question, straight away. |
| The weekly challenge | Not directly. | The same, each week. |
| Example sheets | Not directly. | Worked solutions, and the next session. |
| The work you do in each session | Not directly. | Comments in the room, from me and from each other. |
| The Quanser laboratory | Your measurements go into the coursework. | Your own data, and help in the room. |
| Checkpoints, weeks 4, 8 and 9 | They become the paper. | Automatic checks on what you submit, notes to the whole cohort, and peer review at checkpoint 2. |
| **Coursework, week 11** | **This is the grade.** | Your mark, with written feedback against the rubric. |

Each checkpoint is a draft of part of the final paper, and your decision log
becomes its last section. Do it as you go and you arrive at week 11 with most of
a submission, already checked. Skip it and you write the whole thing in the last
fortnight, alone, with no feedback — which is the same work, done harder.

Nothing formative is randomised: everyone gets the same questions, and you're
welcome to work through them sitting next to each other.

## The textbook {#textbook}

<!-- textbook:start -->
You don't have to buy a book. Each week's handout is the authoritative
version of what you need, and it stands on its own. One is worth knowing
about, though: **Dorf and Bishop's *Modern Control Systems***. Use it **for additional
study and consolidation** — a second explanation when the handout's doesn't
land, and more worked examples — not as a substitute for the handout.

!!! tip "Share the library copies"
    There are **20 print copies and 14 eBook licences** between
    about 190 of you, so the book only works if everyone takes their turn.

    - Reading an eBook online locks that copy while you have it open.
    - Downloading the whole book locks a copy for 24 hours.
    - Downloading a PDF chapter locks nothing, but is capped at 56 pages.

    So: **download the chapter you want and get out**. Don't leave an eBook
    open in a tab overnight, and don't download the whole book unless you
    really need all of it — that takes a copy away from someone else for a
    day. If everything is out, come back in an hour; it usually isn't for long.

Which sections go with which week, and what the library holds, are on
[The textbook](../reading.md).
<!-- textbook:end -->

## Your week {#workload}

This half of the unit is planned around a steady week, not a heroic one: six
hours, every week from 1 to 11.

<figure markdown="span">
  ![Your week: two hours in the lecture, two on your own and two on the coursework, six in total; the two independent hours are 45 minutes on the handout and the week's challenge, an hour on the example sheet and 15 minutes on next week's case. Week 6 replaces the lecture and independent hours with four hours of recommended activities. On top of all of it, four hours in the Quanser laboratory at times you choose](figures/your-week.svg){ width="100%" }
</figure>

<!-- workload:start -->
| In a week with a lecture | Hours |
|---|---|
| The lecture, on Tuesday | 2 |
| Independent learning: go back over the handout and do the week's challenge (45 min), work the example sheet (1 h), and look at next week's case (15 min). | 2 |
| Coursework | 2 |
| **Total** | **6** |

**Consolidation week** has no lecture. Instead, 4 hours of recommended activities that cement what you've done so far, plus the usual 2 hours of coursework.

Why six? A full-time working week is about 35 hours, and you take three units at once, so each gets just under 12 hours a week — and this is half of one.

On top of that, **4 hours in the Quanser laboratory**, at times you choose between week 1 and week 6. Over the term that comes to about 70 hours: 20 in lectures, 20 of independent learning, 4 of consolidation, 22 of coursework and 4 in the laboratory.
<!-- workload:end -->

**Do the coursework in the week, not at the end.** The coursework is set up to
build week by week alongside the lectures: each week's step uses what that
week's lecture has just covered, while it's fresh, and the checkpoints give you
feedback while it can still change your design. Many students leave coursework
until the last few weeks of term. It is possible, but it means learning the
material twice — once in the lecture, and again, alone, under deadline
pressure — and it throws away the feedback. Two hours a week, starting in week
1, is the plan that works.

## AI in this course {#ai}

Three ideas shape how I think about generative AI, and large language models in
particular.

**AI rewards expertise.** Language models let anyone produce seemingly passable
work, but much of it falls down against an expert eye — and, in engineering,
against the real world. Knowing the subject is what lets you ask the precise
question, notice the flaw in a confident answer, and refuse a plausible wrong
turn. Sean Goedecke makes the case[^goedecke] with Terence Tao's conversation
with ChatGPT about the Jacobian conjecture, on 20 July 2026:[^tao-chat] the value
came from Tao's judgement at every step, not from clever prompting. So the
fundamentals in this unit are what will make you good with AI in control
engineering, not what AI makes unnecessary.

!!! danger ""
    A design in a domain you don't understand, produced by a tool you don't
    understand and can't check, runs the risk of being a gamble that it's right.
    That's not responsible, not ethical, and not engineering.

**Learning is how experts are made.** In September 2026, Tao and 24 other
Fields Medallists warned that training exists to build understanding, not only
to produce answers — and that when AI produces the answers directly, the two
come apart.[^tao]

**Work, or gym?** Bruce Schneier's test puts that in everyday terms.[^schneier]
If only the result matters, it's work, and AI is a sensible tool — provided
someone checks it and stands behind it, because in engineering your name is on
it either way. If doing it is the point, because doing it is what builds your
ability, it's the gym, and using AI there is like sending a machine to lift your
weights. Chasing an obscure Simulink error at eleven at night, when you know
what your model should do, is mostly work. Working out why your loop has less
phase margin than you expected is the gym. Most of what you do at university is
the gym, even when it looks like work.

!!! tip ""
    **You're here to build judgement, and in time, taste.**

    Judgement is the sense that a plausible answer is wrong, before you can say
    why. Taste is knowing which of several correct designs is the good one. They
    are the most valuable things you will leave with, and neither can be handed
    to you — not by me, and not by a model. They're built by doing difficult
    things and being changed by them.

    So do the hard part yourself, let it change how you think, and show me that
    in your work. Work a model produced and nobody examined tends to mark
    poorly, and not as a punishment: the credit follows the reasoning, and there
    isn't any.

In this unit you may use AI in the ways the coursework brief sets out; you will
not need to; and you are responsible for everything you submit, including
anything a tool produced. I used AI to help create these materials, but the
pedagogy and content are mine, and I have checked and rewritten all of it.

More on all of this, and how to send me feedback, is on
[AI in this course](../ai.md).



## Further reading {#further-reading .no-slides}

<!-- reading:start -->
- Dorf and Bishop, sections 1.4-1.5: Engineering design, and control system design — the design cycle this unit is built on.
- Dorf and Bishop, sections 4.1-4.2: Feedback control system characteristics; error signal analysis — why feedback at all.

Dorf, R. C. and Bishop, R. H. Modern Control Systems. Pearson. Section numbers are the same in the 12th, 13th and 14th editions; only the page numbers differ. It is [in the library](../reading.md), and is for additional study and consolidation, not a substitute for the handout.
<!-- reading:end -->

[^goedecke]: Goedecke, S. (2026). [LLMs reward expertise](https://www.seangoedecke.com/llms-reward-expertise/).
[^tao-chat]: Tao, T. (2026). [Jacobian conjecture counterexample](https://chatgpt.com/share/6a5fdc7a-d6f8-83e8-bbea-8deb42cfed56), a shared ChatGPT conversation, 20 July 2026.
[^tao]: Tao, T. and 24 other Fields Medallists (2026). [A severe misalignment of AI in mathematics](https://terrytao.wordpress.com/2026/09/11/a-severe-misalignment-of-ai-in-mathematics/).
[^schneier]: Schneier, B. (2026). [Should you use AI for a task? Here's a simple way to decide](https://www.schneier.com/blog/archives/2026/07/should-you-use-ai-for-a-task-heres-a-simple-way-to-decide.html). First published in *The Guardian*.
