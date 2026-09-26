# Build plan: CADE30008 Lecture 2, closed-loop PID control

This file is the resume point. If a session stops part-way, read this file,
run `git log --oneline`, and continue from the first unchecked milestone.
Tick milestones and add notes to the log at the bottom as work lands.

## Brief (agreed with Steve, 2026-09-15)

- Course: **CADE30008 Flight Dynamics & Control**. Lecturer: **Dr. Steve Bullock**.
- Audience: year 3, having taken Bristol's year-2 Dynamics and Control of
  Linear Systems. They know Laplace, transfer functions, Bode plots and
  step-response specifications.
- Lecture 2: **closed-loop PID control**, standalone (skip the intro lecture).
  Link every idea to Bode (frequency domain) and step response (time domain).
- Deliverables:
  1. 50-minute lecture deck: ~25–30 slides with speaker notes, Flight Lab
     Marp theme.
  2. Handout: textbook-style page on the Zensical site.
  3. Example sheet: about 1 hour, 5–6 graded questions, hand calculations
     first, then computational.
  4. Worked solutions: separate public page.
  5. Interactive applets for web and slides: standalone HTML/JS with no
     external dependencies, embedded by iframe in the handout and deck, with a
     static image fallback for PDFs. At least a PID tuner (gain sliders
     driving the step response, Bode plot and margins).
- Code: parallel **Python and MATLAB** snippets in Zensical content tabs
  (`=== "Python"` / `=== "MATLAB"`). Run every snippet: MATLAB R2026a
  headless (`/Applications/MATLAB_R2026a.app/bin/matlab -batch`, about 50 s
  to start, so batch the runs) and Python (python-control) in the project's
  virtual environment.
- Running example: aircraft pitch-attitude control, using a short-period
  model with an elevator actuator. The example sheet adds a multirotor roll
  or altitude loop.
- Notation: parallel PID with a filtered derivative; show the standard form
  (Ti, Td) alongside.
- Scope: what each term does in the time and frequency domains; steady-state
  error and system type; phase margin against overshoot and damping;
  crossover frequency against speed; integrator windup; derivative kick and
  filtering; loop-shaping tuning. Out of scope: root locus, state space,
  digital implementation.
- Look: the Zensical site in Flight Lab red (palette from
  `../control-course.github.io/docs/stylesheets/extra.css`). Slides use the
  theme from `../flightlab-marp-template` as a local file dependency.
- Framework, as designed:
  - handouts in `docs/<lesson>/`, decks mirrored in `slides/<lesson>/index.md`
    (Zensical can't exclude files yet);
  - handout headings carry stable IDs (`{#id}`);
  - slides cite them with `<!-- handout: id -->`;
  - `sync.lock.json` plus a Node checker;
  - `AGENTS.md` for LLM authors;
  - a GitHub Actions workflow, written but not run;
  - PDFs printed through headless Chrome;
  - drift warnings don't fail the build.
- Git: a local repository with a commit per milestone. Never push, never publish.
- Finish: Steve wants to browse the site locally (`zensical serve`). Give a
  summary with screenshots. Do not raise the Marp Safari issue: Steve dropped
  it on 2026-09-15 (marp-cli#499 was closed upstream as wontfix).

## Milestones

- [x] M1 Scaffold: git init; uv venv (zensical, control, numpy, scipy, matplotlib);
      npm (marp-cli + theme); zensical.toml (palette, tabs, arithmatex, attr_list); skeleton pages
- [x] M2 Models and design numbers: plant, PID designs, margins, step specs, verified in MATLAB and Python;
      figure scripts committed with their outputs
- [x] M3 Handout
- [x] M4 Applets (PID tuner and any others), with fallback images
- [x] M5 Lecture deck, speaker notes and handout citations
- [x] M6 Example sheet and solutions, all code run in both languages
- [x] M7 Framework: sync checker, lock file, AGENTS.md, CI workflow, PDF script
- [x] M8 Build and verify: site, deck HTML and PDF, handout PDFs, screenshots, check passes
- [x] M9 Wrap-up: local server running, summary

## Log

- 2026-09-15: Steve said go. Model: Opus. Safari reminder dropped.
- 2026-09-15: M1-M6 done. Plant switched to G = 40/(s(s+2)(s+10)), because the
  short-period zero flattened the Bode magnitude. Designs: P (Kp=1), P (PM 60),
  PD (1.86/0.649), PID (2.03/0.678/0.661). Python and MATLAB agree on 41/41
  numbers. Applet core is a classic script, so it works from file://; 36/36
  applet checks pass. Q6 code agrees in both languages.
  M7 partly done: check-sync.mjs, AGENTS.md, build.yml, build-pdfs.mjs and
  capture-stills.mjs are written. The first check has 0 errors and only
  'not yet accepted' warnings.
  Next: browser verification, sync:accept, final build, commit, summary.
  The dev server runs via Bash on :8000, because preview_start reads the old
  project's launch.json.
- 2026-09-15: M7-M9 done. Full build clean: 29-slide deck as HTML and PDF,
  site, and handout, example-sheet and solutions PDFs. Sync baseline accepted
  (initial authoring, no prior state), so the check reports 0 errors and 0
  warnings. Applet fixes: label layout, 0.001 slider steps, and no drawing
  while hidden. README added. Dev server restarted for Steve on :8000.

<!-- tracking: status=draft version=0 -->
