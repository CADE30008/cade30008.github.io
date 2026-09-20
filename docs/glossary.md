---
title: Glossary
description: Plain definitions of the terms used across CADE30008 Flight Dynamics & Control.
---

# Glossary

Every term this course uses, defined once, in plain words. If a lecture and this
page disagree, tell us: one of them is wrong.

Definitions here are working ones. They are meant to be enough to follow the
argument, not to be the most general statement that could be made. Where a term
has a sharper definition you will meet later, that is said.

!!! tip "How to use this page"
    Use your browser's find (++ctrl+f++ or ++cmd+f++), or the site search, which
    covers this page too. Terms are grouped by where you meet them, not
    alphabetically, so that reading a whole section makes sense on its own.

## How this unit works

**Formative.** Work that doesn't contribute to your unit grade. It exists to
show you, and us, how you're doing while there's still time to act on it: the
diagnostic, the weekly challenges, the example sheets, the case work in each
session, the laboratory and the coursework checkpoints. Formative work is the
foundation of the summative submission, not a warm-up you can skip.

**Summative.** Work that carries your unit grade. In this half of the
unit there is exactly one piece: the coursework, due on the Thursday of week 11.

**Checkpoint.** A point in the term where you're expected — but not required —
to hand in the part of your coursework you've built so far. Formative: it earns
you automatic checks on what you submit, and feedback while it can still change
your design.

**Challenge.** The short weekly set of questions in Numbas or MATLAB Grader that
rehearses that week's material. Formative, automatically marked, with feedback
on each question, and the same questions for everyone.

## The design process

**Control design cycle.** The loop this course is built on: state the
requirements, get a model, design a controller, analyse it, verify it, implement
it, then find out what you got wrong and go round again. Every lecture says
where in this cycle it sits.

**Requirement.** A statement of what the control system must achieve, written so
that you can test whether it did. "Settles within 2 seconds with no more than 10
per cent overshoot" is a requirement. "Responds nicely" is not.

**Specification.** Used interchangeably with requirement in most control
writing. Where this course distinguishes them, a requirement is what the system
must do and a specification is the agreed numbers that express it.

**Plant.** The thing being controlled: the aircraft, the helicopter rig, the
motor. Everything outside the controller.

**Model.** A mathematical description of the plant that is good enough for the
job in hand. Every model is wrong somewhere; the skill is knowing where.

**System identification, or system ID.** Getting a model from measured data
rather than from physics. You excite the system, record what it does, and fit a
model to the recording. The counterpart to deriving a model from first
principles, and often the only honest route when the physics is uncertain.

**Model-based design.** The industrial form of the design cycle, in which one
set of models carries the work from requirements through simulation and
verification to the code that runs on the aircraft. The point is that the model
is the shared artifact, not a drawing that gets out of date.

**Verification.** Checking that the design meets its requirements. "Did we build
it right?"

**Validation.** Checking that the model, or the requirements, describe reality.
"Did we build the right thing, and does our model of it hold?"

**Operating point, or trim.** A condition the aircraft is holding steady at: a
speed, an altitude, an attitude, with the forces balanced. Models are usually
built around one.

**Linearisation.** Replacing the true nonlinear behaviour with a straight-line
approximation valid near an operating point. It is what makes almost every tool
in this course applicable, and it is the first assumption to question when a
design misbehaves far from trim.

## The feedback loop

**Open loop.** The plant driven directly, with no measurement fed back. The
Quanser helicopter cannot be flown open loop, which is why the course starts
there.

**Closed loop, or feedback.** The output is measured, compared with what was
wanted, and the difference used to drive the plant.

**Reference, or setpoint.** What you want the output to be.

**Error.** Reference minus measured output. What the controller acts on.

**Disturbance.** Anything that pushes the plant around that is not your control
input: gusts, turbulence, a shifting load.

**Measurement noise.** Error in the sensor's reading. Feedback acts on it just
as readily as on real motion, which is why more gain is not always better.

**Feedforward.** Acting on a known reference or a measured disturbance directly,
without waiting for an error to appear. Used alongside feedback, not instead of
it.

**Actuator.** What moves the plant: a control surface and its servo, a motor, a
thruster.

**Saturation.** An actuator reaching its limit and being unable to give more.
The commonest reason a design that worked in simulation fails in reality.

**Rate limit.** A limit on how fast an actuator can move, as distinct from how
far. It behaves like a delay that gets worse the harder you push.

