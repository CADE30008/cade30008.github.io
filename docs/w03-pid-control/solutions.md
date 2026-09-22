---
title: "Week 3 solutions: PID, properly"
description: "Worked solutions to the week 3 example sheet."
lesson: w03-pid-control
---

# Solutions: PID, properly

<div class="lesson-links" markdown>
[Example sheet](example-sheet.md)
[Handout](index.md)
[Slides](../slides/w03-pid-control/index.html)
[Slides (PDF)](../slides/w03-pid-control/slides.pdf)
</div>

These are worked solutions to the [example sheet](example-sheet.md). Every number here has been checked by simulation.

## Q1. Forms of the PID controller {#q1}

1. Expanding the standard form gives \(K_\mathrm{p} = K_\mathrm{c} = 2\), \(K_\mathrm{i} = K_\mathrm{c}/T_\mathrm{i} = 0.5\ \text{s}^{-1}\) and \(K_\mathrm{d} = K_\mathrm{c}T_d = 0.5\) s.
2. Over a common denominator,.

    $$
    C(s) = K_\mathrm{c}\,\frac{T_\mathrm{i}T_d s^2 + T_\mathrm{i} s + 1}{T_\mathrm{i} s} = \frac{2(s^2 + 4s + 1)}{4s},
    $$

    since \(T_\mathrm{i}T_d = 1\). The zeros are the roots of \(s^2 + 4s + 1 = 0\), which are \(s = -2 \pm \sqrt{3}\). That is \(s = -0.268\) and \(s = -3.732\).

3. The filter pole is at \(s = -N/T_\mathrm{d} = -40\) rad/s. At high frequency the derivative term tends to \(K_\mathrm{d}/T_\mathrm{f} = K_\mathrm{c}N\). The total gain is therefore \(K_\mathrm{c}(N + 1) = 22\).

## Q2. Steady-state errors on the pitch loop {#q2}

1. **Zero.** The plant contains an integrator, so the loop is type 1, and a type 1 loop tracks a step with zero steady-state error.
2. The velocity constant is.

    $$
    K_\mathrm{v} = \lim_{s\to 0} sL(s) = K_\mathrm{p}\,\frac{40}{2 \times 10} = 2K_p = 3\ \text{s}^{-1}.
    $$

    The ramp error is therefore \(\Omega/K_\mathrm{v} = 2/3 = 0.67^\circ\). The attitude lags the command by about two-thirds of a degree.

3. The disturbance enters before the plant's integrator:

    $$
    \theta_\mathrm{ss} = \lim_{s\to 0}\frac{G(s)}{1 + K_\mathrm{p}G(s)}\,d = \frac{d}{K_\mathrm{p}} = \frac{1.5^\circ}{1.5} = 1.0^\circ,
    $$

    in the nose-down sense of the disturbance.

4. **All three.** A PI controller adds an integrator ahead of the disturbance, so the loop becomes type 2. A type 2 loop tracks steps and ramps with zero error. The controller's integrator also drives the disturbance error to zero.

## Q3. Proportional design on a roll loop {#q3}

1. The phase is −180° where \(\tan^{-1}(\omega/3) + \tan^{-1}(\omega/15) = 90^\circ\). That needs \((\omega/3)(\omega/15) = 1\), so \(\omega_{180} = \sqrt{45} = 6.71\) rad/s. There.

    $$
    |G_\phi(j\omega_{180})| = \frac{81}{\sqrt{45}\,\sqrt{54}\,\sqrt{270}} = \frac{81}{810} = 0.1,
    $$

    so the gain margin with \(K_\mathrm{p} = 1\) is 10, or 20 dB.

2. A 45° phase margin needs \(\tan^{-1}(\omega/3) + \tan^{-1}(\omega/15) = 45^\circ\). Using the tangent identity,.

    $$
    \frac{\omega/3 + \omega/15}{1 - \omega^2/45} = 1 \quad\Rightarrow\quad \omega^2 + 18\omega - 45 = 0,
    $$

    so \(\omega_\mathrm{c} = 2.23\) rad/s. Then

    $$
    K_\mathrm{p} = \frac{\omega_\mathrm{c}\sqrt{\omega_\mathrm{c}^2 + 9}\,\sqrt{\omega_\mathrm{c}^2 + 225}}{81} = 1.56.
    $$

    The gain margin falls to \(10/1.56 = 6.4\), or 16.2 dB.

3. With \(\zeta \approx 0.45\), the rule of thumb predicts \(M_\mathrm{p} = e^{-\pi\zeta/\sqrt{1-\zeta^2}} = 20.5\%\). Simulation gives 23.3%.

4. A 60° margin needs the two lags to sum to 30°:

    $$
    \frac{0.4\,\omega}{1 - \omega^2/45} = \tan 30^\circ = 0.577 \quad\Rightarrow\quad \omega_\mathrm{c} = 1.38\ \text{rad/s},
    $$

    and \(K_\mathrm{p} = 0.849\), about 45% less gain. Rise time scales as \(1/\omega_\mathrm{c}\), so the response should be about \(2.23/1.38 = 1.61\) times slower. Simulation gives rise times of 0.54 s and 0.92 s, a ratio of 1.70. The overshoot falls to 8.1%.

## Q4. Multirotor altitude hold {#q4}

1. With \(C = K_\mathrm{p}\), the loop phase is \(-180^\circ - \tan^{-1}(\omega\tau)\). That is below −180° at every frequency, so no gain gives a positive phase margin. The characteristic polynomial tells the same story. It is \(m\tau s^3 + m s^2 + K_\mathrm{p} = 0\), which has no \(s^1\) term, so by the Routh criterion it is unstable for every \(K_\mathrm{p}\).

