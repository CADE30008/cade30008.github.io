---
title: AI in this course
description: How I think about generative AI in engineering and in learning, how I used it to make these materials, and how to send me feedback.
---

# AI in this course

This page sets out how I think about generative AI — and large language models
in particular — in engineering and in learning; how I used it to make these
materials; and how you can help improve them. It is opinion, and it is mine.

## How I think about it

### AI rewards expertise

Sean Goedecke makes an argument I agree with: language models reward
expertise.[^goedecke] They let anyone produce passable work in almost any field,
which makes everyone look like a generalist. That hides what actually decides how
much you get out of them, which is knowing the subject. An expert asks the precise
question, notices the flaw in a confident answer, rejects a plausible wrong
direction, and knows what "good" looks like before the model offers it. His
example is a leading mathematician working through a hard problem with a chatbot:
the value came from the mathematician's judgement at every step, not from any
clever way of prompting.

For you, that has a direct consequence. The fundamentals in this unit — what a
margin means, why a loop goes unstable, what a model can and cannot tell you —
are not what AI makes unnecessary. They are what will make you good at using AI
in control engineering. An engineer who understands feedback can use a model to
go faster. One who doesn't can only use it to be wrong faster, and won't know.

A design produced by a tool you can't check isn't your design. It's a guess
you're taking responsibility for.

### Work, or gym?

Bruce Schneier describes a simple test for whether to use AI on a task.[^schneier]
Ask whether the task is **work** or **gym**.

- **Work** is a task where only the outcome matters. Nobody cares how it got
  done, as long as it's done well. AI is a sensible tool for work.
- **Gym** is a task where doing it is the point, because doing it is what builds
  your ability. Using AI in the gym is like sending a machine to lift your weights
  for you: the weights move, and you get no stronger.

At university, most tasks are the gym, even when they look like work. Writing up
a design feels like work, but the thinking you do to write it clearly is the gym,
and it's what the assessment is looking for.

The same task can be either, depending on why you're doing it. Chasing down an
obscure Simulink error at eleven at night, when you already understand what your
model should do, is mostly work. Working out why your loop has less phase margin
than you expected is the gym: that struggle is the understanding.

### What that means in this unit

- **You may use AI**, including the AI and agentic tools in MATLAB and Simulink,
  in the ways the coursework brief lists. The coursework is in the University's
  Category 3, "Selective".
- **You won't need it.** You can do everything in this unit, to the highest
  standard, without any AI tool.
- **You are responsible for everything you submit**, including anything a tool
  produced. Checking what an AI tool gives you is an engineering skill, so it is
  taught, and it is assessed.
- **If you can't explain it, you don't understand it yet** — and a design paper
  that asks you to justify your decisions will show that.

## How these materials were made

I used generative AI tools to help create these resources: drafting text,
writing and checking code, building this site, and keeping all of the pieces
consistent with each other.

The pedagogy and the content are mine: what is taught, in what order, how, and
why. I have quality-assured and rewritten all of the content.

Teaching, and all formative and summative assessment, are carried out by people.
Automated scripts help with technical checks, such as whether your code runs and
reproduces your results; those scripts are conventional code, not generative AI,
and they don't award marks.

### Why I work this way

A course like this is a complex learning journey. Nine lectures, each with a
handout, a slide deck, an example sheet, worked solutions, code in two languages
and figures; a coursework that builds through the term; weekly checks; a
laboratory. Every piece has to agree with every other, and has to keep agreeing,
every year, as things change.

That is a great deal of consistency to hold in one head, and it is exactly the
kind of tracking a language model is good at — provided it works to robust,
explicit, written guidance, and a subject and teaching expert stays in the loop.
Here, that guidance lives alongside the materials:

- how we teach, as numbered principles;
- how we assess;
- how the materials are built, checked and kept in step with each other;
- and what each lecture is, from which the schedule, the lecture list and the
  planning views are generated.

Scripts then check that the numbers, figures, slides and handouts agree: every
number on a slide traces to the handout, every figure to the code that made it,
and every code snippet has been run, in Python and MATLAB, with both giving the
same answer. The model proposes and tracks; I decide.

I hope this course is evidence of what that approach can do: materials that are
more consistent, more carefully designed, and easier to review and improve than
either a person or a model would manage alone. You are part of testing that.

## Tell me what you think

I welcome feedback, both specific and general: an error in a derivation, a
figure that doesn't make sense, a badly posed question, a broken link — or a view
on whether this whole approach works.

- **On GitHub.** If you're comfortable doing so, raise an issue in the course's
  repository (link to follow). An issue is simply a public note describing a
  problem; you don't need to know how to use git. Say which page, and what's
  wrong.
- **By email.** You're equally welcome to write to me at
  [steve.bullock@bristol.ac.uk](mailto:steve.bullock@bristol.ac.uk).

[^goedecke]: Goedecke, S. (2026). [LLMs reward expertise](https://www.seangoedecke.com/llms-reward-expertise/).
[^schneier]: Schneier, B. (2026). [Should you use AI for a task? Here's a simple way to decide](https://www.schneier.com/blog/archives/2026/07/should-you-use-ai-for-a-task-heres-a-simple-way-to-decide.html). First published in *The Guardian*.

## Further reading

- University of Bristol. [Using AI in assessments and for studying](https://www.bristol.ac.uk/students/support/academic-advice/using-artificial-intelligence/).
