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

Then open `http://localhost:8011`.

## Layout

| Path | Contents |
|---|---|
| `docs/` | The site. Each week has a folder `wNN-topic`; a lecture week's holds its handout (`index.md`), example sheet, solutions, figures and code. |
| `docs/applets/` | Interactive applets, in plain HTML and JavaScript. |
| `slides/` | Lecture decks, one folder per lecture week, matching `docs/`. |
| `curriculum/` | What each week is (`weeks.yaml`), and term-level facts: the coursework, the laboratory, the workload model (`term.yaml`). The source for the lecture map, the term map and the generated tables. |
| `diagnostics/` | Formative quizzes as YAML, with the Numbas `.exam` built from them. Published; assessed material is not. |
| `examples/` | Sample inputs the tools are tested against, such as gain submissions. Never student work. |
| `teaching/` | Lecturer run sheets, one per lecture week. |
| `models/` | Design scripts that produce every number and figure, plus the MATLAB cross-check. |
| `scripts/` | Build, sync-check, PDF and test scripts. |
| `AGENTS.md` | How to edit the materials, by hand or with an AI assistant. |

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
| [PEDAGOGY.md](PEDAGOGY.md) | How these materials are meant to teach, as numbered principles, and the reasoning behind them. |
| [CURRICULUM.md](CURRICULUM.md) | What the unit teaches, in what order, and why, with the options that were weighed. |
| [curriculum/weeks.yaml](curriculum/weeks.yaml) | Every week's outcomes, activities, case, hook, cliffhanger and reading, from which much of the site is generated. |
| [ASSESSMENT.md](ASSESSMENT.md) | How the coursework is designed, and how submissions are checked. |
| [AGENTS.md](AGENTS.md) | How the materials are built, checked and edited, by a person or an AI assistant. |
| [CONTENT.md](CONTENT.md) | What is written, and what isn't yet. |
| [LICENSE.md](LICENSE.md) | The full licence terms. |

For lecturers, planning views:

