---
title: "Laboratory part 3: find out what the model left out"
description: "Back at the rig: fly the controller you designed, compare what happens with what you predicted, and account for the difference."
---

# Part 3: find out what the model left out

<div class="lesson-links" markdown>
[Laboratory](index.md)
[Part 1: identify](part1-identify.md)
[Part 2: design](part2-design.md)
[Code](code/index.md)
</div>

<!-- drive-version:start -->
**[Download the laboratory files](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0/lab-quanser)** from MATLAB Drive, or [everything for the unit](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0).

*Version 2026.15, 2026-09-22. If this differs from the version in the folder's own README, download it again.*
<!-- drive-version:end -->

**At the rig, about two hours.** You leave with a comparison: what you
predicted, what happened, and an account of the gap.

Bring your predictions in writing. If you did not write them down, do that now,
before you power anything.

## Fly it

1. Amplifier off, then on.
2. Open `part3_validate.slx`. **The Controller block is empty: what goes in it
   is yours.** Build your controller there.

    Two connections the model has already made for you: `Elev(deg)` comes back
    into the block as `elev_output`, and `ElevRate(deg/s)` is brought out to a
    terminator. **Take your derivative term from that rate signal**, not from
    the derivative of the error. [Part 2](part2-design.md) says why, and the
    short version is that differentiating the error asks the amplifier for
    about 40 V it does not have.
3. Build it, then connect with **Monitor & Tune**. Hold the arm horizontal
   and start.

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

4. Command the step you designed for, and record.

Then, before you change anything:

- [ ] Measure the overshoot and settling time you actually got.
- [ ] Put them next to what you predicted.
- [ ] Look at the controller's output, not just the angle. Did it saturate?

## Account for the difference

There will be one. Four usual reasons, and you should be able to say which
applies:

- **The model is wrong.** It came from one axis of a three-axis machine, over
  a hundred seconds, at one trim.
- **The actuators saturate.** A controller demanding 30 V from a 24 V
  amplifier is not the controller you designed, and it is not linear either.
- **There is noise.** The encoder quantises, and derivative action amplifies
  exactly that. Look for it in the motor demand.
- **The plant has moved.** Friction, trim and temperature are not what they
  were in Part 1.

Distinguishing these is the work. "It didn't match" is not a finding.

## Now tune it, and say that you did

Once you have the comparison recorded, tune the gains until the rig meets your
requirement. This is allowed and expected. What is not allowed is quietly
replacing your designed gains with the tuned ones and presenting them as the
design.

Record both sets. The difference between them is evidence about your model,
and it is more interesting than either set on its own.

!!! tip "If nothing works"
    Fall back to a PID block with your designed gains and check the sign
    conventions first: a loop that runs away immediately is usually a sign
    error, not a tuning problem. If the arm slams to a stop, turn the
    amplifier off before you think about why.

## Take away

- Recordings of the designed controller and the tuned one.
- Your predictions, and what actually happened.
- One paragraph on which of the four reasons above accounts for the gap, and
  what measurement would settle it.

That paragraph is the thing this laboratory is for. Everything else is
supporting evidence.
