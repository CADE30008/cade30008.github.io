# About these materials

## How they fit together

Each lecture has a **handout**, which is the authoritative written version, and a **slide deck**, which is a condensed view of it. Every slide names the handout section it covers, so the two can be checked against each other automatically. If a handout section changes, the check reports which slides need revisiting.

The numbers, plots and code all come from one design script per lecture. Every code snippet you see in Python and MATLAB has been run, and both languages give the same numbers.

## Preparing for the course

Before the first lecture, work through [Preparing for Control](preparing/index.md). It checks that your laptop or tablet can run the course code, and lists the MathWorks Onramp courses to complete.

## Interactive applets

Some sections include small interactive applets, such as a PID tuner with sliders. They run entirely in your browser and don't send anything anywhere. The same applets appear in the lecture slides.

## Generative AI

Generative AI tools, including Claude, made by Anthropic, were used to help
develop these learning resources.

Teaching, and all formative and summative assessment, are carried out by people.
Automated scripts help with technical checks, such as whether your code runs and
reproduces your results. Those scripts are conventional code, not generative AI or
large language models, and they don't award marks.

## Building a local copy

You need Python 3.10 or later, Node.js and Google Chrome.

```bash
uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt
npm install
npm run build
npm run serve
```

The site then runs at `http://localhost:8000`.

## Copyright

Teaching content is © 2026 Dr. Steve Bullock. The University of Bristol and Bristol Flight Lab names, logos and visual identity are University brand assets and are not licensed for reuse.