- **The lecture map**, [`docs/planning/lecture-map.html`](docs/planning/lecture-map.html): every week's outcomes, what happens in each part of the session, the work between sessions, the consolidation week, the cliffhanger chain and the student workload model. Open it in a browser; it will also be on the site once published.
- **The term map**, in [week 1's handout](docs/w01-design-cycle/index.md#schedule): the twelve weeks at a glance.
- **Run sheets**, in [`teaching/`](teaching/): the plan for each lecture, and the [Blackboard build sheet](teaching/blackboard.md).
- **Review notes**, in [`reviews/`](reviews/): reviews against the principles, including what was removed and why.

## Commands

| Command | What it does |
|---|---|
| `npm run new:lesson <week> <topic> "<title>"` | Scaffold a lecture week as `wNN-topic`: handout, example sheet, solutions and deck. |
| `npm run slides` | Build each deck to HTML and PDF in `docs/slides/`. |
| `npm run site` | Build the site into `site/`. |
| `npm run pdf` | Print handouts, example sheets and solutions to PDF. |
| `npm run doc:pdf -- a.md b.md -o out.pdf` | Print Markdown documents, such as proposals and rubrics, to one PDF. Needs pandoc. |
| `npm run check` | Check slides against handouts. |
| `npm run sync:accept` | Record the current state as in sync, after reviewing. |
| `npm run curriculum` | Check the week-by-week plan and term facts against each other and the site; regenerate the term map, lecture map, workload and tables. |
| `npm run numbas` | Build a Numbas `.exam` from a quiz's YAML, re-checking every numeric answer. |
| `npm run models` | Rerun the design scripts and compare Python with MATLAB. |
| `npm run stills` | Recapture applet stills for print. |
| `npm test` | Applet maths tests, then the sync check. |
| `npm run build` | Curriculum check, slides, site, PDFs, then the sync check. |
| `npm run serve` | The **in-progress** site, everything, at `http://localhost:8011`. |
| `npm run live` | Build the **live** site — only what `publish.yaml` lists — into `.live/site`, and check its links. |
| `npm run preview:live` | Build the live site and serve it at `http://localhost:8012`, exactly as it will be published. |

Stop `npm run serve` before running `npm run build`, because both use `site/`.

### Preview servers

Two, always on the same ports, so a bookmark keeps working:

| | Port | What it shows |
|---|---|---|
| `npm run serve` | **8011** | The in-progress site: everything, including unwritten weeks. |
| `npm run preview:live` | **8012** | Exactly what `https://cade30008.github.io` will show. |

AVDASI2 uses **8001** and **8002**, so the two repositories never collide.

Both listen on **IPv4 and IPv6**, and on loopback only. That is why the live
preview goes through `scripts/preview.py` rather than `python -m http.server`:
that binds one address family, `localhost` resolves to `::1` first on macOS, and
the result was a server that answered on `http://localhost:8012` but refused
`http://127.0.0.1:8012` outright. It presents as "the preview is down" when it
is up on the other stack.

Neither survives a reboot, and neither survives a **folder rename** — that one
is the quiet failure, because the virtualenv hard-codes absolute paths in its
console scripts, so the server dies with `bad interpreter` rather than anything
about ports. After any rename, rebuild `.venv` before looking at the network at
all.

If a preview is unreachable, work down this list before anything else:

```bash
lsof -nP -iTCP -sTCP:LISTEN | grep -E ':(8011|8012)'   # is it running, on both stacks?
head -1 .venv/bin/zensical                             # does the shebang match this folder?
curl -sI http://127.0.0.1:8011/ | head -1              # IPv4 specifically, not localhost
```

Each line catches a different failure that presents identically: not started,
moved folder, and bound to one address family.

## Publishing

The live site is **https://cade30008.github.io**, published from this
repository by GitHub Actions (`.github/workflows/publish.yml`) on every push to
`main`. It shows only the pages listed in [`publish.yaml`](publish.yaml);
everything else stays on the in-progress site. Links from a published page to
an unpublished one become plain text, and blocks between
`<!-- in-progress:start -->` and `<!-- in-progress:end -->` are left out.

To publish a page: add it to `publish.yaml`, run `npm run preview:live`, look
at it on `http://localhost:8012`, then commit and push. The workflow refuses to
deploy if the live build has a broken link, including a link in the Blackboard
build sheet (`teaching/blackboard.md`).

One-time set-up: the repository is `CADE30008/cade30008.github.io`, in the
`CADE30008` GitHub organisation, and its **Settings › Pages › Source** is set to
**GitHub Actions**.

Not yet handled: slides and PDFs on the live site. They're built locally and git
ignores them. Both themes now come from public, pinned repositories, so CI can
build decks whenever that step is added; nothing published yet needs them, and
the first published lecture week will.

## Keeping slides and handouts in sync

The handout is authoritative. Each handout section has a stable ID, and each slide names the sections it covers in a comment, for example `<!-- handout: derivative -->`. `npm run check` reports three kinds of problem:

- slides that cite sections that don't exist;
- numbers on a slide that its cited sections don't contain;
- sections that have changed since the last confirmed sync, together with the slides to revisit.

Weeks whose handout front matter says `status: draft` are skipped, since scaffolding has nothing to keep in sync; the summary line says how many. Remove that line when a week is written, and it is checked from then on. `npm run check -- --all` includes drafts.

See [AGENTS.md](AGENTS.md) for the full contract.

## The Flight Lab templates

Three repositories, so the branding is in one place rather than copied into every unit:

| Repository | What | How this repo takes it |
|---|---|---|
| [flightlab-brand](https://github.com/BristolFlightLab/flightlab-brand) | The artwork: crest, slanted edges, marks. The single source. | Indirectly, through the two below. |
| [flightlab-zensical-theme](https://github.com/BristolFlightLab/flightlab-zensical-theme) | The site theme. | A git submodule at `theme/`, pinned to a tag; `theme.custom_dir` serves its `dist/`. |
| [flightlab-marp-template](https://github.com/BristolFlightLab/flightlab-marp-template) | The slide theme. | An npm dependency pinned to a tag. |

**Clone with submodules**, or the site builds unbranded and then fails:

```bash
git clone --recurse-submodules https://github.com/CADE30008/cade30008.github.io.git
```

An existing clone catches up with `git submodule update --init`.

To take a newer theme: `git -C theme checkout vX.Y.Z`, rebuild, look at a page, then commit the moved pointer. The submodule records the exact commit, so a site built today builds the same in a year.

## The slide theme

The Flight Lab Marp theme is a package of its own, [BristolFlightLab/flightlab-marp-template](https://github.com/BristolFlightLab/flightlab-marp-template), and `package.json` takes it **from a release tag**:

```json
"marp-template": "github:BristolFlightLab/flightlab-marp-template#v1.1.0"
```

`.marprc.yml` then points Marp at `node_modules/marp-template/themes`.

Pinning to the tag rather than to `main` keeps the build reproducible: the theme moving does not silently restyle every deck, and a deck built today builds the same in a year. Upgrading is a deliberate one-line change — bump the tag, run `npm install`, rebuild and look at a deck.

The repository is public, so no token is needed and CI can build the decks. It was previously a sibling folder, `file:../flightlab-marp-template`, which worked on Steve's machine and nowhere else; keep that form only for local theme work, and put the tag back before committing.

## Licence

© 2026 Dr Steve Bullock, University of Bristol. Teaching material — handouts, slides, example sheets, solutions, figures, glossary and the planning documents — is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Software — `models/`, `scripts/`, `docs/applets/`, `docs/javascripts/` and the lesson `code/` folders — is [MIT](https://opensource.org/license/mit). Both require attribution; MIT carries it in the copyright notice.

University of Bristol and Bristol Flight Lab branding, Quanser and MathWorks material, third-party libraries and everything under `private/` are excluded. See [LICENSE.md](LICENSE.md).
