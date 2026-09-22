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

*Version 2026.6, 2026-09-22. If this differs from the version in the folder's own README, download it again.*
<!-- drive-version:end -->

**At the rig, about two hours.** You leave with a comparison: what you
predicted, what happened, and an account of the gap.

Bring your predictions in writing. If you did not write them down, do that now,
before you power anything.

## Fly it

1. Amplifier off, then on.
2. Open `part3_validate.slx` and put your gains in.
3. Build, hold the arm horizontal, start.
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
