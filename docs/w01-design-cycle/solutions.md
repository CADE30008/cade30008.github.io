---
title: "Lecture 1 solutions: The design cycle, end to end"
description: "Worked solutions to the week 1 example sheet."
lesson: w01-design-cycle
---

# Solutions: The design cycle, end to end

<div class="lesson-links" markdown>
[Example sheet](example-sheet.md)
[Handout](index.md)
[Slides](../slides/w01-design-cycle/index.html)
[Slides (PDF)](../slides/w01-design-cycle/slides.pdf)
</div>

These are worked solutions to the [example sheet](example-sheet.md). The
figure was drawn from a system with \( K = 2.5 \) deg/V,
\( \omega_\mathrm{n} = 1.4 \) rad/s and \( \zeta = 0.12 \), and every number
below comes from a run of `models/w01_example_sheet.py`, which draws it.

Your readings will not match these exactly, and they are not meant to. A gain
within about 5% and a damping ratio within about 20% is a good fit read off a
plot with a ruler.

## Q1. Read the gain and the frequency {#q1}

1. It sits at **3.0°** before the step and settles to **8.0°**. The step was
   2.0 V, so

    $$
    K = \frac{8.0 - 3.0}{2.0} = 2.5\ \text{deg/V}.
    $$

    The common mistake is dividing the final value by the step and getting
    4.0. The gain is about how far it *moved*.

2. The first overshoot is at about \( t = 2.3 \) s and the second at about
   \( t = 6.8 \) s. One full cycle is the gap between them:

    $$
    T_\mathrm{d} \approx 6.8 - 2.3 = 4.5\ \text{s},
    \qquad
    \omega_\mathrm{d} = \frac{2\pi}{T_\mathrm{d}} \approx 1.40\ \text{rad/s}.
    $$

    The exact values are \( T_\mathrm{d} = 4.521 \) s and
    \( \omega_\mathrm{d} = 1.390 \) rad/s.

3. The 2% band is \( 8.0 \pm 0.1 \)°. The trace is still outside it at 25 s:
   the sixth overshoot is about 8.1°. The settling time is

    $$
    t_\mathrm{s} \approx \frac{-\ln\!\left(0.02\sqrt{1-\zeta^{2}}\right)}{\zeta\omega_\mathrm{n}} = 23.3\ \text{s},
    $$

    so it only just settles inside the window shown. **The figure does not
    show it settling**, and reading a settling time off a plot that stops too
    early is how settling times get under-reported.

## Q2. Damping, by log decrement {#q2}

1. Measured from the final value of 8.0°:

    $$
    a_1 = 11.42 - 8.0 = 3.42°, \qquad a_2 = 9.60 - 8.0 = 1.60°.
    $$

2. One cycle apart, so

    $$
    \delta = \ln\!\frac{3.42}{1.60} = 0.760,
    \qquad
    \zeta = \frac{0.760}{\sqrt{4\pi^{2} + 0.760^{2}}} = 0.120.
    $$

3. Then

    $$
    \omega_\mathrm{n} = \frac{\omega_\mathrm{d}}{\sqrt{1-\zeta^{2}}}
    = \frac{1.390}{\sqrt{1 - 0.120^{2}}} = 1.40\ \text{rad/s}.
    $$

4. **Because by the eighth peak there is almost nothing left to measure.**
   The swing has decayed to a few hundredths of a degree, which on a real rig
   is the resolution of the encoder. What is left is quantisation noise, and
   noise does not decay: successive "peaks" come out roughly the same height,
   the ratio tends to 1, \( \delta \) tends to 0, and the damping ratio with
   it. Use early peaks, where the signal is large compared with the
   instrument.

    This is also why `fit_second_order` drops any peak below 10% of the first.

## Q3. What proportional gain does, and does not, do {#q3}

1. The loop transfer is \( L(s) = K_\mathrm{p}G(s) \), so the closed loop is
   \( L/(1+L) \) and its denominator is

    $$
    s^{2} + 2\zeta\omega_\mathrm{n}s + \omega_\mathrm{n}^{2} + K_\mathrm{p}K\omega_\mathrm{n}^{2}
    = s^{2} + 2\zeta\omega_\mathrm{n}s + \omega_\mathrm{n}^{2}(1 + KK_\mathrm{p}).
    $$

