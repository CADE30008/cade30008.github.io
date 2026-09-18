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
