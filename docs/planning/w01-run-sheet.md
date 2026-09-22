---
title: "Run sheet: the design cycle, end to end"
description: "Lecturer's run sheet for the first control session: preflight checks, the setup timeline, the session beat by beat, and what to do when the rig does not cooperate."
---

# Run sheet: the design cycle, end to end

Lecturer-facing. Published so it is reachable from a phone in the laboratory,
not linked from the navigation. Students do not need it, and nothing here is
secret.

The detailed planning document, with the pedagogy codes and the reasoning
behind each choice, is `teaching/w01-design-cycle.md` in the repository. This
page is what you have open on the day.

---

## Preflight

Allow an hour. Run it in order: each step depends on the one above, and the
first three are the ones that stop the session dead.

### 1. The plant model is this rig's, not last year's

Everything downstream is checked against these three numbers, so they come
first.

```matlab
cd models
fit_second_order('rig-data/your-recording.mat')
```

Expect `K` near 3.4 deg/V, `wn` near 1.0 rad/s, `zeta` near 0.06. If the fit
warns that the arm was already swinging before the step, take the recording
again: a starting trim read off a partial oscillation moves the gain by a
quarter.

Write the three numbers into `models/elevation_plant.json`, then push them out
to the folder students have:

```bash
.venv/bin/python scripts/sync_student_code.py
```

It prints what it copied. Running it twice should say nothing was copied the
second time.

### 2. The two envelopes still agree

There is one envelope, implemented twice: MATLAB for the room, Python for the
repository. If they disagree, whose gains fly depends on which tool you ran.

```bash
cd models && matlab -batch compare_envelope
```
```bash
.venv/bin/python scripts/compare_envelope.py
```

Expect `12 gain sets, identical verdicts, metrics within tolerance`. Anything
else stops here.

### 3. A known-good set still passes, and a known-bad set still fails

```matlab
heli_check_one(0.71, 0.59, 0.91)     % expect true
heli_check_one(7.13, 0.20, 12.6)     % expect false: phase margin
```

The second is the fallback from when the plant was assumed to be a double
integrator. It should be refused. If it passes, the model file is wrong.

### 4. What the flown model does with the derivative

**Five minutes, and it decides whether the voltage check means anything.**

The envelope assumes the controller differentiates the *measured angle*, not
the error, which is what the handout calls rate feedback. Open the model you
will actually fly and confirm it.

`m_part3.slx` carries signals named `ElevRate(deg/s)` and `PitchRate(deg/s)`,
which is the structure the envelope assumes, so this is a confirmation rather
than a hunt. But the laboratory's own `PID.slx` differentiates the *error*, so
both structures exist in the material and it is worth ten seconds of looking.

If the flown controller differentiates the error, then for accepted gains the
demand at the start of a ramped command is roughly `Kd` times the command
rate: at `Kd = 0.91` and 45 deg/s, about 41 V.

**This is not a safety problem.** The flown model clamps the motor at
±24 V and the DAC at ±10 V, so it saturates rather than over-driving
anything. It is a fidelity problem: the flight would be a saturated,
non-linear one, and it would not match the design anybody predicted. If that
is the structure, say so in the room rather than pretending the comparison
holds.

### 5. The submission round trip

Do this one for real, as a student would.

```matlab
cd docs/w01-design-cycle/code
submit_gains(0.71, 0.59, 0.91, 'Preflight')
```

Click the link it prints, submit the form, then export the responses and read
them back:

```matlab
collate_gains('~/Downloads/responses.xlsx')
```

Expect one row, `Preflight`, verdict `fly`. Delete that response afterwards so
it does not appear in the room.

### 6. The student scripts run start to finish

```matlab
cd docs/w01-design-cycle/code
s1_identify
s2_tune
```

`s1_identify` should end with the by-hand and `tfest` fits within a few percent
of each other. `s2_tune` should end with your design accepted and `pidtune`
refused for demanding too many volts. That contrast is the session's argument,
so check it is still there.

### 7. The deck

Open `docs/slides/w01-design-cycle/index.html` and step through it. Three
things to confirm rather than assume:

- every bullet on a slide is visible without pressing the arrow again;
- the three rig photographs load;
- the proportional-limit figure is legible from the back of the room.

### 8. The back row

Only checkable in the theatre. Do it while technical services set up: sit in
the back row and confirm you can see the rig, and the camera feed if you are
using one.

---

## Setup, 12:50 onwards

The theatre is in use until 12:50, so setup runs into the session while you
present. That is the standing arrangement, not a problem to solve on the day.

The deadline is not 13:00. The rig is first on camera at minute 20 and must
fly at minute 30.

| By | What |
|---|---|
| 12:50 | Rig in the room, on its bench |
| 13:20 | Guarding, tether, camera and feed working; the rig goes on screen |
| 13:30 | Powered, closed-loop test flight done, both switches tested |

Agree that sequence out loud with the technical staff at 12:50, so it is
theirs rather than assumed.

