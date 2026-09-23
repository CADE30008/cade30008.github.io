# Weekly review

Ten minutes a week, in term. It exists so that the [annual
update](annual-update.md) has something real to work from: a term's worth of
notes on what actually happened, rather than a memory of the year that is
mostly the last two weeks of it.

The whole thing is two habits.

## 1. Five lines, straight after the lecture

**In the room, or on the walk back — not that evening.** What went wrong is
obvious for about twenty minutes and then rationalises itself into "that went
fine".

Append to this file. Don't tidy it; a rough note kept beats a good note not
written.

```
### Week n, <date>

- Where they got stuck:
- What I had to explain twice:
- What ran long or short:
- What broke (kit, software, room):
- One thing to change:
```

That last line is the point. If nothing comes to mind, write "nothing", which
is itself a finding when it appears three weeks running.

## 2. Sunday, ten minutes

Before writing the week's announcement, because the review usually changes it.

- [ ] Read last week's five lines.
- [ ] **Anything wrong in the material?** Fix it now, while you remember what
      you meant. A typo, a wrong number, a question that was ambiguous in the
      room — these cost minutes now and a re-explanation every year otherwise.
- [ ] **Anything wrong in the *plan*?** Don't fix it now. Add it to the term
      notes below; it is annual-update work, and changing the shape of a unit
      mid-term costs students more than it gains them.
- [ ] Check the next session's run sheet in `teaching/` against reality: kit
      booked, files built, anyone else who has to be there told.
- [ ] Write and schedule the announcement from
      [announcements.md](announcements.md).
- [ ] `npm run check` and `npm run curriculum`, so drift surfaces weekly rather
      than in August.

## What counts as which

The distinction that makes this work:

| Finding | When to act |
|---|---|
| A wrong number, a broken link, an ambiguous question | **Now.** It is wrong for the next person who reads it. |
| A slot that ran ten minutes long | **Now**, in the run sheet. Timings are cheap to change and expensive to misremember. |
| "They didn't have the prerequisite" | **Annual update.** It is a curriculum decision, not a fix. |
| "This should come before that" | **Annual update.** Reordering mid-term breaks the coursework, which is keyed to week numbers. |
| "The room can't do this activity" | **Now**, in the run sheet, and again at annual update if it is really a design problem. |

## Term notes

Things for the annual update. One line each, with the week they came from, so
that next summer's read-through has context.

<!-- Add as they arise. Cleared at the start of each year. -->

---

# Lecture notes

Newest at the bottom. Cleared at the start of each year — git keeps them.

### Week 1, Tuesday 22 September 2026

Steve's notes, taken straight after.

- **What ran long:** the start. Too much talking before the hook, and the
  session's shape went with it. Not a content problem: better preparation is
  the fix, so that the opening is delivered rather than improvised.
- **What worked:** the intro landed, and the full-manual Quanser attempt was
  very well received. That is the part to protect if anything has to give.
- **What ran short:** everything after the flight. The room only got as far as
  watching the 2 V elevation step being captured. No fitting, no tuning, no
  gains flown.
- **What was promised to make up for it:** the data and a Live Script for
  students to work through themselves, results collected before the next
  session, and a short run at the start of the next lecture to pick it up.
- **One thing to change, and it is not the resources.** The materials are
  right; the time went at the front. Next year, keep the session as written
  and hold the opening to its five minutes. Do not build the catch-up slot
  into the plan, because it exists to repair an overrun rather than to be part
  of the design.

Two additions to the Quanser introduction, from how it actually went:

- **Say it is a tandem-rotor helicopter first.** Quanser build the model on the
  **Boeing HC-1B Chinook**. Naming it before the axes turns an odd lab
  contraption into an aircraft with a nose and a tail, which makes pitch and
  travel obvious instead of definitions to learn. A photograph would help;
  see the note below.
- **"Half a quadcopter" belongs in the handout, not on a slide.** It is a good
  second way in for anyone who does not think in helicopters, and it is one
  framing too many for the room.

**Still needed: a Chinook photograph.** Not added, because I have none that is
ours and the site is CC-BY. US military photographs are public domain, so a US
Army or Department of Defense image is the clean source; Quanser's own figure
is not, and neither is a search result.

**The schedule changed after this session.** Duc was down to take week 2; that
was reviewed and reversed. Flight dynamics now has both of week 2's slots, with
Mark delivering two lectures, and control makes the time up in week 3, which
runs on the Tuesday and again on the Thursday. Nothing is dropped and weeks 4
onwards are untouched. It is recorded in `curriculum/term.yaml` under
`schedule`, which is where the term map, week 1's schedule table and STATUS.md
all read it from, and `teaching/annual-update.md` says to empty it next year.
The Thursday slot's room and hour are not confirmed yet, so nothing generated
prints them: the pages say to look on Blackboard, and STATUS.md carries it as a
blocker. The announcement to send is in `teaching/announcements.md`, and it is
deliberately held until both facts can go out together.
