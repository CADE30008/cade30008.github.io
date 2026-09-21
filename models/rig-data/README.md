# Recordings from the rig

**Put measured responses here.** This is the evidence behind
`models/elevation_plant.json`, and it is tracked so that the fitted `K` can be
re-derived by anyone rather than taken on trust.

Nothing student-produced belongs here. These are our own measurements of our
own hardware; student work never enters this repository.

## What to drop in, and what to call it

`models/heli_log_session.m` writes the right shape already. From the room:

```matlab
heli_demo_setup
% ... fly or step the rig, with logging on ...
heli_log_session(out.logsout, 'elevation-step-2V', 'models/rig-data')
```

That writes a `.mat` and a `.csv` with three columns:

| Column | Units |
|---|---|
| `time_s` | seconds |
| `input_V` | volts, the commanded increment |
| `elevation_deg` | degrees |

Name them `<what>-<yyyy-mm-dd>`, so `elevation-step-2V-2026-09-21.csv`. Keep
every recording, including the bad ones: a run where the arm hit a stop is
worth having when somebody asks why a fit moved.

## The trim sweep, if you have ten minutes at the rig

The open question about this rig is whether its natural frequency depends on
where the arm is trimmed. `models/rig_trim_sweep.m` answers it from four or
five recordings; its help has the procedure, and the short version is:

1. Set **Elevation Input**, let the arm settle for a full minute.
2. Nudge it by about +0.5 V and leave it.
3. Record 40 s of the swing, save as `trim-<volts>V-<date>.mat`.
4. Repeat at roughly 1.0, 1.5, 2.0, 2.5, 3.0 V.

Then `rig_trim_sweep` fits each and says whether the frequency is constant or
climbing. That decides whether one model covers the working range.

## Then fit it

```matlab
fit_elevation('models/rig-data/elevation-step-2V-2026-09-21.csv')
```

That fits `K` and rewrites `models/elevation_plant.json` with the value, the
file it came from and the date. Both gain checkers read that file, so the whole
toolchain follows the measurement from that point on.

## The one thing to watch

The model week 1 uses is a **double integrator**, so a step should give a
response that curves away and keeps going. If the recording instead rises and
**settles**, the arm has a restoring term — most likely because it is trimmed
away from level, where gravity provides stiffness — and a double-integrator fit
of it is meaningless. `fit_elevation` says so rather than returning a number.

See `models/quanser_trim_stiffness.py` for why that happens and how large it is.
