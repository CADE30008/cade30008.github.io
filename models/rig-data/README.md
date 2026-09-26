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
% ... fly or step the rig, and let the run finish ...
heli_log_session([], 'elevation-step-2V', 'models/rig-data')
```

The `[]` means "read what the model left in the workspace", which is how the
laboratory models log. Pass a `Simulink.SimulationData.Dataset` there instead
if the model you built logs that way.

That writes a `.mat` and a `.csv` with three columns:

| Column | Units |
|---|---|
| `time_s` | seconds |
| `input_V` | Elevation Input, which is what the fitted `K` is per |
| `elevation_deg` | degrees |

`input_V` is not the motor voltage. It is the demand one offset block before
`Velev`, and `K = 3.4 deg/V` was measured by stepping it from 0 to 2.

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
fit_second_order('models/rig-data/elevation-step-2V-2026-09-21.csv')
```

That returns `K`, `wn` and `zeta`. It does not write anything: put the three
numbers into `models/elevation_plant.json` yourself, then run
`scripts/sync_student_code.py` to push them to the folder students have. Every
gain checker reads that file, so the whole toolchain follows the measurement
from that point on.

## The one thing to watch

The model is **second order**, so a step should rise, overshoot and settle
back, swinging slowly for half a minute on the way. Quanser's own
linearisation gives a double integrator, but that is taken about level, where
gravity stiffness is exactly zero; the rig is flown about a trim, and there it
oscillates.

`fit_second_order` reads `K` from where the arm ends up, and `wn` and `zeta`
from the swinging on the way. It warns rather than refusing, in two cases that
both matter:

- **fewer than two peaks**, so `wn` and `zeta` come back as `NaN` and only `K`
  is a number. Either the step was too small to excite the arm, or it is
  trimmed somewhere with no oscillation in it;
- **the arm already swinging before the step**, which makes the starting trim
  wherever that swing happened to be, and moves `K` by about a quarter.

Neither stops it returning a struct, so read what it prints. Both are worth a
second recording rather than a fit.

See `models/quanser_trim_stiffness.py` for where the stiffness comes from and
`models/rig_trim_sweep.m` for the experiment that settles whether one model
covers the working range.

<!-- tracking: status=draft version=0 assisted=true -->
