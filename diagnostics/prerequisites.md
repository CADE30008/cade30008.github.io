# Prerequisite diagnostic — READ THIS ONE, UPLOAD THE OTHER

**Not the upload file.** This is the readable draft. The file to upload to
Numbas is `prerequisites.exam`, beside it. Uploading this one gives
"Didn't parse all input at line 1".


> Generated from `prerequisites.yaml` by `npm run numbas`. Every numerical
> answer is recomputed with python-control on each build rather than typed, so
> a wrong number fails the build instead of reaching a student.

**Purpose.** Formative — it doesn't contribute to the unit grade. It tells each
student where they're solid and where to brush up, and tells us what to spend
time on in the first weeks. About 20 minutes, ten questions, on the mathematics
and control the unit builds on.

**This is published deliberately, answers and all.** Numbas shows the correct
answer and the feedback after each question anyway, there is no randomisation,
and students are welcome to sit it together — so publishing the source changes
who can read the answers by very little, and what the quiz is *for* survives it.
A student who looks the answers up has opted out of finding out where their gaps
are, which costs nobody else anything. Reuse it: it is CC BY like the rest of
the teaching material. See ASSESSMENT.md, "What gets published".

**Feedback is in two layers, both shown whatever the student answered.** Each
option carries its own line, right and wrong alike, so a student who guessed
correctly learns why it was right and a student who missed it is told *which
misconception they have* rather than only that they erred. Under that sits the
worked route, as steps.

**Every wrong option is a real mistake someone makes** — positive feedback in
Q6, the power definition of the decibel in Q9, the sensitivity function mistaken
for the complementary one in Q6. None is filler, and that is what makes the
cohort results diagnostic rather than a score: if thirty people pick \( S \)
instead of \( T \), that's a lecture to give. `npm run numbas` refuses to build
if any option has no feedback.

**Build it in Numbas**, which is integrated with Blackboard. Add it through the
Numbas link so it ticks the progress circle when submitted.

Settings to use:

- **Not counted towards the grade**, or its column hidden from students: it
  must not look as though it counts.
- **One attempt.** It's a baseline; a second attempt after seeing the answers
  measures memory of the answers.
- **Feedback and the correct answer after each question**, which is what Numbas
  is good at.
- No time limit. Due before the week 1 lecture, but accept late.
- Numeric questions: **number entry** with the tolerance given below. Multiple
  choice for the rest.

**No randomisation** (AP11, 20 September). Every student gets the same
questions. They are trusted to use the quiz as they see fit, including sitting
together and working through it — it is formative, and none of it counts.
Randomised values are reserved for assessed work, of which this half currently
has one piece: the week 11 coursework.

---

## The questions

Generated from `prerequisites.yaml` by `npm run numbas`. Edit the YAML, not
this list; the same source builds the `.exam` file.

<!-- questions:start -->
### 1. From an equation to a transfer function

A system obeys \( \dot y + 2y = u \), starting from rest, so that \( y(0) = 0 \), where \( u \) is the input and \( y \) the output. What is its transfer function \( \dfrac{Y(s)}{U(s)} \)?

- \( \dfrac{1}{s+2} \) **← correct**
    <br>*Shown if chosen:* **\( \dfrac{1}{s+2} \):** Right. Every term transforms, the \( s \) stays with \( Y \) on the left, and what's left on top is the coefficient of \( u \).
- \( \dfrac{s}{s+2} \)
    <br>*Shown if chosen:* **\( \dfrac{s}{s+2} \):** The \( s \) from \( \dot y \) has ended up in the numerator. It belongs with \( y \): the left-hand side collects to \( (s+2)Y \), so the numerator is whatever multiplies \( u \), which here is 1.
- \( \dfrac{2}{s+2} \)
    <br>*Shown if chosen:* **\( \dfrac{2}{s+2} \):** The denominator is right, so the left-hand side was collected correctly. The numerator has come from the coefficient of \( y \) instead of the coefficient of \( u \). It is whatever multiplies the *input*, which here is 1.
