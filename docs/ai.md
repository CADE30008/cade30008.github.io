---
title: AI in this course
description: How I think about generative AI in engineering and in learning, how I used it to make these materials, and how to send me feedback.
---

# AI in this course

This page sets out how I think about generative AI — and large language models
in particular — in engineering and in learning; my advice for students; how I
used it to make these materials; and how you can help improve them. It is
opinion, and it is mine.

_— Steve Bullock_

## How I think about AI

### AI rewards expertise

Sean Goedecke makes an argument I agree with: language models _reward
expertise_.[^goedecke] They let anyone produce seemingly passable work in almost
any field, but many outputs fall down against an expert eye, and (importantly in
engineering) against the real world. An expert asks a precise question, notices
the flaw in a confidently phrased answer, rejects a plausible wrong direction,
and knows what "good" looks like before the model offers it.

Goedecke's example is Fields Medal-winning mathematician Terence Tao's
conversation with ChatGPT about the Jacobian conjecture, on 20 July
2026.[^tao-chat] Tao, among other prominent researchers, advocates for, models
and critiques some fascinating and incredibly productive uses of LLMs — and the
value in that conversation comes from his judgement at every step, not from
clever prompting.

For you, the engineering student, that has a direct consequence. Understanding
the fundamentals in this unit — what a margin means, why a system goes unstable,
what a model can and cannot tell you — is what will make you good at control
system engineering, and will enable you, if you choose, to use AI responsibly and
effectively. An engineer who understands the domain can use a model to
go faster. One who doesn't can only use it to be wrong faster, and won't know.

!!! danger ""
    A design in a domain you don't understand, produced by a tool you don't
    understand and can't check, runs the risk of being a gamble that it's right.
    That's not responsible, not ethical, and not engineering.

### Work, or gym?

In September 2026, Tao and 24 other Fields Medallists published a joint
declaration on the impact of AI on mathematics, the people within it, and the
future of the discipline.[^tao] Part of their argument is about how
mathematicians are made. Years of training have always been meant to develop
understanding, not only to produce answers; students are set problems precisely
to build the skills that research needs. Now that AI can produce the answers
directly, those two aims come apart — and a discipline that lets them come
apart risks losing the understanding its training was for. I think this is
*extremely* important in the context of learning — *your* development, and how
*we* assess and quality-assure our students.

Bruce Schneier describes an oft-repeated, simple and effective test that puts
the same idea in everyday terms.[^schneier] Before using AI on a task, ask
whether the task is **work** or **gym**.

- **Work** is a task where only the outcome matters. Nobody cares how it got
  done, as long as it's done well. AI is a sensible tool for work — with a
  caveat of my own, which is really about engineering rather than AI: someone
  is still accountable for the result. Using AI for work is responsible and
  ethical only if you check what it produces, understand it well enough to stand
  behind it, and accept that your name is on it either way.
- **Gym** is a task where doing it is the point, because doing it is what builds
  your ability. Using AI in the gym is like sending a machine to lift your weights
  for you: the weights move, but you don't change.

At university, most tasks are the gym, even when they look like work. Writing up
a design feels like work, but the thinking you do to write it clearly is the gym,
and it's what we're trying to assess.

_The same task can be either_, depending on why you're doing it. Chasing down an
obscure Simulink error at eleven at night, when you already understand what your
model should do, is (mostly) work. Working out why your loop has less phase margin
than you expected is the gym: the struggle is what _changes you_.

!!! warning ""
    Dumping materials into an LLM and asking it to do the work for you doesn't reflect why you 
    or I should be here. It reduces your efforts to button-pushing, and means I have to 
    mark a load of slop, to which I'll award the marks it deserves.
    Do the hard stuff, learn and change the way you think, and 
    show me through your work.

## What that means in this unit

- **You may use AI**, including the AI and agentic tools in MATLAB and Simulink,
  in the ways the coursework brief lists. The coursework is in the University's
  [Category 3, "Selective"](https://www.bristol.ac.uk/students/support/academic-advice/using-artificial-intelligence/).
- **You won't need it.** You can do everything in this unit, to the highest
  standard, without any AI tool.
- **You are responsible for everything you submit**, including anything a tool
  produced. Checking what an AI tool gives you is an engineering skill, so it is
  taught, and (if you use it) it is included in your assessment.
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

A course like this is a complex learning journey. A series of lectures, with
handouts, slide decks, example sheets, worked solutions, code in two languages
and figures; a coursework that builds through the term; periodic checks; a hands-on
laboratory. Every piece has to agree with every other, and has to keep agreeing,
every year, as I change things.

That is a great deal of consistency to hold in one head, and it is exactly the
kind of tracking a language model is good at — provided it works to robust,
explicit, written guidance, and a subject and teaching expert stays in the loop.
Here, that guidance lives alongside the materials:

- how we teach, as numbered principles;
- how we assess;
- how the materials are built, checked and kept in step with each other;
- and what each week is, from which the schedule, the week-by-week list and the
  planning views are generated.

Scripts then check that the numbers, figures, slides and handouts agree: every
number on a slide traces to the handout, every figure to the code that made it,
and every code snippet has been run, in Python and MATLAB, with both giving the
same answer. The model tracks; I decide.

I hope this course is evidence of what that approach can do: materials that are
more consistent, more carefully designed, and easier to review and improve than
either a person or a model would manage alone. You are part of testing that.

I'm new to this. I'm using this course to develop principles that I want to
deploy in other courses, and to share with other educators — _as long as it
supports my students' learning and experience_. So please let me know.

## Tell me what you think

I welcome feedback, both specific and general: an error in a derivation, a
figure that doesn't make sense, a badly posed question, a broken link — or a view
on whether this whole approach works.

- **On GitHub.** If you're comfortable doing so,
  [raise an issue](https://github.com/cade30008/cade30008.github.io/issues) in
  the course's repository. An issue is simply a public note describing a
  problem; you don't need to know how to use git. Say which page, and what's
  wrong.
- **By email.** You're equally welcome to write to me at
  [steve.bullock@bristol.ac.uk](mailto:steve.bullock@bristol.ac.uk).

[^goedecke]: Goedecke, S. (2026). [LLMs reward expertise](https://www.seangoedecke.com/llms-reward-expertise/).
[^tao-chat]: Tao, T. (2026). [Jacobian conjecture counterexample](https://chatgpt.com/share/6a5fdc7a-d6f8-83e8-bbea-8deb42cfed56), a shared ChatGPT conversation, 20 July 2026.
[^tao]: Tao, T. and 24 other Fields Medallists (2026). [A severe misalignment of AI in mathematics](https://terrytao.wordpress.com/2026/09/11/a-severe-misalignment-of-ai-in-mathematics/).
[^schneier]: Schneier, B. (2026). [Should you use AI for a task? Here's a simple way to decide](https://www.schneier.com/blog/archives/2026/07/should-you-use-ai-for-a-task-heres-a-simple-way-to-decide.html). First published in *The Guardian*.
