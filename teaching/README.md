# Run sheets

One file per session, `l0N.md`, written for the person standing at the front.
Not student-facing, and not built into the site.

A run sheet is derived from three things and holds nothing that belongs in any
of them:

- **[PEDAGOGY.md](../PEDAGOGY.md)** gives the session's shape (P17's slots), its
  case, hook and cliffhanger (P18), and any plan recorded for that session.
- **The handout** (`docs/<lesson>/index.md`) is authoritative for every fact,
  number and equation. A run sheet never restates one; it points at the section.
- **The deck** (`slides/<lesson>/index.md`) gives the slide order.

So a run sheet answers only: what happens, when, with what in front of you, and
what to do when it goes wrong. If you find yourself writing content into one,
it belongs in the handout.

## The template

Every run sheet has these headings, in this order.

```markdown
# Lecture N: <title> — run sheet

**In advance** — everything that has to be true before you walk in.
**In the room** — set-up, in the order you do it, with times.
**Files** — every file needed, with its path, and where students get theirs.
**Hook** — where the last session left off, and how this one grabs them.
**The plan** — a table of P17's slots: minutes, what happens, what's on screen.
**Cliffhanger** — what the session ends on, and what resolves it next week.
**If it goes wrong** — the two or three failures that are actually likely.
**After** — what to collect, post or check before next week.
```

## Rules

- **Times are cumulative as well as per-slot,** so you can tell at a glance
  whether you are behind.
- **Every file is named with a full path,** including student-facing ones and
  where students get them.
- **The contingencies are real ones.** Three likely failures beat a dozen
  hypothetical ones; a run sheet nobody reads under pressure is useless.
- **Update it the same day you teach it.** What actually took 20 minutes rather
  than 15 is the most valuable thing in the file, and it is also P19 evidence:
  a session that reliably overruns is over budget.
- **Hook and cliffhanger are not the same thing,** and the words are not
  interchangeable. A session opens on its hook and closes on its cliffhanger,
  and week *n*'s cliffhanger is week *n* + 1's hook. P18 defines both.
- **Check the chain.** Session *n*'s Cliffhanger and session *n* + 1's Hook
  should describe the same gap. If they don't, one of the two sessions has
  moved and nobody updated the other.
