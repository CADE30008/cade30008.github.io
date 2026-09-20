"""Pitch-attitude loop for CADE30008 week 3 (PID): model, designs, numbers and figures.

This script is the single source for every number and plot in the week 3 (PID)
handout and slides. Run it from the repository root:

    .venv/bin/python models/pitch.py

It writes the figures to docs/w03-pid-control/figures/ and the numbers to
models/pitch_numbers.json. models/pitch_check.m recomputes the same numbers
in MATLAB, and models/compare.py checks that the two agree.
"""

import json
from pathlib import Path

import control as ct
import matplotlib
import numpy as np
from scipy.optimize import brentq

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "docs" / "w03-pid-control" / "figures"
NUMBERS = ROOT / "models" / "pitch_numbers.json"

# --------------------------------------------------------------------------
# Plant: small fixed-wing UAV, pitch attitude from elevator.
#   pitch rate responds to elevator with time constant 0.5 s and gain 2 (rad/s)/rad,
#   the elevator servo lags with time constant 0.1 s,
#   and attitude is the integral of pitch rate.
#   G(s) = 2/(0.5 s + 1) * 1/(0.1 s + 1) * 1/s = 40 / (s (s + 2) (s + 10))
# --------------------------------------------------------------------------
s = ct.tf("s")
G = 40 / (s * (s + 2) * (s + 10))
N = 10                       # derivative filter: pole at N / Td
U_MAX = np.deg2rad(20.0)     # elevator travel limit, +/- 20 deg
STEP = np.deg2rad(10.0)      # standard attitude step for comparisons
T_END = 8.0

# Flight Lab palette (matches the slide theme)
RED, TEAL, ORANGE, PURPLE, GREY, INK = "#B01C2E", "#00A89E", "#EE7219", "#9278D1", "#8A8F8D", "#1D1D1B"


# --------------------------------------------------------------------------
# Controller: parallel PID with a first-order filter on the derivative term
#   C(s) = Kp + Ki/s + Kd s / (Tf s + 1),   Tf = Td / N,   Td = Kd / Kp
# In the reference path the derivative acts on the measurement only.
# --------------------------------------------------------------------------
def controller(Kp, Ki=0.0, Kd=0.0):
    C = ct.tf([Kp], [1])
    if Ki:
        C = C + Ki / s
    if Kd:
        Tf = Kd / (N * Kp)
        C = C + Kd * s / (Tf * s + 1)
    return C


def margins(L):
    gm, pm, w180, wc = ct.margin(L)
    return {
        "GM": float(gm),
        "GM_dB": float(20 * np.log10(gm)),
        "PM_deg": float(pm),
        "wc": float(wc),
        "w180": float(w180),
    }


def closed_loops(Kp, Ki=0.0, Kd=0.0):
    """Reference-to-attitude, reference-to-elevator and disturbance-to-attitude."""
    C = controller(Kp, Ki, Kd)
    Cr = controller(Kp, Ki)          # what the reference sees (D on measurement)
    den = 1 + C * G
    T_ref = ct.minreal(Cr * G / den, verbose=False)
    T_u = ct.minreal(Cr / den, verbose=False)
    T_dist = ct.minreal(G / den, verbose=False)   # input (elevator-equivalent) disturbance
    return C, T_ref, T_u, T_dist


def step_metrics(T, t_end=T_END):
    info = ct.step_info(T, T=np.linspace(0, t_end, 8001), SettlingTimeThreshold=0.02)
    return {
        "rise_time": float(info["RiseTime"]),
        "overshoot_pct": float(info["Overshoot"]),
        "settling_time": float(info["SettlingTime"]),
    }


def design_p_for_pm(pm_target):
    return brentq(lambda k: margins(k * G)["PM_deg"] - pm_target, 0.1, 5.9)


def design_pd(wc, pm):
    """Filtered PD giving phase margin pm (deg) at crossover wc (rad/s)."""
    Gj = complex(ct.evalfr(G, 1j * wc))
    need = pm - (180 + np.degrees(np.angle(Gj)))
    lead = lambda Td: np.degrees(np.angle(1 + 1j * wc * Td / (1j * wc * Td / N + 1))) - need
    Tds = np.logspace(-3, 2, 5000)
    k = int(np.argmax([lead(T) >= 0 for T in Tds]))
    Td = brentq(lead, Tds[k - 1], Tds[k])
    Kp = 1 / abs((1 + 1j * wc * Td / (1j * wc * Td / N + 1)) * Gj)
    return Kp, Td


