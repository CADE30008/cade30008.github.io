---
title: "Session code"
description: "The MATLAB files for the first session: fit the elevation axis, tune a controller, and submit your gains."
---

# Session code

**[Download the whole folder from MATLAB Drive](https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students)**, which is the easy
way and gets the laboratory files too. The table below is for when you only
want one file.

Keep them in one folder: several of them call each other.

<!-- drive-version:start -->
**MATLAB Drive files: version 2026.1**, 2026-09-22. [Download them all](https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students).
<!-- drive-version:end -->

| File | What it does |
|---|---|
| [`s1_identify.m`](s1_identify.m) | Fit the elevation axis from a measured step, by hand and then with `tfest` |
| [`s2_tune.m`](s2_tune.m) | Tune a PID three ways: sliders, pole placement, `pidtune` |
| [`tune_sliders.m`](tune_sliders.m) | Three sliders, a live response, and the envelope's verdict |
| [`submit_gains.m`](submit_gains.m) | Check your gains, then hand you a pre-filled submission link |
| [`heli_check_one.m`](heli_check_one.m) | The flight envelope. The same one applied at the rig |
| [`heli_plant.m`](heli_plant.m) | Reads the fitted model |
| [`heli_envelope.m`](heli_envelope.m) | The limits, in one place |
| [`gain_form_url.m`](gain_form_url.m) | Builds the submission link |
| [`gain_form.json`](gain_form.json) | Which form, and which field is which |
| [`elevation_plant.json`](elevation_plant.json) | The fitted model: K, wn, zeta |

You also need the recording: [`elevation-step.mat`](../data/elevation-step.mat),
and the [note on what is in it](../data/README.md).

## Running them

Start with `s1_identify`, one section at a time rather than all at once. It
ends by saving `my_model.mat`, which `s2_tune` then loads.

They run the same on a laptop or in MATLAB Online. `s1_identify` uses System
Identification Toolbox for the `tfest` comparison, and everything else is
Control System Toolbox or base MATLAB.

!!! tip "If a function is not found"
    All of these have to be in the same folder, and that folder has to be the
    one MATLAB is looking at. `pwd` tells you where you are.
