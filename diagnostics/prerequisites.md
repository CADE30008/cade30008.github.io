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

A system obeys \( \dot y + 2y = u \), starting from rest. What is its transfer function \( Y(s)/U(s) \)?

- \( \dfrac{1}{s+2} \) **← correct**
    <br>*Shown if chosen:* Right. Every term transforms, the \( s \) stays with \( Y \) on the left, and what's left on top is the coefficient of \( u \).
- \( \dfrac{s}{s+2} \)
    <br>*Shown if chosen:* The \( s \) from \( \dot y \) has ended up in the numerator. It belongs with \( y \): the left-hand side collects to \( (s+2)Y \), so the numerator is whatever multiplies \( u \), which here is 1.
- \( \dfrac{2}{s+1} \)
    <br>*Shown if chosen:* The two coefficients have swapped. The coefficient of \( y \), which is 2, joins \( s \) in the denominator; the coefficient of \( u \), which is 1, is the numerator.
- \( s + 2 \)
    <br>*Shown if chosen:* That's the characteristic polynomial, or equivalently \( U/Y \) — the right answer upside down. A transfer function is always output over input.

*Checks:* Laplace transform of a derivative with zero initial conditions

*Worked route, shown to everyone:*

- Transform every term, using \( \dot y \to sY \) because the system starts from rest. That gives \( sY + 2Y = U \).
- Collect \( Y \): \( (s+2)Y = U \).
- Divide: \( Y/U = \dfrac{1}{s+2} \).

The denominator, \( s+2 \), is the characteristic polynomial, and its root
\( s = -2 \) is the pole. This is the move behind every block diagram in
the unit, so it is worth being quick at.

### 2. Poles and what they mean

\( G(s) = \dfrac{5}{s^2 + 2s + 5} \) has poles at \( -1 \pm 2j \). Its step response is:

- unstable
    <br>*Shown if chosen:* Stability is decided by the *real* part, and here it is \( -1 \). A complex pole isn't unstable in itself — it's what makes a response oscillate rather than what makes it grow.
- stable, and settles without oscillating
    <br>*Shown if chosen:* The stability half is right, but the \( \pm 2j \) has been dropped. A non-zero imaginary part means the response oscillates on its way in, here at 2 rad/s.
- stable, with a decaying oscillation **← correct**
    <br>*Shown if chosen:* Right — and you read both halves. Real part negative, so it decays; imaginary part non-zero, so it oscillates while decaying.
- an oscillation that never decays
    <br>*Shown if chosen:* That needs the poles *on* the imaginary axis, at \( \pm 2j \) with no real part at all. The \( -1 \) is what makes it die away.

*Checks:* reading stability and oscillation from pole locations

*Worked route, shown to everyone:*

Read a complex pair \( \sigma \pm j\omega_d \) as two separate facts:

- **the real part \( \sigma \) sets the envelope.** Negative decays like \( e^{\sigma t} \), positive grows, zero neither.
- **the imaginary part \( \omega_d \) sets the ringing.** Non-zero means it oscillates at \( \omega_d \) rad/s; zero means it doesn't.

Here \( \sigma = -1 \) and \( \omega_d = 2 \), so the response rings at
2 rad/s inside an \( e^{-t} \) envelope — most of it gone within about
four seconds.

### 3. Natural frequency and damping ratio

For \( G(s) = \dfrac{25}{s^2 + 4s + 25} \), give the natural frequency \( \omega_n \), in rad/s, and the damping ratio \( \zeta \).

- \( \omega_n \) (rad/s): **5** (tolerance ±0.01)
- \( \zeta \): **0.4** (tolerance ±0.01)
- *Common error* \( \omega_n = 25 \): that's \( \omega_n^2 \). The constant term is the square, so take the root.
- *Common error* \( \zeta = 0.16 \): you divided 4 by \( \omega_n^2 \). The middle coefficient is \( 2\zeta\omega_n \), so divide by \( 2\omega_n = 10 \).
- *Common error* \( \zeta = 0.8 \): you divided by \( \omega_n \) but not by the 2. It is easy to lose; the factor of 2 is there so that \( \zeta = 1 \) is exactly critical damping.
- *Common error* \( \zeta = 2 \): that's \( \zeta\omega_n \), which is the decay rate \( \sigma \) — a useful number, but not the damping ratio.

