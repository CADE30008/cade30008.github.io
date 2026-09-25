---
title: "Lecture 1 example sheet: The design cycle, end to end"
description: "About an hour of questions on reading a second-order response, what proportional gain can and cannot do, and turning a vague requirement into a testable one."
lesson: w01-design-cycle
---

# Example sheet: The design cycle, end to end

<div class="lesson-links" markdown>
[Handout](index.md)
[Slides](../slides/w01-design-cycle/index.html)
[Slides (PDF)](../slides/w01-design-cycle/slides.pdf)
[Solutions](solutions.md)
</div>

This sheet takes about an hour. Questions 1 to 5 need a calculator, a ruler and
the figure below. Question 6 needs MATLAB. Try each question before looking at
the [solutions](solutions.md).

The response below is a different machine from the one in the session, with
different numbers. It was recorded by stepping the input by 2.0 V at
\( t = 0 \), and the angle was sitting steady before that.

<figure markdown="span">
  ![A measured angular response to a 2 V step. The trace starts at 3 degrees, rises to a first peak of about 11.4 degrees at about 2.3 seconds, falls to about 5.7 at about 4.5 seconds, and continues oscillating with decreasing amplitude about a final value of 8 degrees, still visibly moving at 25 seconds](figures/example-response.png){ width="100%" }
</figure>

Throughout, the model is

$$
G(s) = \frac{K\,\omega_\mathrm{n}^{2}}{s^{2} + 2\zeta\omega_\mathrm{n}s + \omega_\mathrm{n}^{2}}.
$$

## Q1. Read the gain and the frequency {#q1}

<span class="marks">about 10 min</span>

Use a ruler on the figure. Quote the values you read, not just the answers you
compute from them.

1. What was the angle before the step, and what does it settle to? Hence find
   the steady gain \( K \), in degrees per volt.
2. Read the times of the first two overshoots. Hence find the period of the
   oscillation and the damped natural frequency \( \omega_\mathrm{d} \).
3. Estimate how long the response takes to settle within 2% of its final value.
   Does the figure show it settling?

## Q2. Damping, by log decrement {#q2}

<span class="marks">about 12 min</span>

1. Read the heights of the first two overshoots, measured from the final value
   rather than from zero. Call them \( a_1 \) and \( a_2 \).
2. They are one full cycle apart. The log decrement is
   \( \delta = \ln(a_1/a_2) \). Find it, then find the damping ratio from

    $$
    \zeta = \frac{\delta}{\sqrt{4\pi^{2} + \delta^{2}}}.
    $$

3. Combine with your \( \omega_\mathrm{d} \) from Q1 to find
   \( \omega_\mathrm{n} \).
4. A classmate uses the eighth and ninth peaks instead, on the grounds that
   more of the trace is better. On a real recording their damping ratio comes
   out far too small. Why?

## Q3. What proportional gain does, and does not, do {#q3}

<span class="marks">about 15 min</span>

A proportional controller \( C(s) = K_\mathrm{p} \) is put around this plant.

1. Show that the closed-loop characteristic polynomial is

    $$
    s^{2} + 2\zeta\omega_\mathrm{n}s + \omega_\mathrm{n}^{2}\left(1 + KK_\mathrm{p}\right).
    $$

2. Hence show that the closed-loop natural frequency and damping ratio are

    $$
    \omega_\mathrm{n}' = \omega_\mathrm{n}\sqrt{1 + KK_\mathrm{p}},
    \qquad
    \zeta' = \frac{\zeta}{\sqrt{1 + KK_\mathrm{p}}}.
    $$

3. Using your fitted numbers, complete this table.

    | \( K_\mathrm{p} \) | \( \zeta' \) | \( \omega_\mathrm{n}' \) | Overshoot | \( t_\mathrm{s} \) (2%) |
    |---|---|---|---|---|
    | 0 | | | | |
    | 1 | | | | |
    | 4 | | | | |

4. The settling time barely moves. Explain why, in one sentence, using the
   real part of the closed-loop poles.
5. Can any positive \( K_\mathrm{p} \) make this loop unstable? Justify your
   answer from the characteristic polynomial.

## Q4. Steady-state error {#q4}

<span class="marks">about 8 min</span>

1. For the proportional loop above, show that a unit step demand leaves a
   steady-state error of \( 1/(1 + KK_\mathrm{p}) \).
2. Evaluate it for \( K_\mathrm{p} = 1 \) and \( K_\mathrm{p} = 4 \), using
   your fitted \( K \).
3. Raising \( K_\mathrm{p} \) shrinks this error. Give two reasons from Q3 why
   that is not a good way to remove it.
4. Which term would remove it completely, and why?

## Q5. Turning a wish into a requirement {#q5}

<span class="marks">about 8 min</span>

Each of these appeared in a real design discussion. Rewrite each as a
requirement that can be met, missed, or argued about, and say what you would
measure to decide.

1. "It should settle quickly."
2. "Don't let it overshoot much."
3. "It needs to be accurate."
4. "It shouldn't strain the motors."

For each, state one number you had to invent, and what you would do to find
the right value.

## Q6. Do it in MATLAB {#q6}

<span class="marks">about 10 min</span>

Use the session's files, in `docs/w01-design-cycle/code`.

1. Run `s1_identify` on the recording in `data/elevation-step.mat`. Compare the
   by-hand fit with the one `tfest` returns. Which of the three numbers agree
   best, and which worst?
2. Take the starting trim as the mean of the *whole* stretch before the step,
   instead of the tared start of the record. How much does \( K \) change, and
   why?
3. Run `heli_check_one(2.18, 1.01, 1.18)`. These are the gains `pidtune`
   produces for the rig's fitted model. Why are they refused, and what would
   you change to get a set that is accepted?
