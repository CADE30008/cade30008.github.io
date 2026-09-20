# Review: our materials against what DCLS actually teaches

20 September 2026. Source: the 2025/26 CADE20002 materials in
`private/dcls_2025/` — 77 PDFs, 831 pages, indexed there. Conclusions distilled
into [curriculum/prerequisites.md](../curriculum/prerequisites.md).

Nothing here is applied yet. Items are numbered 1 to 16, one sequence throughout, so there is a single way to name any of them.

---

## They arrive much further along than we assumed

**1 — Their assessment is our week 1, on paper.**

CADE20002's final assessment, question 4, gives students a **double integrator**
`G(s) = Θ/U = 1/(Js²)` under unity feedback with a PID controller, has them
derive `T(s)`, show the characteristic equation is `1000s³ + K_D s² + K_P s + K_I = 0`,
match it to `s² + 2ζωₙs + ωₙ²` against overshoot and peak-time specifications,
and implement it in MATLAB. Question 5 adds a lightly damped flexible mode and
tunes it by Ziegler–Nichols.

The Quanser elevation axis is a double integrator. Week 1 has students fit it,
tune a PID, and fly it. **That is the same problem, the same controller and the
same design route as the exercise they finished in April.**

This is an opportunity, not a clash — but only if it is deliberate. The hook
becomes much stronger: *you solved this on paper for a satellite; here it is,
in the room, and the paper answer is about to disappoint you.* The gap between
their simulated result and the rig's behaviour is then the entire point, and it
is a gap they have personally earned.

**Amendment:** rewrite week 1's framing to name the connection explicitly, in
`curriculum/weeks.yaml` and the run sheet. Do not present the double integrator
or PID as new. Present *hardware* as new.

**2 — They already know Ziegler–Nichols and pole placement.**

Handbook 3.6 covers manual tuning, Ziegler–Nichols (both methods),
characteristic equation matching and optimisation-based tuning. Week 3 of their
control theme works pole placement through in detail.

Our week 3 is titled **"PID, properly"**. As scoped it risks being a re-run.

**Amendment:** re-scope week 3 around what they genuinely have not got — the
frequency-domain view of PID, derivative filtering as a design choice rather
than a footnote, anti-windup, setpoint weighting, and *why* Ziegler–Nichols
gives what it gives. Steve has already said this week is a placeholder needing
review; this is the evidence for what it should become.

**3 — The diagnostic is pitched below them.**

Q6 asks for `G/(1+G)` on a first-order-times-integrator plant. Q7 asks for
steady-state error with proportional control. Both are comfortably inside what
their assessment required them to do unaided.

**Amendment:** keep them — an easy opener is fine, and a diagnostic that
everyone fails tells us nothing — but retitle the quiz's framing so it reads as
*confirming* rather than *testing*, and consider replacing one item with
something that genuinely discriminates. See item 10.

---

## Notation, where we are actually wrong

**4 — "Magnitude" should be "gain".** Q8 asks for "the magnitude, in
decibels". DCLS writes **"Gain dB"** on every Bode axis (19 occurrences) and
"gain response" 13 times, against a single use of "magnitude plot". Our week 3
handout says "slides the magnitude plot up or down" too.
**Amendment:** use *gain* for the Bode ordinate throughout, and say once that
some books call it magnitude.

**5 — Q9's distractor teaches something they have never seen.** The "100"
option is explained as the `10 log₁₀` power definition. **`10 log₁₀` appears
nowhere in DCLS.** A student choosing 100 has not confused power with amplitude;
they have most likely just mis-remembered. The feedback diagnoses a
misconception they do not have.
**Amendment:** rewrite that distractor around the error they actually make —
treating the dB number as the factor, or misplacing the decade — and mention the
power definition only as an aside.

**6 — Q6's best distractor names a concept they have never met.** The
`(s²+s)/(s²+s+4)` option is explained as "the *sensitivity* `S = 1/(1+G)`… note
`S + T = 1`". **The word "sensitivity" is not used in the control sense anywhere
in DCLS.** This is week 7 material. As written, the feedback for our most
interesting wrong answer is unreadable to the student who picks it.
**Amendment:** describe it in terms they have — "that is the transfer function
from reference to *error*, not to output" — and add, as a forward reference,
that it has a name we will meet in week 7.

**7 — `C(s)` collides, and DCLS collides with itself.** In their assessment,
`C(s)` is the controller, matching us. In example sheet C1, `C(s)` is the
**output**. Students have seen both.
**Amendment:** state our convention explicitly the first time `C(s)` appears in
week 3, with a one-line note that some of their DCLS material uses C for the
output. Never use `C` for an output anywhere in our materials.

