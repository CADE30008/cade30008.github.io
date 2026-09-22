<!-- version: 2026.3 (2026-09-22) -->

# Measuring this rig

Five things, in the order that matters. The first two are two minutes each and
both change what the lecture can claim.

Work in this folder. Everything it needs is here.

---

## 1. Does the flown model differentiate the measurement, or the error?

**Two minutes, and it decides whether the voltage check means anything.**

The envelope assumes the controller differentiates the *measured angle*. If it
differentiates the *error*, then for gains we accept, the demand at the start
of a ramped command is about `Kd` times the command rate: at Kd = 0.91 and
45 deg/s, roughly 41 V.

Not dangerous — the model clamps the motor at 24 V and the DAC at 10 V, so it
saturates rather than over-driving anything. But a saturated flight does not
match the design anybody predicted, and I would rather say so in the room than
discover it live.

Open `m_part3.slx`. Look at what feeds the derivative in the elevation loop.

- **Measured elevation** (there are signals named `ElevRate(deg/s)` and
  `PitchRate(deg/s)` in there, which is the structure I expect) → we are fine.
- **The error** → tell me, and I will change the envelope before 13:00.

The laboratory's own `PID.slx` differentiates the error, which is why this is
worth looking at rather than assuming.

**SEND ME:** measurement, or error.

---

## 2. What voltage holds the arm level?

**Two minutes.** The envelope assumes 8 V and works the controller's headroom
out from what is left up to 24. Quanser publish "approximately 7.5". Nobody
has measured this rig.

With `m_part1.slx` running and no controller, raise `Elevation Input` until
the arm sits level and steady. Read the voltage.

**SEND ME:** that number. A long way from 8 and the voltage limit moves, and
some currently accepted gains stop being accepted.

---

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
5. `s_save` into `data/`.

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
3. Save each into `data/` as `trim-<volts>V.mat`.

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
