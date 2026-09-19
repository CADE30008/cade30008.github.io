import control as ct
import numpy as np

s = ct.tf("s")
G = 40 / (s * (s + 2) * (s + 10))        # pitch attitude / elevator (rad/rad)
Kp0, Ki0, Kd0, N = 2.03, 0.678, 0.661, 10
t = np.linspace(0, 10, 5001)


def evaluate(k):
    """Scale all three gains by k; return PM, crossover, peak elevator, overshoot."""
    Kp, Ki, Kd = k * Kp0, k * Ki0, k * Kd0
    Tf = Kd / (N * Kp)
    C = Kp + Ki / s + Kd * s / (Tf * s + 1)
    Cr = Kp + Ki / s                     # derivative on measurement
    T_ref = ct.minreal(Cr * G / (1 + C * G), verbose=False)
    T_u = ct.minreal(Cr / (1 + C * G), verbose=False)
    gm, pm, w180, wc = ct.margin(C * G)
    u_peak = 10 * np.max(np.abs(ct.step_response(T_u, t).outputs))   # deg, 10 deg step
    overshoot = ct.step_info(T_ref)["Overshoot"]        # relative to the final value, 1
    return pm, wc, u_peak, overshoot


# Part (a): the lecture design
pm, wc, u_peak, os_pct = evaluate(1.0)
print(f"k = 1.00: PM {pm:.1f} deg, wc {wc:.2f} rad/s, peak elevator {u_peak:.1f} deg")

# Part (b): largest k with PM >= 50 deg and peak elevator <= 15 deg
best = None
for k in np.arange(0.30, 1.50, 0.01):
    pm, wc, u_peak, os_pct = evaluate(k)
    if pm >= 50 and u_peak <= 15:
        best = (k, pm, wc, u_peak, os_pct)
k, pm, wc, u_peak, os_pct = best
print(f"best k = {k:.2f}: PM {pm:.1f} deg, wc {wc:.2f} rad/s, "
      f"peak elevator {u_peak:.1f} deg, overshoot {os_pct:.1f} %")