**8 — ωₙ is right, but flag the variants.** They have seen **ω₀** in the
signals and vibrations halves, **wₙ** in Acar's slides, and **ωₙ** in the
example sheets and assessment. Ours matches what they were examined on, which is
the right choice.
**Amendment:** one sentence at first use — "you may have seen this written ω₀" —
and a glossary entry. Not a change of symbol.

**9 — PID subscripts should be uppercase.** Their assessment writes
`K_P, K_I, K_D`; Acar's slides use lowercase. We use lowercase.
**Amendment:** worth deciding deliberately rather than drifting. Uppercase
matches the assessment; lowercase matches most textbooks including Dorf. My
recommendation is to keep lowercase and not mention it, because unlike ω₀/ωₙ
there is no chance of a student misreading `K_p` — but it should be a decision.
Either way, the subscripts go **upright**, which they currently are not.

---

## The diagnostic, question by question

| Quiz Q | Finding | Proposed amendment |
|---|---|---|
| 1 | Fine. Laplace of a derivative is handbook 1.4 and 2.2. | None. |
| 2 | Fine, and they know **BIBO stability** by name — we could use the term. | Optionally name BIBO in the feedback. |
| 3 | Nearly identical to their example sheet C1 2.2, which uses `G(s) = 25/(s²+6s+25)`. Ours is `25/(s²+4s+25)`. | None — the echo is good. Consider naming the connection in the feedback. |
| 4 | Overshoot from ζ. They have Dorf's Figure 5.8 chart for exactly this. | Mention the chart; it is a tool they own. |
| 5 | Final value theorem — handbook 3.2, and Acar week 2. Fine. | None. |
| 6 | **Item 6**: the sensitivity distractor is unreadable to them. | Rewrite that feedback. |
| 7 | Steady-state error. Below their level but a fair check. | Keep. |
| 8 | **Item 4**: "magnitude" → "gain". | Reword the stem. |
| 9 | **Item 5**: the power-definition distractor misdiagnoses. | Rewrite that distractor. |
| 10 | Feedback and noise. **Genuinely new to them** — nothing in DCLS covers the noise trade. Our best question. | Keep, and consider making more of it. |

**10 — a candidate replacement question**, if we want one that discriminates:
reading ζ and ωₙ off a **Bode plot** of a lightly damped second-order system.
Their assessment Q5(i) required exactly this, so it is fair; it is harder than
anything currently in our set; and it bridges the time and frequency domains,
which is where week 4 starts.

---

## Elsewhere in the course

**11 — The textbook page gets stronger.** DCLS credits **Dorf and Bishop**
throughout its control lectures. Our reading page can say that this is a
continuation of a text they have already been pointed at, not a new purchase.
They also use **Norman Nise, *Control Systems Engineering***, which is worth
adding as an alternative on `docs/reading.md`.

**12 — Week 4 is well placed.** Nyquist and margins are genuinely new; they have
BIBO and pole-location stability only. No change needed, and it is worth telling
students that this is new so they do not assume it is revision.

**13 — Week 7's sensitivity is new, and is a bigger step than the map implies.**
They have never met `S`, `T`, or `S + T = 1`. The lecture map treats it as one
of several ideas in the week; on this evidence it needs more room, and the P19
budget warning already flagged for week 7 is probably right.

**14 — Week 2's system ID is less new than assumed.** They have fitted transfer
functions to mass–spring–damper systems and read parameters off Bode plots.
Fitting a second-order model to a measured response is a smaller step than the
scope implies.

**15 — They have had MATLAB and Simulink for control.** The Simulink brief and
Simulink Lab 2 in DCLS are both control-flavoured. The Onramp framing on the
prep page — "recommended, not required" — is right, and we could say *why*: most
of you have done this in DCLS.

**16 — The AI position needs a look.** The DCLS assessment permits AI under the
University's **Category 2: Minimal**, with an academic integrity statement
required. Our coursework is **Category 3: Selective**. Students moving from one
to the other in the same subject area need that difference stated plainly, or
they will carry last year's rules forward.

---

## Suggested order

An ordered list of item numbers would read as two competing numberings, so:

- **First, items 4, 5 and 6.** The diagnostic goes out soonest, and these three
  are what make its feedback readable rather than merely correct. Small and
  contained.
- **Then items 7 and 8** — one sentence each, wherever the symbol first appears.
- **Then item 1**, week 1's framing. It changes the hook, so it wants doing
  before the lecture is written rather than after.
- **Then item 16**, the AI category difference. A paragraph, and it protects
  students.
- **Then item 2**, week 3's re-scope. Substantial, and already flagged as a
  week needing review.
- **Last, items 10, 13 and 14** — curriculum-level, for the lecture map review.
