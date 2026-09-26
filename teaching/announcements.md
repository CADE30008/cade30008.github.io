# Blackboard announcements

What to post, and when. **Sunday evening** is the default slot: it lands before
the week starts, while there is still time to act on it, and it doesn't compete
with the lecture itself. A second, shorter nudge on **Friday** is worth it only
in weeks with a checkpoint.

Each announcement below is written to be **copied and pasted**. Edit the parts
in *italics*; everything else should stand.

## Rules for these

- **One ask per announcement.** Two asks means neither gets done.
- **Say what's in it for them**, not what the system requires.
- **Never make an announcement the only place a fact lives.** Announcements
  aren't searchable and aren't there in week 8. Say it, then link to the page
  that holds it.
- **No deadline unless there is one.** This unit has one summative deadline;
  inventing urgency for anything else spends credibility you'll want later.
- Dates go in [annual-update.md](annual-update.md) and are re-set each year.
  Nothing here should assume a particular year.

---

## Sent: the unit is open

**Scheduled 21 September 2026, to go out 09:00**, and corrected in Blackboard
before it sent. This is the text as actually sent, not as drafted. Keep it that
way: next year's starting point should be what worked, not what was proposed.

**Subject:** *Welcome to Flight Dynamics & Control!*

> Welcome to Flight Dynamics & Control!
>
> Initial resources for the unit are now on Blackboard. Two halves: Flight
> Dynamics, delivered by Prof. Richardson and Prof. Lowenberg, on Thursdays, and
> Control, delivered by Dr. Bullock and Dr. Nguyen on Tuesdays.
>
> Two minutes, worth doing before we start: go to Preparing for Control and run
> the device check. It runs a small control example in your browser or in MATLAB
> and tells you whether your laptop is ready. Doing it now means our first
> session goes on control rather than on installing software.
>
> In the same section you'll find links to three MathWorks Onramp courses. Two
> cover skills you likely already have; the third takes only 30 minutes. There's
> also a short diagnostic quiz on the maths we build on. All are recommended
> rather than required. Do them now if you have the time; otherwise pick them up
> when you can. None contribute to your grade, and nothing in the unit assumes
> you've done them.
>
> Bring a laptop to sessions if you have one. If you don't, you'll share —
> activities are done in pairs and threes.
>
> See you tomorrow!
> -Steve

### What the sent version changed, and why it is better

Worth carrying into the weekly pattern rather than treating as one-off edits.

- **It orients them across the whole unit**, not just our half: both halves,
  all four names, and which day each runs. The draft opened inside the control
  half and assumed they knew the rest. First contact is the wrong moment to
  assume that.
- **It points at places, not URLs.** "On Blackboard", "Preparing for Control".
  A named destination survives a moved link, and Blackboard is where they are
  already going.
- **It signs off towards the next thing**, not away from it.

### For next year

- **Send this a week in advance.** It went out the morning before the first
  session, which leaves no time to act on the device check, and the device check
  is the one thing in it with a deadline attached in practice.
- The Onramp sentence was caught and fixed before sending, but only just. Three
  courses and a quiz in one clause is the failure mode to watch: this paragraph
  carries the most items of any in the announcement, so it is the one to read
  aloud before scheduling.

---

## To send: the fit and tune everyone was promised

**Send as soon as the files are checked**, and before the schedule
announcement below, because it has a date in it and the schedule one moves that
date two weeks out.

Week 1 ran out of time: the room watched the 2 V elevation step being captured
and got no further. What was promised in the room was the data, a script to
follow, and that the results would be collected before the next session. This
is that promise, in writing, with a date on it.

Own the overrun in one clause and then move on. The point of the message is the
task, not the apology.

**Subject:** *CADE30008 Control — the fit and tune, to do before we next meet*

> We ran out of time before we got to the fitting, so here is the part you
> didn't get to do. It is the most useful hour you can spend on this unit right
> now, and it feeds the coursework directly.
>
> Everything is on the unit site under Session code: the recording we captured
> in the room, and the scripts that fit a second-order model to it and tune a
> PID against it. Start with `s1_identify` and run it a section at a time,
> then `s2_tune`.
>
> **Submit your gains by *<date>***, through the link `submit_gains` hands you.
> It checks them against the flight envelope first, so you will know before you
> submit whether they can be flown. We fly them at the start of the next
> session: the extremes, the cohort average, and the best few.
>
> Session code: *<link>*
>
> *Steve*

### For next year

The fix is not this announcement; it is not needing it. The opening ran long
and everything after the flight was squeezed. See the week 1 entry in
[weekly-review.md](weekly-review.md).

---

## To send: the schedule change

**Not yet sent.** Hold it until the Thursday slot's room and hour are confirmed
and on Blackboard, then send both facts together. Sending "there is no lecture
next week" on its own invites a fortnight of email asking when the replacement
is.

It breaks the one-ask rule, and it has to. The absence and the replacement are a
single fact, and splitting them across two announcements is what makes people
miss the second one.

**Subject:** *CADE30008 Control — no session next week, two the week after*

> A change to the control half's schedule.
>
> **Next week there is no control session.** Flight Dynamics has both of the
> week's slots, and Prof. Lowenberg will use them.
>
> **The week after, control runs twice**: the usual Tuesday, and again on
> *<day, time, room>*. Nothing is dropped and nothing moves after that, so
> weeks 4 onwards are where they always were.
>
> The week-by-week table on the unit site has been updated: *<link to How this
> unit runs>*.
>
> *Steve*

### For next year

This one is a timetable accident, not a pattern. What is worth keeping is the
shape: name the absence, name the replacement in the same message, and say
explicitly that the rest of the term is unchanged. The third sentence is the one
that stops the email.

---

## The weekly pattern, once teaching starts

Written once, adapted each week. Keep them to four lines.

**Subject:** *CADE30008 Control — week n: <the week's question>*

> This week: *<the week's design question, from `curriculum/weeks.yaml`>*
>
> *<One sentence on what the session will actually do — the activity, not the
> syllabus.>*
>
> Handout and slides: *<link>*
> *<Anything they need to bring or do beforehand, or delete this line.>*
>
> *Steve*

Pull the question and the case from `curriculum/weeks.yaml`; don't re-invent
them, or the announcement and the handout will drift.

## Checkpoint weeks

Weeks 4, 8 and 9. Send on the **Sunday before**, and again on the **Friday** of
that week only if submissions are visibly low.

> Checkpoint *n* is open this week. It's formative — it doesn't contribute to
> your grade — but it *is* the draft of part *<x>* of your final paper, so doing
> it now is the cheapest version of writing it.
>
> You'll get automatic checks on what you submit*<, and peer review — see the
> brief>*. *<Link.>*

## The last one

Week 11, after the deadline passes.

> The coursework is in. Thank you — that was the hard part.
>
> Feedback comes back *<when>*. The site stays up: the handouts, worked
> solutions and applets are all still there if you want them for the exam
> period or beyond.

---

## Log

Keep one line per announcement actually sent, so next year's dates have a real
basis rather than a guess.

| Sent | What | Notes |
|---|---|---|
| | | |

<!-- tracking: status=draft version=0 -->