def design_pid(wc, pm, Ti):
    """Filtered PID with fixed Ti, giving phase margin pm at crossover wc."""
    Gj = complex(ct.evalfr(G, 1j * wc))
    shape = lambda Td: 1 + 1 / (1j * wc * Ti) + 1j * wc * Td / (1j * wc * Td / N + 1)
    need = pm - (180 + np.degrees(np.angle(Gj)))
    f = lambda Td: np.degrees(np.angle(shape(Td))) - need
    Tds = np.logspace(-3, 2, 5000)
    k = int(np.argmax([f(T) >= 0 for T in Tds]))
    Td = brentq(f, Tds[k - 1], Tds[k])
    Kp = 1 / abs(shape(Td) * Gj)
    return Kp, Td


def simulate(Kp, Ki, Kd, r_step, d_step=0.0, t_d=None, u_max=np.inf,
             anti_windup=False, d_on_error=False, t_end=T_END, dt=5e-4):
    """Fixed-step RK4 simulation of the loop with an elevator limit.

    Anti-windup is conditional integration: the integrator holds while the
    elevator is saturated and the error would drive it further into the limit.
    """
    A, B, Cm, _ = ct.ssdata(ct.ss(G))
    A, B, Cm = np.asarray(A), np.asarray(B).ravel(), np.asarray(Cm).ravel()
    Tf = Kd / (N * Kp) if Kd else 1.0
    n = int(round(t_end / dt)) + 1
    t = np.linspace(0, t_end, n)
    x = np.zeros(A.shape[0]); xi = 0.0; xf = 0.0
    y_out, u_out = np.zeros(n), np.zeros(n)

    def control(xp, xi_, xf_, tk):
        y = Cm @ xp
        r = r_step
        e = r - y
        sig = e if d_on_error else -y          # signal the derivative acts on
        D = Kd * (sig - xf_) / Tf if Kd else 0.0
        u_raw = Kp * e + Ki * xi_ + D
        u = float(np.clip(u_raw, -u_max, u_max))
        return y, e, sig, u, u_raw

    def deriv(xp, xi_, xf_, tk):
        y, e, sig, u, u_raw = control(xp, xi_, xf_, tk)
        d = d_step if (t_d is not None and tk >= t_d) else 0.0
        dx = A @ xp + B * (u + d)
        hold = anti_windup and (u != u_raw) and (np.sign(e) == np.sign(u_raw))
        dxi = 0.0 if hold else e
        dxf = (sig - xf_) / Tf if Kd else 0.0
        return dx, dxi, dxf

    # The derivative filter starts at rest on zero. With D on the measurement its
    # input is -y = 0 at t = 0, so nothing happens; with D on the error its input
    # jumps to the step size, which is exactly the derivative kick.
    for k in range(n):
        y, e, sig, u, _ = control(x, xi, xf, t[k])
        y_out[k], u_out[k] = y, u
        if k == n - 1:
            break
        tk = t[k]
        k1 = deriv(x, xi, xf, tk)
        k2 = deriv(x + dt / 2 * k1[0], xi + dt / 2 * k1[1], xf + dt / 2 * k1[2], tk + dt / 2)
        k3 = deriv(x + dt / 2 * k2[0], xi + dt / 2 * k2[1], xf + dt / 2 * k2[2], tk + dt / 2)
        k4 = deriv(x + dt * k3[0], xi + dt * k3[1], xf + dt * k3[2], tk + dt)
        x = x + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        xi = xi + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        xf = xf + dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
    return t, y_out, u_out


# --------------------------------------------------------------------------
# Designs. Gains are rounded to three significant figures, and every metric
# quoted in the teaching material is computed from the rounded gains.
# --------------------------------------------------------------------------
def r3(x):
    return float(f"{x:.3g}")


