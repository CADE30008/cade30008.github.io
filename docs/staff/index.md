---
title: "Staff area"
description: "Everything for running the unit in one place: run sheets, the curriculum map, and the MATLAB Drive folders."
---

# Staff area

**[cade30008.github.io/staff](https://cade30008.github.io/staff/)**

Not in the site navigation. Publicly reachable by anyone given the link, which
is the same arrangement as the run sheets: none of it is secret, and none of
it is anything students need.

!!! warning "Public, so watch what goes near it"
    Anything linked from here can be opened by anyone with the address. That
    is fine for run sheets and code, and it is **not** fine for assessment
    material, marks, or anything with a student's name on it. Those live in
    `private/` in the repository and are never committed.

## Run sheets

| | |
|---|---|
| [Week 1: the design cycle](w01-run-sheet.md) | Preflight, the setup timeline, the session beat by beat, and what to do when each part fails |
| [Lecture map](lecture-map.html) | The whole term: what each week does, the hooks, the coursework checkpoints, and the draft markers |

## MATLAB Drive

<!-- drive-links:start -->
| Folder | Link |
|---|---|
| Everything students get | [https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students](https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students) |
| `w01-design-cycle` | [https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students/w01-design-cycle](https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students/w01-design-cycle) |
| `lab-quanser` | [https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students/lab-quanser](https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students/lab-quanser) |

Student files are at **version 2026.2**, 2026-09-22.

The staff folder, `cade30008-staff/`, sits beside the student one and is **not shared**. It holds the laboratory test kit. If you want a link to it here, share it from MATLAB Drive and put the URL in `STAFF_SHARE_URL` in `scripts/sync_drive.py`.

**Check these annually.** A new cohort folder means a new share id, and a stale share link is dead rather than wrong, so nothing in the build will notice. See `teaching/annual-update.md`.
<!-- drive-links:end -->

The repository is the source for all of it. Nothing is authored in the Drive:
edit in `docs/` or `drive/`, then

```bash
npm run drive -- --bump
```

which copies everything out and bumps the version students check. See
`teaching/matlab-drive.md`.

## The repository

[github.com/CADE30008/cade30008.github.io](https://github.com/CADE30008/cade30008.github.io)

| Where | What |
|---|---|
| `teaching/` | Run sheets, the Blackboard checklist, the annual update |
| `drive/` | What goes to MATLAB Drive, staff kit included |
| `models/` | The plant, the flight envelope, the figure generators |
| `curriculum/` | `weeks.yaml` and `term.yaml`, which the site is built from |
| `private/` | Assessment, licences, reviews. Never committed |

## Before teaching

The preflight is the first section of the [week 1 run
sheet](w01-run-sheet.md). Eight steps, about an hour, ordered so
the ones that stop a session dead come first.
