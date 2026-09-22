<!-- version: 2026.10 (2026-09-22) -->

# Measuring this rig

Five things, in the order that matters. The first two are two minutes each and
both change what the lecture can claim.

Work in this folder. Everything it needs is here.

---

## 1. The derivative question — ANSWERED, 22 September

**Neither. The controller block is empty, and the students build what goes in
it.** So the structure is whatever they wire, not something the rig decides.

What the model gives them:

| Signal | Where it goes |
|---|---|
| `Elev(deg)` from the plant | back into the Controller block as `elev_output` |
| `ElevRate(deg/s)` | a terminator |

That terminator is the whole point. The measured rate is there, brought out,
and deliberately not connected: the obvious thing a student does is put a PID
on the error, and the rate signal is sitting beside it unused.

**Why it matters.** The envelope assumes the derivative acts on the measured
angle. If a student differentiates the error instead, the demand at the start
of a ramped command is about `Kd` times the command rate: at Kd = 0.91 and
45 deg/s, roughly 41 V. The model clamps the motor at 24 V and the DAC at 10,
so it saturates rather than damaging anything, but the flight then has nothing
to do with the design they checked.

So it is not a question about the rig any more. It is **a requirement on the
controller they build**, and the laboratory pages now say so in Part 2 and
Part 3. Nothing further to test here.

## 2. What holds the arm level — PART ANSWERED, and one thing left

**There is an `elev offset` summed with `Elevation Input` before `Velev`, and
it is set to 18.** So the trim is built into the model rather than dialled in,
which answers half the question.

**What the fitted model is unaffected by.** K = 3.4 deg/V came from a *step*
in Elevation Input, 0 to 2. A constant offset cancels out of a step response,
so K, wn and zeta all stand, and every gain we have checked is still checked
against the right plant. Nothing about the controller design changes.

**What it may change is the voltage headroom**, which is the one envelope
limit not derived from the fit. The envelope assumes the arm sits at 8 V and
gives the controller 0.7 of what is left up to 24, which is 11.2 V. Whether
that is right depends on what `Velev` is measured in, and I cannot tell from
the file:

| If `Velev` is... | Then 18 means | Headroom up | Our 11.2 V is |
|---|---|---|---|
| volts at each motor | 18 V per motor | about 6 V to the 24 V rail | **far too generous** |
| a combined demand, halved between the two | 9 V per motor | about 15 V per motor | about right |

Nine volts per motor sits nicely beside the 7.5 V Quanser publish, so the
second reading is the likely one. Likely is not checked.

**The check, and it is a look rather than a measurement.** Follow `Velev` out
of that sum block. If it goes through a gain of 0.5, or fans out to two motor
channels that each take half, it is a combined demand and we are fine. If it
goes to a motor channel as it stands, the envelope is roughly twice as
permissive as it should be and I will tighten it before anybody flies.

**SEND ME:** which of those it does. One line.

## `results.mat` — fixed in the supplied models

**Both models here have file logging off**, so neither writes `results.mat`
and there is nothing to lock. Nothing is lost by it: the data comes from the
scopes, which log `inputData`, `elevData`, `pitchData` and `travelData`
straight to the workspace, and that is what `save_recording` reads.

It was Simulink's own setting, not QUARC's: **Configuration Parameters ->
Data Import/Export -> Log Dataset data to file**, which is `LoggingToFile`.
QUARC has a button that opens that panel, which is why it looked like theirs.
`part1_identify` had it on and pointed at `results.mat`; `part3_validate`
already had it off.

**If you meet a bench copy with it still on**, the file is held by the target
process rather than by MATLAB, which is why Explorer will not delete it
either, and stopping the model does not release it:

1. `QUARC -> Unload`, or `qc_unload_model`. Stop, then unload.
2. Still locked: kill the `*.rt-win64.exe` for this model in Task Manager.
3. Then turn the setting off rather than working around it again:
   `set_param('part1_identify', 'LoggingToFile', 'off')`.

## 3. One clean step at the level datum

**Six minutes, most of it waiting.** Start the student code checker while this
settles.

1. `Yaw Demand = 0`, `Elevation Input = 0`.
2. **Hold the arm level** and start the model. The encoder zeroes itself
   wherever the arm is when the model starts, so where you hold it *is* the
   datum for everything that follows.
3. Let it settle. Give it a full minute: at this damping a disturbance rings
   for about that long, and a leftover swing lands in the fit.
4. Step `Elevation Input` from 0 to 2. Do not touch anything else.
5. `save_recording('level-datum')`, which writes into whatever folder you are in.

Then:

```matlab
t1_fit_this_rig
```

It fits the newest recording, prints K, wn and zeta, and compares them with
the stored laboratory fit.

**SEND ME:** the three numbers, and whether it warned about the arm already
swinging.

---

## 4. Three more, at different trims

**Eight minutes.** This settles something the recording we have cannot.

In the stored recording the arm swings with a period of 5.85 s about the level
datum and 6.02 s at +7 degrees: the same, within 3%. The old claim in the run
sheet was that gravity stiffness goes as sin(elevation), which needs the
period at level to grow without limit. It does not, so that story is out. What
is still unknown is how much wn moves across the *whole* range.

1. Elevation Input to 1.0, settle fully, step to 1.5, record 40 s.
2. Repeat 2.0 → 2.5, and 2.5 → 3.0.
3. `save_recording('trim-2V')`, and so on.

```matlab
rig_trim_sweep('data/*.mat')
```

It fits each, plots wn against trim, and says which story the data looks like.

**SEND ME:** the table it prints, or just the .mat files.

---

## 5. Fly four sets of gains

**Six minutes.**

```matlab
t2_fly_these                      % against the stored model
t2_fly_these(3.5, 1.02, 0.07)     % against your own fit from §3
```

Four sets, with what each should do. Two accepted, one refused on volts, one
refused as unstable.

Fly the two accepted. Fly the volts one as well if you are willing: it should
saturate and look worse than the model claims, which is the point the session
ends on. **Do not fly the unstable one.**

**SEND ME:** overshoot and settling time for the two accepted sets, and
whether the motors sounded like they were saturating.

---

## Afterwards

If the fit in §3 differs much from the stored one, that is the number the
whole session is checked against. Put it into `elevation_plant.json` in the
repository, then:

```bash
.venv/bin/python scripts/sync_student_code.py
npm run drive -- --bump
```

The second one is what tells students their copy is stale.
