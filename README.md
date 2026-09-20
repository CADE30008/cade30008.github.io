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
| `docs/` | The site. Each week has a folder `wNN-topic`; a lecture week's holds its handout (`index.md`), example sheet, solutions, figures and code |
| `docs/applets/` | Interactive applets, in plain HTML and JavaScript |
| `slides/` | Lecture decks, one folder per lecture week, matching `docs/` |
| `curriculum/` | What each week is (`weeks.yaml`), and term-level facts: the coursework, the laboratory, the workload model (`term.yaml`). The source for the lecture map, the term map and the generated tables |
| `teaching/` | Lecturer run sheets, one per lecture week |
| `models/` | Design scripts that produce every number and figure, plus the MATLAB cross-check |
| `scripts/` | Build, sync-check, PDF and test scripts |
| `AGENTS.md` | How to edit the materials, by hand or with an AI assistant |

## Course structure

The course is designed to the University calendar: eleven weeks of content,
named "Week 1" to "Week 11" — nine lecture weeks, a guest lecture in week 5, and
the consolidation week in week 6, which has no lecture. The scope is in
[CURRICULUM.md](CURRICULUM.md) and `curriculum/weeks.yaml`, and what actually
exists is tracked in [CONTENT.md](CONTENT.md).

Each week is a folder `wNN-topic` under `docs/`. A lecture week holds its handout
(`index.md`), example sheet and solutions, with its deck in the matching folder
under `slides/`. The term is drawn as the term map in week 1 and the lecture map
at `/planning/lecture-map.html`.

Week 3 (PID) has written content, from before the current scope. The rest are
scoped scaffolds, so that the navigation and the build cover the whole course
while the content is written.

## Behind the materials

The documents that say how the course is designed and kept consistent:

| Document | What it's for |
|---|---|
| [PEDAGOGY.md](PEDAGOGY.md) | How these materials are meant to teach, as numbered principles, and the reasoning behind them |
| [CURRICULUM.md](CURRICULUM.md) | What the unit teaches, in what order, and why, with the options that were weighed |
| [curriculum/weeks.yaml](curriculum/weeks.yaml) | Every week's outcomes, activities, case, hook, cliffhanger and reading, from which much of the site is generated |
| [ASSESSMENT.md](ASSESSMENT.md) | How the coursework is designed, and how submissions are checked |
| [AGENTS.md](AGENTS.md) | How the materials are built, checked and edited, by a person or an AI assistant |
| [CONTENT.md](CONTENT.md) | What is written, and what isn't yet |
| [LICENSE.md](LICENSE.md) | The full licence terms |

For lecturers, planning views:

- **The lecture map**, [`docs/planning/lecture-map.html`](docs/planning/lecture-map.html): every week's outcomes, what happens in each part of the session, the work between sessions, the consolidation week, the cliffhanger chain and the student workload model. Open it in a browser; it will also be on the site once published.
- **The term map**, in [week 1's handout](docs/w01-design-cycle/index.md#schedule): the twelve weeks at a glance.
- **Run sheets**, in [`teaching/`](teaching/): the plan for each lecture, and the [Blackboard build sheet](teaching/blackboard.md).
- **Review notes**, in [`reviews/`](reviews/): reviews against the principles, including what was removed and why.

## Commands

| Command | What it does |
|---|---|
| `npm run new:lesson <week> <topic> "<title>"` | Scaffold a lecture week as `wNN-topic`: handout, example sheet, solutions and deck |
| `npm run slides` | Build each deck to HTML and PDF in `docs/slides/` |
| `npm run site` | Build the site into `site/` |
| `npm run pdf` | Print handouts, example sheets and solutions to PDF |
| `npm run doc:pdf -- a.md b.md -o out.pdf` | Print Markdown documents, such as proposals and rubrics, to one PDF. Needs pandoc |
| `npm run check` | Check slides against handouts |
| `npm run sync:accept` | Record the current state as in sync, after reviewing |
| `npm run curriculum` | Check the week-by-week plan and term facts against each other and the site; regenerate the term map, lecture map, workload and tables |
| `npm run numbas` | Build a Numbas `.exam` from a quiz's YAML, re-checking every numeric answer |
| `npm run models` | Rerun the design scripts and compare Python with MATLAB |
| `npm run stills` | Recapture applet stills for print |
| `npm test` | Applet maths tests, then the sync check |
| `npm run build` | Curriculum check, slides, site, PDFs, then the sync check |
| `npm run serve` | The **in-progress** site, everything, at `http://localhost:8000` |
| `npm run live` | Build the **live** site — only what `publish.yaml` lists — into `.live/site`, and check its links |
| `npm run preview:live` | Build the live site and serve it at `http://localhost:8010`, exactly as it will be published |

Stop `npm run serve` before running `npm run build`, because both use `site/`.

## Publishing

The live site is **https://cade30008.github.io**, published from this
repository by GitHub Actions (`.github/workflows/publish.yml`) on every push to
`main`. It shows only the pages listed in [`publish.yaml`](publish.yaml);
everything else stays on the in-progress site. Links from a published page to
an unpublished one become plain text, and blocks between
`<!-- in-progress:start -->` and `<!-- in-progress:end -->` are left out.

To publish a page: add it to `publish.yaml`, run `npm run preview:live`, look
at it on `http://localhost:8010`, then commit and push. The workflow refuses to
deploy if the live build has a broken link, including a link in the Blackboard
build sheet (`teaching/blackboard.md`).

One-time set-up: the repository is `CADE30008/cade30008.github.io`, in the
`CADE30008` GitHub organisation, and its **Settings › Pages › Source** is set to
**GitHub Actions**.

Not yet handled: slides and PDFs on the live site. They're built locally, git
ignores them, and the slide theme comes from a sibling folder that CI can't see
("The slide theme", below). Nothing published yet needs them; the first
published lecture week will.

## Keeping slides and handouts in sync

The handout is authoritative. Each handout section has a stable ID, and each slide names the sections it covers in a comment, for example `<!-- handout: derivative -->`. `npm run check` reports three kinds of problem:

- slides that cite sections that don't exist;
- numbers on a slide that its cited sections don't contain;
- sections that have changed since the last confirmed sync, together with the slides to revisit.

Weeks whose handout front matter says `status: draft` are skipped, since scaffolding has nothing to keep in sync; the summary line says how many. Remove that line when a week is written, and it is checked from then on. `npm run check -- --all` includes drafts.

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
