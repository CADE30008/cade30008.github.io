<!-- version: 2026.21 (2026-09-22) -->

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

## 2. What holds the arm level — ANSWERED, and it moved the envelope

**An Elevation Input of -1.6 holds the arm level, with the `elev offset DO NOT
TOUCH` block at 18.** So Velev trims at 16.4, and each motor sits at about
8.2 V, which agrees with the 7.5 Quanser publish.

The signal path, traced at the rig:

```
Elevation Input + elev offset (18)  ->  Velev
Velev -> saturate +/-25 -> voltage calculations
      -> summed and halved with the elevation motor demand
      -> u_front, u_back -> saturate +/-24 -> gain 1/3 -> DAC
```

**The envelope was working the budget out from the wrong limit.** It assumed
the motors bind and allowed 0.7*(24-8) = 11.2 V. They do not:

| Limit | Head-room, in Elevation Input units |
|---|---|
| Velev, +/-25 against a trim of 16.4 | **8.6** |
| motors, +/-24 against 8.2 each | 31.6 |

Velev binds, at 8.6, and the motors have room to spare. Keeping 0.7 of it
gives **6.0 V**, not 11.2, so the old figure was 1.9 times what the rig can
deliver and designs were being accepted that would have clipped.

Fixed in both envelopes, and the student design in `s2_tune` was retuned: at
the old limit it asked for 8.4 V, which would now be refused. The fallback
gains are unaffected and still pass with room.

Nothing further to check here.

## `results.mat` — fixed in the supplied models

**Both models here have file logging off**, so neither writes `results.mat`
and there is nothing to lock. Nothing is lost by it: the data comes from the
scopes, which log straight to the workspace, and that is what
`save_recording` reads.

It was Simulink's own setting, not QUARC's: **Configuration Parameters →
Data Import/Export → Log Dataset data to file**, which is `LoggingToFile`.
QUARC has a button that opens that panel, which is why it looked like theirs.

**MATLAB holds the file open**, which is why it could not be deleted or
renamed from MATLAB's file browser or from Explorer. Turning the setting off
is the fix; there is nothing to unload.

## 3. Level it, and check the activity works

**Three minutes, and it is the new first thing students do.** Every rig has
its own trim, so every group calibrates the one in front of them, and the
voltage budget follows from it.

1. `Elevation Input = 0`, arm **resting on the floor**, start the model. Not
   held: the encoder zeroes where it starts, and the floor is a position the
   rig will choose again.
2. Raise `Elevation Input` slowly until the arm sits level. Small steps, a few
   seconds each.
3. **Stop the model** with the arm sitting level. Nothing reaches the
   workspace until a run ends, so there is no angle to read before that, and
   stopping while it is level leaves the level angle at the end of the record.
4. `level_rig(<the value that held it>)`.

**Measured on this rig, 22 September: -1.6, giving a trim of 16.4 and 8.6 V
of head-room, of which the envelope keeps 6.0. Repeatable across two runs.**
So the figures the envelope is built on are this rig's, not an assumption.

**What to check while you are doing it:**

- Does the arm actually reach level, or does it run out of travel first?
- Is the value repeatable if you start over? Twice is enough to know.
- Does `level_rig` warn? It complains below 4 V of head-room and above 12,
  and both usually mean something is wrong rather than unusual.

**SEND ME:** the value for this rig, and whether the two runs agreed.

**Then check the other rigs, if there is time.** The spread across benches is
the thing I cannot guess at, and it decides whether one envelope serves the
whole laboratory or each group needs their own. `level_rig` writes
`rig_calibration.mat` and `heli_envelope` reads it, so per-group already
works; what I do not know is whether it is needed.

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
