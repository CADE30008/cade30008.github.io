# Licence

Copyright © 2026 Dr Steve Bullock, University of Bristol.

Except where stated below, the material in this repository is licensed under the
**[Creative Commons Attribution 4.0 International Licence (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**.

You are free to share and adapt it, including commercially, provided you give
appropriate credit, link to the licence, and say if you made changes.

## What this covers

- **Teaching content** — lecture handouts, slide decks, example sheets, worked
  solutions, figures and the glossary, under `docs/` and `slides/`.
- **Code we wrote** — the design and check scripts in `models/`, the build,
  sync, PDF and test scripts in `scripts/`, and the interactive applets in
  `docs/applets/`.
- **Planning and process documents** — `PEDAGOGY.md`, `ASSESSMENT.md`,
  `AGENTS.md`, `README.md`, the run sheets in `teaching/`, and the review notes
  in `reviews/`.
- **Site styling we wrote** — `docs/stylesheets/course.css`, and the
  configuration in `zensical.toml` and `package.json`.

## Suggested attribution

> Bullock, S. (2026). *CADE30008 Flight Dynamics & Control: course materials*.
> University of Bristol. CC BY 4.0.

## What this does not cover

Nothing below is ours to license, and none of it is covered by the grant above.

| Excluded | Why | Where |
|---|---|---|
| University of Bristol and Bristol Flight Lab names, logos, wordmarks and visual identity | University brand assets and trade marks. Not licensed for reuse, and a CC BY licence cannot grant trade mark rights | `docs/assets/brand/logo-bristol*.svg`, `edge-*.svg`, and the branding rules in `docs/stylesheets/flightlab.css` |
| Quanser materials — laboratory guides, Simulink models, QUARC software and licence files | Third-party copyright, and the QUARC licences are confidential | `private/quanser/`, which git ignores |
| Assessment material — briefs, marking schemes, per-student parameters, previous years' coursework | Not published, and some of it is third-party | `private/`, which git ignores |
| University of Bristol marking criteria, policies and guidance | University documents, reproduced or referenced under their own terms | quoted in `ASSESSMENT.md` |
| MathWorks material — MATLAB, Simulink, Onramp courses, toolbox documentation | Third-party, used under the University's licence | referenced throughout |
| Third-party libraries | Their own licences apply | `node_modules/`, `requirements.txt`, and anything loaded from a CDN |
| Quotations, figures and data from published work | Copyright of their authors, used here by citation | cited at the point of use |

If you reuse this material, remove the University branding and the Flight Lab
identity, or replace them with your own. The content is yours to use; the
institution's marks are not.

## A note on the code

CC BY is a content licence, not a software licence: it has no patent grant and
no warranty disclaimer, which is why most projects use a licence such as MIT or
Apache 2.0 for code. It is used here for everything so that there is one licence
to reason about, which matters more for a teaching repository than the finer
points do.

If you want to reuse the scripts or applets in software, and CC BY is awkward
for your purpose, ask — a permissive software licence for those files
specifically is likely to be agreed.

## Third-party notices

The site is built with [Zensical](https://zensical.org) and the slides with
[Marp](https://marp.app), each under its own licence. Python and JavaScript
dependencies are listed in `requirements.txt` and `package.json` and are
licensed by their authors.
