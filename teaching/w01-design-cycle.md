# Week 1: the Quanser session — run sheet

Draft, from the plan in [PEDAGOGY.md](../PEDAGOGY.md) under "Week 1: the
Quanser session". Times are provisional until the session is taught once.

This session deviates from P17's standard shape, and that is said to students in
the first two minutes: there is no previous week to retrieve, and the case hour
is built round the hardware.

## How the session is set up

**This is the standing arrangement, from week 1 onwards**, not a one-off for the
first session.

The theatre is in use until 12:50 — the AVDASI 2 intro runs 12:00–12:50 in this
same room — so **technical services bring the rig in at 12:50 and set up from
there**, continuing through the opening blocks of this session while the
lecturer presents. Setup is not a reason to start late.

**Everything runs on the TSRs' own laptops.** No laboratory PC is brought over,
and nothing depends on the lectern machine.

The deadline that matters is not 13:00. Working from the plan below, the rig is
first on camera at **minute 20** and must be **ready to fly by minute 30**, when
the open-loop attempt happens. So:

| By | What |
|---|---|
| 12:50 | Rig in the room, on its bench |
| ~13:20 (min 20) | Guarding, tether, camera and feed working — the rig goes on screen |
| ~13:30 (min 30) | Powered, closed-loop test flight done, switches tested — it flies |

Agree that with the TSRs in the room at 12:50, out loud, so the sequence is
theirs and not assumed.

## In advance

State as of Mon 21 Sep. Done items are kept rather than deleted, so the list
stays a record of what the session needs each year.

- [x] Technical services: rig released from the laboratory, transported, and
      returned. Their time, arranged with them; not teaching support.
- [x] At least one TA confirmed for the session, to help in the room during the
      system-ID and tuning blocks, and to watch the switches during flights.
- [x] Quanser rig booked out of the laboratory and into the theatre, with
      transport and a bench.
- [x] Two joysticks, tested with direct per-motor control.
- [x] **Cutting power: the amplifier switch and the mains switch.** In reach of
      the lecturer or TA throughout, and identified out loud before anything is
      powered. Nothing flies until both are located and tested. *No separate
      e-stop is fitted — decided 21 Sep; these two switches are the means of
      stopping the rig, so treat them with the seriousness an e-stop would get.*
- [x] Guarding and tether fitted as in the laboratory.
- [x] Camera: webcam, tripod and extension cable tested and packed. **Sight line
      from the back row still to be checked** — it can only be done in the room,
      so check it while the TSRs set up.
- [ ] Clean measured elevation response recorded from *this* rig, on the day or
      the day before, and placed in this week's `data/` folder. **The rig is in
      the laboratory until 12:50 on the day**, so record it there, not in the
      theatre.
- [x] **Gain submission form built and tested end to end**, 21 Sep. A link
      built by MATLAB pre-filled the form, the submission came back through the
      export, and `collate_gains` read it as the right name and the right
      numbers. Field ids are in `docs/w01-design-cycle/code/gain_form.json`,
      with a note on regenerating them for next year's form.
- [ ] **Form link on Blackboard**, and the students' code folder distributed.
- [x] Gain filter tested on synthetic submissions including deliberately bad
      ones, and the MATLAB and Python envelopes cross-checked against each
      other on twelve gain sets (`scripts/compare_envelope.py`).
- [ ] Selection tool tested end to end on a dummy set of submissions.
- [ ] Preparing for Control page live, and the device check working.

## In the room

Arrive for 12:50, with the TSRs. Order of work: rig and bench, guarding, tether,
camera and feed, then power, then a closed-loop test flight, then a test of the
amplifier and mains switches under power. The lecturer's own job in that window
is the back-row sight line and locating both switches.

## Files

