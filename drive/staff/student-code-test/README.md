<!-- version: 2026.17 (2026-09-22) -->

# Testing what students are handed

This is a copy of the two student folders, exactly as they come off the
MATLAB Drive link. Not the repository version: the point is to test the thing
students actually download.

Most of it is automated, because bench time should not be spent watching
scripts finish.

---

## 1. Run everything, unattended

```matlab
run_all_student_code
```

About 30 seconds. Start it while the rig settles between recordings.

It runs both bundles in the order a student meets them, and prints one line
per step:

```
w01: s1_identify (fit the model)             ok         19.7
w01: my_model.mat was written                ok          0.1
w01: s2_tune (three ways to tune)            ok          9.0
w01: submit_gains accepts good gains         ok          0.3
w01: submit_gains refuses bad gains          ok          0.1
lab: lab1_fit (fit your recordings)          ok          0.3
lab: lab2_3dof (three axes, three loops)     ok          1.5
lab: lab3_statespace (LQR)                   ok          0.8
```

Anything in red is something a student will hit.

**It does not submit anything.** `submit_gains` builds the link and checks it,
and does not open a browser under `-batch` or when called with
`'Open', false`.

**SEND ME:** anything printed in red.

---

## 2. The two it cannot check, by hand

Four minutes, and they are the two pieces a student actually touches.

### tune_sliders

```matlab
cd w01-design-cycle
load my_model.mat
tune_sliders(K, wn, zeta)
```

- Does the window open?
- Do all three sliders move, and does the plot follow?
- Does the verdict line change between INSIDE and OUTSIDE as you drag?
- Does the panel name two models, your fit for the plot and the rig's for the
  verdict?

That last one matters: the response is simulated against your fit, but the
verdict is taken against the model fitted from the rig, because that is what
`submit_gains` uses. If a student's slider said "accepted" and submission
refused them, they would rightly be annoyed.

### submit_gains, all the way through

```matlab
submit_gains(0.71, 0.59, 0.91, 'Preflight')
```

- Does a browser open on the form?
- Are all four boxes already filled: `Preflight`, `0.71`, `0.59`, `0.91`?
- Submit it, then export the responses and read them back:

```matlab
cd ../../rig-characterisation
collate_gains('~/Downloads/<the export>.xlsx')
```

- One row, `Preflight`, verdict `fly`.
- **Delete that response afterwards**, so it is not in the room.

**SEND ME:** whether both worked, and anything that looked wrong.

---

## 3. If you changed the plant

If §3 of the rig work gave numbers much different from the stored fit, this
copy is now testing the wrong model. Refresh it:

```bash
.venv/bin/python scripts/sync_student_code.py
npm run drive -- --bump
```

then re-copy the two folders in here from the Drive and run §1 again.

---

## What this folder is not

It is a copy, and copies go stale. Do not edit anything in here expecting it
to reach students: the repository is the source, and `npm run drive` is what
publishes. If something here needs fixing, fix it in the repository.