designs = {}
designs["P"] = dict(Kp=1.0, Ki=0.0, Kd=0.0, note="P, Kp = 1")
designs["P_pm60"] = dict(Kp=r3(design_p_for_pm(60)), Ki=0.0, Kd=0.0, note="P tuned for 60 deg PM")
Kp_pd, Td_pd = design_pd(3.0, 60)
designs["PD"] = dict(Kp=r3(Kp_pd), Ki=0.0, Kd=r3(Kp_pd * Td_pd), note="PD, wc = 3 rad/s, PM = 60 deg")
TI = 3.0
Kp_pid, Td_pid = design_pid(3.0, 55, TI)
designs["PID"] = dict(Kp=r3(Kp_pid), Ki=r3(Kp_pid / TI), Kd=r3(Kp_pid * Td_pid),
                      note="PID, wc = 3 rad/s, PM = 55 deg, Ti = 3 s")

numbers = {"plant": "40/(s(s+2)(s+10))", "N": N, "u_max_deg": 20.0, "designs": {}}
for name, d in designs.items():
    Kp, Ki, Kd = d["Kp"], d["Ki"], d["Kd"]
    C, T_ref, T_u, T_dist = closed_loops(Kp, Ki, Kd)
    m = margins(C * G)
    sm = step_metrics(T_ref)
    t = np.linspace(0, T_END, 8001)
    u10 = ct.step_response(T_u, t).outputs * STEP
    td = np.linspace(0, 30, 30001)
    yd = ct.step_response(T_dist, td).outputs
    numbers["designs"][name] = {
        **d,
        "Ti": Kp / Ki if Ki else None,
        "Td": Kd / Kp if Kd else None,
        **m,
        **sm,
        "peak_elevator_deg_per_10deg_step": float(np.degrees(np.max(np.abs(u10)))),
        "dist_final_per_unit": float(ct.dcgain(T_dist)),
        "dist_peak_per_unit": float(np.max(yd)),
    }

# Derivative kick: filtered D on the error, 10 deg step. Initial elevator = Kp (N + 1) * step.
pd = designs["PD"]
_, _, u_err = simulate(pd["Kp"], 0, pd["Kd"], STEP, d_on_error=True, t_end=1.0)
numbers["kick"] = {
    "peak_elevator_deg_D_on_error": float(np.degrees(np.max(np.abs(u_err)))),
    "formula_Kp_N_plus_1_times_step_deg": float(pd["Kp"] * (N + 1) * 10.0),
}

# Integrator windup: 25 deg attitude step, elevator limited to +/- 20 deg.
pid = designs["PID"]
WIND_STEP = np.deg2rad(25.0)
runs = {}
for label, kw in [("linear", dict()),
                  ("saturated", dict(u_max=U_MAX)),
                  ("anti_windup", dict(u_max=U_MAX, anti_windup=True))]:
    t, y, u = simulate(pid["Kp"], pid["Ki"], pid["Kd"], WIND_STEP, t_end=12.0, **kw)
    runs[label] = (t, y, u)
    ref = WIND_STEP
    over = (np.max(y) - ref) / ref * 100
    band = np.abs(y - ref) > 0.02 * ref
    ts = float(t[np.nonzero(band)[0][-1]]) if band.any() else 0.0
    numbers.setdefault("windup", {})[label] = {"overshoot_pct": float(over), "settling_time": ts}

NUMBERS.write_text(json.dumps(numbers, indent=2) + "\n")


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": ["Trebuchet MS", "DejaVu Sans"],
    "font.size": 11,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.grid": True,
    "grid.color": "#D9DCDB",
    "grid.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
    "svg.fonttype": "path",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    # Matplotlib seeds the SVG clip-path and marker element IDs from a random
    # salt, so an unchanged figure re-saves with fresh IDs and shows up as a
    # diff. Pinning the salt keeps the IDs stable, which (with the suppressed
    # date in save() below) means git only reports figures that really changed.
    "svg.hashsalt": "cade30008-pitch",
})
FIG.mkdir(parents=True, exist_ok=True)
LABEL = {
    "P": r"P, $K_p = 1$",
    "P_pm60": r"P, $K_p = 0.509$",
    "PD": r"PD, $\omega_c = 3$ rad/s",
    "PID": r"PID, $\omega_c = 3$ rad/s",
}
W = np.logspace(-1, 2, 800)


def bode_data(L, w=W):
    resp = ct.frequency_response(L, w)
    mag = 20 * np.log10(np.abs(resp.complex).ravel())
    ph = np.degrees(np.unwrap(np.angle(resp.complex).ravel()))
    if ph[0] > 0:
        ph -= 360
    return mag, ph