*Checks:* the standard second-order form

*Worked route, shown to everyone:*

Match the denominator against the standard form
\( s^2 + 2\zeta\omega_n s + \omega_n^2 \), one coefficient at a time:

- **constant term:** \( \omega_n^2 = 25 \), so \( \omega_n = 5 \) rad/s.
- **middle term:** \( 2\zeta\omega_n = 4 \), and \( \omega_n \) is now known, so \( \zeta = 4/(2 \times 5) = 0.4 \).

Always do them in that order — the middle term needs \( \omega_n \), so
there is nothing to be gained by starting there. A quick check: \( \zeta \)
between 0 and 1 means an oscillatory response, which matches the complex
poles this denominator has.

### 4. Overshoot

A second-order system with \( \zeta = 0.4 \) is given a step. Its percentage overshoot is closest to:

- 5%
    <br>*Shown if chosen:* That's roughly \( \zeta = 0.7 \) — the value often quoted as a good compromise, so it is an easy one to reach for. This system is less damped than that.
- 10%
    <br>*Shown if chosen:* That's roughly \( \zeta = 0.6 \). You're in the right region but a little too damped; the relationship is steep here, so small changes in \( \zeta \) move the overshoot a lot.
- 25% **← correct**
    <br>*Shown if chosen:* Right. \( M_p = 25.4\% \), and the useful thing to carry away is the pairing: \( \zeta = 0.4 \) with about a quarter overshoot.
- 50%
    <br>*Shown if chosen:* That's roughly \( \zeta = 0.2 \), considerably livelier than this. Half the height of the step as overshoot would be a very underdamped system.

*Checks:* the link between damping and overshoot

*Worked route, shown to everyone:*

Exactly, \( M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}} \), which for
\( \zeta = 0.4 \) gives 0.254, so about 25%.

In practice nobody evaluates that in a design meeting. Carry three anchors
instead and interpolate:

- \( \zeta = 0.2 \) → about 50%
- \( \zeta = 0.4 \) → about 25%
- \( \zeta = 0.7 \) → about 5%

Less damping, more overshoot, and the curve is steep — which is why phase
margin, its frequency-domain cousin, is worth watching closely in week 4.

### 5. Steady state

What does the step response of \( G(s) = \dfrac{3}{s+2} \) settle to?

- final value: **1.5** (tolerance ±0.01)
- *Common error* 3: you took the numerator alone. Setting \( s = 0 \) leaves the denominator's constant term too, so it's \( 3/2 \), not 3.
- *Common error* 0: you may have applied \( \lim_{s \to 0} sG(s) \), which is the final value of the *impulse* response. For a step the \( s \) in the theorem cancels the \( 1/s \) of the step itself.
- *Common error* 0.667: that's \( 2/3 \) — the right two numbers, inverted.

*Checks:* the final value theorem, or DC gain

*Worked route, shown to everyone:*

The steady-state value of a step response is just \( G(0) \), the DC gain.
Set \( s = 0 \): \( G(0) = 3/2 = 1.5 \).

If you would rather use the final value theorem, the step is \( 1/s \), so

$$ \lim_{s\to0} s \cdot G(s) \cdot \frac{1}{s} = \lim_{s\to0} G(s) = G(0). $$

The \( s \) and the \( 1/s \) cancel, which is why the shortcut works. The
theorem is only valid when the response actually settles, so check the
poles are in the left half plane first — here the single pole is at
\( s = -2 \), so it does.

### 6. Closing the loop

A plant \( G(s) = \dfrac{4}{s(s+1)} \) is put in a unity negative feedback loop. The closed-loop transfer function from reference to output is:

