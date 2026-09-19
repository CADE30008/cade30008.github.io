# Lecture 1: the Quanser session — run sheet

Draft, from the plan in [PEDAGOGY.md](../PEDAGOGY.md) under "Lecture 1: the
Quanser session". Times are provisional until the session is taught once.

This session deviates from P17's standard shape, and that is said to students in
the first two minutes: there is no previous week to retrieve, and the case hour
is built round the hardware.

## In advance

- [ ] Technical services: rig released from the laboratory, transported, and
      returned. Their time, arranged with them; not teaching support.
- [ ] At least one TA confirmed for the session, to help in the room during the
      system-ID and tuning blocks, and to watch the e-stop during flights.
- [ ] Quanser rig booked out of the laboratory and into the theatre, with
      transport and a bench.
- [ ] Two joysticks, tested with direct per-motor control.
- [ ] **E-stop fitted to the amplifier and tested.** In reach of the lecturer or TA throughout.
      Nothing runs before this is confirmed.
- [ ] Guarding and tether fitted as in the laboratory.
- [ ] Camera on the rig, feed on the main screen, sight line checked from the
      back row.
- [ ] Clean measured elevation response recorded from *this* rig, on the day or
      the day before, and placed in MATLAB Drive.
- [ ] MATLAB Drive: data folder shared read-only; submission folder shared
      writable; both tested from a student account.
- [ ] Gain filter tested on last year's or synthetic submissions, including
      deliberately bad ones.
- [ ] Selection tool tested end to end on a dummy folder of submissions.
- [ ] Preparing for Control page live, and the device check working.

## In the room

Arrive 45 minutes early. Rig, guarding, tether, e-stop, camera, then power, then
a test flight in closed loop, then a test of the e-stop under power.

## Files

| What | Where |
|---|---|
| Deck | `slides/l01-design-cycle/index.md` |
| Handout | `docs/l01-design-cycle/index.md` |
| Run sheet | this file |
| Existing lab material to adapt | `private/quanser/Quanser Lab/Quanser Lab 1 - System ID and PID/` |
| System-ID Live Script to adapt | `.../solution_files/s_1_system_identification.mlx` |
| Rig Simulink models | `.../m_part1.slx`, `.../m_part3.slx` |
| Student Live Script | MATLAB Drive, read-only folder — **to build** |
| Measured response data | MATLAB Drive, read-only folder — **recorded on the day** |
| Submission folder | MATLAB Drive, writable — **to create** |
| Gain filter and selection tool | **to build** |

Everything marked "to build" is a prerequisite, not a nice-to-have.

## Hook

No previous session, so nothing to resolve. The grab is the claim, made in the
first five minutes and left unproven until minute 30:

> **This machine cannot be flown by hand. One of you is going to try.**

Say it early, name the volunteer early, and let it hang over the taught blocks.
Everything before minute 30 is then something the room wants, rather than
something it is being given.

Do not soften it into "it is quite hard to fly". The claim has to be strong
enough that some of the room disbelieves it, or the vote at minute 30 is
meaningless (P12).

## The plan

### Hour 1 — 60 minutes

| At | Min | What | On screen |
|---|---|---|---|
| 0 | 5 | Welcome, and **the hook**. What the unit is, how the two halves fit, how a session runs (P17) and how today differs | Deck: unit map |
| 5 | 15 | Why control exists. The design cycle as the spine of everything after today (P1) | Deck: the cycle |
| 20 | 10 | The rig: what it is, how it is driven, how it is made safe | Camera on rig |
| 30 | 15 | **The open-loop flight attempt.** Vote first on how long they last (P12), then a volunteer flies it on two joysticks | Camera, with the vote on screen |
| 45 | 15 | What a requirement is. Agree the requirement we design to today | Deck; requirement written up and left up |

The open-loop attempt is the session. Protect its 15 minutes: if hour 1 is
running late, cut the design-cycle block, not this.

### Hour 2 — 50 minutes

| At | Min | What | On screen |
|---|---|---|---|
| 0 | 10 | **System ID** from the measured response. Floor: manual second-order fit. Ceiling: `tfest` | Live Script |
| 10 | 15 | **Tune a PID** in simulation against the agreed requirement. Submit gains to MATLAB Drive | Live Script; requirement still visible |
| 25 | 15 | **Fly the submitted gains**, three rounds | Camera, with the display name on screen |
| 40 | 10 | **The cliffhanger,** and set the independent work | Deck |

**System ID, the floor.** Oscillation period gives the damped frequency, the
ratio of successive peaks gives the damping ratio, the steady state gives the
gain. The existing lab material puts this axis near ζ = 0.06, so the ringing is
readable by eye. Everyone can reach a model; `tfest` is the stretch.

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
| Rig won't run, or fails mid-session | Fall back to the recorded response and a recorded flight. Everything after system ID works unchanged; only the live flying is lost. Have the recording on the machine, not in the cloud |
| MATLAB Drive submission folder fails, or students can't write to it | Take gains verbally from four or five pairs and type them in. The three rounds still work with a handful of submissions |
| Students can't get MATLAB working in the room | Pair them with someone who can. This is why the device check exists; note who, and chase before Lecture 2 |
| Running late at the 25-minute mark of hour 2 | Cut round 1 to two sets. Never cut the cliffhanger |

## After

- [ ] Download the submissions folder; keep it, it is the first cohort data of
      the year and it says who has MATLAB working.
- [ ] Post the recorded flight, the data and the Live Script for anyone absent.
- [ ] Note actual timings against the plan above, and update this file today.
- [ ] Check who did not submit anything: earliest signal of a student in
      difficulty (P16).
