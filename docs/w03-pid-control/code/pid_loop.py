import control as ct

s = ct.tf("s")
G = 40 / (s * (s + 2) * (s + 10))   # pitch attitude / elevator (rad/rad)

Kp, Ki, Kd, N = 2.03, 0.678, 0.661, 10
Tf = Kd / (N * Kp)                        # derivative filter time constant

C = Kp + Ki / s + Kd * s / (Tf * s + 1)   # full controller: sets the loop
Cr = Kp + Ki / s                          # what the reference sees
T_ref = ct.minreal(Cr * G / (1 + C * G), verbose=False)   # D on measurement

gm, pm, w180, wc = ct.margin(C * G)
info = ct.step_info(T_ref, SettlingTimeThreshold=0.02)
print(f"PM = {pm:.1f} deg at {wc:.2f} rad/s, GM = {gm:.1f}")
print(f"rise {info['RiseTime']:.2f} s, overshoot {info['Overshoot']:.1f} %, "
      f"settling {info['SettlingTime']:.2f} s")

# tracking: status=draft version=0
