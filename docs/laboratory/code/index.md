---
title: "Laboratory code"
description: "The MATLAB files for the laboratory sessions: fit your own recordings, design against them, and extend to all three axes."
---

# Laboratory code

The laboratory files, in one folder. Put your own `.mat` recordings in the
same folder as these. Several of them call each other, so keep them together.

<!-- drive-version:start -->
**[Download the laboratory files](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0/lab-quanser)** from MATLAB Drive, or [everything for the unit](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0).

*Version 2026.10, 2026-09-22. If this differs from the version in the folder's own README, download it again.*
<!-- drive-version:end -->

| File | What it does |
|---|---|
| `lab1_fit.m` | Fit every recording you took, and report how much they disagree |
| `lab2_3dof.m` | All three axes as three loops, with the cascade for travel |
| `lab3_statespace.m` | The same machine by state feedback, with LQR |
| `heli3d_model.m` | The linearised six-state model, from the published constants |
| `fit_second_order.m` | The fitter `lab1_fit` calls |
| `heli_check_one.m` | The flight envelope |
| `heli_plant.m` | Reads the fitted model |
| `heli_envelope.m` | The limits, in one place |
| `elevation_plant.json` | A fitted model, to compare yours against |

## Order

`lab1_fit` first, on your own recordings from [Part 1](../part1-identify.md).
It saves `my_model.mat`.

Then the single-axis design, which is the same flow as the first session's
`s2_tune`.

`lab2_3dof` and `lab3_statespace` are the extension, and they do not need your
recordings: they work from the manufacturer's model of the whole machine. Read
the comments at the top of each before running them, particularly about what
that model does and does not include.
