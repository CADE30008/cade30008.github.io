---
title: "Session code"
description: "The MATLAB files for the first session: fit the elevation axis, tune a controller, and submit your gains."
---

# Session code

Everything the session needs, in one folder. Several of these call each other,
so keep them together.

<!-- drive-version:start -->
**[Download the first session's files](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0/w01-design-cycle)** from MATLAB Drive, or [everything for the unit](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0).

*Version 2026.3, 2026-09-22. If this differs from the version in the folder's own README, download it again.*
<!-- drive-version:end -->

| File | What it does |
|---|---|
| `s1_identify.m` | Fit the elevation axis from a measured step, by hand and then with `tfest` |
| `s2_tune.m` | Tune a PID three ways: sliders, pole placement, `pidtune` |
| `tune_sliders.m` | Three sliders, a live response, and the envelope's verdict |
| `submit_gains.m` | Check your gains, then hand you a pre-filled submission link |
| `heli_check_one.m` | The flight envelope. The same one applied at the rig |
| `heli_plant.m` | Reads the fitted model |
| `heli_envelope.m` | The limits, in one place |
| `gain_form_url.m` | Builds the submission link |
| `gain_form.json` | Which form, and which field is which |
| `elevation_plant.json` | The fitted model: K, wn, zeta |

The recording you fit, `elevation-step.mat`, comes with them in `data/`,
along with a note on what is in it.

## Running them

Start with `s1_identify`, one section at a time rather than all at once. It
ends by saving `my_model.mat`, which `s2_tune` then loads.

They run the same on a laptop or in MATLAB Online. `s1_identify` uses System
Identification Toolbox for the `tfest` comparison, and everything else is
Control System Toolbox or base MATLAB.

!!! tip "If a function is not found"
    All of these have to be in the same folder, and that folder has to be the
    one MATLAB is looking at. `pwd` tells you where you are.