**Time delay.** Any lag between a command and its effect: computation,
communication, actuator response. Delay costs phase, and phase is what stability
margin is made of.

## PID control

**PID.** Proportional–integral–derivative control: the controller formed by
adding three terms computed from the error. By a wide margin the most used
controller in engineering, and the first one to try.

**Proportional term.** Acts in proportion to the present error. More of it means
a faster response and, usually, less stability.

**Integral term.** Acts on the accumulated error over time. It removes steady
offsets, at the cost of phase and therefore of stability margin.

**Derivative term.** Acts on how fast the error is changing, which is a crude
prediction of where it is going. It adds damping, and it amplifies measurement
noise, so it is almost always used with a filter.

**Gains.** The three constants $K_p$, $K_i$, $K_d$ that set how much of each
term is used. Tuning means choosing them.

**Tuning.** Choosing gains to meet the requirements. It has rules of thumb, it
has systematic methods, and it has no single right answer until the requirements
are stated.

**Integral windup.** The integral term accumulating while the actuator is
saturated and nothing can be done about the error. The result is a large,
delayed overshoot when the actuator comes off its limit. Preventing it is called
anti-windup.

**Derivative kick.** The large transient the derivative term produces when the
reference is stepped, because the error jumps. Fixed by differentiating the
measurement rather than the error.

**Ziegler–Nichols.** A classical set of tuning rules from measured
characteristics of the plant. Historically important, widely taught, and rarely
the best answer.

## Describing behaviour

**Transfer function.** The relationship between a system's input and its output,
written in the Laplace variable $s$. The compact description that most of this
course works with.

**Pole.** A root of a transfer function's denominator. Poles determine how a
system responds on its own: how fast it settles, whether it oscillates, whether
it diverges.

**Zero.** A root of the numerator. Zeros shape how the response starts, and a
zero in the right half-plane makes a system initially go the wrong way.

**Characteristic equation.** The denominator of the closed-loop transfer
function set to zero. Its roots are the closed-loop poles, so it is where
stability is decided.

**Stability.** A stable system, disturbed, returns to where it was. An unstable
one does not. For a linear system this is exactly the question of whether every
pole lies in the left half-plane.

**Marginal stability.** Poles exactly on the boundary: the system neither
settles nor diverges, but oscillates forever. A mathematical case rather than a
practical one, since nothing real sits exactly on a boundary.

**Damping ratio, $\zeta$.** How quickly oscillation dies away, on a scale where 0
oscillates forever and 1 does not oscillate at all. The Quanser helicopter's
elevation axis is around 0.06, which is why it rings.

**Natural frequency, $\omega_n$.** How fast an oscillatory system wants to move.
Together with the damping ratio it fixes a second-order response entirely.

**Overshoot.** How far past the target the response goes, as a percentage of the
step. Set by the damping ratio alone, for a simple second-order system.

**Rise time, settling time, steady-state error.** How fast it gets there, how
long until it stops moving, and how far off it ends up. With overshoot, the
usual language of a time-domain requirement.

**Step response.** What the system does when the reference jumps. The most
readable single test of a control system, and the one most requirements are
written against.

## Frequency domain

**Frequency response.** How a system responds to sinusoids of each frequency: by
how much it magnifies them, and by how much it delays them. A complete
description of a linear system, obtained by measurement as readily as by
calculation.

**Bode plot.** Magnitude and phase of the frequency response, plotted against
frequency on logarithmic axes. The working diagram of classical control design.

**Nyquist plot.** The frequency response drawn as a path in the complex plane.
Harder to read than a Bode plot, and it answers the stability question
definitively where the Bode plot can mislead.

**Nyquist criterion.** The rule that decides closed-loop stability from the
shape of that path, including for plants that are unstable open loop.

**Loop gain.** Controller times plant, taken round the loop once. Nearly every
classical result is a statement about it.

**Crossover frequency.** Where the loop gain passes through 1. Roughly, the
fastest the closed loop can be expected to act.

**Bandwidth.** The range of frequencies over which the closed loop follows its
reference. More bandwidth means a faster system, more actuator effort, and more
noise let through: a choice, not a free good.

**Gain margin.** How much extra gain the loop can take before it goes unstable.

**Phase margin.** How much extra phase lag, or equivalently how much extra
delay, the loop can take before it goes unstable.