!!! danger "Before anything is powered"
    Locate the amplifier's rocker switch and the mains switch, and say out
    loud which is which. **There is no separate emergency stop and no software
    interlock.** These two switches are how the rig is stopped, and the risk
    assessment describes them that way. Test both under power before anybody
    else is near it.

---

## The session

Seven beats. The transitions are the structure students are meant to feel, so
they are named here in the same order as the slides and the handout.

| Beat | At | For | What happens |
|---|---|---|---|
| **Hook** | 0 | 5 | The claim, the vote, the volunteer named |
| **Learn A** | 5 | 15 | Why control exists; the design cycle |
| | 20 | 10 | Feedback as a trade |
| **Do A** | 30 | 5 | The rig: axes, and how it is made safe |
| **Learn B** | 35 | 15 | **The open-loop flight attempt**, and why a person loses |
| **Do B** | 50 | 10 | One axis, the fitted model, what Kp cannot do |
| | 60 | 10 | What a requirement is; agree today's, out loud |
| **Case** | 70 | 15 | System ID in the Live Script |
| | 85 | 12 | Tune, check, submit |
| | 97 | 15 | **Fly the submitted gains**, three rounds |
| **Cliffhanger** | 112 | 5 | The two gaps, and the independent work |
| | 117 | 3 | How the unit runs; the rest is on the site |

!!! warning "That last slot does not fit and you should decide now, not at 14:57"
    Eight slides sit in it: the term map, your week, what counts, four on AI,
    and the sources. Three minutes covers two or three of them.

    The removal candidate is the **four AI slides**. The handout carries that
    argument in full and the [AI in this course](../ai.md) page carries it
    again, so one sentence and a pointer does the job. Keep "What counts",
    because nothing else this term says plainly what carries the grade.

    The alternative is to take the time from round 3 of the flying, which is
    the wrong trade: the flying is why they turned up.

**Protect the flight attempt.** If hour one is running late, cut the
design-cycle block, not this. It is the thing the session is built on.

### The transitions, in words

Each one is a question the next beat answers. They are in the handout as
italic lines and on the slides as dividers.

1. *So what is that shape?* → the design cycle
2. *Step 1 is understanding the plant. Before that, one idea the whole loop rests on.* → feedback as a trade
3. *Enough theory. Here is the machine.* → the rig
4. *Why does a person, who can catch a ball and ride a bicycle, lose to this?* → the post-mortem
5. *So: what would count as having fixed it?* → requirements
6. *You have a target. You still need a model to design against.* → system ID
7. *Model, requirement, and a controller to find.* → tuning
8. *That is one full turn of the loop.* → the cliffhanger

### Three things to say, in these words

**Before the flight attempt**, define the task and the losing condition, then
vote. "Hold the marked elevation, on the marker, for 30 seconds; it ends when
it leaves plus or minus 10 degrees or goes past the marker." Without a losing
condition the vote may not resolve: elevation is stable, so the beam will not
fall, and travel has no stop to hit.

Afterwards, put the actual number next to the vote on the board, and be
specific that the failure is the machine's and not the pilot's.

**Before anybody submits:**

> The form asks for a display name, and that name goes on screen when your
> gains are flown. Put whatever you like: your own name, or a nickname. The
> form records your University account so I know whose is whose, and that is
> never shown to the room. Round one is the extremes, chosen because they
> misbehave, so somebody's name is going on a public failure.

Say it before, not after. Consent after the fact is not consent, and a student
who would be embarrassed will otherwise not submit at all, which costs the
exercise the spread it depends on.

**Before round two**, ask for a prediction. The cohort average is checked like
any other submission and it can fail even though every input passed. If it
does, do not fly it, and say why: it is a better lesson than the flight.

### Flying the submissions

```matlab
flights = collate_gains('~/Downloads/responses.xlsx')
```

Last submission per person, envelope applied, flyable ones first. Announce the
display name, never the account.

**Fallback gains**, if nothing passes or the form fails:
`Kp = 0.71, Ki = 0.59, Kd = 0.91`. Damping 0.66, phase margin 55°, 5.2 V peak,
settles in 5.9 s.

---

## If it goes wrong

| What | What to do |
|---|---|
| Rig will not run, or fails mid-session | Fall back to the recorded response and a recorded flight. Everything from system ID onwards works unchanged; only the live flying is lost. Have the recording on the machine, not in the cloud. |
| The form fails, or students cannot reach it | Take gains verbally from four or five pairs and type them into `heli_check_one`. Three rounds still work with a handful. |
| Students cannot get MATLAB working | Pair them with someone who can. Note who, and chase before next week. |
| `collate_gains` cannot find a column | It prints every header it found. The four questions are Display name, Kp, Ki, Kd. |
| The model file is missing or has only `K` | The tools refuse rather than guess. Refit, or pass the numbers directly. |
| Running late at minute 97 | Cut round one to two sets. Never cut the cliffhanger. |

---

## Afterwards

- Export the form responses and keep them. First cohort data of the year, and
  it says who has MATLAB working.
- Post the recorded flight, the data and the Live Scripts for anyone absent.
- Note the actual timings against the table above and update it the same day.
- Check who did not submit. Earliest signal of a student in difficulty.
