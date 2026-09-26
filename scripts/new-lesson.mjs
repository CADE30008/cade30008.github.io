// Scaffold a lecture: handout, example sheet, solutions and deck.
//
// Usage:
//   node scripts/new-lesson.mjs 6 loop-shaping "Loop shaping"
//
// Creates docs/w08-loop-shaping/{index.md,example-sheet.md,solutions.md} and
// slides/w08-loop-shaping/index.md, wired to each other and following the sync
// contract in AGENTS.md: the handout's sections carry stable IDs, and every
// content slide cites the section it covers.
//
// Folders are wNN-topic, where NN is the University week: the course is
// designed to the calendar, and "Week n" is how students see it.
//
// Existing files are never overwritten; the script reports them and moves on.
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const [numberArg, slug, title] = process.argv.slice(2);
if (!numberArg || !slug || !title) {
  console.error('usage: node scripts/new-lesson.mjs <week> <topic> "<title>"');
  process.exit(1);
}

const n = Number(numberArg);
if (!Number.isInteger(n) || n < 1) {
  console.error(`not a lecture number: ${numberArg}`);
  process.exit(1);
}

const root = resolve(import.meta.dirname, "..");
const lesson = `w${String(n).padStart(2, "0")}-${slug}`;

// Placeholder bodies deliberately carry no figures and no numerals: the sync
// check verifies that every number on a slide appears in the handout section it
// cites, and there is nothing to verify against yet.
const handout = `---
title: "Week ${n}: ${title}"
description: "Placeholder. Scoped in curriculum/weeks.yaml; content not yet written."
lesson: ${lesson}
order: ${n}
duration: 110 min
status: draft
---

# Week ${n}: ${title}

<div class="lesson-links" markdown>
[Slides](../slides/${lesson}/index.html)
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
<!-- outcomes:end -->

## Where we are {#recap}

What the student already knows that this lecture builds on, and where it came from.

## First idea {#idea-one}

The first main idea, developed from what the recap established.

## Second idea {#idea-two}

The second main idea, and how it changes the picture.

## Worked example {#worked-example}

A worked example carrying the ideas above through to numbers. Numbers belong in
a script under \`models/\`, not typed in here.

## Summary {#summary}

The few things to take away.

## Further reading {#further-reading .no-slides}

Textbook chapters and papers. This section is handout-only, which is what
\`.no-slides\` marks.
`;

const deck = `---
marp: true
theme: flightlab
paginate: true
header: "CADE30008 Flight Dynamics & Control"
footer: "Dr. Steve Bullock · Week ${n}"
title: "Week ${n}: ${title}"
description: "Placeholder deck for week ${n}."
author: "Dr. Steve Bullock"
---

<!-- _class: title -->

# ${title}

## Week ${n} · CADE30008 Flight Dynamics & Control

Dr. Steve Bullock

<!--
Presenter notes. Anything in an HTML comment becomes a note rather than slide
content, and does not appear on the slide itself.
-->

---

<!-- handout: recap -->

# Where we are

- what the student already knows
- where it came from
- why it is not yet enough

---

<!-- handout: idea-one -->

# First idea

- the idea, in one line
- what it changes
- what it costs

---

<!-- handout: idea-two -->

# Second idea

- the idea, in one line
- how it builds on the first
- when it applies

---

<!-- handout: worked-example -->

# Worked example

- the set-up
- the design step
- the result, and whether it met the specification

---

<!-- handout: summary -->

# Summary

- first takeaway
- second takeaway
- third takeaway
`;

const exampleSheet = `---
title: "Week ${n} example sheet: ${title}"
description: "Placeholder example sheet for week ${n}."
lesson: ${lesson}
---

# Example sheet: ${title}

<div class="lesson-links" markdown>
[Handout](index.md)
[Slides](../slides/${lesson}/index.html)
[Solutions](solutions.md)
</div>

This sheet takes about an hour. Try each question before looking at the
[solutions](solutions.md).

## Q1. First question {#q1}

<span class="marks">[10 marks · 15 min]</span>

A question that can be done by hand, testing the first idea.

## Q2. Second question {#q2}

<span class="marks">[10 marks · 20 min]</span>

A question that builds on Q1.

## Q3. Computational question {#q3}

<span class="marks">[10 marks · 25 min]</span>

A question needing Python with the \`control\` package, or MATLAB with the
Control System Toolbox.
`;

const solutions = `---
title: "Week ${n} solutions: ${title}"
description: "Placeholder solutions for the week ${n} example sheet."
lesson: ${lesson}
---

# Solutions: ${title}

<div class="lesson-links" markdown>
[Example sheet](example-sheet.md)
[Handout](index.md)
[Slides](../slides/${lesson}/index.html)
</div>

These are worked solutions to the [example sheet](example-sheet.md). Every
number should be checked against a script in \`models/\` before publishing.

## Q1. First question {#q1}

The worked solution, with the reasoning shown rather than just the answer.

## Q2. Second question {#q2}

The worked solution.

## Q3. Computational question {#q3}

The worked solution, with the code that produces it.
`;

const files = [
  [join(root, "docs", lesson, "index.md"), handout],
  [join(root, "docs", lesson, "example-sheet.md"), exampleSheet],
  [join(root, "docs", lesson, "solutions.md"), solutions],
  [join(root, "slides", lesson, "index.md"), deck],
];

mkdirSync(join(root, "docs", lesson), { recursive: true });
mkdirSync(join(root, "slides", lesson), { recursive: true });

let written = 0;
for (const [file, body] of files) {
  const shown = file.slice(root.length + 1);
  if (existsSync(file)) {
    console.log(`kept     ${shown} (already exists)`);
    continue;
  }
  writeFileSync(file, body);
  console.log(`created  ${shown}`);
  written++;
}

if (written) {
  console.log(`\nAdd "Week ${n}: ${title}" to nav in zensical.toml and an entry to curriculum/weeks.yaml, then run npm run curriculum.`);
}

// tracking: status=draft version=0 assisted=true
