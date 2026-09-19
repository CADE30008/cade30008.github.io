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
| `curriculum/` | What each lecture is (`lectures.yaml`) and which week it falls in each year (`schedule-<year>.yaml`). The source for the planning views and schedules |
| `teaching/` | Lecturer run sheets, one per lecture |
| `models/` | Design scripts that produce every number and figure, plus the MATLAB cross-check |
| `scripts/` | Build, sync-check, PDF and test scripts |
| `AGENTS.md` | How to edit the materials, by hand or with an AI assistant |

## Course structure

The course is nine lectures plus an unnumbered guest lecture. The scope is in
[CURRICULUM.md](CURRICULUM.md) and `curriculum/lectures.yaml`, and what actually
exists is tracked in [CONTENT.md](CONTENT.md).

Each lecture is a folder `lNN-topic` under `docs/`, holding its handout
(`index.md`), example sheet and solutions, with its deck in the matching folder
under `slides/`. NN is the lecture number, not a week: this year's mapping of
lectures to weeks is in `curriculum/schedule-2026-27.yaml`, and drawn as the term
map in Lecture 1 and the lecture map at `/planning/lecture-map.html`.

Lecture 3 (PID) has written content, from before the current scope. The rest are
scoped scaffolds, so that the navigation and the build cover the whole course
while the content is written.

## Commands

| Command | What it does |
|---|---|
| `npm run new:lesson <n> <topic> "<title>"` | Scaffold lecture n as `lNN-topic`: handout, example sheet, solutions and deck |
| `npm run slides` | Build each deck to HTML and PDF in `docs/slides/` |
| `npm run site` | Build the site into `site/` |
| `npm run pdf` | Print handouts, example sheets and solutions to PDF |
| `npm run doc:pdf -- a.md b.md -o out.pdf` | Print Markdown documents, such as proposals and rubrics, to one PDF. Needs pandoc |
| `npm run check` | Check slides against handouts |
| `npm run sync:accept` | Record the current state as in sync, after reviewing |
| `npm run curriculum` | Check the lecture set and schedule against each other and the site; regenerate the term map, lecture map, workload and tables |
| `npm run models` | Rerun the design scripts and compare Python with MATLAB |
| `npm run stills` | Recapture applet stills for print |
| `npm test` | Applet maths tests, then the sync check |
| `npm run build` | Curriculum check, slides, site, PDFs, then the sync check |

Stop `npm run serve` before running `npm run build`, because both use `site/`.

## Keeping slides and handouts in sync

The handout is authoritative. Each handout section has a stable ID, and each slide names the sections it covers in a comment, for example `<!-- handout: derivative -->`. `npm run check` reports three kinds of problem:

- slides that cite sections that don't exist;
- numbers on a slide that its cited sections don't contain;
- sections that have changed since the last confirmed sync, together with the slides to revisit.

See [AGENTS.md](AGENTS.md) for the full contract.

## The slide theme

`package.json` takes the Flight Lab Marp theme from a sibling folder, `"marp-template": "file:../flightlab-marp-template"`. That works on Steve's machine and nowhere else: a fresh clone, a colleague, or CI cannot build the slides.

Once the theme repository is published, **pin to a release tag rather than to a branch**:

```json
"marp-template": "github:BristolFlightLab/marp-template#v1.0.0"
```

npm resolves that to a tarball of the tag, so the build is reproducible: `main` moving does not silently restyle every deck, and a deck built today builds the same in a year. Upgrading is then a deliberate one-line change.

What the theme repository needs for this to work:

- a `package.json` with matching `name` and `version`, and the CSS in `files` (or no `.npmignore` excluding it) — npm installs the repo as a package, not as a folder of loose files;
- no build step, or a `prepare` script, since npm runs `prepare` when installing from git;
- semver tags, `v1.0.0` style.

Alternatives, if the repository stays private: `#semver:^1.0.0` tracks compatible releases rather than one tag, at the cost of reproducibility; a GitHub Actions token or deploy key is needed either way for CI to read a private repository. Publishing to npm under a scope avoids the token problem entirely and is worth considering if the theme is meant to be reused across units.

## Licence

© 2026 Dr Steve Bullock, University of Bristol. Teaching material — handouts, slides, example sheets, solutions, figures, glossary and the planning documents — is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Software — `models/`, `scripts/`, `docs/applets/`, `docs/javascripts/` and the lesson `code/` folders — is [MIT](https://opensource.org/license/mit). Both require attribution; MIT carries it in the copyright notice.

University of Bristol and Bristol Flight Lab branding, Quanser and MathWorks material, third-party libraries and everything under `private/` are excluded. See [LICENSE.md](LICENSE.md).
