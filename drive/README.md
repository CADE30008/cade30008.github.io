<!-- version: 2026.21 (2026-09-22) -->

# CADE30008 Flight Dynamics & Control — control half, 2026/27

**Version 2026.21**, 2026-09-22.

Everything given out during the control half of this unit. Open any file in
[MATLAB Online](https://matlab.mathworks.com/): it runs in the browser, so
there is nothing to install.

**This folder is shared view only.** You can open and run anything here and
save your own copy, but you cannot change what is here, and nothing you do
affects anyone else.

## Check the version before each laboratory session

> **All of this is new for 2026/27.** It will be corrected and improved during
> the year, mostly because of things you tell me.

So the files here will change. Before each laboratory session, compare the
version at the top of this page with the one on the
[course site](https://cade30008.github.io/laboratory/). If they differ,
**download the folder again**. It takes a few seconds and saves you debugging
something that was fixed a fortnight ago.

| Version | Date | What changed |
|---|---|---|
| 2026.21 | 2026-09-22 | The models capture a whole run now: the external mode buffer held only 100 seconds, which is why a recording could start at 100.00 with the step missing. |
| 2026.20 | 2026-09-22 | Levelling: stop the model while the arm is level, then run `level_rig`. Nothing reaches the workspace until a run ends. |
| 2026.19 | 2026-09-22 | Clearer on getting a complete recording: the capture starts when you connect, so stop, build, connect, then start. |
| 2026.18 | 2026-09-22 | The scopes log at 20 Hz instead of 1000. A full run is about two thousand rows, still over a hundred samples per oscillation. |
| 2026.17 | 2026-09-22 | Part 1 spells out the order that gets a complete recording: unload, build, connect, then start. And why the run stops itself at 99.9 s. |
| 2026.16 | 2026-09-22 | `check_recording` names the right cause when a record starts late: the model was never unloaded, not the scopes dropping data. |
| 2026.15 | 2026-09-22 | `save_recording` warns when a recording does not start at zero, which means the model was never unloaded and the clock carried on from an earlier run. Part 1 says to unload between runs. |
| 2026.14 | 2026-09-22 | `check_scopes` added: what each scope logs, and whether it is dropping data. |
| 2026.13 | 2026-09-22 | `check_recording` added, and the step in Part 1 is now taken from your level value rather than from zero. Setting the box back to 0 after levelling can leave a recording with no step in it. |
| 2026.12 | 2026-09-22 | `level_rig` added, and Part 1 now starts with the arm on the floor and a levelling step. Every rig trims differently, and your voltage budget follows from yours. |
| 2026.11 | 2026-09-22 | The voltage limit is measured now, not assumed: the demand saturates 8.6 V above the trim, so the check allows 6 V rather than 11.2. `s2_tune`'s starting design is retuned to suit. |
| 2026.10 | 2026-09-22 | `part1_identify.slx` no longer writes `results.mat`. That file was held open by the rig's process and blocked the next run. Nothing is lost: the data comes from the scopes. |
| 2026.8 | 2026-09-22 | Part 1 and Part 3 warn against **Build, Deploy & Start**: use **Build** then **Monitor & Tune**, or the model runs on the rig with no way to stop it. |
| 2026.7 | 2026-09-22 | Part 2 and Part 3 now say to take the derivative term from the `ElevRate` signal rather than from the error, and why. |
| 2026.6 | 2026-09-22 | `save_recording` and `plot_recording` added. Save each run under its own name: the laboratory's `s_save` always wrote `d_Part1.mat`, so a second recording overwrote the first. |
| 2026.5 | 2026-09-22 | The two Simulink models are renamed to match the parts they belong to: `part1_identify.slx` and `part3_validate.slx`. Same models. The bench machines still have them as `m_part1.slx` and `m_part3.slx`. |
| 2026.4 | 2026-09-22 | The two rig Simulink models, `m_part1.slx` and `m_part3.slx`, are in `lab-quanser/`. They only open on a laboratory machine. |
| 2026.3 | 2026-09-22 | The Drive folder is now `cade30008`, with a clearer landing page. No change to any script or data. |
| 2026.2 | 2026-09-22 | `s1_identify` now finds the recording wherever you keep it. Plainer wording in the three-axis model about what it is linearised about. |
| 2026.1 | 2026-09-22 | First release: week 1 session files and the Quanser laboratory files. |

### Your recordings do not go stale

The scripts here may change. **Data you recorded will still work.** A file you
saved in your first laboratory session will still load and still fit under a
later version, because the format is the one the rig's own `s_save` writes and
that is fixed by the hardware rather than by us.

So you never need to re-record anything because the code moved on. If a later
version ever cannot read something you measured, that is a fault, and I would
like to know.

## Layout

| Folder | What is in it |
|---|---|
| `w01-design-cycle/` | The first session: fit the elevation axis, tune a PID, submit your gains |
| `lab-quanser/` | The open-access laboratory: fit your own recordings, then all three axes |

## Submitting work

**Nothing is submitted into this folder** — it is read only. Where a session
asks you to submit something, it tells you where it goes. In the first session
that is the PID gains you tune, and `submit_gains` hands you a link.

## If a file will not open

Try it in [MATLAB Online](https://matlab.mathworks.com/) rather than a desktop
install, which is where these are tested. If it still will not open, say so
rather than working around it: a file that does not open for you probably does
not open for others either.

<!-- tracking: status=draft version=0 -->
