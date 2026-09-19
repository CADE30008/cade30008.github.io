# About these materials

## How they fit together

Each lecture has a **handout**, which is the authoritative written version, and a **slide deck**, which is a condensed view of it. Every slide names the handout section it covers, so the two can be checked against each other automatically. If a handout section changes, the check reports which slides need revisiting.

The numbers, plots and code all come from one design script per lecture. Every code snippet you see in Python and MATLAB has been run, and both languages give the same numbers.

## Preparing for the course

Before the first lecture, work through [Preparing for Control](preparing/index.md). It checks that your laptop or tablet can run the course code, and lists the MathWorks Onramp courses to complete.

## Interactive applets

Some sections include small interactive applets, such as a PID tuner with sliders. They run entirely in your browser and don't send anything anywhere. The same applets appear in the lecture slides.

## Generative AI

Generative AI tools were used to help develop these learning resources. The
pedagogy and content are mine, and I have checked and rewritten all of it.

Teaching, and all formative and summative assessment, are carried out by people.
Automated scripts help with technical checks, such as whether your code runs and
reproduces your results. Those scripts are conventional code, not generative AI or
large language models, and they don't award marks.

How I think about AI in engineering and in learning, why I built these materials
the way I did, and how to send me feedback, are on
[AI in this course](ai.md).

## Behind these materials {#behind}

Everything on this site is built from one repository on GitHub: the handouts,
slide decks and example sheets, the code behind every figure and number, and
the documents that say how the course is designed and kept consistent. **The
repository isn't public yet, so the GitHub links below won't work until it
is.**

- **[The course repository][repo]** — the source of the lecture resources:
  handouts, example sheets and solutions in [`docs/`][repo-docs], slide decks in
  [`slides/`][repo-slides], and the design scripts that generate every number
  and figure in [`models/`][repo-models].

### For the curious

How the course is designed, and how it keeps its many parts in step. These are
plain documents in the repository:

- [**PEDAGOGY.md**][pedagogy] — how these materials are meant to teach, as
  numbered principles, and the reasoning behind them.
- [**CURRICULUM.md**][curriculum] — what the unit teaches, in what order, and why,
  with the options that were weighed.
- [**The lecture set**][lectures] — every lecture's learning outcomes,
  activities, case, hook and cliffhanger, in one file from which much of this
  site is generated.
- [**ASSESSMENT.md**][assessment] — how the coursework is designed.
- [**AGENTS.md**][agents] — how the materials are built, checked and edited,
  whether by a person or an AI assistant.
- [**CONTENT.md**][content] — what is written, and what isn't yet.
- [**LICENSE.md**][licence] — the full licence terms.

### For lecturers

Planning views, for anyone teaching this material or building something like it:

- [**The lecture map**](planning/lecture-map.html) — every lecture's outcomes,
  what happens in each part of the session, the work between sessions, the
  cliffhanger chain, and the student workload model, on one page.
- [**The term map**](l01-design-cycle/index.md#schedule) — which lecture falls in
  which week this year.
- [**Run sheets**][teaching] — the lecturer's plan for each session: timings,
  files, set-up, and what to do when it goes wrong.
- [**Review notes**][reviews] — reviews of the materials against the principles,
  including what was removed and why.

<!-- Placeholder repository address. Confirm the organisation and name when the
     repository is made public, and change it here: every link above uses it. -->
[repo]: https://github.com/BristolFlightLab/aero-control-course
[repo-docs]: https://github.com/BristolFlightLab/aero-control-course/tree/main/docs
[repo-slides]: https://github.com/BristolFlightLab/aero-control-course/tree/main/slides
[repo-models]: https://github.com/BristolFlightLab/aero-control-course/tree/main/models
[pedagogy]: https://github.com/BristolFlightLab/aero-control-course/blob/main/PEDAGOGY.md
[curriculum]: https://github.com/BristolFlightLab/aero-control-course/blob/main/CURRICULUM.md
[lectures]: https://github.com/BristolFlightLab/aero-control-course/blob/main/curriculum/lectures.yaml
[assessment]: https://github.com/BristolFlightLab/aero-control-course/blob/main/ASSESSMENT.md
[agents]: https://github.com/BristolFlightLab/aero-control-course/blob/main/AGENTS.md
[content]: https://github.com/BristolFlightLab/aero-control-course/blob/main/CONTENT.md
[licence]: https://github.com/BristolFlightLab/aero-control-course/blob/main/LICENSE.md
[teaching]: https://github.com/BristolFlightLab/aero-control-course/tree/main/teaching
[reviews]: https://github.com/BristolFlightLab/aero-control-course/tree/main/reviews

## Building a local copy

You need Python 3.10 or later, Node.js and Google Chrome.

```bash
uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt
npm install
npm run build
npm run serve
```

The site then runs at `http://localhost:8000`.

## Licence

© 2026 Dr Steve Bullock, University of Bristol. Two licences, both of which ask
for attribution:

- **Teaching material** — handouts, slides, example sheets, solutions, figures
  and the glossary — under
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Share and adapt it,
  including commercially, provided you give credit, link to the licence, and say
  if you changed anything.
- **Software** — the applets, the scripts that generate the figures and numbers,
  and the build tooling — under the
  [MIT licence](https://opensource.org/license/mit). Reusing it means keeping the
  copyright notice, which is how the attribution travels with the code.

> Bullock, S. (2026). *CADE30008 Flight Dynamics & Control: course materials*.
> University of Bristol. CC BY 4.0.

Some things in these pages are **not** ours to license, and neither licence
covers them:

- the University of Bristol and Bristol Flight Lab names, logos and visual
  identity, which are University brand assets and trade marks;
- Quanser's laboratory materials, models and software;
- MathWorks material, including MATLAB, Simulink and the Onramp courses;
- assessment material, which is not published here;
- quotations, figures and data from published work, which are cited where they
  are used.

If you reuse this material, replace the University branding with your own. The
full terms, and the complete list of what is excluded, are in `LICENSE.md` in
the source repository.