| What | Where |
|---|---|
| Deck | `slides/w01-design-cycle/index.md` |
| Handout | `docs/w01-design-cycle/index.md` |
| Run sheet | this file |
| Existing lab material to adapt | `private/quanser/Quanser Lab/Quanser Lab 1 - System ID and PID/` |
| System-ID Live Script to adapt | `.../solution_files/s_1_system_identification.mlx` |
| Rig Simulink models | `.../part1_identify.slx`, `.../part3_validate.slx` |
| Student code folder | `docs/w01-design-cycle/code/` — synced by `scripts/sync_student_code.py`. |
| Measured response data | recorded on the day; see the checklist above. |
| Gain submission | Microsoft Form; ids in `docs/w01-design-cycle/code/gain_form.json`. |
| Collate the form export | `models/collate_gains.m` — **run this one live**. |
| The envelope, once | `models/heli_check_one.m`, mirrored by `scripts/gains.py`. |
| Envelope cross-check | `scripts/compare_envelope.py`. |
| Example submissions, to test against | `examples/gains/` — fixtures only, never student work. |
| Fitted elevation model | `models/elevation_plant.json` — **the laboratory's fit; replace from this rig**. |

Everything marked "to build" is a prerequisite, not a nice-to-have.

## Before anyone uploads

Say this, in these words or close to them, **before** the first submission goes
in. It takes fifteen seconds and cannot be said afterwards.

> The form asks for a display name, and that name goes on the screen when your
> gains are flown. Put whatever you like: your own name, or a nickname. The
> form records your University account so I know whose is whose, and that is
> never shown to the room. Round one is the extremes, chosen because they
> misbehave, so somebody's name is going on a public failure.

Two reasons it matters. It is the students' data and their choice, and consent
after the fact is not consent. And a student who would be embarrassed by a
visibly bad set of gains will otherwise simply not submit, which costs the
exercise the spread it depends on.

The display name field exists for exactly this, and it is worth saying that it
does.

## Gains: filtering and choosing

Submissions arrive as the form's Excel export. In MATLAB, in the room:

```matlab
flights = collate_gains('~/Downloads/responses.xlsx');
```

That is the one to run live: it reads the export, keeps each person's last
submission, applies the envelope, and returns the flight list in order. The
Python side reads a folder of files instead and applies the same envelope:

```bash
.venv/bin/python scripts/gains.py check path/to/responses
.venv/bin/python scripts/gains.py pick  path/to/responses --round 2
```

**Before anything is filtered**, fit the rig's own step response with
`fit_second_order` and write `K`, `wn` and `zeta` into
`models/elevation_plant.json`, then run
`.venv/bin/python scripts/sync_student_code.py` so the students' folder matches.
The file that ships carries the laboratory's stored fit, not this rig today,
and the tools print their source in the banner every time they run — check that
banner in the room. They refuse to run at all if the file is missing or carries
only `K`, deliberately: a report produced against a guessed plant reads exactly
like a real one.

Every check is a **refusal, never a clamp**. Nothing is quietly adjusted into
range, so a student whose gains are flown sees their own gains.

**Fallback gains, if nothing passes or the form fails:**
`Kp = 0.71, Ki = 0.59, Kd = 0.91` — settles in 5.9 s, damping 0.66, peak demand
5.2 V, phase margin 55°. Found by pole placement against the fitted plant and
checked against the envelope, so it is inside it by construction. Recompute it
once the rig's own fit is in, since these numbers follow the plant.

!!! danger "The previous fallback would not have flown"
    `Kp = 7.13, Ki = 0.2, Kd = 12.6` was the fallback while the plant was
    assumed to be a double integrator. Against the measured plant it is
    **rejected**: 18.2° of phase margin, and a 23.2 V demand from an amplifier
    with 6.0 V of usable headroom. If you have that set written down
    anywhere, throw it away.

**Round 2 is the interesting one.** The average of the cohort's accepted gains
is checked like any other submission, and it can fail even though every input
passed — the stable set is not convex. If that happens, do not fly it, and say
why: it is a better lesson than the flight would have been.

### The physics, for the room

The elevation axis, as measured, is a **stable but very lightly damped second
order**:

> `G(s) = K·ωₙ² / (s² + 2ζωₙs + ωₙ²)`, with `K ≈ 3.4 deg/V`, `ωₙ ≈ 1.0 rad/s`, `ζ ≈ 0.06`

Disturb it and it does come back, but the oscillation has a six-second period
and takes about a minute to die away.

