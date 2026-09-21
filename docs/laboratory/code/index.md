---
title: "Laboratory code"
description: "The MATLAB files for the laboratory sessions: fit your own recordings, design against them, and extend to all three axes."
---

# Laboratory code

Download these into one folder, and put your own `.mat` recordings in the same
folder. Several of them call each other.

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

!!! warning "The two models disagree about the elevation axis, on purpose"
    `heli3d_model` is linearised about level, where gravity stiffness is
    exactly zero, so it makes elevation a double integrator. The model you fit
    from a recording is taken about a trim, where the stiffness is not zero,
    so it comes out as a lightly damped second order.

    Both are right about the case they describe. Which one you should be using
    depends on where you are flying, and noticing that is most of the skill.
