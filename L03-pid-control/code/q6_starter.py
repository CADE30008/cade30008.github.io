import control as ct
import numpy as np

s = ct.tf("s")
G = 40 / (s * (s + 2) * (s + 10))        # pitch attitude / elevator (rad/rad)
Kp, Ki, Kd, N = 2.03, 0.678, 0.661, 10   # the lecture's PID design
Tf = Kd / (N * Kp)

C = Kp + Ki / s + Kd * s / (Tf * s + 1)  # full controller: sets the loop
Cr = Kp + Ki / s                         # the reference sees P and I only
T_ref = ct.minreal(Cr * G / (1 + C * G), verbose=False)   # reference to attitude
T_u = ct.minreal(Cr / (1 + C * G), verbose=False)         # reference to elevator

gm, pm, w180, wc = ct.margin(C * G)
print(f"PM = {pm:.1f} deg at {wc:.2f} rad/s")

t = np.linspace(0, 10, 5001)
u = ct.step_response(T_u, t).outputs * 10   # elevator (deg) for a 10 deg step
print(f"peak elevator = {np.max(np.abs(u)):.1f} deg")

# (b) Scale Kp, Ki and Kd by the same factor k and search for the largest k
#     meeting the requirements. Your code here.
