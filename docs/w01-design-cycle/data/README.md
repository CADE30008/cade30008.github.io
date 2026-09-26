# Measured elevation response

`elevation-step.mat` is a recorded step response of the Quanser 3-DOF
helicopter's elevation axis, taken in the laboratory. It is the recording you
fit a model to in the first half of the session.

Four variables, which is what the laboratory's own `s_save` writes:

| Variable | What |
|---|---|
| `inputTime` | time stamps for the input, seconds |
| `input` | motor voltage command, volts |
| `outputTime` | time stamps for the measured angle, seconds |
| `output` | measured elevation, degrees |

The input and the output are sampled on separate clocks, so they have their own
time vectors. Interpolate the input onto the output's clock before you fit
anything, or use `fit_second_order`, which does it for you.

Replaced each year with a recording from the rig as it stands. A model fitted
to last year's rig is a model of last year's rig.

<!-- tracking: status=draft version=0 assisted=true -->
