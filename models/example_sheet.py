"""Numbers for the week 3 (PID) example sheet and its worked solutions.

Every answer quoted in the solutions is computed here, and checked against
the hand-calculation route where there is one. Run from the repository root:

    .venv/bin/python models/example_sheet.py

Writes models/example_numbers.json.
"""

import json
from pathlib import Path

import control as ct
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "models" / "example_numbers.json"
s = ct.tf("s")
D2R = np.pi / 180
ans = {}


def margins(L):
    gm, pm, w180, wc = ct.margin(L)
    return dict(GM=float(gm), GM_dB=float(20 * np.log10(gm)) if np.isfinite(gm) else None,
                PM=float(pm), wc=float(wc), w180=float(w180))


def step_info(T, t_end=15):
    i = ct.step_info(T, T=np.linspace(0, t_end, 15001), SettlingTimeThreshold=0.02)
    return dict(rise=float(i["RiseTime"]), OS=float(i["Overshoot"]), ts=float(i["SettlingTime"]))


# ---------------------------------------------------------------- Q1: PID forms
Kc, Ti, Td, N = 2.0, 4.0, 0.25, 10
zeros = np.sort(np.roots([Td * Ti, Ti, 1]))
ans["Q1"] = dict(Kp=Kc, Ki=Kc / Ti, Kd=Kc * Td, filter_pole=N / Td,
                 zeros=[float(z) for z in zeros], hf_gain=Kc * (N + 1))

# ------------------------------------------------ Q2: steady-state errors, pitch loop
G = 40 / (s * (s + 2) * (s + 10))
Kp = 1.5
L = Kp * G
Kv = float(ct.dcgain(ct.minreal(s * L, verbose=False)))
omega = 2.0                  # deg/s pitch-over rate
d = 1.5                      # deg of elevator-equivalent disturbance
# check the ramp error by simulation
t = np.linspace(0, 40, 40001)
y_ramp = ct.forced_response(ct.feedback(L, 1), t, omega * t).outputs
e_ramp = float(omega * t[-1] - y_ramp[-1])
y_dist = ct.step_response(ct.minreal(G / (1 + L), verbose=False), t).outputs * d
ans["Q2"] = dict(Kp=Kp, Kv=Kv, ramp_error_deg=omega / Kv, ramp_error_sim=e_ramp,
                 dist_offset_deg=d / Kp, dist_offset_sim=float(y_dist[-1]))

# ------------------------------------------------ Q3: P design on a roll loop
Gr = 81 / (s * (s + 3) * (s + 15))
w180 = np.sqrt(45.0)
gm1 = 1 / abs(complex(ct.evalfr(Gr, 1j * w180)))
# PM = 45 deg: atan(w/3) + atan(w/15) = 45 deg  ->  w^2 + 18 w - 45 = 0
wc45 = (-18 + np.sqrt(18**2 + 4 * 45)) / 2
Kp45 = 1 / abs(complex(ct.evalfr(Gr, 1j * wc45)))
# PM = 60 deg: atan(w/3) + atan(w/15) = 30 deg
t30 = np.tan(30 * D2R)
a, b, c = t30 / 45, 0.4, -t30
wc60 = (-b + np.sqrt(b * b - 4 * a * c)) / (2 * a)
Kp60 = 1 / abs(complex(ct.evalfr(Gr, 1j * wc60)))
zeta = 0.45
os_est = 100 * np.exp(-np.pi * zeta / np.sqrt(1 - zeta**2))
s45 = step_info(ct.feedback(Kp45 * Gr, 1))
s60 = step_info(ct.feedback(Kp60 * Gr, 1))
ans["Q3"] = dict(w180=float(w180), GM_Kp1=float(gm1), GM_Kp1_dB=float(20 * np.log10(gm1)),
                 wc45=float(wc45), Kp45=float(Kp45), check45=margins(Kp45 * Gr),
                 os_estimate=float(os_est), step45=s45,
                 wc60=float(wc60), Kp60=float(Kp60), check60=margins(Kp60 * Gr), step60=s60,
                 rise_ratio_estimate=float(wc45 / wc60),
                 rise_ratio_actual=s60["rise"] / s45["rise"])

