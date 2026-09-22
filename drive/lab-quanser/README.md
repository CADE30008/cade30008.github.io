<!-- version: 2026.3 (2026-09-22) -->

# The Quanser laboratory

**Version 2026.3**, 2026-09-22.

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

`fit_second_order.m`, `heli_*.m` and `elevation_plant.json` are called by
those. Keep everything in one folder.

## Order

`lab1_fit` first, on your own recordings. It saves `my_model.mat`.

`lab2_3dof` and `lab3_statespace` do not need your recordings: they work from
the manufacturer's model of the whole machine. Read the comments at the top of
each before running it, particularly about what that model leaves out.
