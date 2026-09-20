# Annual update

What to do before each cohort starts. It exists because the same small set of
things goes stale every year, and they go stale **quietly** — the site keeps
working while it slowly stops being true.

Work down it in order; each step feeds the next. Budget half a day.

## 1. The calendar, first

Everything else depends on it. In `curriculum/term.yaml`:

- [ ] `year`
- [ ] `week1_date` — the Tuesday of week 1. Every other week's date is derived
      from it by adding seven days, so **check the University calendar for a gap
      in teaching block 1**. If one appears, the derivation is wrong and
      `STATUS.md` will be confidently wrong with it.
- [ ] `day`, `time`, `room` — from the timetable, not from memory.
- [ ] `consolidation_week`, `revision_week`.
- [ ] `coursework.deadline`, and the week of each checkpoint.
- [ ] `laboratory.from_week` / `to_week`.
- [ ] `cohort` — the registered number. It drives the library-copies note in
      week 1 and the laboratory capacity sums.

Then `npm run curriculum`. It fails until the weeks, folders, pages, decks and
nav agree with the new calendar.

## 2. Things with a date or a number in them

- [ ] **Announcement dates** in [announcements.md](announcements.md): re-anchor
      the Sunday slots to this year's weeks, and clear last year's send log.
- [ ] **The Onramp courses** — check the three still exist, still have those
      names, and still take about as long. MathWorks retires and renames them.
- [ ] **Library holdings** in `curriculum/weeks.yaml` under `sources.dorf`:
      print and eBook counts, and whether a new edition has appeared. If it has,
      check the section numbers against the mapping before trusting it.
- [ ] **The MATLAB release** named on the Preparing page, and re-run both device
      checks on it.
- [ ] **Every external link.** They move silently:
      ```bash
      grep -rhoE 'https?://[^)"<> ]+' docs --include='*.md' | sort -u | \
        xargs -P8 -I{} sh -c 'printf "%s %s\n" "$(curl -s -o /dev/null -m 10 -w "%{http_code}" "{}")" "{}"' | grep -v '^2'
      ```

## 3. The rig and the software

- [ ] Re-fit `models/elevation_plant.json` from **this** rig. It is the plant
      every submitted gain is checked against, and the tool refuses to run
      without it for that reason. A previous year's fit is not this year's rig.
- [ ] Re-run `scripts/gains.py check` on last year's submissions, if kept, and
      confirm the envelope still accepts and rejects the right ones.
- [ ] QUARC licences current; rig serviced; e-stop tested.
- [ ] **MATLAB Drive**, following [matlab-drive.md](matlab-drive.md): copy
      `templates/` to a new `20xx-yy/`, fill each `data/`, empty each `submit/`,
      re-share both — which produces **new links** — then replace every link in
      Blackboard and test each one **from a student account, not your own**.
      Leave last year's folder alone: don't delete it, don't re-share it.
      Replacing the links is the step that gets skipped, because the old ones
      still open for you while showing students last year's material.

## 4. Content, from what actually happened

This is the part that gets skipped, and the part that matters. Its input is the
weekly review ([weekly-review.md](weekly-review.md)) — a term's worth of notes
on what went wrong in the room.

- [ ] Read the term's review notes end to end, in one sitting. Patterns are only
      visible in aggregate; individually each one looked like a bad day.
- [ ] For each recurring problem, decide: **change the material, change the
      order, or accept it.** Record which, and why, in `private/reviews/`.
- [ ] Apply P19's budget to anything that grew during the year. Content
      accretes; nothing removes it unless someone is made to.
- [ ] `npm run check -- --all`, and re-accept every week you have actually
      re-read. Never `sync:accept` to clear warnings you haven't read.
- [ ] Update [CONTENT.md](../CONTENT.md) so it still says what really exists.

## 5. Assessment

- [ ] New coursework variants, and confirm last year's answers don't transfer.
- [ ] Rubric against the current University marking criteria.
- [ ] Check what students may reuse: last year's released brief is in `private/`
      and stays there.

## 6. Reset and open

- [ ] Clear the announcement log, the review notes and `private/gains/`.
- [ ] Rebuild everything: `npm run build`, then `npm run live`, then look at it.
- [ ] Rebuild Blackboard from [blackboard.md](blackboard.md) and run its student
      preview checklist.
- [ ] Send the first announcement from [announcements.md](announcements.md).

## Deferred, year to year

Things worth doing that were not possible this time. Re-read this list each
year rather than rediscovering them.

| Item | Why it was deferred | Revisit when |
|---|---|---|
| MathWorks Onramp LTI integration in Blackboard | IT had not enabled it. | IT confirm it's available. |
| Move schedule-linked material off the site and into Blackboard | See "Evergreen", below | Before the next cohort. |
| A repository link in the site header (`repo_url` in `zensical.toml`) | Left off for the first cohort: it is a prominent invitation into a repository that was mostly unwritten weeks, and it makes every page load call `api.github.com` from the student's browser. | Once the weeks are written. Add `repo_url` alone; `edit_uri` puts an "Edit this page" pencil on every page, which leads readers without write access into a fork prompt. |

## Evergreen: what belongs where

The public site should be **usable by someone who is not in this year's
cohort** — a student revisiting it later, a colleague, another institution.
Anything tied to a particular run of the unit works against that, and also has
to be edited every year.

So, as a direction of travel:

- **The site holds what is true about control**: handouts, worked examples,
  solutions, applets, the glossary, the textbook mapping, the AI position.
- **Blackboard holds what is true about this cohort**: dates, rooms, deadlines,
  who is covering which week, announcements, submission links.

It is not there yet. The term map, the week-by-week schedule and the workload
table are still on the site, in week 1's handout and the home page, and they
are generated from `curriculum/term.yaml`. That is deliberate for now — it is
better to have them generated and correct than scattered and wrong — but the
target is that they move to Blackboard and the site keeps only the shape of the
unit, not its calendar. **Do not add new date-linked content to the site in the
meantime.**