2. At 4 rad/s the plant phase is \(-180^\circ - \tan^{-1}(0.2) = -191.3^\circ\). The controller must supply \(45^\circ + 11.3^\circ = 56.3^\circ\) of lead. Conveniently,.

    $$
    \tan(56.3^\circ) = \tan(45^\circ + 11.3^\circ) = \frac{1 + 0.2}{1 - 0.2} = 1.5,
    $$

    so \(4T_d = 1.5\) and \(T_\mathrm{d} = 0.375\) s. The plant gain at 4 rad/s is

    $$
    |G_z(j4)| = \frac{1}{1.5 \times 16 \times \sqrt{1 + 0.04}} = 0.0409,
    $$

    and \(|1 + j1.5| = 1.80\). Setting \(|L(j4)| = 1\) gives \(K_\mathrm{p} = 13.6\) N/m and \(K_\mathrm{d} = K_\mathrm{p}T_d = 5.09\) N s/m.

    A practical controller filters the derivative. With \(N = 20\) the margin drops to 42°, so leave a few degrees in hand.

3. The thrust shortfall is \(\Delta T = 0.05 \times 1.5 \times 9.81 = 0.736\) N. It enters before the plant's double integrator, so the PD controller settles with \(z_\mathrm{ss} = \Delta T/K_\mathrm{p} = 0.054\) m. The multirotor hovers 5.4 cm low.

4. The integral term costs \(\tan^{-1}\!\big(1/(4 \times 2.5)\big) = 5.7^\circ\) at 4 rad/s. For the ideal PID,.

    $$
    \frac{C(j4)}{K_\mathrm{p}} = 1 + \frac{1}{j4T_i} + j4T_d = 1 + j\,(4T_d - 0.1).
    $$

    With \(T_\mathrm{d} = 0.4\) s this is \(1 + j1.5\), exactly as for the PD design. Both phase and magnitude at 4 rad/s are unchanged, so the phase margin is 45° with the same \(K_\mathrm{p} = 13.6\) N/m. That gives \(K_\mathrm{i} = K_\mathrm{p}/T_\mathrm{i} = 5.43\) N/(m s) and \(K_\mathrm{d} = 5.43\) N s/m. The altitude offset is now removed.

    !!! note "A gain margin below 1 doesn't mean unstable here"
        With three integrators in \(L\), the phase starts at −270°, so it crosses −180° at 1.07 rad/s, below crossover. Python and MATLAB report this as a gain margin of 0.126, or −18 dB. That is a **gain-reduction** margin: cutting the gain by a factor of 8 would destabilise the loop. The closed-loop poles confirm the design is stable. The slowest has real part −0.48.

5. Altitude is a double integrator of thrust, with no drag term to provide damping. Proportional control acts like a spring, and with the motor lag the oscillation grows. The derivative term supplies the missing damping, which is vertical-velocity feedback. In practice it uses the vertical speed from the state estimator, which fuses the barometer, accelerometers and GNSS. Differentiating a noisy altitude signal would not work well.

## Q5. Kick, noise and windup {#q5}

1. With D on the error, the first-instant demand is \(K_\mathrm{p}(N + 1)\,\Delta\theta_\mathrm{ref} = 2.03 \times 11 \times 5^\circ = 112^\circ\). The elevator slams to its 20° stop. With D on the measurement only the proportional term reacts, giving \(K_\mathrm{p}\,\Delta\theta_\mathrm{ref} = 10.2^\circ\).
2. At high frequency the filtered derivative acting on attitude has gain \(K_\mathrm{p}N = 20.3\), and the whole controller \(K_\mathrm{p}(N+1) = 22.3\). So 0.1° of attitude noise can produce up to about 2.2° of elevator jitter. Using the gyro, the derivative path multiplies pitch rate by \(K_\mathrm{d} = 0.661\) s. So 0.5°/s of gyro noise gives only about 0.33° of elevator jitter.
3. The sequence runs like this:
    1. The large error drives the elevator to its limit.
    2. The attitude responds at the rate the saturated elevator allows. The error stays large, and the integrator keeps accumulating.
    3. When the attitude reaches the target, the integrator holds far more than the trim needs. The elevator stays deflected past the point where it should reverse.
    4. The attitude overshoots until the error has been negative long enough to unwind the integrator.

    Conditional integration stops the integrator whenever the elevator is saturated and the error would push it further into the limit. The integrator then holds only what it needs when the elevator comes off the stop. For a 25° step with a ±20° limit, it cuts the overshoot from 25.4% to 8.7%.

## Q6. Trading speed for actuator demand {#q6}

1. The starter code prints a 55.0° phase margin at 3.00 rad/s and a peak elevator demand of 20.4° for a 10° step, matching the lecture.
2. The largest scaling is \(k = 0.73\), which gives \(K_\mathrm{p} = 1.48\), \(K_\mathrm{i} = 0.495\) and \(K_\mathrm{d} = 0.483\). It crosses over at 2.30 rad/s with a 57.6° phase margin. The peak elevator demand for a 10° step is 14.9°, and the overshoot is 22.0%. The elevator limit is the binding constraint, since the phase margin never falls below 50° in this range.
3. Scaling every gain by \(k\) slides \(|L(j\omega)|\) up or down, but leaves \(\angle L(j\omega)\) unchanged at every frequency. What changes is *where* the loop crosses over. Crossover moves down to 2.30 rad/s, where the plant has less lag, so the phase margin rises. The overshoot rises too, even though the margin improves. The PI zero stays at 0.33 rad/s, which is now only 7 times below crossover instead of 9, so the reference sees more of it.

=== "MATLAB"

    ```matlab
    --8<-- "w03-pid-control/code/q6_solution.m"
    ```

=== "Python"

    ```python
    --8<-- "w03-pid-control/code/q6_solution.py"
    ```

