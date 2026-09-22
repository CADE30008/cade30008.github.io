---
title: "Laboratory part 2: design away from the machine"
description: "Between sessions: fit a model to what you recorded, design a controller against a requirement you have written down, and predict what will happen before you go back."
---

# Part 2: design away from the machine

<div class="lesson-links" markdown>
[Laboratory](index.md)
[Part 1: identify](part1-identify.md)
[Part 3: validate](part3-validate.md)
</div>

**Your own time, no rig.** You leave with gains, a predicted response, and a
written requirement you are prepared to be judged against.

Having no machine is the point. You cannot tune until it looks right, so you
have to decide what right means first.

## Fit a model

Start with `lab1_fit.m` from [MATLAB Drive](https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students), which walks through the
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
controller demand under 11 V.*

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