2. Comparing with \( s^{2} + 2\zeta'\omega_\mathrm{n}'s + \omega_\mathrm{n}'^{2} \):
   the constant term gives
   \( \omega_\mathrm{n}' = \omega_\mathrm{n}\sqrt{1 + KK_\mathrm{p}} \). The
   \( s \) coefficient is unchanged, so
   \( 2\zeta'\omega_\mathrm{n}' = 2\zeta\omega_\mathrm{n} \), giving

    $$
    \zeta' = \zeta\,\frac{\omega_\mathrm{n}}{\omega_\mathrm{n}'} = \frac{\zeta}{\sqrt{1 + KK_\mathrm{p}}}.
    $$

3. With \( K = 2.5 \), \( \omega_\mathrm{n} = 1.4 \), \( \zeta = 0.12 \):

    | \( K_\mathrm{p} \) | \( \zeta' \) | \( \omega_\mathrm{n}' \) | Overshoot | \( t_\mathrm{s} \) (2%) |
    |---|---|---|---|---|
    | 0 | 0.120 | 1.40 | 68.4% | 23.3 s |
    | 1 | 0.064 | 2.62 | 81.7% | 23.3 s |
    | 4 | 0.036 | 4.64 | 89.2% | 23.3 s |

4. **The real part of the poles does not depend on \( K_\mathrm{p} \).** The
   poles are at \( -\zeta'\omega_\mathrm{n}' \pm j\omega_\mathrm{d}' \), and
   \( \zeta'\omega_\mathrm{n}' = \zeta\omega_\mathrm{n} \) whatever the gain,
   so the decay rate is fixed and the settling time with it. On a root locus
   the poles slide straight up a vertical line.

5. **No.** For a quadratic, all coefficients positive is sufficient for
   stability. The \( s \) coefficient is \( 2\zeta\omega_\mathrm{n} > 0 \)
   regardless of \( K_\mathrm{p} \), and the constant term
   \( \omega_\mathrm{n}^{2}(1 + KK_\mathrm{p}) > 0 \) for any
   \( K_\mathrm{p} > 0 \). The loop is stable for every positive gain.

    This is worth noticing, because it means the Ziegler-Nichols rule that
    hunts for an ultimate gain has nothing to find on this plant.

## Q4. Steady-state error {#q4}

1. The error transfer is \( E/R = 1/(1+L) \). By the final value theorem, for
   a unit step,

    $$
    e_\infty = \lim_{s\to 0}\frac{1}{1 + K_\mathrm{p}G(s)} = \frac{1}{1 + K_\mathrm{p}K},
    $$

    since \( G(0) = K \).

2. \( K = 2.5 \), so \( K_\mathrm{p} = 1 \) leaves \( 1/3.5 = 28.6\% \), and
   \( K_\mathrm{p} = 4 \) leaves \( 1/11 = 9.1\% \).

3. From Q3: the damping ratio falls as \( K_\mathrm{p} \) rises, so the
   response overshoots more and oscillates harder; and the settling time does
   not improve at all, so you pay for the smaller error entirely in
   overshoot. On hardware there is a third reason, which is that the motors
   are asked for proportionally more voltage.

4. **Integral action.** Adding \( K_\mathrm{i}/s \) puts a pole at the origin
   in the loop, making it type 1, and a type 1 loop tracks a step with zero
   steady-state error. The integrator keeps accumulating while any error
   remains, so the only steady state it permits is the one with no error.

## Q5. Turning a wish into a requirement {#q5}

There is no single right answer. A good one names a quantity, a number, and a
test. These are defensible:

| Wish | Requirement | Measured how |
|---|---|---|
| "settle quickly" | Settle within 2% of the demand inside 8 s | Step the demand by 7.5°, record, find the last time outside the band |
| "don't overshoot much" | Peak overshoot no more than 20% of the commanded change | Same recording, peak value against final value |
| "accurate" | Steady-state error under 1° thirty seconds after a step | Same recording, mean of the last 5 s against the demand |
| "shouldn't strain the motors" | Peak controller demand no more than 6 V, and no more than 6 sign changes in one step | Log the controller output, not just the angle |

Numbers you had to invent: the 2% band, the 8 s, the 20%, the 1°. The 6 V
is the exception: it is measured, not chosen. The demand saturates 8.6 V
above the trim, and 6 keeps a third of that back.
None comes from the mathematics.

How to find the right values: ask what the machine is for. The settling time
comes from how often the demand changes in service. The overshoot comes from
how much clearance the arm has before it hits something. The voltage comes
from the amplifier's rating and how much of it you are willing to spend. The
honest answer to "where did 8 seconds come from?" is often "we agreed it in
the room", and saying so is better than implying it was derived.

**Always name the band with a settling time.** "Settles in 8 s" is unreadable
without it; 2% and 5% give different numbers for the same response.

## Q6. Do it in MATLAB {#q6}

1. On the supplied recording, by hand gives \( K = 3.41 \),
   \( \omega_\mathrm{n} = 1.047 \), \( \zeta = 0.065 \); `tfest` gives
   \( 3.42 \), \( 1.019 \), \( 0.058 \).

    **The gain agrees best**, to three significant figures, because it depends
    only on where the trace starts and ends and both are easy to read.
    **The damping agrees worst**, by about 11%, because it depends on peak
    heights, and which peaks you keep changes it.

2. \( K \) goes from **3.41 to 4.26**, a change of 25%.

    The arm was already swinging through 4.2° before the step, because
    somebody nudged it and this axis takes about a minute to stop. Averaging
    that whole stretch returns the mean of a partial oscillation, which is
    wherever the cycle happened to be cut off, not the trim. The encoder was
    zeroed against a datum at the start of the record, so the start of the
    record is the trim.

3. They are refused because they **demand 13.6 V for a 7.5° step, against the
   6.0 V the envelope allows**. Everything else about them is good: damping
   0.92, phase margin 57°, settling 4.8 s.

    `pidtune` was not wrong. It optimised for the specification it was given,
    and the amplifier was not in that specification.

    To get an accepted set, ask for less bandwidth. Lower \( K_\mathrm{p} \)
    is the direct lever, since the peak demand is dominated by
    \( K_\mathrm{p} \) acting on the initial error. The pole-placement design
    in `s2_tune`, \( K_\mathrm{p} = 1.10 \), \( K_\mathrm{i} = 0.80 \),
    \( K_\mathrm{d} = 1.14 \), peaks at 7.5 V and is accepted.
