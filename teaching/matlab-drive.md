# MATLAB Drive

Anything students touch during a session lives in one place, laid out the same
way every week, so that setting up week 7 is the same job as setting up week 1
and neither is improvised on the morning.

## The layout

```
Teaching/                           NOT shared
  cade30008-students/               shared on its own
    README.md                       version, changelog, how to check it
    VERSION.txt                     the current version, one line
    w01-design-cycle/               the first session's files
      data/                         the measured recording
    lab-quanser/                    the open-access laboratory files
  cade30008-staff/                  shared on its own
    rig-characterisation/           bench work: fit the rig, fly gains
    student-code-test/              a copy of what students download
```

**Two folders, two shares, and no parent.** They were briefly inside a shared
`cade30008/`, which meant Drive's web interface offered a breadcrumb up from
the student folder and from there into the staff one. Sharing the leaves
rather than the branch removes that: `Teaching/` is not shared, so neither
link offers a way up or across.

**The staff link is public, on purpose.** It is on the staff page so the test
kit can be fetched on a laboratory machine without signing in to MATLAB
Drive. That makes `cade30008-staff/` staff-*facing*, not private: working
files yes, anything with a student's name on it or anything about assessment
no. Those stay in `private/` and are never committed.

Renaming either folder in Drive breaks the paths in `scripts/sync_drive.py`,
which is why the script checks they exist and names the rename as the likely
cause rather than copying nothing and reporting success.

## The links

One base link, and the subfolder links are that plus the folder name, which is
how MATLAB Drive builds them. **All of them die and are replaced when the
folder is re-shared for a new cohort**, so they are checked annually:
[annual-update.md](annual-update.md).

| Links to | Used on |
|---|---|
| `.../cade30008-students` | Anywhere the whole unit's files are meant |
| `.../cade30008-students/w01-design-cycle` | The first session's code page |
| `.../cade30008-students/lab-quanser` | The laboratory overview, its three part pages, its code page |

The base is `SHARE_URL` in `scripts/sync_drive.py`, and the subfolder links
are derived from it. **Change it in that one place and run
`npm run drive -- --bump`**; every page is rewritten between
`<!-- drive-version:start -->` markers. Nothing is typed into a page by hand,
which is the only way a dozen links stay consistent.

Nothing in the build checks these links. The site's own link check follows
internal links and does not reach out to MathWorks, so a dead share link
fails silently and stays failed until somebody clicks it. That is the reason
for the annual check rather than a hope that it would be noticed.

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
| `cade30008-students/` | **View only**, its own link | Everything given out: scripts, models, measured data |
| `cade30008-staff/` | **View only**, its own link | The laboratory test kit |

The student link, which goes on Blackboard and on the student-facing pages:

```
https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0
```

The staff link, which is on the staff page and nowhere else:

```
https://drive.mathworks.com/sharing/a3596484-f0e7-4d6b-bbb8-46d263c3cc4b
```

Both are in `scripts/sync_drive.py`, as `SHARE_URL` and `STAFF_SHARE_URL`,
which is what writes them onto the site. Change it there and re-run the script rather than editing
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