- \( s + 2 \)
    <br>*Shown if chosen:* **\( s+2 \):** That's the characteristic polynomial, or equivalently \( \dfrac{U}{Y} \): the right answer upside down. A transfer function is always output over input.

*Checks:* Laplace transform of a derivative with zero initial conditions

*Worked route, shown to everyone:*

- Transform every term, using \( \dot y \to sY \) because the system starts from rest. That gives \( sY + 2Y = U \).
- Collect \( Y \): \( (s+2)Y = U \).
- Divide: \( \dfrac{Y}{U} = \dfrac{1}{s+2} \).

The denominator, \( s+2 \), is the characteristic polynomial, and its root
\( s = -2 \) is the pole. You will do this for every block diagram in the
unit, so practise until it is quick.

<details><summary><em>Full working, folded away in the quiz</em></summary>

**1. Transform the equation, because it turns calculus into algebra.**

A differential equation ties a quantity to its own slope, which is awkward
to rearrange. The Laplace transform turns differentiation into
multiplication by \( s \), so the equation becomes something you can move
around like any other. There is one rule to remember:

$$ \mathcal{L}\{\dot y(t)\} = sY(s) - y(0), $$

and everything without a dot on it simply changes case:
\( y(t) \to Y(s) \) and \( u(t) \to U(s) \).

**2. Apply \( y(0) = 0 \).**

The \( -y(0) \) term disappears, leaving
\( \mathcal{L}\{\dot y\} = sY(s) \). That condition is in the question for
a reason: without it there is no single transfer function to find, because
the answer would depend on where the system happened to start. A transfer
function describes the system, not the situation it was in.

**3. Transform the whole equation.**

$$ \dot y + 2y = u \quad \longrightarrow \quad sY(s) + 2Y(s) = U(s). $$

**4. Collect the output terms.**

Both terms on the left have \( Y(s) \) in them, so take it outside:

$$ (s + 2)\,Y(s) = U(s). $$

**5. Divide to get output over input.**

$$ \dfrac{Y(s)}{U(s)} = \dfrac{1}{s+2}. $$

**6. Check it.** Two quick tests. Do both every time.

- **Shape.** One derivative of \( y \) should give one power of \( s \) in
  the denominator. It does.
- **Steady state.** Set \( s = 0 \) to get \( \dfrac{Y}{U} = \dfrac{1}{2} \), so a steady
  input of 1 settles the output at 0.5. Setting \( \dot y = 0 \) in the
  original equation gives \( 2y = u \), and so \( y = 0.5 \). They agree.

</details>

### 2. Poles and what they mean

A system has transfer function \( G(s) = \dfrac{5}{s^2 + 2s + 5} \), whose poles are at \( -1 \pm 2j \). Its step response is:

- unstable
    <br>*Shown if chosen:* **Unstable:** Stability is decided by the *real* part, and here it is \( -1 \). A complex pole isn't unstable in itself: it's what makes a response oscillate rather than what makes it grow.
- stable, and settles without oscillating
    <br>*Shown if chosen:* **Stable, no oscillation:** The stability half is right, but the \( \pm 2j \) has been dropped. A non-zero imaginary part means the response oscillates on its way in, here at 2 rad/s.
- stable, with a decaying oscillation **← correct**
    <br>*Shown if chosen:* **Stable, decaying oscillation:** Right, and you read both halves. Real part negative, so it decays; imaginary part non-zero, so it oscillates while decaying.
- an oscillation that never decays
    <br>*Shown if chosen:* **Never decays:** That needs the poles *on* the imaginary axis, at \( \pm 2j \) with no real part at all. The \( -1 \) is what makes it die away.

*Checks:* reading stability and oscillation from pole locations

*Worked route, shown to everyone:*

Read a complex pair \( \sigma \pm j\omega_\mathrm{d} \) as two separate facts:

