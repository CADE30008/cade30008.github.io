# MATLAB Drive

Anything students touch during a session lives in one place, laid out the same
way every week, so that setting up week 7 is the same job as setting up week 1
and neither is improvised on the morning.

## The layout

```
CADE30008/                          top level, in Steve's MATLAB Drive
  2026-27/                          one folder per cohort
    w01-design-cycle/
      data/                         read-only  — given to students
      submit/                       writable   — students put work here
    w03-pid-control/
      data/
      submit/
    ...
  templates/                        not shared; the empty week, to copy
```

Week folder names match `docs/wNN-topic/` exactly. One vocabulary for the site,
the repository and the Drive means a run sheet can say "week 4's `data/`" and
nobody has to work out which folder that is.

**A folder per cohort**, not one folder reused. Rolling over is then a copy of
`templates/` rather than an edit of last year's live folder, last year's
submissions stay where they were without being reachable by this year's
students, and — importantly — **the share links change**, which is why they are
checked annually rather than assumed.

Weeks that need nothing get no folder. Don't create empty ones; a folder that
exists implies something is in it.

## Sharing

| Folder | Shared as | Holds |
|---|---|---|
| `data/` | **View only**, link | Live Scripts, measured data, anything given out. |
| `submit/` | **Can edit**, link | Student submissions. |
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
2. Put this year's files into each `data/`.
3. Empty each `submit/`.
4. Re-share every `data/` and `submit/`, which produces **new links**.
5. Replace every link in Blackboard, and run the checks above on each one.
6. Leave last year's folder alone. Don't delete it and don't re-share it.

Step 5 is the one that gets skipped, because the old links still open — for
*you*. A stale link from last year's folder will show this year's students last
year's material, or silently accept their work into a folder nobody reads.
