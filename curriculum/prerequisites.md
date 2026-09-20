# What students arrive with

Derived from the 2025/26 CADE20002 *Dynamics and Control of Linear Systems*
materials — lectures, handbook, example sheets and the assessment. The source
material sits in `private/dcls_2025/`, with a full index there; it is not ours
to publish, so this file carries only our own conclusions.

Re-derive it when DCLS changes. It is the thing every FDAC Control page is
pitched against, so it going stale is expensive.

DCLS has two themes: vibrations and aeroelasticity (Brano Titurus), and signals,
systems and control (Steve Burrow for signals and systems, Yusuf Acar for the
control add-on).

## Assume they can do this

Treat as revision, not as new material. Teaching it again as if it were new
wastes their time and ours.

- **Block diagrams**: reduction, multiple inputs, disturbance paths.
- **Open versus closed loop**, the characteristics of feedback, feedforward.
- **Poles and zeros**, the s-plane, reading stability from pole locations.
- **BIBO stability**, by name.
- **Bode plots** built up from first- and second-order factors, with slopes in
  dB/decade; integrators and differentiators.
- **The standard second-order form**, and reading ζ and ωₙ out of it.
- **Transient metrics**: rise time, peak time, settling time to 2%, maximum
  overshoot, steady-state value.
- **The final value theorem**, and steady-state error for P, PD and PID.
- **PID in parallel form**, and what each term does.
- **Ziegler–Nichols tuning**, both the step-response and the oscillation method.
- **Pole placement by characteristic equation matching.**
- **MATLAB and Simulink** applied to control design.

Their assessment had them design a PID controller for a **double integrator**
under unity feedback, match the closed loop to a standard second-order response
against overshoot and peak-time specifications, then add a lightly damped
flexible mode, tune it by Ziegler–Nichols, and discuss the integral gain.

## They have not met these

Genuinely new in FDAC Control, and worth pitching as such.

- Nyquist, and **stability margins of any kind** — gain margin, phase margin.
- Loop shaping, lead and lag compensation.
- **The sensitivity function**, complementary sensitivity, `S + T = 1`. The word
  "sensitivity" does not appear in the control sense anywhere in DCLS.
- Robustness as a formal idea; model uncertainty.
- State space, controllability, observability, observers, LQR.
- Digital control design. They have sampling and the DFT from the signals half,
  but not discrete-time controller design.
- Identifying a model from measured data, beyond fitting to a known structure.

## Notation

**DCLS is not internally consistent**, so this cannot be a matter of copying
one convention. Where it disagrees with itself, we pick one and say what else
they may have seen.

| Quantity | We write | They wrote | Note |
|---|---|---|---|
| Natural frequency | ωₙ | **ω₀** in signals and vibrations, **wₙ** in Acar's slides, **ωₙ** in the example sheets and the assessment | Ours matches what they were examined on. Say once, at first use, that they may have seen ω₀. |
| Damping ratio | ζ | ζ | Universal. No issue. |
| Damped frequency | ωd | ωd | |
| PID gains | K_P, K_I, K_D | **uppercase in the assessment**, lowercase in Acar's slides | Match the assessment. |
| Controller | C(s) | **C(s) in the assessment; C(s) is the *output* in example sheet C1** | A genuine collision inside DCLS. We use C(s) for the controller and must say so explicitly the first time. |
| Plant | G(s) | G(s), P(s) | |
| Closed loop | T(s) | T(s) | |
| Output | y, Y(s) | Y(s), and C(s) in one sheet | Never use C for an output. |
| Bode ordinate | **gain**, in dB | "Gain dB" nearly always | We had "magnitude". Use gain. |
| Decibels | 20 log₁₀ | 20 log₁₀ only | The power definition, 10 log₁₀, never appears. Don't assume they know it. |
| Transient metrics | Mp, tp, tr, ts, yss | same | ts to a 2% band. |
| Steady-state error | e_ss | ess | |
| Reference | θref, r(t) | θref, r(t) | |
| Ultimate gain | Ku | Ku | Ziegler–Nichols. |

Descriptive subscripts are **upright**, per the house style in
[AGENTS.md](../AGENTS.md). The DCLS assessment does this too in places.

## Textbooks they have already seen

DCLS credits **Dorf and Bishop, *Modern Control Systems*** throughout Acar's
lectures, and **Norman Nise, *Control Systems Engineering*** for the antenna
azimuth and steady-state error material.

Dorf being their text as well as ours is worth saying to students: the sections
on [the textbook page](../docs/reading.md) are a continuation of a book they
have already been pointed at, not a new purchase.