**Why "turn Kp up" does not work.** Close a proportional loop alone and the
characteristic polynomial is `s² + 2ζωₙs + ωₙ²(1 + K·Kp)`. Kp is absent from
the coefficient of `s`, so the real part of the poles is pinned at `-ζωₙ`
however hard you push: the locus is a vertical line. Going from Kp = 0.5 to
Kp = 10 takes the overshoot from 89% to 97% and leaves the settling time at 65
seconds. Figure: `models/w01_proportional_limit.py`.

That is the motivation for the other two terms, and it is worth doing on the
board: damping has to come from somewhere other than Kp, which is the
derivative; the gap to the demand needs something with memory, which is the
integral.

**With PID**, the characteristic polynomial is

> `s³ + (2ζωₙ + K·ωₙ²·Kd)·s² + (ωₙ² + K·ωₙ²·Kp)·s + K·ωₙ²·Ki`

and Routh on `s³ + a₂s² + a₁s + a₀` asks for all coefficients positive and
**`a₂·a₁ > a₀`**. That is the condition students can check on paper. Raise Ki
far enough with Kp and Kd fixed and the loop goes unstable, which is the one
place integral action is visibly not free.

!!! warning "A claim that used to be here, and was wrong"
    This file previously said the loop was *conditionally stable*, so that
    turning the gain **down** was what broke it. That is true of a double
    integrator and false of this plant: scale a working design's gains down by
    a factor of a hundred and it stays stable. Do not say it in the room.

**Derivative acts on the measurement, not the error.** That is what Quanser
do, and it is what the handout means by rate feedback. It matters because the
demand is rate-limited at 45 deg/s, so derivative on the error would ask for
`Kd × 45` volts before the arm has moved at all.

## Hook

No previous session, so nothing to resolve. The grab is the claim, made in the
first five minutes and left unproven until minute 30:

> **This machine cannot be flown by hand. One of you is going to try.**

Say it early, name the volunteer early, and let it hang over the Learn slots.
Everything before minute 30 is then something the room wants, rather than
something it is being given.

Do not soften it into "it is quite hard to fly". The claim has to be strong
enough that some of the room disbelieves it, or the vote at minute 30 is
meaningless (P12).

## The plan

### Hour 1 — 60 minutes

| At | Min | What | On screen |
|---|---|---|---|
| 0 | 5 | Welcome, and **the hook**. What the unit is, how the two halves fit, how a session runs (P17) and how today differs. | Deck: unit map |
| 5 | 15 | Why control exists. The design cycle as the spine of everything after today (P1). | Deck: the cycle |
| 20 | 10 | The rig: what it is, how it is driven, how it is made safe. | Camera on rig |
| 30 | 15 | **The open-loop flight attempt.** Vote first on how long they last (P12), then a volunteer flies it on two joysticks. | Camera, with the vote on screen. |
| 45 | 15 | What a requirement is. Agree the requirement we design to today. | Deck; requirement written up and left up. |

The open-loop attempt is the session. Protect its 15 minutes: if hour 1 is
running late, cut the design-cycle block, not this.

### Hour 2 — 50 minutes

| At | Min | What | On screen |
|---|---|---|---|
| 0 | 10 | **System ID** from the measured response. Floor: manual second-order fit. Ceiling: `tfest`. | Live Script |
| 10 | 15 | **Tune a PID** in simulation against the agreed requirement. **Say the display-name line below before anyone submits**, then `submit_gains` hands them a pre-filled form link. | Live Script; requirement still visible. |
| 25 | 15 | **Fly the submitted gains**, three rounds. | Camera, with the display name on screen. |
| 40 | 10 | **The cliffhanger,** and set the independent work. | Deck |

**System ID, the floor.** Oscillation period gives the damped frequency, the
ratio of successive peaks gives the damping ratio, the steady state gives the
gain. The existing lab material puts this axis near ζ = 0.06 and ωₙ = 1 rad/s, so the
oscillation is readable by eye: a 6.3 s period, still visible after a minute.
Source: Quanser Lab 1's own solution, `solution_files/s_1_system_identification.mlx`, fits the measured `d_Part1.mat` and reports poles at -0.0600 +/- 0.9982j, so zeta = 0.06 and omega_n = 1.0 rad/s.
Checked against the raw data: the first two peaks give ζ = 0.057 and 0.059, which
is what a manual log-decrement fit will produce. Below about 0.5° the encoder
floor takes over and later peaks give nonsense, so tell them to use early peaks. Everyone can reach a model; `tfest` is the stretch.