def save(fig, name):
    # metadata Date=None drops the <dc:date> stamp, which would otherwise make
    # every run a diff. See the svg.hashsalt note in the rcParams above.
    fig.savefig(FIG / f"{name}.svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)


def bode_axes():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True,
                                 gridspec_kw={"height_ratios": [1, 1]})
    a1.set_xscale("log")
    a1.set_ylabel("Magnitude (dB)")
    a2.set_ylabel("Phase (deg)")
    a2.set_xlabel("Frequency (rad/s)")
    a2.set_yticks([-90, -135, -180, -225, -270])
    return fig, a1, a2


# 1. Plant Bode with asymptotes
fig, a1, a2 = bode_axes()
mag, ph = bode_data(G)
a1.plot(W, mag, color=RED, lw=2.2, label=r"$G(j\omega)$")
asym = np.where(W < 2, 20 * np.log10(2 / W),
                np.where(W < 10, 20 * np.log10(2 / 2) - 40 * np.log10(W / 2),
                         -40 * np.log10(10 / 2) - 60 * np.log10(W / 10)))
a1.plot(W, asym, color=GREY, lw=1.2, ls="--", label="asymptotes")
for w0 in (2, 10):
    a1.axvline(w0, color=GREY, lw=0.8, ls=":")
    a2.axvline(w0, color=GREY, lw=0.8, ls=":")
a1.text(0.25, 12, "−20 dB/dec", color=GREY)
a1.text(3.2, -10, "−40", color=GREY)
a1.text(16, -48, "−60", color=GREY)
a1.set_ylim(-80, 30)
a1.legend(loc="upper right")
a2.plot(W, ph, color=RED, lw=2.2)
a2.axhline(-180, color=INK, lw=0.8)
a2.set_ylim(-275, -85)
a1.set_title(r"Pitch attitude plant  $G(s)=\dfrac{40}{s(s+2)(s+10)}$", color=INK)
save(fig, "plant-bode")

# 2. P control: loop Bode with margins for Kp = 1
dP = numbers["designs"]["P"]
fig, a1, a2 = bode_axes()
mag, ph = bode_data(1.0 * G)
a1.plot(W, mag, color=RED, lw=2.2, label=r"$L = K_pG$,  $K_p=1$")
a1.axhline(0, color=INK, lw=0.8)
a2.plot(W, ph, color=RED, lw=2.2)
a2.axhline(-180, color=INK, lw=0.8)
wc, w180 = dP["wc"], dP["w180"]
a1.axvline(wc, color=TEAL, lw=1, ls="--")
a2.axvline(wc, color=TEAL, lw=1, ls="--")
a1.axvline(w180, color=ORANGE, lw=1, ls="--")
a2.axvline(w180, color=ORANGE, lw=1, ls="--")
a2.annotate("", xy=(wc, -180), xytext=(wc, -180 + dP["PM_deg"]),
            arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.6))
a2.text(wc * 0.93, -168, f"PM = {dP['PM_deg']:.0f}°", color=TEAL, ha="right")
a1.annotate("", xy=(w180, 0), xytext=(w180, -dP["GM_dB"]),
            arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.6))
a1.text(w180 * 1.08, -9, f"GM = {dP['GM_dB']:.1f} dB", color=ORANGE)
a1.text(wc * 0.62, 18, rf"$\omega_c$ = {wc:.2f}", color=TEAL, ha="right")
a1.text(w180 * 1.08, 18, rf"$\omega_{{180}}$ = {w180:.2f}", color=ORANGE)
a1.set_ylim(-60, 30)
a2.set_ylim(-275, -85)
a1.legend(loc="lower left")
save(fig, "p-bode-margins")

# 3. P control: step responses for a range of Kp
fig, ax = plt.subplots(figsize=(8, 4.2))
t = np.linspace(0, T_END, 4001)
for Kp, col in [(0.5, TEAL), (1.0, RED), (2.0, ORANGE), (4.0, PURPLE)]:
    T = ct.feedback(Kp * G, 1)
    y = ct.step_response(T, t).outputs
    pm = margins(Kp * G)["PM_deg"]
    ax.plot(t, y, color=col, lw=2, label=rf"$K_p$ = {Kp:g}  (PM {pm:.0f}°)")
ax.axhline(1, color=INK, lw=0.8)
ax.set_xlabel("Time (s)")
ax.set_ylabel(r"$\theta/\theta_{ref}$")
ax.set_xlim(0, T_END)
ax.legend(loc="lower right")
ax.set_title("Proportional control: more gain is faster but less damped", color=INK)
save(fig, "p-step-gains")

