# What this folder is

The authoring home for everything that goes into the students' MATLAB Drive
folder.

**This repository is the canonical source.** It is what anyone forking the
unit gets, and it is what the site and the Drive are both built from. The
MATLAB Drive folder is an output: the script only ever copies outward, never
back. A change made directly in the Drive is not in version control and will
be overwritten the next time the script runs.

`scripts/sync_drive.py` assembles the Drive folder from two places:

| Goes to the Drive | Authored in |
|---|---|
| `README.md`, and one per subfolder | **here**, in `drive/` |
| `VERSION.txt` | **here** |
| The `.m`, `.json` and `.mat` files | `docs/`, where the site also serves them |
| The staff test kit | **here**, in `drive/staff/` |

`drive/staff/` goes to `cade30008-staff/`, which is not shared with students.
It is the laboratory test kit: the process READMEs and the two scripts that
only make sense at the rig. It is not versioned with the student material,
because nobody downloads it.

The code is not duplicated here. It has one home, under `docs/`, because the
site and the Drive hand out the same files and two copies would drift. This
folder holds only what the Drive needs and the site does not: the READMEs a
student reads when they open the folder, and the version they check.

`README-repo.md` is this file and is not copied out. `VERSION.txt` is the
current version, written by the script and copied out with the rest.

## Editing

Edit the READMEs here, never in the Drive. A change made in the Drive is
outside version control and will be overwritten the next time the script runs.

```bash
npm run drive -- --check    # has anything drifted?
npm run drive -- --bump     # copy out, and bump the version
```

The version line in each README is rewritten by the script, so leave it alone;
what you maintain by hand is the changelog table in `README.md`.
