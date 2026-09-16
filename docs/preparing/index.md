---
title: Preparing for Control
description: Check that your device can run the course code, and complete the MathWorks Onramp courses, before Lecture 1.
---

# Preparing for Control

Work through this page before the first lecture. Most of the time goes on the
Onramp courses. Doing it beforehand means lecture time goes on control, not on
installing software.

<div class="lesson-links" markdown>
[Check your device](#check)
[Onramp courses](#onramps)
[Diagnostic quiz](#diagnostic)
</div>

## What you'll use {#software}

Every example in the course comes in both MATLAB and Python, and for most tasks
you can use either. Simulink, and the Quanser helicopter in the laboratory, need
MATLAB.

| Tool | What it's for | Where to get it |
|---|---|---|
| MATLAB, with the Control System Toolbox | The main tool for the course | Bristol students can get it through the University's [MATLAB licence](https://www.mathworks.com/academia/tah-portal/university-of-bristol-30911639.html). Install it, or use [MATLAB Online](https://matlab.mathworks.com/) in a browser. The licence includes the Control System Toolbox, the Aerospace Toolbox and most other toolboxes |
| Simulink | Block-diagram simulation, for activities and the Quanser laboratory | Comes with MATLAB. Select it when you install |
| Python, with the `control` package | A free alternative for everything except Simulink | Install it on your computer, or run it in your browser on this page |

## Which device? {#devices}

Bring a laptop to lectures if you have one. Activities are done in pairs and
threes, so if you don't have one, you'll share with someone who does.

| Device | Python | MATLAB and Simulink | Onramp courses |
|---|---|---|---|
| Windows, macOS or Linux laptop | Install it, or run it in the browser | Install them, or use MATLAB Online | Yes |
| Chromebook | Run it in the browser | MATLAB Online, in a [supported browser](https://www.mathworks.com/support/requirements/browser-requirements.html) | In a supported browser |
| iPad or other tablet | Run it in the browser | Not supported online. [MATLAB Mobile](https://www.mathworks.com/products/matlab-mobile.html) covers the basics, but not Simulink | No |

If you only have a tablet, you can do the Python work on it, but pair up with
someone who has a laptop for MATLAB, Simulink and the Onramp courses.

## Check your device {#check}

Each check runs the same small example: the pitch-attitude loop from Lecture 2.
Wherever you run it, it should report a phase margin of 43.21° at 1.559 rad/s and
a gain margin of 6.00, and draw a step response.

### In your browser, on any device {#check-browser}

Press **Run in your browser**. The first run downloads Python and its packages,
which can take a minute on a slow connection; after that it's quick. Nothing is
sent anywhere: the code runs on your own device.

<div class="py-runnable" markdown>

```python
--8<-- "preparing/code/check_setup.py"
```

</div>

This is the same script as the one for your computer below. If it works here but
not there, the problem is the installation on your computer, not the code.

### Python on your computer {#check-python}

1. Install Python 3.10 or later, from [python.org](https://www.python.org/downloads/)
   or with [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Install the packages:

    ```bash
    pip install control matplotlib
    ```

3. Download [check_setup.py](code/check_setup.py), and run it from the folder
   you saved it in:

    ```bash
    python check_setup.py
    ```

You should see this, though your version numbers will differ, and a window
showing the step response:

```text
[ok] Python 3.10 or later: 3.12.8
[ok] packages: numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.2, control 0.10.2
[ok] loop margins: phase margin 43.21 deg at 1.559 rad/s, gain margin 6.00
[ok] closed loop: steady-state gain 1.000
All checks passed
```

### MATLAB and Simulink {#check-matlab}

This works in MATLAB on your computer and in MATLAB Online. It was tested with
MATLAB R2026a; any recent release should work.

1. Get MATLAB through the University's licence, with the Control System Toolbox
   and Simulink.
2. Download [check_setup.m](code/check_setup.m), open it in MATLAB and press
   **Run**. Or create a new script, paste in the code below, and run that.

```matlab
--8<-- "preparing/code/check_setup.m"
```

You should see this, with your own MATLAB version on the first line:

```text
[ok] MATLAB: 26.1 (R2026a)
[ok] Control System Toolbox
[ok] Simulink
[ok] loop margins: phase margin 43.21 deg at 1.559 rad/s, gain margin 6.00
[ok] closed loop: steady-state gain 1.000
[ok] Simulink simulation: final pitch attitude 1.000
All checks passed
```

You'll also get a step-response plot, and a small Simulink model called
`cade30008_check`. Have a look at the model, which is the same loop drawn as
blocks, then close it without saving.

### If a check fails {#troubleshooting}

| What you see | What to do |
|---|---|
| `[FAIL] packages`, or a `ModuleNotFoundError` | Run `pip install control matplotlib` with the same Python you used to run the script |
| `[FAIL] Control System Toolbox` or `[FAIL] Simulink` | Add the missing product. In MATLAB, go to **Home › Add-Ons › Get Add-Ons**, or reinstall with it selected |
| The browser run stalls, or reports an error | Use an up-to-date browser, and try another network: some block large downloads |
| Anything else | Pair up with someone whose set-up works, and bring the error message to Lecture 1 |

## MathWorks Onramp courses {#onramps}

Three free, self-paced courses that run in your browser and check your work as
you go. Take them in this order. You'll need a laptop or desktop computer, as
MathWorks online courses don't run on tablets or phones.

1. [MATLAB Onramp](https://matlabacademy.mathworks.com/details/matlab-onramp/gettingstarted):
   the MATLAB language and environment.
2. [Simulink Onramp](https://matlabacademy.mathworks.com/details/simulink-onramp/simulink):
   building and simulating models from blocks.
3. [Control Design Onramp with Simulink](https://matlabacademy.mathworks.com/details/control-design-onramp-with-simulink/controls):
   designing a feedback controller in Simulink.

Sign in with the MathWorks account linked to your University email address.

## Diagnostic quiz {#diagnostic}

!!! note "Planned"
    A short quiz on the mathematics and control this course builds on is
    planned, on Blackboard. It won't be marked. It tells you, and us, where to
    focus in the first weeks. Details will follow here.