- **the real part \( \sigma \) sets the envelope.** Negative decays like \( e^{\sigma t} \), positive grows, zero neither.
- **the imaginary part \( \omega_\mathrm{d} \) sets the oscillation.** Non-zero means it oscillates at \( \omega_\mathrm{d} \) rad/s; zero means it doesn't.

Here \( \sigma = -1 \) and \( \omega_\mathrm{d} = 2 \), so the response oscillates at
2 rad/s inside an \( e^{-t} \) envelope, most of it gone within about four
seconds. That is case 1 in the figure below, and each of the other three
is one of the answers you could have chosen.

The numerator does not change that shape, but it does set where the
response ends up. Putting \( s = 0 \) gives \( G(0) = \dfrac{5}{5} = 1 \), so
by the final value theorem the step settles at exactly 1. The poles say
what it does on the way; the DC gain says where it stops.

### 3. Natural frequency and damping ratio

A system has transfer function \( G(s) = \dfrac{25}{s^2 + 4s + 25} \). Comparing it with the standard second-order form \( G(s) = \dfrac{\omega_\mathrm{n}^2}{s^2 + 2\zeta\omega_\mathrm{n}s + \omega_\mathrm{n}^2} \), give the natural frequency \( \omega_\mathrm{n} \), in rad/s, and the damping ratio \( \zeta \).

- \( \omega_\mathrm{n} \) (rad/s): **5** (tolerance ±0.01)
- \( \zeta \): **0.4** (tolerance ±0.01)
- *Common error* \( \omega_\mathrm{n} = 25 \): that's \( \omega_\mathrm{n}^2 \). The constant term is the square, so take the root.
- *Common error* \( \zeta = 0.16 \): you divided 4 by \( \omega_\mathrm{n}^2 \). The middle coefficient is \( 2\zeta\omega_\mathrm{n} \), so divide by \( 2\omega_\mathrm{n} = 10 \).
- *Common error* \( \zeta = 0.8 \): you divided by \( \omega_\mathrm{n} \) but not by the 2. It is easy to lose; the factor of 2 is there so that \( \zeta = 1 \) is exactly critical damping.
- *Common error* \( \zeta = 2 \): that's \( \zeta\omega_\mathrm{n} \), which is the decay rate \( \sigma \), a useful number, but not the damping ratio.

*Checks:* the standard second-order form

*Worked route, shown to everyone:*

Match the denominator against the standard form
\( s^2 + 2\zeta\omega_\mathrm{n} s + \omega_\mathrm{n}^2 \), one coefficient at a time:

- **constant term:** \( \omega_\mathrm{n}^2 = 25 \), so \( \omega_\mathrm{n} = 5 \) rad/s.
- **middle term:** \( 2\zeta\omega_\mathrm{n} = 4 \), and \( \omega_\mathrm{n} \) is now known, so \( \zeta = \dfrac{4}{2 \times 5} = 0.4 \).

Always do them in that order, because the middle term needs \(
\omega_\mathrm{n} \) and there is nothing to be gained by starting
there. A quick check: \( \zeta \)
between 0 and 1 means an oscillatory response, which matches the complex
poles this denominator has.

### 4. Overshoot

A second-order system with damping ratio \( \zeta = 0.4 \) is given a step input. Its overshoot (how far the response goes past its final value, as a percentage of it) is closest to:

- 5%
    <br>*Shown if chosen:* **5%:** That's roughly \( \zeta = 0.7 \), the value often quoted as a good compromise, so it is an easy one to reach for. This system is less damped than that.
- 10%
    <br>*Shown if chosen:* **10%:** That's roughly \( \zeta = 0.6 \). You're in the right region but a little too damped; the relationship is steep here, so small changes in \( \zeta \) move the overshoot a lot.
- 25% **← correct**
    <br>*Shown if chosen:* **25%:** Right. \( M_\mathrm{p} = 25.4\% \), and the useful thing to carry away is the pairing: \( \zeta = 0.4 \) with about a quarter overshoot.
