---
title: Recommended reading
description: Dorf and Bishop's Modern Control Systems — a recommended text for further reading, what the library has, and which sections go with which part of the unit.
---

# Recommended reading

**You don't have to buy a book for this unit.** Each week's handout is the
authoritative version of what you need, and it stands on its own.

One textbook is worth knowing about, though:

> Dorf, R. C. and Bishop, R. H. *Modern Control Systems*. Pearson.

It's the closest in spirit to how this unit teaches — it frames everything
around the control design cycle — and the library has plenty of copies. Use it
**for additional study and consolidation**: a second explanation when the
handout's doesn't land, worked examples beyond the example sheets, and depth
if you want it. Nothing in the unit assumes you've read it.

<!-- reading:start -->
### What the library has

Dorf, R. C. and Bishop, R. H. Modern Control Systems. Pearson. Earlier editions than the 12th are not mapped here.

| Edition | Year | Print copies | eBook copies |
|---|---|---|---|
| 14th | 2022 | 2 | 4 |
| 13th | 2017 | 9 | 10 |
| 12th | 2011 | 9 | — |

Search the library for "Dorf Modern Control", then open **View All** to see other editions and formats. Some eBooks are listed under more than one provider.

- Reading an eBook online locks that copy while you have it open.
- Downloading the whole book locks a copy for 24 hours.
- Downloading a PDF chapter locks nothing, but is capped at 56 pages.

### Which sections go with which week

**Section numbers are the same in the 12th, 13th and 14th editions**, so any of them works. Only the page numbers differ.

| Week | What it covers | Sections in Dorf and Bishop |
|---|---|---|
| [1](w01-design-cycle/index.md) | The design cycle, end to end | **1.4-1.5** Engineering design, and control system design<br>**4.1-4.2** Feedback control system characteristics; error signal analysis |
| [2](w02-requirements-and-models/index.md) | Requirements and models you can trust | **2.3** Linear approximations of physical systems<br>**2.5-2.6** The transfer function of linear systems; block diagram models<br>**5.2-5.3** Test input signals; performance of second-order systems |
| [3](w03-pid-control/index.md) | PID, properly | **7.6** PID controllers<br>**9.9** PID controllers in the frequency domain<br>**5.6** The steady-state error of feedback control systems |
| [4](w04-stability-margins/index.md) | Stability and margins | **8.2, 8.4** Frequency response plots; performance specifications in the frequency domain<br>**9.3-9.4** The Nyquist criterion; relative stability and the Nyquist criterion<br>**9.7** The stability of control systems with time delays |
| [7](w07-robustness/index.md) | Robustness and trade-offs | **4.3-4.4** Sensitivity to parameter variations; disturbance signals<br>**9.6** System bandwidth<br>**12.2-12.4** Robust control systems and system sensitivity; analysis of robustness; systems with uncertain parameters |
| [8](w08-loop-shaping/index.md) | Loop shaping | **10.2-10.4** Approaches to system design; cascade compensators; phase-lead design using the Bode plot<br>**10.6, 10.8** System design using integration compensators; phase-lag design using the Bode plot |
| [9](w09-flight-control-architecture/index.md) | Flight control architecture | *No chapter covers this; a flight-control text is needed* |
| [10](w10-state-space/index.md) | State space and state feedback | **3.2-3.3** The state variables of a dynamic system; the state differential equation<br>**11.2-11.3** Controllability and observability; full-state feedback control design<br>**11.7** Optimal control systems |
| [11](w11-beyond-this-course/index.md) | What comes next | **11.4** Observer design<br>**12.5-12.6** The design of robust control systems; robust PID-controlled systems<br>**13.1-13.3** Digital control systems: applications, sampled-data systems |
<!-- reading:end -->

## The full list is on Blackboard

This page names one book and explains what it is for. **The unit's complete
reading list lives on Blackboard**, maintained through the library, and it has
a good deal more on it: alternative textbooks, the flight-dynamics half's
reading, and the video series below. Editions and availability change during
the year there and not here, so treat it as the current version.

Two of the video series on it are worth calling out, because for a lot of
people they work better than any book:

- **[Brian Douglas, *Control System Lectures*](http://readinglists.bris.ac.uk/items/702c23d8-e618-4dc8-8b96-0d80dfec866b.html).**
  Short, unhurried videos that build intuition before algebra. If a Bode plot
  or a root locus has never quite made sense as a picture, start here. He also
  makes the MATLAB Tech Talks, which cover much of this unit.
- **[Steve Brunton, *Control Bootcamp*](http://readinglists.bris.ac.uk/items/78aee3f5-6869-4803-bedb-8f96f0ca226e.html).**
  A full course, pitched a little higher, and unusually good on state space and
  on why the frequency domain and the time domain are two views of one thing.

Both are free, both are on the Blackboard list, and both are recommended
rather than required, like everything else here.

## A free second opinion

If Dorf and Bishop doesn't suit you, a different author's explanation of the
same idea is often exactly what's needed, and one good one costs nothing:

> Åström, K. J. and Murray, R. M. (2021). *Feedback Systems: An Introduction for
> Scientists and Engineers*, 2nd edition. Princeton University Press.
> [The authors' page at Caltech](http://www.cds.caltech.edu/~murray/amwiki/){ .go },
> and the book itself as
> [one PDF](https://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-public_24Jul2020.pdf)
> (33 MB).

The whole book is on that site as a PDF, chapter by chapter or in one file, put
there by the authors. It is worth reading for two things in particular:

- **Sensitivity, robustness and the limits of what feedback can do.** This is
  the book's strongest material, and it goes further than Dorf.
- **A different route through the subject.** It reaches state space early and
  the frequency domain late, the opposite way round from this unit. That makes
  it a genuine second opinion rather than a paraphrase: if an idea hasn't landed
  one way round, try the other.

It is pitched at scientists as well as engineers, so it is more mathematical and
less aircraft-shaped than Dorf. Treat it as somewhere to go when you want depth,
not as a parallel text to read alongside the handouts.

!!! info "It's free, but it isn't open"
    The publisher has allowed the authors to keep the book on the web:
    *"Copyright in this book is held by Princeton University Press, who have
    kindly agreed to allow us to keep the book available on the web."* That is
    permission to host, not a Creative Commons licence, and it is not the same
    arrangement as [this site's](about.md#licence). Download it from the
    authors' own page rather than from anywhere else; don't re-post the PDF,
    and cite it properly if you use it in your coursework.
