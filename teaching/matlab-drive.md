# MATLAB Drive

Anything students touch during a session lives in one place, laid out the same
way every week, so that setting up week 7 is the same job as setting up week 1
and neither is improvised on the morning.

## The layout

```
Teaching/Control 2026/              in Steve's MATLAB Drive
  cade30008-students/               shared view only, one link, the link
    README.md                       version, changelog, how to check it
    VERSION.txt                     the current version, one line
    w01-design-cycle/               the first session's files
      data/                         the measured recording
    lab-quanser/                    the open-access laboratory files
  cade30008-staff/                  not shared; test kit and anything in progress
```

**One link, to `cade30008-students/`.** Students are never given a link into a
subfolder. A deep link goes stale as soon as the layout moves, and anybody who
bookmarks one never sees the rest of the material.

Folder names match `docs/` exactly, so a run sheet can say "week 1's folder"
and that means one thing on the site, in the repository and on the Drive.

**Nothing is submitted into the Drive.** Gains go through the form; the Drive
is read only in both directions as far as students are concerned. That is a
change from 2025/26, when a writable `submit/` folder was used, and it removes
the awkwardness of a shared writable folder being readable by the whole
cohort.

## The repository is the source

Everything in the student folder is authored here and copied out. The READMEs
and the version live in `drive/`; the scripts and data live under `docs/`,
where the site serves the same files. Nothing is authored in the Drive itself.

That matters beyond tidiness: this repository is what somebody forking the
unit gets. A file that exists only in a synced folder on one laptop is not
part of the unit, it is part of that laptop.

## Versioning

The material is new, so it will change during the year, and a student holding
a fortnight-old copy needs to be able to tell.

One version for the whole student folder, `<year>.<n>`, in `VERSION.txt` and
in every README's header. The same number is written onto the site between
`<!-- drive-version:start -->` markers, so the two cannot disagree.

```bash
.venv/bin/python scripts/sync_drive.py --check   # has anything drifted?
.venv/bin/python scripts/sync_drive.py --bump    # copy, and bump the version
```

Use `--bump` whenever the files change after students have been given them.
Without it the copy is silent and a student cannot tell theirs is old.

**Recorded data is forward compatible, and that is a promise worth keeping.**
The loaders accept the layout the rig's own `s_save` writes, which is fixed by
the hardware. A recording made under 2026.1 still fits under 2026.9. If that
ever stops being true it is a fault, not a release.

## Sharing

| Folder | Shared as | Holds |
|---|---|---|
| `cade30008-students/` | **View only**, one link | Everything given out: scripts, models, measured data. |
| `cade30008-staff/` | **Not shared** | The laboratory test kit, and anything not ready. |

The student link, which is what goes on Blackboard and on the site:

```
https://drive.mathworks.com/sharing/93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students
```

It is also in `scripts/sync_drive.py` as `SHARE_URL`, which is what writes it
onto the site. Change it there and re-run the script rather than editing
pages.
| everything else | not shared | Working files, previous cohorts, templates. |

Two things follow from `submit/` being writable, and both matter:

- **It is readable too.** Every student can see every other submission, by
  whatever name it carries. That is deliberate — seeing the spread is half the
  exercise — but it means **students are told before they upload**, and they are
  offered an alias. The words are in each run sheet under "Before anyone
  uploads".
- **Nothing writes back into it.** `scripts/gains.py --out` defaults to the
  working directory and never to the folder it read: putting a report of whose
  gains passed into a folder the cohort can read would publish exactly what the
  alias was protecting.

Share at the level of `data/` and `submit/`, never the week folder or the year
folder. Sharing a parent shares everything below it, including next week's
material before it is ready.

## Links go on Blackboard

The links are cohort-specific and change every year, so they belong in
Blackboard rather than on the public site — see the evergreen note in
[annual-update.md](annual-update.md). Each week's learning module gets:

| Item | Type | Points at |
|---|---|---|
| **Files for this session** | Link | that week's `data/` view-only link. |
| **Submit your work** | Link | that week's `submit/` edit link. |

Same two titles every week, in that order, so students learn where to look
once. [blackboard.md](blackboard.md) is the build sheet.

## Checking, and it has to be from a student account

**Open every link signed out, or in a private window, or from a test student
account — never as yourself.** As the owner, every link works and every folder
is visible, so testing while signed in tells you nothing at all. This is the
single most common way a session fails in the room with everyone watching.

For each link, check the thing you would not want to discover live:

- `data/` opens and the files are **readable but not editable**.
- `submit/` **accepts a file**. Upload one, confirm it lands, delete it.
- Nothing above the shared folder is reachable — no next week, no other cohort,
  no working files.

Do this once when the folders are made, and again in the annual update.

## Each year

In [annual-update.md](annual-update.md), and repeated here because this is the
page someone will be looking at:

1. Copy `templates/` into a new `20xx-yy/` folder.
2. Put this year's files into each `data/`, including a current copy of
   `models/elevation_plant.json` beside `submit_gains.m`. Without it the
   student-side check refuses to run before the identification block; with a
   stale one, students check against a plant nobody uses.
3. Empty each `submit/`.
4. Re-share every `data/` and `submit/`, which produces **new links**.
5. Replace every link in Blackboard, and run the checks above on each one.
6. Leave last year's folder alone. Don't delete it and don't re-share it.

Step 5 is the one that gets skipped, because the old links still open — for
*you*. A stale link from last year's folder will show this year's students last
year's material, or silently accept their work into a folder nobody reads.
