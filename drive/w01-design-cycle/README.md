<!-- version: 2026.5 (2026-09-22) -->

# Week 1 — The design cycle, end to end

**Version 2026.5**, 2026-09-22.

The session's files. Work through them in order, one section at a time rather
than running the whole script at once.

| File | What it does |
|---|---|
| `s1_identify.m` | Fit the elevation axis from the measured step, by hand and then with `tfest` |
| `s2_tune.m` | Tune a PID three ways: sliders, pole placement, `pidtune` |
| `tune_sliders.m` | Three sliders, a live response, and the envelope's verdict |
| `submit_gains.m` | Check your gains, then hand you a pre-filled submission link |
| `data/elevation-step.mat` | The measured response you fit |

The rest (`heli_*.m`, `gain_form*`, `elevation_plant.json`) are called by
those four. Keep them all in one folder.

## Order

1. `s1_identify` — ends by saving `my_model.mat`.
2. `s2_tune` — loads it.
3. `submit_gains` — called for you at the end of `s2_tune`.

`s1_identify` uses System Identification Toolbox for the `tfest` comparison
only. If you do not have it, the script still saves your by-hand model before
that section, so you can carry straight on to `s2_tune`.

## Submitting

`submit_gains` checks your gains against the same envelope applied at the rig,
then gives you a link to the form with your numbers already in it. You press
Submit yourself.

Gains outside the envelope are refused and you are told which limit they
missed. Nothing is quietly adjusted: gains changed without telling you would
put a flight on screen under your name that was not yours.
