---
title: Preparing for Control
description: Check that your device can run the course code, and work through the MathWorks Onramp courses and the diagnostic quiz — recommended before you start, and useful at any point in the unit.
status: draft
version: 0
assisted: true
---

# Preparing for Control

One thing here takes a few minutes and is worth doing early. The rest is
recommended up front and useful at any point in the unit.

!!! abstract "Start here"
    1. **[Check your device](#check)** runs the course code, in your browser or
       on your computer. A few minutes, and it means lecture time goes on
       control rather than on installing software.
    2. **Bring a laptop** to lectures if you have one. If you don't, you'll
       share — activities are done in pairs and threes.

!!! tip "Recommended, and available whenever you want them"
    The **[Onramp courses](#onramps)** and the **[diagnostic quiz](#diagnostic)**
    (about 20 minutes) are the best preparation for this unit. Of the three
    Onramps, the 30-minute **Control Design** one is the one worth your time —
    the other two are a refresher if you have used MATLAB and Simulink before,
    and a good starting point if you haven't.

    **They are not a gate.** Each Onramp is most useful just before the part of
    the unit that leans on it, and the diagnostic is as useful once you have
    found a gap yourself as it is at the outset. Nothing in the unit assumes you
    have done either, so reach for them when they help.

    Blackboard lists them too, with a circle beside each to tick off as you go.

!!! info "Links tell you what a click does"
    Across this site, a link carries a small marker saying where it goes.
    Hovering over one names the site it leads to. Here is each kind, shown as
    itself:

    - [The glossary](../glossary.md) — no marker: another page here, and you're
      not leaving the site.
    - [check_setup.py](code/check_setup.py) — a file downloads.
    - [MATLAB Mobile](https://www.mathworks.com/products/matlab-mobile.html) —
      another website, for reference. Follow it if you want to; nothing depends
      on it.
    - [MATLAB Onramp](https://matlabacademy.mathworks.com/details/matlab-onramp/gettingstarted){ .go }
      — another website, and going there is part of the task. Do it, then come
      back.

## What you'll use {#software}

Every example in the course comes in both MATLAB and Python, and for most tasks
you can use either. Simulink, and the Quanser helicopter in the laboratory, need
MATLAB.

| Tool | What it's for | Where to get it |
|---|---|---|
| MATLAB, with the Control System Toolbox | The main tool for the course. | Bristol students can get it through the University's [MATLAB licence](https://www.mathworks.com/academia/tah-portal/university-of-bristol-30911639.html){ .go }. Install it, or use [MATLAB Online](https://matlab.mathworks.com/) in a browser. The licence includes the Control System Toolbox, the Aerospace Toolbox and most other toolboxes. |
| Simulink | Block-diagram simulation, for activities and the Quanser laboratory. | Comes with MATLAB. Select it when you install. |
| Python, with the `control` package | A free alternative for everything except Simulink. | Install it on your computer, or run it in your browser on this page. |

## Which device? {#devices}

Bring a laptop to lectures if you have one. Activities are done in pairs and
threes, so if you don't have one, you'll share with someone who does.

| Device | MATLAB and Simulink | Python | Onramp courses |
|---|---|---|---|
| Windows, macOS or Linux laptop | Install them, or use MATLAB Online. | Install it, or run it in the browser. | Yes |
| Chromebook | MATLAB Online, in a [supported browser](https://www.mathworks.com/support/requirements/browser-requirements.html). | Run it in the browser. | In a supported browser. |
| iPad or other tablet | Not supported online. [MATLAB Mobile](https://www.mathworks.com/products/matlab-mobile.html) covers the basics, but not Simulink. | Run it in the browser. | No |

If you only have a tablet, you can do the Python work on it, but pair up with
someone who has a laptop for MATLAB, Simulink and the Onramp courses.

## Check your device {#check}

Each check runs the same small example, the pitch-attitude loop from week 3, in
MATLAB or in Python. Wherever you run it, it should report a phase margin of 43.21° at 1.559 rad/s and
a gain margin of 6.00, and draw a step response.

### MATLAB and Simulink {#check-matlab}

This works in MATLAB on your computer and in MATLAB Online. It was tested with
MATLAB R2026a; any recent release should work.

1. Get MATLAB through the University's licence, with the Control System Toolbox
   and Simulink.
2. Download [check_setup.m](code/check_setup.m), open it in MATLAB and press
   **Run**. Or create a new script, paste in the code below, and run that.

<div class="code-scroll" markdown>

```matlab
--8<-- "preparing/code/check_setup.m"
```

</div>

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

### Python in your browser, on any device {#check-browser}

Press **Run in your browser**. The first run downloads Python and its packages,
which can take a minute on a slow connection; after that it's quick. Nothing is
sent anywhere: the code runs on your own device.

<div class="py-runnable code-scroll" markdown>

```python
--8<-- "preparing/code/check_setup.py"
```

</div>

This is the same script as the one for your computer, below. If it works here but
not there, the problem is the installation on your computer, not the code.

### Python on your computer {#check-python}

1. Install Python 3.10 or later, from [python.org](https://www.python.org/downloads/){ .go }
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

### If a check fails {#troubleshooting}

| Where | What you see | What to do |
|---|---|---|
| MATLAB | `[FAIL] Control System Toolbox` or `[FAIL] Simulink` | Add the missing product. In MATLAB, go to **Home › Add-Ons › Get Add-Ons**, or reinstall with it selected. |
| MATLAB | `Unrecognized function or variable 'tf'` | The Control System Toolbox isn't installed, or isn't on the path. Add it as above. |
| MATLAB | It won't start, or the licence is refused. | Sign in with the MathWorks account linked to your University email address, through the University's [MATLAB licence](https://www.mathworks.com/academia/tah-portal/university-of-bristol-30911639.html). |
| Python, on your computer | `[FAIL] packages`, or a `ModuleNotFoundError` | Run `pip install control matplotlib` with the same Python you used to run the script. |
| Python, on your computer | `python: command not found` | Python isn't installed, or isn't on your path. Try `python3`, or install it again. |
| Python, in the browser | The run stalls, or reports an error. | Use an up-to-date browser, and try another network: some block large downloads. It downloads several megabytes the first time. |
| Any | Anything else | Pair up with someone whose set-up works so you're not held up, then get it fixed properly, below. |

### Getting help with your device {#help}

A laptop that won't run MATLAB or Python is an IT problem, not a control one,
and the people who fix those are better at it than I am:

- **[IT Services](https://www.bristol.ac.uk/it-services/)** — for installation,
  licences, accounts and network problems.
- **The Student Laptop Clinic**, run by IT Services, for hands-on help with your
  own machine. Times and places are on the IT Services pages.

Take the exact error message with you. If you can't get it working before the
first lecture, come anyway: you'll work in a pair, and no session depends on
your own machine.

## MathWorks Onramp courses {#onramps}

Three free, self-paced courses that run in your browser and check your work as
you go. Take them in this order. You'll need a laptop or desktop computer, as
MathWorks online courses don't run on tablets or phones.

**Many students are likely to have used MATLAB and Simulink before, including
for control**, so these three are not equally useful to everyone.

| Course | Time | Worth it? |
|---|---|---|
| **Control Design Onramp with Simulink** | 30 min | **Yes — this is the one.** It covers designing a feedback controller, which is what this unit builds on. |
| MATLAB Onramp | 2 h | If you're new to MATLAB, or want a refresher on good practices. |
| Simulink Onramp | 2 h | The same, and worth it before you meet the laboratory rig if blocks are unfamiliar. |

They stop and resume as often as you like, and progress is saved.

**Already done one, in a previous year or another unit?** Upload that
certificate — an older version of the course counts. And if you have done none
of them, come to the session anyway: you will be able to follow it, and you will
work in a pair for the parts that need software.

1. [MATLAB Onramp](https://matlabacademy.mathworks.com/details/matlab-onramp/gettingstarted){ .go }:
   the MATLAB language and environment.
2. [Simulink Onramp](https://matlabacademy.mathworks.com/details/simulink-onramp/simulink){ .go }:
   building and simulating models from blocks.
3. [Control Design Onramp with Simulink](https://matlabacademy.mathworks.com/details/control-design-onramp-with-simulink/controls){ .go }:
   designing a feedback controller in Simulink.

Sign in with the MathWorks account linked to your University email address.

**If you finish one, upload the certificate.** MATLAB Academy gives you a
certificate of completion; download it as a PDF and put it in the **Onramp
certificates** assignment on Blackboard. There is no deadline, and it doesn't
contribute to your grade — it tells me how the cohort
is placed, so I can pitch the software side of each session accordingly. Partial
is fine and useful: upload one, or two, as you go.

## Diagnostic quiz {#diagnostic}

A short quiz on the mathematics and control this course builds on — Laplace
transforms, transfer functions, poles, step responses, Bode plots and basic
feedback — mostly from the year 2 unit Dynamics and Control of Linear Systems.
It takes about 20 minutes.

**It's formative: it doesn't contribute to your unit grade.** What it does is
tell you where you're solid and where to brush up, with automatic feedback on
every question, and tell us what to spend more time on in the first weeks.
Everyone gets the same questions. Do it without looking things up — a flattering
score helps nobody — though you're welcome to sit with someone else and talk it
through.

You'll find it on Blackboard. It opens in Numbas, and marks and gives feedback
on each answer as you go.

**There's no deadline, and it stays open all term.** Sitting it at the start
tells you what to brush up before you begin. Sitting it later, when something
hasn't landed and you want to know whether the gap is in this unit or in last
year's, is just as good a use of it — and the feedback on each question is
written to be read either way.
