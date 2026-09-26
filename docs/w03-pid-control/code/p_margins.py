import control as ct

s = ct.tf("s")
G = 40 / (s * (s + 2) * (s + 10))   # pitch attitude / elevator (rad/rad)

Kp = 1.0
gm, pm, w180, wc = ct.margin(Kp * G)
print(f"GM = {gm:.2f} at {w180:.2f} rad/s, PM = {pm:.1f} deg at {wc:.2f} rad/s")

# tracking: status=draft version=0 assisted=true