- 50%
    <br>*Shown if chosen:* **50%:** That's roughly \( \zeta = 0.2 \), considerably livelier than this. Half the height of the step as overshoot would be a very underdamped system.

*Checks:* the link between damping and overshoot

*Worked route, shown to everyone:*

Exactly, \( M_\mathrm{p} = e^{-\pi\zeta/\sqrt{1-\zeta^2}} \), which for
\( \zeta = 0.4 \) gives 0.254, so about 25%.

You may have met this written as
\( M_\mathrm{p} = 100e^{-\zeta\omega_\mathrm{n}t_\mathrm{p}}\% \), which is
the same thing: substitute the peak time
\( t_\mathrm{p} = \dfrac{\pi}{\omega_\mathrm{d}} \) and the
\( \omega_\mathrm{n} \) cancels, leaving the form above. That version
needs the peak time first; this one does not, which is why it is the one
worth remembering.

In practice nobody evaluates that in a design meeting. Carry three anchors
instead and interpolate:

- \( \zeta = 0.2 \) → about 50%
- \( \zeta = 0.4 \) → about 25%
- \( \zeta = 0.7 \) → about 5%

Less damping, more overshoot, and the curve is steep. That steepness is
why phase margin, the frequency-domain cousin of damping, is worth watching
closely once we get to it.

### 5. Steady state

A system has transfer function \( G(s) = \dfrac{3}{s+2} \). What value does its response to a unit step settle to?

- final value: **1.5** (tolerance ±0.01)
- *Common error* 3: you took the numerator alone. Setting \( s = 0 \) leaves the denominator's constant term too, so it's \( \dfrac{3}{2} \), not 3.
- *Common error* 0: you may have applied \( \lim_{s \to 0} sG(s) \), which is the final value of the *impulse* response. For a step the \( s \) in the theorem cancels the \( \dfrac{1}{s} \) of the step itself.
- *Common error* 0.667: that's \( \dfrac{2}{3} \), the right two numbers inverted.

*Checks:* the final value theorem, or DC gain

*Worked route, shown to everyone:*

The steady-state value of a step response is just \( G(0) \), the DC gain.
Set \( s = 0 \): \( G(0) = \dfrac{3}{2} = 1.5 \).

If you would rather use the final value theorem, the step is \( \dfrac{1}{s} \), so

$$ \lim_{s\to0} s \cdot G(s) \cdot \dfrac{1}{s} = \lim_{s\to0} G(s) = G(0). $$

The \( s \) and the \( \dfrac{1}{s} \) cancel, which is why the shortcut works. The
theorem is only valid when the response actually settles, so check the poles are in the left half-plane first. Here the single pole
is at \( s = -2 \), so it does.

### 6. Closing the loop

A plant \( G(s) = \dfrac{4}{s(s+1)} \) is put in a unity negative feedback loop, with reference \( R(s) \) and output \( Y(s) \). The closed-loop transfer function \( T(s) = \dfrac{Y(s)}{R(s)} \) is:

- \( \dfrac{4}{s^2 + s + 4} \) **← correct**
    <br>*Shown if chosen:* **\( \dfrac{4}{s^2+s+4} \):** Right. \( T = \dfrac{G}{1+G} \), then multiply top and bottom by \( s(s+1) \) to clear the fraction within a fraction.
- \( \dfrac{4}{s^2 + s - 4} \)
    <br>*Shown if chosen:* **\( \dfrac{4}{s^2+s-4} \):** A sign error: this is \( \dfrac{G}{1-G} \), which is *positive* feedback. The sign is the whole point: this version has a pole in the right half-plane and would run away.
- \( \dfrac{4}{s^2 + s} \)
    <br>*Shown if chosen:* **\( \dfrac{4}{s^2+s} \):** That's the open loop \( G \) with its denominator multiplied out. The loop hasn't been closed: there is no \( +4 \) contributed by the feedback path.