# ------------------------------------------------ Q4: multirotor altitude hold
m, tau, g0 = 1.5, 0.05, 9.81
Ga = 1 / (m * s**2 * (tau * s + 1))                 # altitude (m) per thrust (N)
wc = 4.0
ph_plant = -180 - np.degrees(np.arctan(wc * tau))
lead = 45 - (180 + ph_plant)
Td4 = np.tan(np.radians(lead)) / wc
Gj = abs(complex(ct.evalfr(Ga, 1j * wc)))
Kp4 = 1 / (abs(1 + 1j * wc * Td4) * Gj)
Kd4 = Kp4 * Td4
C_pd = Kp4 * (1 + Td4 * s)
dT = 0.05 * m * g0
C_pd_real = Kp4 + Kd4 * s / (Td4 / 20 * s + 1)      # check with a mild filter too
# PI addition with Ti = 2.5 s
Ti4 = 2.5
cost = np.degrees(np.arctan(1 / (wc * Ti4)))
C_pid_same = Kp4 * (1 + 1 / (Ti4 * s) + Td4 * s)
# redesign: find Td, Kp for PM 45 at 4 rad/s including the integral lag
shape = lambda T: 1 + 1 / (1j * wc * Ti4) + 1j * wc * T
Td4b = brentq(lambda T: np.degrees(np.angle(shape(T))) - lead, 0.05, 5)
Kp4b = 1 / (abs(shape(Td4b)) * Gj)
C_pid = Kp4b * (1 + 1 / (Ti4 * s) + Td4b * s)
t = np.linspace(0, 30, 30001)
off_pd = ct.step_response(ct.minreal(Ga / (1 + C_pd * Ga), verbose=False), t).outputs * dT
off_pid = ct.step_response(ct.minreal(Ga / (1 + C_pid * Ga), verbose=False), t).outputs * dT
cl_p = np.roots([m * tau, m, 0, 1.0])   # P only, Kp = 1: m tau s^3 + m s^2 + Kp
ans["Q4"] = dict(m=m, tau=tau, wc=wc, plant_phase=float(ph_plant), lead=float(lead),
                 Td=float(Td4), Kp=float(Kp4), Kd=float(Kd4), plant_mag=float(Gj),
                 check_pd=margins(C_pd * Ga), check_pd_filtered_N20=margins(C_pd_real * Ga),
                 dT=float(dT), offset_pd_m=float(dT / Kp4), offset_pd_sim=float(off_pd[-1]),
                 Ti=Ti4, integral_cost=float(cost), check_pid_unchanged=margins(C_pid_same * Ga),
                 Td_redesign=float(Td4b), Kp_redesign=float(Kp4b), Ki_redesign=float(Kp4b / Ti4),
                 Kd_redesign=float(Kp4b * Td4b), check_pid=margins(C_pid * Ga),
                 offset_pid_sim=float(off_pid[-1]),
                 p_only_poles=[complex(r) for r in cl_p].__repr__())

# ------------------------------------------------ Q5: kick and noise, lecture PID
Kp5, Ki5, Kd5, N5 = 2.03, 0.678, 0.661, 10
step5 = 5.0
ans["Q5"] = dict(kick_deg=Kp5 * (N5 + 1) * step5, meas_initial_deg=Kp5 * step5,
                 hf_gain=Kp5 * (N5 + 1), theta_noise_deg=0.1,
                 elevator_jitter_deg=Kp5 * (N5 + 1) * 0.1,
                 gyro_noise_dps=0.5, gyro_elevator_jitter_deg=Kd5 * 0.5)

# Closed-loop stability checks. With three integrators in L, the PID loop's
# phase crosses -180 deg at low frequency, so margin() reports a gain-reduction
# margin below 1; the closed-loop poles settle the question.
def max_real_pole(L):
    return float(np.max(np.real(ct.poles(ct.feedback(L, 1)))))

ans["Q4"]["pd_max_real_pole"] = max_real_pole(C_pd * Ga)
ans["Q4"]["pid_max_real_pole"] = max_real_pole(C_pid * Ga)
ans["Q4"]["pid_unchanged_max_real_pole"] = max_real_pole(C_pid_same * Ga)
ans["Q4"]["pid_gain_reduction_margin"] = ans["Q4"]["check_pid"]["GM"]
ans["Q3"]["kp45_max_real_pole"] = max_real_pole(Kp45 * Gr)

OUT.write_text(json.dumps(ans, indent=2) + "\n")
print(json.dumps(ans, indent=2))

# tracking: status=draft version=0