!!! warning "A margin is not a safety guarantee"
    A loop can have textbook margins and still be fragile, because margins
    measure two particular directions of change and a real plant varies in
    many. Treat them as a necessary check, not a certificate.

**Sensitivity.** How much a disturbance, or a change in the plant, reaches the
output. Design largely consists of pushing it down where it matters and
accepting that it rises elsewhere.

**Complementary sensitivity.** How much of the reference, and of the measurement
noise, reaches the output. It and the sensitivity add to one at every frequency,
which is the most useful constraint in classical design.

**Loop shaping.** Designing by deciding what you want the loop gain to look like
against frequency, then building a controller that produces it.

**Lead and lag compensators.** Simple controllers that add phase where you need
it, or gain where you need it, at the cost of the other. The classical
alternative to PID, and the route into loop shaping.

**Root locus.** A plot of how the closed-loop poles move as a gain is varied.
The bridge between the frequency domain and what the response actually looks
like.

## Robustness

**Uncertainty.** What you do not know about the plant: parameters you measured
imprecisely, dynamics you left out, behaviour that changes with flight
condition.

**Robustness.** A design's tolerance of that uncertainty. A robust design still
meets its requirements when the plant is not quite what the model said.

**Model error.** The difference between the plant and the model of it. Bounding
it honestly is more useful than pretending it is zero.

## State space and beyond

**State.** The smallest set of numbers that, with the future inputs, determines
the system's future entirely. For an aircraft, its velocities, rates and
attitude.

**State-space model.** The description of a system as a set of first-order
differential equations in its state. It handles many inputs and outputs at once,
where a transfer function handles one pair.

**State feedback.** Driving the plant from all of its states at once, rather
than from the output error alone.

**Observer, or state estimator.** Something that reconstructs the states you
cannot measure from the ones you can, so that state feedback becomes possible.

**Controllability, observability.** Whether the inputs can move every state, and
whether the outputs reveal every state. If either fails, no amount of design
effort will fix it.

**Pole placement.** Choosing state feedback gains so that the closed-loop poles
land exactly where you want them. Possible, and not always wise.

**LQR.** Linear quadratic regulator: state feedback chosen to minimise a
weighted sum of state error and control effort. It turns "how aggressive should
this be?" into a choice of weights.

## Aircraft

**Handling qualities.** How an aircraft feels and behaves to the pilot flying
it, assessed against published standards rather than against opinion. The usual
source of a flight control system's requirements.

**Short period, phugoid.** The two longitudinal modes of a conventional
aircraft: a fast pitching oscillation, and a slow exchange of speed and
altitude.

**Dutch roll, spiral, roll subsidence.** The three lateral-directional modes: an
oscillation coupling yaw and roll, a slow divergence or convergence in bank, and
the rapid damping of roll rate.

**Stability augmentation system, or SAS.** Feedback added to improve an
aircraft's natural behaviour, without the pilot handing over control.

**Autopilot mode.** A named behaviour the autopilot can be in, such as holding
altitude or tracking a heading, each with its own loop and its own requirements.

**Control authority.** How much the control surfaces can actually do. A design
that asks for more than exists is not a design.

**Pilot-induced oscillation, or PIO.** An oscillation sustained by the pilot's
own corrections, usually because delay or a rate limit has put them out of phase
with the aircraft. A control problem with a human in the loop.

## Our systems and tools

**Quanser 3-DoF helicopter.** The laboratory rig: two motors on a beam, free to
move in elevation, pitch and travel. Used from week 1 onwards.

**Elevation, pitch, travel.** The rig's three axes: how high the beam is, how
the rotor head is tilted, and how far round the base it has rotated.

**MATLAB, Simulink.** The numerical environment and its block-diagram modelling
tool, both licensed to you by the University.

**Live Script.** A MATLAB document that mixes text, code and its output.
Several of this course's activities are Live Scripts.

**MATLAB Drive.** Cloud storage attached to your MATLAB account, used here to
give you data and to collect what you produce in a lecture.

**python-control.** The Python library that does what MATLAB's Control System
Toolbox does. This course gives both, and they agree.

**Pyodide.** Python compiled to run in a web browser, which is how the runnable
code on this site works without your installing anything.

---

!!! note "This page grows"
    Terms are added as lectures introduce them, and every lecture review checks
    this page against the lecture. If a term you need is missing, that is a
    fault worth reporting.
