"""Check your Python set-up for CADE30008.

Run it on your own computer with

    python check_setup.py

or press "Run in your browser" on the course website. It should finish by
printing "All checks passed" and drawing one step-response plot.
"""
import sys


def report(label, ok, detail=""):
    print(f"[{'ok' if ok else 'FAIL'}] {label}" + (f": {detail}" if detail else ""))
    return ok


passed = report("Python 3.10 or later", sys.version_info >= (3, 10),
                sys.version.split()[0])

try:
    import numpy
    import scipy
    import matplotlib
    import matplotlib.pyplot as plt
    import control as ct
except ImportError as missing:
    report("packages", False,
           f"{missing.name} is missing. Install with: pip install control matplotlib")
    sys.exit(1)

passed &= report("packages", True,
                 f"numpy {numpy.__version__}, scipy {scipy.__version__}, "
                 f"matplotlib {matplotlib.__version__}, control {ct.__version__}")

# The pitch-attitude loop from week 3, with a proportional gain of 1.
G = ct.tf([40], [1, 12, 20, 0])
gm, pm, wg, wc = ct.margin(G)
passed &= report("loop margins",
                 abs(pm - 43.21) < 0.05 and abs(wc - 1.559) < 0.005 and abs(gm - 6.0) < 0.01,
                 f"phase margin {pm:.2f} deg at {wc:.3f} rad/s, gain margin {gm:.2f}")

# The closed loop follows a step with no steady-state error.
T = ct.feedback(G, 1)
passed &= report("closed loop", abs(ct.dcgain(T) - 1) < 1e-9,
                 f"steady-state gain {ct.dcgain(T):.3f}")

t, y = ct.step_response(T, 10)
plt.plot(t, y)
plt.xlabel("Time (s)")
plt.ylabel("Pitch attitude (per unit step)")
plt.title("Set-up check: closed-loop step response")
plt.grid(True)

print("All checks passed" if passed else "Some checks failed: see the lines marked FAIL")
plt.show()
