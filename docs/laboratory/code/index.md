---
title: "Laboratory code"
description: "The MATLAB files for the laboratory sessions: fit your own recordings, design against them, and extend to all three axes."
---

# Laboratory code

**[Download the whole folder from MATLAB Drive](https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students)**, which is the easy
way and gets the week 1 files too. The table below is for when you only want
one file.

Put your own `.mat` recordings in the same folder as these. Several of them
call each other, so keep them together.

<!-- drive-version:start -->
**MATLAB Drive files: version 2026.2**, 2026-09-22. [Download them all](https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students).
<!-- drive-version:end -->

| File | What it does |
|---|---|
| [`lab1_fit.m`](lab1_fit.m) | Fit every recording you took, and report how much they disagree |
| [`lab2_3dof.m`](lab2_3dof.m) | All three axes as three loops, with the cascade for travel |
| [`lab3_statespace.m`](lab3_statespace.m) | The same machine by state feedback, with LQR |
| [`heli3d_model.m`](heli3d_model.m) | The linearised six-state model, from the published constants |
| [`fit_second_order.m`](fit_second_order.m) | The fitter `lab1_fit` calls |
| [`heli_check_one.m`](heli_check_one.m) | The flight envelope |
| [`heli_plant.m`](heli_plant.m) | Reads the fitted model |
| [`heli_envelope.m`](heli_envelope.m) | The limits, in one place |
| [`elevation_plant.json`](elevation_plant.json) | A fitted model, to compare yours against |

## Order

`lab1_fit` first, on your own recordings from [Part 1](../part1-identify.md).
It saves `my_model.mat`.

Then the single-axis design, which is the same flow as the first session's
[`s2_tune`](../../w01-design-cycle/code/s2_tune.m).

`lab2_3dof` and `lab3_statespace` are the extension, and they do not need your
recordings: they work from the manufacturer's model of the whole machine. Read
the comments at the top of each before running them, particularly about what
that model does and does not include.