# 4. Phase margin vs overshoot (standard second-order loop)
z = np.linspace(0.05, 0.95, 400)
pm_z = np.degrees(np.arctan(2 * z / np.sqrt(np.sqrt(1 + 4 * z**4) - 2 * z**2)))
os_z = 100 * np.exp(-np.pi * z / np.sqrt(1 - z**2))
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(pm_z, os_z, color=RED, lw=2.2, label="second-order loop (exact)")
ax.plot(pm_z, 100 * np.exp(-np.pi * (pm_z / 100) / np.sqrt(1 - (pm_z / 100) ** 2)),
        color=GREY, lw=1.4, ls="--", label=r"using $\zeta \approx PM/100$")
for name, col in [("P", RED), ("P_pm60", TEAL)]:
    d = numbers["designs"][name]
    ax.plot(d["PM_deg"], d["overshoot_pct"], "o", color=col, ms=8)
    ax.text(d["PM_deg"] + 1.2, d["overshoot_pct"] + 2, LABEL[name], color=col)
ax.set_xlabel("Phase margin (deg)")
ax.set_ylabel("Step overshoot (%)")
ax.set_xlim(10, 80)
ax.set_ylim(0, 80)
ax.legend(loc="upper right")
ax.set_title("Phase margin sets damping, so it sets overshoot", color=INK)
save(fig, "pm-overshoot")

# 5. Input disturbance: P and PD leave an offset, PID removes it
fig, ax = plt.subplots(figsize=(8, 4.2))
td = np.linspace(0, 15, 6001)
for name, col in [("P", RED), ("PD", ORANGE), ("PID", TEAL)]:
    d = numbers["designs"][name]
    _, _, _, Tdist = closed_loops(d["Kp"], d["Ki"], d["Kd"])
    y = ct.step_response(Tdist, td).outputs * np.deg2rad(2.0)
    ax.plot(td, np.degrees(y), color=col, lw=2, label=LABEL[name])
ax.axhline(0, color=INK, lw=0.8)
ax.set_xlabel("Time (s)")
ax.set_ylabel(r"Attitude error $\theta$ (deg)")
ax.set_xlim(0, 15)
ax.legend(loc="upper right")
ax.set_title("A 2° trim offset at the elevator: only integral action removes it", color=INK)
save(fig, "disturbance-offset")

# 6. PD: loop Bode, P vs PD (phase lead at crossover)
dPD = numbers["designs"]["PD"]
fig, a1, a2 = bode_axes()
for name, col in [("P", RED), ("PD", ORANGE)]:
    d = numbers["designs"][name]
    mag, ph = bode_data(controller(d["Kp"], d["Ki"], d["Kd"]) * G)
    a1.plot(W, mag, color=col, lw=2.2, label=LABEL[name])
    a2.plot(W, ph, color=col, lw=2.2)
    a1.axvline(d["wc"], color=col, lw=0.9, ls="--")
    a2.axvline(d["wc"], color=col, lw=0.9, ls="--")
    a2.plot(d["wc"], -180 + d["PM_deg"], "o", color=col, ms=6)
a1.axhline(0, color=INK, lw=0.8)
a2.axhline(-180, color=INK, lw=0.8)
a2.text(dPD["wc"] * 1.1, -180 + dPD["PM_deg"] + 4, f"PM {dPD['PM_deg']:.0f}°", color=ORANGE)
a2.text(dP["wc"] * 0.45, -180 + dP["PM_deg"] - 16, f"PM {dP['PM_deg']:.0f}°", color=RED)
a1.set_ylim(-60, 40)
a2.set_ylim(-275, -85)
a1.legend(loc="lower left")
save(fig, "pd-bode")

# 7. PD vs P step response
fig, ax = plt.subplots(figsize=(8, 4.2))
t = np.linspace(0, T_END, 4001)
for name, col in [("P", RED), ("P_pm60", TEAL), ("PD", ORANGE)]:
    d = numbers["designs"][name]
    _, Tr, _, _ = closed_loops(d["Kp"], d["Ki"], d["Kd"])
    ax.plot(t, ct.step_response(Tr, t).outputs, color=col, lw=2, label=LABEL[name])
