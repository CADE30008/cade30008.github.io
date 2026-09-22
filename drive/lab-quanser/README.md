<!-- version: 2026.10 (2026-09-22) -->

# The Quanser laboratory

**Version 2026.10**, 2026-09-22.

Files for the open-access laboratory sessions. The three parts of the
experiment, and what to read before each, are on the
[course site](https://cade30008.github.io/laboratory/).

Put your own `.mat` recordings in the same folder as these files.

| File | What it does |
|---|---|
| `lab1_fit.m` | Fit every recording you took, and report how much they disagree |
| `lab2_3dof.m` | All three axes as three loops, with the cascade for travel |
| `lab3_statespace.m` | The same machine by state feedback, with LQR |
| `heli3d_model.m` | The linearised six-state model, from the published constants |
| `part1_identify.slx` | The rig model you record from, in Part 1 |
| `part3_validate.slx` | The rig model you fly your controller on, in Part 3 |

`fit_second_order.m`, `heli_*.m` and `elevation_plant.json` are called by
those. Keep everything in one folder.

!!! warning "The two `.slx` files only open on a laboratory machine"
    They talk to the hardware through QUARC, which is installed on the bench
    machines and nowhere else. They will not open in MATLAB Online or on your
    own laptop, and that is not something you have done wrong.

    Everything else here runs anywhere.

!!! warning "Use the files you downloaded, not the ones already on the machine"
    The bench machines carry older copies of these models under different
    names, `m_part1.slx` and `m_part3.slx`, left from previous years. Work
    from your own downloaded folder: it is the one these instructions match,
    and it is the one that has `save_recording` in it.

## Order

`lab1_fit` first, on your own recordings. It saves `my_model.mat`.

`lab2_3dof` and `lab3_statespace` do not need your recordings: they work from
the manufacturer's model of the whole machine. Read the comments at the top of
each before running it, particularly about what that model leaves out.
