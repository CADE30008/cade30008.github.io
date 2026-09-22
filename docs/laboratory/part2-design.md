---
title: "Laboratory part 2: design away from the machine"
description: "Between sessions: fit a model to what you recorded, design a controller against a requirement you have written down, and predict what will happen before you go back."
---

# Part 2: design away from the machine

<div class="lesson-links" markdown>
[Laboratory](index.md)
[Part 1: identify](part1-identify.md)
[Part 3: validate](part3-validate.md)
[Code](code/index.md)
</div>

<!-- drive-version:start -->
**[Download the laboratory files](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0/lab-quanser)** from MATLAB Drive, or [everything for the unit](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0).

*Version 2026.11, 2026-09-22. If this differs from the version in the folder's own README, download it again.*
<!-- drive-version:end -->

**Your own time, no rig.** You leave with gains, a predicted response, and a
written requirement you are prepared to be judged against.

Having no machine is the point. You cannot tune until it looks right, so you
have to decide what right means first.

## Fit a model

Start with `lab1_fit.m` from the [laboratory files](https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0/lab-quanser), which walks through the
manual fit and then the toolbox one. Do the manual fit first even though the
toolbox is one line: a fit you got by hand is one you can argue with.

Three numbers, three measurements:

| Number | From |
|---|---|
| \( K \) | how far it moved, divided by the step that moved it |
| \( \omega_\mathrm{d} \) | the spacing of the peaks |
| \( \zeta \) | the ratio of successive peaks, by log decrement |

Then \( \omega_\mathrm{n} = \omega_\mathrm{d}/\sqrt{1-\zeta^{2}} \).

Fit **each** of your recordings separately and compare. They will not agree
exactly. How much they disagree is your first honest estimate of how well you
know this machine, and it matters more than any single fit.

!!! tip "Use the early peaks"
    Once the swing is down to a few tenths of a degree you are measuring the
    encoder's resolution, not the arm. Those late "peaks" do not decay, so
    including them drags your damping ratio towards zero.

## Write the requirement down

Before you design anything. A requirement is a number with a test attached.

Something like: *for a 7.5° step in commanded elevation, overshoot no more
than 20%, settled within 2% inside 8 s, steady-state error under 1°, and peak
controller demand under 6 V.*

Then argue with your group about the numbers, and write down where each came
from. "We agreed it" is an acceptable answer. "It came out of the design" is
not, because then it is a description and not a specification.

## Design

`lab1_design.m` takes you through three ways, in this order.

1. **By feel**, with sliders, so you know what each term does.
2. **By design**: choose where you want the closed-loop poles and solve for
   the gains that put them there. Three equations, three unknowns, doable on
   paper.
3. **By function**: `pidtune`, now that you have something to check it
   against.

Expect the last two to disagree, and work out why before you decide which to
take. One of them will probably ask the motors for more voltage than the
amplifier has.

## Take the derivative from the rate signal, not from the error

The model brings the measured elevation rate out as `ElevRate(deg/s)` and
leaves it on a terminator. It is there for you.

Wire your derivative term to **that**, not to the derivative of the error.
Both are called D and they are not the same thing:

- On the **error**, the derivative sees the demand as well as the machine. A
  demand that steps or ramps goes straight through \( K_\mathrm{d} \) before
  the arm has moved at all. The rig ramps its demand at 45 deg/s, so at
  \( K_\mathrm{d} = 0.9 \) that is about 40 V asked for in the first instant,
  from an amplifier that has 24.
- On the **measurement**, the derivative only sees the machine moving, which
  is the thing you actually wanted to damp.

The loop transfer is the same either way, so your poles, damping and margins
are unchanged and everything you designed still holds. What changes is what
the motors are asked for.

This is why the checks in Part 2 pass and a flight can still saturate: the
check assumes the rate signal, and the wiring is yours.

## Predict, in writing

Before you go back. For the gains you are taking:

- [ ] What overshoot do you expect?
- [ ] What settling time?
- [ ] What peak voltage will the controller demand?
- [ ] Where do you expect the rig to disagree with the simulation, and why?

Write the numbers down. A prediction you made before the test is worth more
than any amount of explanation afterwards, and the last question is the one
that turns a laboratory session into evidence.

## Then the three-axis version

Once one axis works, the same three parts run again on the whole machine.
`lab2_3dof.m` sets up the coupled model and three PID loops: elevation from
the sum of the rotor voltages, pitch from their difference, and travel from
pitch.

The travel loop is the interesting one. You cannot command travel, so you
command pitch and let travel follow, which makes it an inner and outer loop
pair with everything that implies about how fast each can be.

After that, `lab3_statespace.m` uses the manufacturer's own linearised model
and designs for all three axes at once. Compare it with your three loops:
which is better depends on what you asked for, which is the same lesson in a
larger form.

Then [Part 3](part3-validate.md).
