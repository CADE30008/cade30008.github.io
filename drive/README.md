<!-- version: 2026.6 (2026-09-22) -->

# CADE30008 Flight Dynamics & Control — control half, 2026/27

**Version 2026.6**, 2026-09-22.

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