- \( \dfrac{s^2 + s}{s^2 + s + 4} \)
    <br>*Shown if chosen:* **\( \dfrac{s^2+s}{s^2+s+4} \):** Very close, and worth having derived: that is the transfer function from the reference to the **error**, \( \dfrac{E}{R} = \dfrac{1}{1+G} \), not to the output. The question asked for reference to output, which is \( T = \dfrac{G}{1+G} \). The two add to one. They have names: \( S \) for the sensitivity, which is this one, and \( T \) for the complementary sensitivity, which is the closed loop. \( S + T = 1 \) always, and much of control design is deciding where to spend that one.

*Checks:* \( \dfrac{G}{1+G} \), the step everything in the unit builds on

*Worked route, shown to everyone:*

- Write the closed-loop form: \( T = \dfrac{G}{1+G} \).
- Substitute: \( T = \dfrac{\frac{4}{s(s+1)}}{1 + \frac{4}{s(s+1)}} \).
- Multiply top and bottom by \( s(s+1) \): \( T = \dfrac{4}{s(s+1) + 4} = \dfrac{4}{s^2+s+4} \).

Two habits that save time later. **The closed-loop denominator is
\( 1 + G \) cleared of fractions**, so you can often write it down without
the algebra. And **the numerator of \( T \) is the numerator of \( G \)**,
unchanged: feedback moves poles, never zeros.

This one has \( \omega_\mathrm{n} = 2 \) and \( \zeta = 0.25 \), so expect a lively
response with around 45% overshoot. The Quanser rig in the first session is
far less damped still.

### 7. Steady-state error

The same unity negative feedback loop, but with a plant \( G(s) = \dfrac{4}{s+1} \). After a unit step in the reference \( R(s) \), what steady-state error \( e_\mathrm{ss} \) remains?

- steady-state error: **0.2** (tolerance ±0.01)
- *Common error* 0.25: you used \( \dfrac{1}{G(0)} \). The formula is \( \dfrac{1}{1+G(0)} \), and that extra 1 is the reference itself, since the error is what the reference asks for minus what the loop delivers.
- *Common error* 0.8: that's the steady-state *output*, \( \dfrac{G(0)}{1+G(0)} \). The error is what's left over: \( 1 - 0.8 = 0.2 \).
- *Common error* 0: that would need an integrator in the loop. This plant has none: a pole at \( s = -1 \), not at the origin, so a finite error survives.

*Checks:* steady-state error of a type 0 loop, and why integral action exists

*Worked route, shown to everyone:*

- For unity feedback, the error transfer function is \( \dfrac{E}{R} = S = \dfrac{1}{1+G} \).
- A unit step's final error is therefore \( e_\mathrm{ss} = \dfrac{1}{1+G(0)} \).
- Here \( G(0) = 4 \), so \( e_\mathrm{ss} = \dfrac{1}{5} = 0.2 \), a 20% error that never goes away.

**Why it matters.** The only way to drive that to zero is to make
\( G(0) \) infinite, which means putting an integrator in the loop: a pole
at \( s = 0 \). That is exactly what the I in PID does, and it is the
reason integral action exists at all rather than being an optional extra.

Raising the gain instead shrinks the error but never removes it, and costs
you damping on the way. That trade returns in almost every week of this
unit.

### 8. Reading a Bode plot

A system has transfer function \( G(s) = \dfrac{10}{s+10} \). At a frequency \( \omega = 10 \) rad/s, what are the magnitude of \( G(j\omega) \), in decibels, and its phase?

- 0 dB, 0°
    <br>*Shown if chosen:* **0 dB, 0°:** Those are the low-frequency values, well *below* the corner. At \( \omega = 10 \) you are standing exactly on the corner, where the asymptotes meet and neither one is accurate.
- −3 dB, −45° **← correct**
    <br>*Shown if chosen:* **−3 dB, −45°:** Right, and these two numbers travel together: every first-order corner is −3 dB and −45°, whatever the frequency. Worth memorising as a pair.
- −6 dB, −90°
    <br>*Shown if chosen:* **−6 dB, −90°:** −90° is the high-frequency limit, only approached well *above* the corner. At the corner the phase is exactly halfway there.
