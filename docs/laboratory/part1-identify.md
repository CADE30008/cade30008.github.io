---
title: "Laboratory part 1: identify the machine"
description: "At the rig: record the elevation axis responding to a step, check the recording is usable before you leave, and take away data you can fit."
---

# Part 1: identify the machine

<div class="lesson-links" markdown>
[Laboratory](index.md)
[Part 2: design](part2-design.md)
[Part 3: validate](part3-validate.md)
[Code](code/index.md)
</div>

<!-- drive-version:start -->
**[Download the laboratory files](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0/lab-quanser)** from MATLAB Drive, or [everything for the unit](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0).

*Version 2026.9, 2026-09-22. If this differs from the version in the folder's own README, download it again.*
<!-- drive-version:end -->

**At the rig, about two hours.** You leave with recordings. You do not leave
with a controller.

The whole of this session is step 1 of the design cycle: find out what the
machine actually does. Resist designing anything while you are here. The
recording is the deliverable.

## Set up

1. **The amplifier should be off when you arrive.** If it is on, turn it off,
   then on again. Find the switch and agree who is watching it.
2. Open MATLAB on the bench machine and open `part1_identify.slx`.
3. Build it: **Hardware → Build, Deploy & Start → Build**. It takes a minute
   or two. Read the warning below before you click anything.
4. Connect to it with **Monitor & Tune**.
5. Set `Yaw Demand = 0` and `Elevation Input = 0` before you start anything.
6. **Hold the arm horizontal** and start the model. The elevation encoder zeroes
   itself wherever the arm is when the model starts, so where you hold it *is*
   your datum. Hold it level and hold it still.
7. If the machine is not facing you, adjust `Yaw Demand` until it is.

!!! danger "Build. Do not Build, Deploy & Start"
    The button you want is **Hardware → Build, Deploy & Start → Build**, which
    only builds. The one directly above it, **Build, Deploy & Start**, builds
    *and* starts the model on the rig immediately.

    If you start it that way there is no stop button, because the model is
    running on the hardware and not under MATLAB's control. Your only way out
    is to switch the amplifier off and wait for the run to time out, which is
    99 seconds unless somebody changed it. With the rotors already spinning.

    So: **Build**, wait for it to finish, then **Monitor & Tune** to connect to
    it. Monitor & Tune is the one that leaves you in charge: you can stop it,
    change a value and watch the effect while it runs.

!!! warning "The zero you set here is the zero everything else is measured from"
    If you start the model with the arm drooping, every angle you record is
    offset, and the gain you fit from it will be wrong. It costs nothing to
    start again.

## Record a step

1. With the arm settled and steady, change `Elevation Input` from 0 to **2**.
2. Leave it. Do not touch anything for the rest of the run. The model stops
   itself at 100 s.
3. Save it with a name you will recognise later:

    ```matlab
    save_recording('trim-2V')
    ```

    Not the laboratory's `s_save`, which always writes to `d_Part1.mat`. You
    are about to take several recordings, and with one filename each
    overwrites the last.

That is one usable run. Take **at least three**, and take them properly:

- Let the arm settle completely between runs. At this damping a disturbance
  takes about a minute to die away, and a swing left over from the last run
  ends up in this one's fit.
- Vary the step: 1.5 V, 2 V, 2.5 V. If the gain you fit is the same each time,
  the axis is linear over that range. If it is not, you have found the limit
  of the single model you were about to design against.

!!! tip "If a file is locked between runs"
    QUARC can archive each run to `results.mat`, and the target process holds
    that file open, so a second run cannot write it and you cannot delete it
    from the file browser either. Stopping the model is not enough; it has to
    be **unloaded**.

    You do not need that archive. The scopes log to the workspace, which is
    where `save_recording` gets the data from, so the simplest answer is to
    turn QUARC's archiving off and forget about it. Ask a demonstrator if you
    are not sure where that setting is.

## Check it before you leave

This is the part groups skip and then regret. Plot each recording before you
pack up:

```matlab
plot_recording('trim-2V.mat')
```

Three things to confirm on the plot:

- [ ] **It was steady before the step.** If the trace is already swinging, the
      starting trim is whatever the swing happened to be doing, and your gain
      will be out by anything up to 25%. Take it again.
- [ ] **The step is in there.** You changed the input, not just thought about
      it.
- [ ] **There are at least four clear oscillations** after the step, above the
      noise. You need peak heights to get damping, and you need several.

If any of those fail, you have the rig in front of you right now. Take it
again. You cannot fix a bad recording in Part 2.

## If there is time left

Two things worth having, in this order.

**Repeat at a different trim.** Set `Elevation Input` to 1, let it settle,
then step to 1.5. Then from 2.5 to 3. Fit each later and see whether the
natural frequency is the same. Gravity stiffness on an arm goes as
\( \sin\varepsilon \), so there is a real question about whether one model
serves the whole range, and it is settled by measurement rather than argument.

**Watch the coupling.** With the model running, change `Yaw Demand` and watch
what elevation does. Then disturb pitch by hand, gently, and watch what travel
does. Write down what you see. You are not measuring it yet; you are finding
out what you will be up against when you come back for three axes.

## Take away

- Your `.mat` recordings. Email them to yourself before you leave the room.
- Your notes on what the rig did that the data will not show: what you held,
  what you nudged, anything that looked wrong.

Then [Part 2](part2-design.md).
