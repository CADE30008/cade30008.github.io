# CADE30008 Flight Dynamics & Control

Lecture handouts, slides, interactive applets, example sheets and worked solutions for CADE30008 at the University of Bristol.

The site is built with [Zensical](https://zensical.org), and the slides with [Marp](https://marp.app) in the Bristol Flight Lab theme. Each lecture's numbers and plots come from a design script, with Python and MATLAB results checked against each other.

## Quick start

You need Python 3.10 or later, Node.js, Google Chrome, and [uv](https://docs.astral.sh/uv/) or pip.

```bash
uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt
npm install
npm run build
npm run serve
```

Then open `http://localhost:8000`.

## Layout

| Path | Contents |
|---|---|
| `docs/` | The site. Each lecture has a folder holding its handout (`index.md`), example sheet, solutions, figures and code |
| `docs/applets/` | Interactive applets, in plain HTML and JavaScript |
| `slides/` | Lecture decks, one folder per lecture, matching `docs/` |
| `models/` | Design scripts that produce every number and figure, plus the MATLAB cross-check |
| `scripts/` | Build, sync-check, PDF and test scripts |
| `AGENTS.md` | How to edit the materials, by hand or with an AI assistant |

## Course structure

The course is nine lectures. Each one is a folder under `docs/` holding its
handout (`index.md`), example sheet and solutions, with its deck in the matching
folder under `slides/`. In the site's navigation each lecture is a collapsible
section whose own link is the handout.

Lecture 2 is written. The rest are scaffolds produced by `npm run new:lesson`,
with provisional topics, so that the navigation and the build cover the whole
course while the content is written.

## Commands

| Command | What it does |
|---|---|
| `npm run new:lesson <n> <slug> "<title>"` | Scaffold a lecture: handout, example sheet, solutions and deck |
| `npm run slides` | Build each deck to HTML and PDF in `docs/slides/` |
| `npm run site` | Build the site into `site/` |
| `npm run pdf` | Print handouts, example sheets and solutions to PDF |
| `npm run check` | Check slides against handouts |
| `npm run sync:accept` | Record the current state as in sync, after reviewing |
| `npm run models` | Rerun the design scripts and compare Python with MATLAB |
| `npm run stills` | Recapture applet stills for print |
| `npm test` | Applet maths tests, then the sync check |
| `npm run build` | Slides, site, PDFs, then the sync check |

Stop `npm run serve` before running `npm run build`, because both use `site/`.

## Keeping slides and handouts in sync

The handout is authoritative. Each handout section has a stable ID, and each slide names the sections it covers in a comment, for example `<!-- handout: derivative -->`. `npm run check` reports three kinds of problem:

- slides that cite sections that don't exist;
- numbers on a slide that its cited sections don't contain;
- sections that have changed since the last confirmed sync, together with the slides to revisit.

See [AGENTS.md](AGENTS.md) for the full contract.

## The slide theme

`package.json` takes the Flight Lab Marp theme from a sibling folder, `../flightlab-marp-template`. Once the theme is published, change that dependency to `github:BristolFlightLab/marp-template` so that CI can install it.

## Copyright

Teaching content is © 2026 Dr. Steve Bullock. The University of Bristol and Bristol Flight Lab names, logos, colours and visual design are University brand assets, and are not licensed for reuse.