- \( \dfrac{4}{s^2 + s + 4} \) **← correct**
    <br>*Shown if chosen:* Right. \( T = G/(1+G) \), then multiply top and bottom by \( s(s+1) \) to clear the fraction within a fraction.
- \( \dfrac{4}{s^2 + s - 4} \)
    <br>*Shown if chosen:* A sign error: this is \( G/(1-G) \), which is *positive* feedback. The sign is the whole point — this version has a pole in the right half plane and would run away.
- \( \dfrac{4}{s^2 + s} \)
    <br>*Shown if chosen:* That's the open loop \( G \) with its denominator multiplied out. The loop hasn't been closed: there is no \( +4 \) contributed by the feedback path.
- \( \dfrac{s^2 + s}{s^2 + s + 4} \)
    <br>*Shown if chosen:* Very close, and a useful thing to have derived: that's the *sensitivity* \( S = 1/(1+G) \), which maps the reference to the **error**. The question asked for reference to **output**, which is \( T = G/(1+G) \). Note \( S + T = 1 \) — worth remembering.

*Checks:* \( G/(1+G) \), the step everything in the unit builds on

*Worked route, shown to everyone:*

- Write the closed-loop form: \( T = \dfrac{G}{1+G} \).
- Substitute: \( T = \dfrac{4/(s(s+1))}{1 + 4/(s(s+1))} \).
- Multiply top and bottom by \( s(s+1) \): \( T = \dfrac{4}{s(s+1) + 4} = \dfrac{4}{s^2+s+4} \).

Two habits that save time later. **The closed-loop denominator is
\( 1 + G \) cleared of fractions**, so you can often write it down without
the algebra. And **the numerator of \( T \) is the numerator of \( G \)**,
unchanged — feedback moves poles, never zeros.

This one has \( \omega_n = 2 \) and \( \zeta = 0.25 \), so expect a lively
response with around 45% overshoot. The Quanser rig in the first session is
far less damped still.

### 7. Steady-state error

The same unity feedback loop, but with \( G(s) = \dfrac{4}{s+1} \). After a unit step in the reference, what error remains?

- steady-state error: **0.2** (tolerance ±0.01)
- *Common error* 0.25: you used \( 1/G(0) \). The formula is \( 1/(1+G(0)) \), and that extra 1 is the reference itself — the error is what the reference asks for minus what the loop delivers.
- *Common error* 0.8: that's the steady-state *output*, \( G(0)/(1+G(0)) \). The error is what's left over: \( 1 - 0.8 = 0.2 \).
- *Common error* 0: that would need an integrator in the loop. This plant has none — a pole at \( s = -1 \), not at the origin — so a finite error survives.

*Checks:* steady-state error of a type 0 loop, and why integral action exists

*Worked route, shown to everyone:*

- For unity feedback, the error transfer function is \( E/R = S = \dfrac{1}{1+G} \).
- A unit step's final error is therefore \( e_{ss} = \dfrac{1}{1+G(0)} \).
- Here \( G(0) = 4 \), so \( e_{ss} = 1/5 = 0.2 \) — a 20% error that never goes away.

**Why it matters.** The only way to drive that to zero is to make
\( G(0) \) infinite, which means putting an integrator in the loop: a pole
at \( s = 0 \). That is exactly what the I in PID does, and it is the
reason integral action exists at all rather than being an optional extra.

Raising the gain instead shrinks the error but never removes it, and costs
you damping on the way — the trade you will meet again in almost every week
of this unit.

### 8. Reading a Bode plot

For \( G(s) = \dfrac{10}{s+10} \) at \( \omega = 10 \) rad/s, what are the magnitude, in decibels, and the phase?

- 0 dB, 0°
    <br>*Shown if chosen:* Those are the low-frequency values, well *below* the corner. At \( \omega = 10 \) you are standing exactly on the corner, where the asymptotes meet and neither one is accurate.
- −3 dB, −45° **← correct**
    <br>*Shown if chosen:* Right, and these two numbers travel together: every first-order corner is −3 dB and −45°, whatever the frequency. Worth memorising as a pair.
