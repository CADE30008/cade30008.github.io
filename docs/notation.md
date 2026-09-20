---
title: Notation
description: Every symbol used in this half of the unit, what it means, and the alternatives you may have met elsewhere.
---

# Notation

Control notation is not standardised. Every textbook makes slightly different
choices, and you will have met some of these symbols under other names. This
page is the list we use, and — just as usefully — **what else the same thing
gets called**, so that a different book or a different lecturer doesn't read as
a different subject.

!!! tip "If a symbol here looks unfamiliar, check the last column"
    It is very likely something you already know, wearing a different hat. That
    is normal, and learning to read across notations is part of becoming
    fluent — you will meet it constantly in papers and datasheets.

## How we chose

**We follow MATLAB.** You will spend more hours reading MATLAB's output than
reading any book, so when MATLAB names something, we use its name: the
controller is `C`, the plant is `G`, a Bode plot's vertical axis is
**magnitude** in decibels.

Where MATLAB is silent we follow Dorf and Bishop, the
[recommended textbook for further reading](reading.md). Where the two disagree
we say so below rather than picking silently.

Two house rules:

- **Descriptive subscripts are upright, variable subscripts are italic.** So
  \(K_\mathrm{p}\) — p is short for "proportional", a label — but \(x_i\), where
  \(i\) is an index that ranges over values. The test: could the subscript be
  replaced by a number? If yes it stays italic.
- **Every question and worked example defines its symbols**, even the obvious
  ones. It costs a line and removes all doubt.
- **An equation always carries its left-hand side.** You will see
  \(\omega_\mathrm{d} = \omega_\mathrm{n}\sqrt{1-\zeta^2}\), never a bare
  \(\omega_\mathrm{n}\sqrt{1-\zeta^2}\) with the name left in the prose.

!!! note "The \((s)\) often goes missing, and that's normal"
    Once it is clear that everything is a function of \(s\), almost everyone
    drops it: \(L = CG\) rather than \(L(s) = C(s)G(s)\), and \(T = L/(1+L)\)
    rather than the full form. We do it too, in slides especially, where space
    is short.

    It means the same thing. Watch for the one place it matters: \(G(0)\) and
    \(G(j\omega)\) are *particular values* of \(G(s)\), so when an argument is
    written explicitly it is usually there for a reason.

## Signals round the loop

| Symbol | Means | Also written |
|---|---|---|
| \(r\), \(R(s)\) | Reference, or setpoint — what you're asking for. | \(y_\mathrm{d}\), \(\theta_\mathrm{ref}\), "command", "demand". |
| \(y\), \(Y(s)\) | Output — what the system actually does. | \(C(s)\) in some books, which we avoid: here \(C\) is the controller. |
| \(e\), \(E(s)\) | Error, \(e = r - y\) for unity feedback. | |
| \(u\), \(U(s)\) | Control signal — what the controller asks the actuator for. | \(m\) in older texts. |
| \(d\), \(D(s)\) | Disturbance — anything that moves the output without being asked. | \(T_\mathrm{d}(s)\) in Dorf, which we avoid because \(T_\mathrm{d}\) is also derivative time. |
| \(n\), \(N(s)\) | Measurement noise — what the sensor adds that isn't real. | |

## Blocks

| Symbol | Means | Also written |
|---|---|---|
| \(G(s)\) | The plant: what you are controlling. | \(P(s)\), \(G_\mathrm{p}(s)\). |
| \(C(s)\) | The controller: what you design. | \(G_\mathrm{c}(s)\) in Dorf, \(K(s)\), \(D(s)\). Note some courses use \(C\) for the *output* — here it is always the controller. |
| \(H(s)\) | The sensor, in the feedback path. Usually 1. | |
| \(L(s) = C(s)G(s)\) | Loop gain, or open-loop transfer function — what you get going once round the loop. | \(G_\mathrm{ol}\), \(GH\). |
| \(T(s)\) | Closed-loop transfer function, reference to output. | Also called the complementary sensitivity, once sensitivity has been introduced. |
| \(S(s)\) | Sensitivity: reference to error, \(S(s) = 1/(1 + L(s))\). It and \(T\) satisfy \(S + T = 1\). | |

## Second-order response