- −20 dB, −45°
    <br>*Shown if chosen:* **−20 dB, −45°:** The phase is right. −20 dB is the magnitude a *decade* above the corner, at \( \omega = 100 \), once the −20 dB/decade slope has had a full decade to act.

*Checks:* the corner frequency of a first-order lag

*Worked route, shown to everyone:*

A first-order lag \( \dfrac{1}{1 + s/\omega_\mathrm{c}} \) has three landmarks:

- **well below \( \omega_\mathrm{c} \):** 0 dB and 0°. The system passes the signal through.
- **at \( \omega_\mathrm{c} \):** \( |G| = \dfrac{1}{\sqrt2} \), which is −3 dB, and the phase is exactly −45°, halfway to its limit.
- **well above \( \omega_\mathrm{c} \):** falling at −20 dB/decade, phase heading to −90°.

Here \( G = \dfrac{10}{s+10} = \dfrac{1}{1 + s/10} \), so \( \omega_\mathrm{c} = 10 \) rad/s and
the question is asking for the corner itself.

**−3 dB and −45° at the corner is the single most reused fact in this
unit.** Every lag you meet in weeks 4 and 8 is built from it.

### 9. Decibels

A gain is quoted as 20 dB. As a plain multiplying factor, that is:

- 2
    <br>*Shown if chosen:* **2:** That's about 6 dB. Two are worth carrying: 6 dB ≈ ×2, and 20 dB = ×10 exactly.
- 10 **← correct**
    <br>*Shown if chosen:* **10:** Right. \( 20\log_{10}(10) = 20 \) dB, so every 20 dB is another factor of ten.
- 20
    <br>*Shown if chosen:* **20:** Decibels are a logarithmic scale, so the number is never the factor itself. If it were, the scale would be doing nothing.
- 100
    <br>*Shown if chosen:* **100:** A factor of 100 is 40 dB, not 20: you have gone one decade too far. Each ×10 adds 20 dB, so ×10 is 20 dB and ×100 is 40 dB. The usual way in is to double the decibels when you meant to multiply the factor by ten.

*Checks:* the decibel scale, used on every Bode plot in the unit

*Worked route, shown to everyone:*

For a gain (an amplitude ratio, which is what a Bode magnitude plot shows) the
definition is \( 20\log_{10}|G| \).

Anchors worth carrying:

- ×1 → 0 dB
- ×2 → 6 dB (and ÷2 → −6 dB)
- ×10 → 20 dB
- ×100 → 40 dB

The factor-of-two one is the one that slips. And note the **20** rather
than **10**: the 10 version is for *power*, and power goes as amplitude
squared, which is exactly where the factor of two in front comes from.

### 10. Reading a second-order system off its Bode plot

Below is the Bode plot of a second-order system \( G(s) = \dfrac{\omega_\mathrm{n}^2}{s^2 + 2\zeta\omega_\mathrm{n}s + \omega_\mathrm{n}^2} \), where \( \omega_\mathrm{n} \) is the natural frequency in rad/s and \( \zeta \) the damping ratio. Read \( \omega_\mathrm{n} \) and estimate \( \zeta \).

- \( \omega_\mathrm{n} \) (rad/s): **5** (tolerance ±0.4)
- \( \zeta \): **0.2** (tolerance ±0.06)
- *Common error* \( \omega_\mathrm{n} \approx 4.8 \): you read the frequency of the **peak**. That is the resonant frequency, \( \omega_\mathrm{r} = \omega_\mathrm{n}\sqrt{1 - 2\zeta^2} \), which sits a little *below* \( \omega_\mathrm{n} \) and moves as the damping changes. The phase curve is the reliable one.
- *Common error* \( \zeta \approx 0.7 \): that would have no peak at all. Any peak in the magnitude means \( \zeta < 0.707 \); the taller the peak, the lighter the damping.
- *Common error* \( \zeta \approx 0.1 \): the right idea but too light. A peak of 8 dB is a factor of about 2.5; \( \zeta = 0.1 \) would give about 14 dB, which is a factor of 5.

