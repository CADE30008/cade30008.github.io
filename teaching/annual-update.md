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
- [ ] `laboratory.from_week` / `to_week`. **Reset `to_week` to 6**, whatever
      last year ended up as. The window is short on purpose: closing it before
      the coursework gets hard is what makes people book early. Access will
      very likely be extended towards week 12 once the year is running, and
      that is fine as a concession granted later; it is not the number to
      advertise in week 1, because a twelve-week window removes the reason to
      go in week 2.
- [ ] `cohort` — the registered number. It drives the library-copies note in
      week 1 and the laboratory capacity sums.
- [ ] `schedule` — **empty it.** It holds the departures from the timetable in
      one particular year: which weeks lost their session and which ran twice.
      Carrying last year's over would move weeks that are not moving, and the
      note it generates on the site and in week 1's handout would be a
      confident lie. Fill it again only when a session is actually lost.

Then `npm run curriculum`. It fails until the weeks, folders, pages, decks and
nav agree with the new calendar.

## 2. Things with a date or a number in them

- [ ] **Announcement dates** in [announcements.md](announcements.md): re-anchor
      the Sunday slots to this year's weeks, and clear last year's send log.
- [ ] **Send the opening announcement a week before the first session.** In
      2026/27 it went out the morning before, which left no time to act on the
      device check — the one thing in it that actually wants doing beforehand.
      Schedule it when you set the calendar in step 1, not when term starts.
- [ ] **The Onramp courses** — check the three still exist, still have those
      names, and still take about as long. MathWorks retires and renames them.
- [ ] **Export the Blackboard reading list** afresh into
      `curriculum/reading-list/`, dated, keeping the old exports. The site
      describes that list without reproducing it, so a stale description is the
      failure mode to watch.
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
- [ ] QUARC licences current; rig serviced. **Amplifier switch and mains
      switch located and tested** — there is no separate e-stop, decided
      21 September 2026, and these two are what stops the rig.
- [ ] **MATLAB Drive**, following [matlab-drive.md](matlab-drive.md): make a
      new `Control <year>/` with `cade30008-students/` and
      `cade30008-staff/`, re-share the student folder — which produces a
      **new share id, and so new links for every subfolder** — then put the
      new base link into `SHARE_URL` in `scripts/sync_drive.py` and run
      `npm run drive -- --bump`. That rewrites every link on the site from one
      place. Then test the links **from a student account, not your own**.
      Leave last year's folder alone: don't delete it, don't re-share it.

      Replacing the links is the step that gets skipped, because the old ones
      still work for you as the owner. **A stale share link is a dead link
      rather than a wrong one**, so nothing in the build will notice: the
      site check follows internal links and does not reach out to MathWorks,
      and MATLAB Drive answers 200 to any share id at all, including one made
      up on the spot, so a script could not check them either. Open them.
      **Open them signed out**, because a subfolder link works when you are
      signed in and asks a student to sign in when they are not.
      The index of every link is in
      [matlab-drive.md](matlab-drive.md#the-links), and it is short enough to
      click through in a minute.
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
| A tare button in the rig's Simulink models | The elevation encoder is zeroed wherever the arm happens to be, so nobody knows what angle they identified at. Since the gravity stiffness goes as sin(elevation), the model students fit is a property of that unknown angle. Tare against a known datum and the measurement becomes repeatable. | When the lecture and student-lab Simulink models are redeveloped. See `models/quanser_trim_stiffness.py`. |
| AVDASI 2 pitch-rig data as example systems | Offered in September 2026, too late to rebuild this year's examples around. Other systems used instead. The link must stay one-way: not every AVDASI 2 student takes the avionics strand, so nothing here may assume it. | Planning next year's examples, before week 3's plant is rewritten. Details and verified numbers in `private/reviews/2026-09-21-avdasi2-pitch-rig.md`. |
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
