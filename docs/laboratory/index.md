---
title: "The Quanser laboratory"
description: "Open-access sessions on the 3-DOF helicopter: identify the machine, design a controller away from it, then come back and find out whether you were right."
---

# The Quanser laboratory

<div class="lesson-links" markdown>
[Part 1: identify](part1-identify.md)
[Part 2: design](part2-design.md)
[Part 3: validate](part3-validate.md)
</div>

The laboratory runs one experiment in three parts, and the parts are
deliberately not all in the same room on the same afternoon.

| Part | Where | Roughly |
|---|---|---|
| **1. Identify** | At the rig | One 2-hour session |
| **2. Design** | Anywhere | Your own time, between sessions |
| **3. Validate** | At the rig | One 2-hour session |

You measure the machine, you go away and design something against what you
measured, and then you come back and find out what the measurement left out.
That shape is the point. A laboratory where you design and test in the same
hour teaches you to tune until it looks right, which is a different skill and
a less useful one.

## Booking

Sessions are booked through the form on Blackboard. **You work in pairs or
threes, and one of you books for the group.**

Book early rather than late. The window closes before the coursework gets
hard, and the last week is always the busy one.

## Before you go

- [ ] Read [Part 1](part1-identify.md) all the way through. It is short, and
      the rig is not the place to read it.
- [ ] Bring a laptop if you have one. The bench machines work, but your own
      MATLAB means you can carry on afterwards.
- [ ] Download the [laboratory code](code/index.md) into a folder you can find.
- [ ] Agree with your group who is driving and who is writing things down.
      Swap halfway.

## Safety, and it is short

!!! danger "The amplifier switch is how you stop the rig"
    The rocker switch on the amplifier is the emergency stop. **There is no
    separate stop button and no software interlock.** Before you power
    anything, find that switch and make sure whoever is not driving can reach
    it.

    If the rig does something you do not like, switch the amplifier off. Do
    not try to catch the arm, and do not try to fix it in software while it is
    moving.

Beyond that: keep fingers and hair away from the rotors, do not lean over the
arm's travel, and leave the guarding where it is.

## What you are building towards

The three parts run twice, at two levels. Do the first before the second.

**One axis.** Elevation alone, with the other two held still. A second-order
plant, a PID controller, and a requirement you can check. Everything in the
first session's lecture applies directly.

**Three axes.** The whole machine: elevation, pitch and travel, two motors,
and the coupling between them. First as three PID loops, which is what most
real vehicles fly with and which will show you why decoupling is a design
decision rather than an approximation. Then as a state-space design against
the model the manufacturer supplies, which is where the second half of the
unit is heading.

Most groups get one axis working comfortably in their two sessions. Three
axes is what the open-access time is for.

## The rig

<figure markdown="span">
  ![The Quanser 3-DOF helicopter: a blue beam pivoted on a central column, two ducted rotors at the near end, a counterweight at the far end, standing on a circular track](../assets/rig/rig-oblique.jpg){ width="100%" }
</figure>

Three angles, two motors.

| Axis | Symbol | Positive when |
|---|---|---|
| Elevation | \( \varepsilon \) | the body is above horizontal; zero when level |
| Pitch | \( \rho \) | the front motor is higher than the back motor |
| Travel | \( \lambda \) | the body rotates counter-clockwise, seen from above |

You command two rotor voltages. Elevation comes from their sum and pitch from
their difference. **Travel is not commanded at all**: it happens because pitch
tilts the thrust sideways and the machine slides round the track after it.
That is the coupling, and it is why three axes is harder than three times one
axis.

Each rotor is driven about an operating voltage of roughly 7.5 V, which is
what holds the arm up. Your controller's output is added to that, so what you
have to play with is the headroom between there and the amplifier's limit.