*Checks:* the link between the time-domain parameters and the frequency response, and that the resonant peak is not at \( \omega_\mathrm{n} \)

*Worked route, shown to everyone:*

Two readings, and the second one is the point of the question.

- **\( \omega_\mathrm{n} \) comes from the phase.** For any second-order system of this form the phase passes through exactly \( -90^\circ \) at \( \omega = \omega_\mathrm{n} \), whatever the damping. Here that is **5 rad/s**.
- **\( \zeta \) comes from the height of the peak.** The peak is about 8 dB, which is a linear factor of \( M_\mathrm{r} = 10^{8/20} \approx 2.5 \), and \( M_\mathrm{r} = \dfrac{1}{2\zeta\sqrt{1-\zeta^2}} \), giving \( \zeta \approx 0.2 \).

**The peak is not at \( \omega_\mathrm{n} \).** It sits at
\( \omega_\mathrm{r} = \omega_\mathrm{n}\sqrt{1 - 2\zeta^2} \), which here is
4.8 rad/s, close enough to be easy to mistake and far enough to matter.
The two coincide only when \( \zeta = 0 \), and above \( \zeta = 0.707 \)
there is no peak at all.

If you would rather not remember the \( M_\mathrm{r} \) formula, the
qualitative version gets you most of the way: a peak means light damping,
a big peak means very light damping, and no peak means \( \zeta \)
at or above about 0.7.

### 11. What feedback is for

Which of these does negative feedback *not* do, on its own (that is, with a sensor, a controller and a plant, but nothing else added)?

- Reduce the effect of disturbances on the output
    <br>*Shown if chosen:* **Disturbances:** It does do this, and it is arguably the main reason feedback exists. A disturbance shows up in the measurement, the error changes, and the controller pushes back.
- Reduce the effect of changes in the plant's gain
    <br>*Shown if chosen:* **Plant gain changes:** It does do this. It is why a feedback design survives an aircraft getting lighter as it burns fuel, and it is what the sensitivity function measures.
- Make an unstable plant stable, with a suitable controller
    <br>*Shown if chosen:* **Stabilising an unstable plant:** It does do this, and you will see it in the first session: the Quanser rig cannot be flown open-loop by hand, and closing the loop is what makes it flyable.
- Remove the effect of sensor noise on the output **← correct**
    <br>*Shown if chosen:* **Sensor noise:** Right, and this is the one that catches people. Feedback acts on what the sensor *says*. It cannot tell noise from real motion, so it faithfully corrects for both.

*Checks:* the unit's first threshold concept, that feedback is a trade rather than a fix

*Worked route, shown to everyone:*

Feedback compares the reference with the **measurement**, not with the
truth. Anything the sensor reports, real motion or noise alike, is treated
identically, so noise is driven into the actuator and back out into the
output.

That is why more gain is not always better. Raising the loop gain
suppresses disturbances *and* amplifies the effect of noise, and the two
pull in opposite directions. There is no setting that wins both, only a
choice about where to sit.

**Feedback is a trade, not a fix.** It is the first idea this unit is
built on, and the lecture on robustness is where that trade gets made
deliberately rather than by accident.
<!-- questions:end -->

## Reading the results

For the cohort, before the week 2 lecture:

| If many miss | It means | Where to put it |
|---|---|---|
| 1, 5, 6 | Transfer functions and closing the loop are shaky | A retrieval slot in week 2's hook; a short Preparing for Control addition |
| 2, 3, 4 | Second-order behaviour is shaky | Week 1's system ID fit depends on it: extra support in the case hour |
| 7 | Steady-state error | Week 3, when integral action arrives |
| 8, 9 | Bode plots | Week 4 depends on them: point to the glossary and year 2 notes before then |
| 10 | The idea of feedback itself | Week 1's first Learn slot |