- −6 dB, −90°
    <br>*Shown if chosen:* −90° is the high-frequency limit, only approached well *above* the corner. At the corner the phase is exactly halfway there.
- −20 dB, −45°
    <br>*Shown if chosen:* The phase is right. −20 dB is the magnitude a *decade* above the corner, at \( \omega = 100 \), once the −20 dB/decade slope has had a full decade to act.

*Checks:* the corner frequency of a first-order lag

*Worked route, shown to everyone:*

A first-order lag \( \dfrac{1}{1 + s/\omega_c} \) has three landmarks:

- **well below \( \omega_c \):** 0 dB and 0°. The system passes the signal through.
- **at \( \omega_c \):** \( |G| = 1/\sqrt2 \), which is −3 dB, and the phase is exactly −45°, halfway to its limit.
- **well above \( \omega_c \):** falling at −20 dB/decade, phase heading to −90°.

Here \( G = 10/(s+10) = 1/(1 + s/10) \), so \( \omega_c = 10 \) rad/s and
the question is asking for the corner itself.

**−3 dB and −45° at the corner is the single most reused fact in this
unit.** Every lag you meet in weeks 4 and 8 is built from it.

### 9. Decibels

A gain of 20 dB is a factor of:

- 2
    <br>*Shown if chosen:* That's about 6 dB. The two worth knowing are 6 dB ≈ ×2 and 20 dB = ×10 exactly.
- 10 **← correct**
    <br>*Shown if chosen:* Right. \( 20\log_{10}(10) = 20 \) dB, so every 20 dB is another factor of ten.
- 20
    <br>*Shown if chosen:* Decibels are a logarithmic scale, so the number is never the factor itself. If it were, the scale would be doing nothing.
- 100
    <br>*Shown if chosen:* That's the answer for \( 10\log_{10} \), the **power** definition. A gain is an amplitude ratio, so it's \( 20\log_{10} \). ×100 would be 40 dB.

*Checks:* the decibel scale, used on every Bode plot in the unit

*Worked route, shown to everyone:*

For a gain — an amplitude ratio, which is what a Bode magnitude plot
shows — the definition is \( 20\log_{10}|G| \).

Anchors worth carrying:

- ×1 → 0 dB
- ×2 → 6 dB (and ÷2 → −6 dB)
- ×10 → 20 dB
- ×100 → 40 dB

The factor-of-two one is the one that slips. And note the **20** rather
than **10**: the 10 version is for *power*, and power goes as amplitude
squared, which is exactly where the factor of two in front comes from.

### 10. What feedback is for

Which of these does negative feedback <em>not</em> do, on its own?

- Reduce the effect of disturbances on the output
    <br>*Shown if chosen:* It does do this — arguably the main reason feedback exists. A disturbance shows up in the measurement, the error changes, and the controller pushes back.
- Reduce the effect of changes in the plant's gain
    <br>*Shown if chosen:* It does do this. It is why a feedback design survives an aircraft getting lighter as it burns fuel, and it is what the sensitivity function measures.
- Make an unstable plant stable, with a suitable controller
    <br>*Shown if chosen:* It does do this, and you will see it in the first session: the Quanser rig cannot be flown open-loop by hand, and closing the loop is what makes it flyable.
- Remove the effect of sensor noise on the output **← correct**
    <br>*Shown if chosen:* Right, and this is the one that catches people. Feedback acts on what the sensor *says*. It cannot tell noise from real motion, so it faithfully corrects for both.

*Checks:* the unit's first threshold concept — feedback is a trade, not a fix

*Worked route, shown to everyone:*

Feedback compares the reference with the **measurement**, not with the
truth. Anything the sensor reports — real motion or noise — is treated
identically, so noise is driven into the actuator and back out into the
output.

That is why more gain is not always better. Raising the loop gain
suppresses disturbances *and* amplifies the effect of noise, and the two
pull in opposite directions. There is no setting that wins both, only a
choice about where to sit.

**Feedback is a trade, not a fix.** It is the first idea this unit is
built on, and where week 7 picks up.
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