| Symbol | Means | Also written |
|---|---|---|
| \(\zeta\) | Damping ratio. | Universal; no competing symbol. |
| \(\omega_\mathrm{n}\) | Natural frequency, rad/s. | **\(\omega_0\)** and **\(w_\mathrm{n}\)** are both common, and you may well have seen either. |
| \(\omega_\mathrm{d}\) | Damped frequency, \(\omega_\mathrm{d} = \omega_\mathrm{n}\sqrt{1-\zeta^2}\) — the frequency a ringing response actually oscillates at. | |
| \(M_\mathrm{p}\) | Overshoot: how far the step response goes past its final value, as a percentage of it. | **P.O.**, and *percent overshoot* written out. Beware: some books use \(M_\mathrm{p}\) for the *resonant peak* of a frequency response instead, which is a different quantity — context decides. |
| \(t_\mathrm{r}\) | Rise time. | \(T_\mathrm{r}\). |
| \(t_\mathrm{p}\) | Peak time. | \(T_\mathrm{p}\). |
| \(t_\mathrm{s}\) | Settling time, to a 2% band unless said otherwise. | \(T_\mathrm{s}\), which also means sample time — we use \(t_\mathrm{s}\) to keep them apart. |
| \(e_\mathrm{ss}\) | Steady-state error. | \(e(\infty)\). |
| \(y_\mathrm{ss}\) | Steady-state output. | \(y(\infty)\). |

## Controllers

| Symbol | Means | Also written |
|---|---|---|
| \(K_\mathrm{p}\) | Proportional gain. | \(K_P\) uppercase in Dorf and in many courses. Same thing. |
| \(K_\mathrm{i}\) | Integral gain. | \(K_I\). |
| \(K_\mathrm{d}\) | Derivative gain. | \(K_D\). |
| \(T_\mathrm{i}\) | Integral time, \(T_\mathrm{i} = K_\mathrm{p}/K_\mathrm{i}\). | Used in the *standard* form of PID, below. |
| \(T_\mathrm{d}\) | Derivative time, \(T_\mathrm{d} = K_\mathrm{d}/K_\mathrm{p}\). | |
| \(N\) | Derivative filter ratio. We use \(N = 10\) throughout. | \(1/T_\mathrm{f}\) forms appear too. |
| \(K_\mathrm{u}\) | Ultimate gain, in Ziegler–Nichols tuning. | \(K_\mathrm{cr}\), critical gain. |

**Parallel form**, which is what we use and what MATLAB's `pid` object takes:

$$
C(s) = K_\mathrm{p} + \frac{K_\mathrm{i}}{s} + K_\mathrm{d}s.
$$

**Standard form**, which you will meet in industry and in Dorf:

$$
C(s) = K_\mathrm{p}\left(1 + \frac{1}{T_\mathrm{i}s} + T_\mathrm{d}s\right).
$$

Same controller, different parameters, and converting between them is a skill
the unit will ask for.

## Frequency domain

| Symbol | Means | Also written |
|---|---|---|
| \(\omega\) | Frequency, **rad/s** unless stated. | \(f\) in Hz; \(\omega = 2\pi f\). |
| \(\lvert G(j\omega)\rvert\) | **Magnitude** — the vertical axis of a Bode plot, in decibels. | Very often called **gain**, and written "Gain (dB)". We say magnitude, because *gain* is already doing three other jobs: loop gain, DC gain and gain margin. MATLAB and Dorf both label the axis Magnitude. |
| \(\angle G(j\omega)\) | Phase, in degrees. | \(\arg G(j\omega)\), \(\phi\), \(\Phi\). |
| dB | Decibels, \(20\log_{10}\lvert G\rvert\) for a gain. | The \(10\log_{10}\) form is for *power*; we never use it. |
| \(\omega_\mathrm{c}\) | Corner, or break, frequency of a first-order factor: \(\omega_\mathrm{c} = 1/\tau\). | \(\omega_\mathrm{b}\). |
| \(\omega_\mathrm{gc}\) | Gain crossover: where \(\lvert L \rvert = 1\), i.e. 0 dB. | \(\omega_\mathrm{c}\) in some books, which is why we keep \(\omega_\mathrm{c}\) for the corner. |
| \(\omega_\mathrm{pc}\) | Phase crossover: where \(\angle L = -180^\circ\). | \(\omega_{180}\). |
| GM | Gain margin — how much the loop gain can rise before instability. | \(G_\mathrm{m}\), \(K_\mathrm{g}\). |
| PM | Phase margin, in degrees. | \(P_\mathrm{m}\), \(\phi_\mathrm{m}\), \(\gamma\). |

## Laplace and the s-plane

| Symbol | Means | Also written |
|---|---|---|
| \(s = \sigma + j\omega\) | The Laplace variable. | |
| \(j\) | \(\sqrt{-1}\). | \(i\) in mathematics and physics. Engineering uses \(j\) because \(i\) is current. |
| \(X(s)\) | Laplace transform of \(x(t)\). Capital for the transform, lower case for the signal. | \(\mathcal{L}\{x(t)\}\). |
| \(\sigma\) | Real part of a pole — sets how fast a response decays. | |

---

*Found something we use that isn't here, or a name for it we've missed? Tell
me — either way it's a gap worth closing.*