ax.axhline(1, color=INK, lw=0.8)
ax.set_xlabel("Time (s)")
ax.set_ylabel(r"$\theta/\theta_{ref}$")
ax.set_xlim(0, 6)
ax.legend(loc="lower right")
ax.set_title("Derivative action buys speed and damping together", color=INK)
save(fig, "pd-step")

# 8. PID vs PD loop Bode (integral lifts low-frequency gain)
dPID = numbers["designs"]["PID"]
fig, a1, a2 = bode_axes()
for name, col in [("PD", ORANGE), ("PID", TEAL)]:
    d = numbers["designs"][name]
    mag, ph = bode_data(controller(d["Kp"], d["Ki"], d["Kd"]) * G)
    a1.plot(W, mag, color=col, lw=2.2, label=LABEL[name])
    a2.plot(W, ph, color=col, lw=2.2)
a1.axhline(0, color=INK, lw=0.8)
a2.axhline(-180, color=INK, lw=0.8)
a1.axvline(1 / dPID["Ti"], color=GREY, lw=0.9, ls=":")
a2.axvline(1 / dPID["Ti"], color=GREY, lw=0.9, ls=":")
a1.text(1 / dPID["Ti"] * 1.08, 45, r"$1/T_i$", color=GREY)
a1.set_ylim(-60, 60)
a2.set_ylim(-275, -85)
a1.legend(loc="lower left")
save(fig, "pid-bode")

# 9. PID step response and elevator demand
fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True)
t = np.linspace(0, 10, 4001)
for name, col in [("PD", ORANGE), ("PID", TEAL)]:
    d = numbers["designs"][name]
    _, Tr, Tu, _ = closed_loops(d["Kp"], d["Ki"], d["Kd"])
    a1.plot(t, ct.step_response(Tr, t).outputs * 10, color=col, lw=2, label=LABEL[name])
    a2.plot(t, np.degrees(ct.step_response(Tu, t).outputs * STEP), color=col, lw=2)
a1.axhline(10, color=INK, lw=0.8)
a1.set_ylabel(r"$\theta$ (deg)")
a2.set_ylabel(r"Elevator $\delta_e$ (deg)")
a2.set_xlabel("Time (s)")
a1.legend(loc="lower right")
a1.set_title("10° attitude step: PID keeps the speed but gains a slower tail", color=INK)
save(fig, "pid-step")

# 10. Derivative kick: D on error vs D on measurement
fig, ax = plt.subplots(figsize=(8, 4.2))
t_m, y_m, u_m = simulate(pd["Kp"], 0, pd["Kd"], STEP, t_end=2.0)
t_e, y_e, u_e = simulate(pd["Kp"], 0, pd["Kd"], STEP, d_on_error=True, t_end=2.0)
ax.plot(t_e, np.degrees(u_e), color=RED, lw=2, label="D on error")
ax.plot(t_m, np.degrees(u_m), color=TEAL, lw=2, label="D on measurement")
ax.axhspan(-20, 20, color=TEAL, alpha=0.08, lw=0)
ax.text(1.35, 24, "elevator travel ±20°", color=GREY)
ax.set_xlabel("Time (s)")
ax.set_ylabel(r"Elevator demand $\delta_e$ (deg)")
ax.set_xlim(0, 2)
ax.legend(loc="upper right")
ax.set_title("Derivative kick on a 10° attitude step (PD design)", color=INK)
save(fig, "derivative-kick")

# 11. Integrator windup
fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True)
for label, col, name in [("linear", GREY, "no limit"),
                         ("saturated", RED, "±20° limit, no anti-windup"),
                         ("anti_windup", TEAL, "±20° limit, conditional integration")]:
    t, y, u = runs[label]
    a1.plot(t, np.degrees(y), color=col, lw=2, label=name, ls="--" if label == "linear" else "-")
    a2.plot(t, np.degrees(u), color=col, lw=2, ls="--" if label == "linear" else "-")
a1.axhline(25, color=INK, lw=0.8)
a2.axhspan(-20, 20, color=TEAL, alpha=0.08, lw=0)
a1.set_ylabel(r"$\theta$ (deg)")
a2.set_ylabel(r"Elevator $\delta_e$ (deg)")
a2.set_xlabel("Time (s)")
a1.set_xlim(0, 12)
a1.legend(loc="lower right")
a1.set_title("25° attitude step with the PID design", color=INK)
save(fig, "windup")

print(json.dumps(numbers, indent=2))