**The model they fit is the trim, not the rig** — but do not say the numbers this file used to carry.

It previously read: "gravity stiffness goes as sin(elevation), so identify at 5° and get ωₙ = 0.84, at 10° get 1.19, at 20° get 1.67". **The recording contradicts that.** Before the step the arm swings about the level datum with a period of 5.85 s; after it, at +7°, the period is 6.02 s. The same frequency at level and at seven degrees. If gravity on an offset mass were the only restoring term, the period at level would grow without limit, and it does not: this rig has stiffness at level, which points at the centre of mass sitting below the arm line.

What is still true and worth saying: Quanser's linearisation is taken about level and has every pole at the origin, the rig plainly oscillates, and a fit is taken about a trim. What is **not** established is how much ωₙ moves across the full range, because two trims seven degrees apart do not settle it. `models/rig_trim_sweep.m` is the experiment, and it wants runs from 1 V to 3 V.

Keep `models/quanser_trim_stiffness.py` out of the session: it draws the prediction the data has just failed.

!!! note "Not said to students, for now"
    The student-facing material used to point out that the two models of the
    elevation axis disagree: Quanser's, linearised about level, makes it a
    double integrator, and a fit taken about a trim makes it a lightly damped
    second order. That note is **out of the laboratory pages and the Drive
    README**, on Steve's call, 22 September: until we have settled which
    applies where, presenting it as an open disagreement costs more confusion
    than it buys understanding.

    What the student material says now is the plain fact with no framing:
    `heli3d_model` is linearised about level and so has no restoring term on
    elevation, and if your own fit looks different, use the one that matches
    where you are flying.

    The reasoning is kept in `models/quanser_elevation.py`, along with the
    measurement that rules out the strong sin(elevation) story, and
    `models/rig_trim_sweep.m` is the experiment that would settle it. Put the
    note back once it is settled, as a finding rather than a puzzle.

**The three rounds.** Announce the display name, not the username.

1. **Extremes,** chosen by the selection tool: the most aggressive, the most
   sluggish, the most integral. Cause and effect before any good answer.
2. **The cohort average.** Often worse than most of its parts. Say so before
   flying it, and ask for a prediction.
3. **A few of the best** against the agreed requirement, and whose prediction
   came closest to what the rig actually did.

Nothing reaches the hardware that the filter has not passed.

## Cliffhanger

Two gaps, both real, both resolved later in the unit:

- **There is no right answer until you say what you want.** Re-rank the three
  rounds under a different requirement and the winner changes. Resolved in the
  requirements strand, and it is the coursework's first criterion.
- **Simulation and hardware disagree.** Resolved in the model-validation
  strand, and it is what the coursework's virtual flight test is for.

Set the independent work in the last two minutes, by P17's three parts.

## If it goes wrong

| Likely failure | What to do |
|---|---|
| Rig won't run, or fails mid-session | Fall back to the recorded response and a recorded flight. Everything after system ID works unchanged; only the live flying is lost. Have the recording on the machine, not in the cloud. |
| The form fails, or students can't reach it | Take gains verbally from four or five pairs and type them straight into `heli_check_one`. The three rounds still work with a handful of submissions. |
| Students can't get MATLAB working in the room | Pair them with someone who can. This is why the device check exists; note who, and chase before week 2. |
| Running late at the 25-minute mark of hour 2 | Cut round 1 to two sets. Never cut the cliffhanger. |

## After

- [ ] Export the form's responses; keep them, they are the first cohort data of
      the year and they say who has MATLAB working.
- [ ] Post the recorded flight, the data and the Live Script for anyone absent.
- [ ] Note actual timings against the plan above, and update this file today.
- [ ] Check who did not submit anything: earliest signal of a student in
      difficulty (P16).

<!-- tracking: status=draft version=0 -->
