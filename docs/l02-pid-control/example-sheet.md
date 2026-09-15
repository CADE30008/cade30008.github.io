---
title: "Lecture 2 example sheet: PID control"
description: "About an hour of questions on PID control, steady-state error and loop shaping."
lesson: l02-pid-control
---

# Example sheet: PID control

<div class="lesson-links" markdown>
[Handout](index.md)
[Slides](../slides/l02-pid-control/index.html)
[Solutions](solutions.md)
</div>

This sheet takes about an hour. Questions 1 to 5 need only a calculator. Question 6 needs Python with the `control` package, or MATLAB with the Control System Toolbox. Try each question before looking at the [solutions](solutions.md).

Three plants appear:

| Plant | Transfer function | Used in |
|---|---|---|
| UAV pitch attitude from elevator, as in the lecture | \(G(s) = \dfrac{40}{s(s+2)(s+10)}\) | Q2, Q5, Q6 |
| UAV roll attitude from aileron | \(G_\phi(s) = \dfrac{81}{s(s+3)(s+15)}\) | Q3 |
| Multirotor altitude from thrust | \(G_z(s) = \dfrac{1}{m s^2(\tau s + 1)}\) | Q4 |

A useful identity for questions 3 and 4:

$$
\tan(A + B) = \frac{\tan A + \tan B}{1 - \tan A \tan B}.
$$

## Q1. Forms of the PID controller {#q1}

<span class="marks">about 6 min</span>

A controller is given in standard form,

$$
C(s) = K_c\left(1 + \frac{1}{T_i s} + T_d s\right), \qquad K_c = 2,\quad T_i = 4\ \text{s},\quad T_d = 0.25\ \text{s}.
$$

1. Write it in parallel form, \(K_p + K_i/s + K_d s\), and give \(K_p\), \(K_i\) and \(K_d\).
2. Show that the ideal PID controller has two zeros, and find them.
3. The derivative is filtered with \(N = 10\), so that \(T_f = T_d/N\). Where is the filter pole, and what is the controller's gain at high frequency?

## Q2. Steady-state errors on the pitch loop {#q2}

<span class="marks">about 10 min</span>

The pitch loop of the lecture is controlled by proportional control with \(K_p = 1.5\).

1. What is the steady-state attitude error after a step in \(\theta_{ref}\)? Explain using the system type.
2. The aircraft is commanded to pitch over at a steady 2°/s, so \(\theta_{ref} = \Omega t\) with \(\Omega = 2^\circ\)/s. Find the steady-state tracking error.
3. Deploying flap adds a nose-down pitching moment equivalent to 1.5° of elevator. Find the steady-state attitude error it causes.
4. Which of these errors would a PI controller remove? Justify your answer using system type.

## Q3. Proportional design on a roll loop {#q3}

<span class="marks">about 14 min</span>

The roll attitude of a small UAV responds to aileron as \(G_\phi(s) = 81/(s(s+3)(s+15))\), with proportional control \(K_p\).

1. Find the phase-crossover frequency \(\omega_{180}\), and the gain margin when \(K_p = 1\).
2. Find the crossover frequency and the value of \(K_p\) that give a 45° phase margin.
3. Estimate the step overshoot for the design in part 2, using the rule of thumb from the lecture.
4. Repeat part 2 for a 60° phase margin. Estimate how much slower the step response becomes.

## Q4. Multirotor altitude hold {#q4}

<span class="marks">about 16 min</span>

A multirotor of mass \(m = 1.5\) kg holds altitude by adjusting its total thrust. The motors lag their commands with a time constant \(\tau = 0.05\) s. About hover, the altitude \(z\) responds to a thrust change \(\delta T\) as

$$
G_z(s) = \frac{z(s)}{\delta T(s)} = \frac{1}{m s^2(\tau s + 1)}.
$$

1. Show that no proportional gain can stabilise the altitude. You can use either the Bode phase or the characteristic polynomial.
2. Design an ideal PD controller, \(K_p(1 + T_d s)\), for crossover at 4 rad/s with a 45° phase margin. Give \(K_p\) in N/m and \(K_d\) in N s/m.
3. The hover-thrust estimate is 5% of the weight too low, for example because of battery sag. Find the steady-state altitude error with your PD controller.
4. Add integral action with \(T_i = 2.5\) s. How much phase does it cost at 4 rad/s? Show that raising \(T_d\) to 0.4 s restores the 45° margin without changing \(K_p\).
5. Explain physically why the derivative term is essential for this plant, and which sensor it would use in practice.

## Q5. Kick, noise and windup {#q5}

<span class="marks">about 8 min</span>

Use the lecture's PID design: \(K_p = 2.03\), \(K_i = 0.678\), \(K_d = 0.661\), \(N = 10\).

1. With the derivative acting on the error, what elevator demand appears the instant a 5° attitude step is commanded? What is it with the derivative acting on the measurement?
2. The attitude estimate carries 0.1° of high-frequency noise. Up to how much elevator jitter can the filtered derivative produce if it acts on that estimate? The rate gyro has 0.5°/s of noise. How much elevator jitter results if the derivative uses the gyro instead?
3. The elevator saturates during a large attitude command. Describe, in order, what happens to the integrator, and explain how conditional integration prevents the resulting overshoot.

## Q6. Trading speed for actuator demand {#q6}

<span class="marks">about 15 min</span>

A different airframe uses the same pitch dynamics, but its elevator can move only ±15°. You keep the shape of the lecture's PID design, and scale all three gains by the same factor \(k\).

1. Run the starter code. Confirm that the lecture design gives a 55.0° phase margin at 3.00 rad/s, and that a 10° attitude step demands 20.4° of elevator.
2. Find the largest \(k\), to two decimal places, for which the phase margin is at least 50° and the peak elevator demand for a 10° step is at most 15°. Report the crossover frequency, phase margin, peak elevator and overshoot.
3. The controller's shape doesn't change with \(k\), yet the phase margin does. Explain why.

=== "Python"

    ```python
    --8<-- "l02-pid-control/code/q6_starter.py"
    ```

=== "MATLAB"

    ```matlab
    --8<-- "l02-pid-control/code/q6_starter.m"
    ```
