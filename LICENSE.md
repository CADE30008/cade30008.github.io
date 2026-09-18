# Licence

Copyright © 2026 Dr Steve Bullock, University of Bristol.

This repository holds two kinds of work, under two licences.

| | Licence | What it covers |
|---|---|---|
| **Teaching material** | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Words, figures, decks, example sheets, planning and process documents |
| **Software** | [MIT](https://opensource.org/license/mit) | Scripts, applets, models, build tooling |

Both require attribution. They are split because CC BY is a content licence
with no patent grant and no warranty disclaimer, which makes it an awkward
licence to build software on; and MIT says nothing useful about a lecture
handout.

Where a file is arguably both — a Live Script or a notebook that is half prose
and half code, say — take the licence of the directory it sits in.

## Teaching material: CC BY 4.0

You are free to share and adapt it, including commercially, provided you give
appropriate credit, link to the licence, and say if you made changes.

- lecture handouts, slide decks, example sheets, worked solutions, figures and
  the glossary, under `docs/` and `slides/`, excluding code files;
- planning and process documents: `PEDAGOGY.md`, `ASSESSMENT.md`, `AGENTS.md`,
  `CONTENT.md`, `CURRICULUM.md`, `README.md`, `LICENSE.md`, the run sheets in `teaching/`, and
  the review notes in `reviews/`.

**Attribution:**

> Bullock, S. (2026). *CADE30008 Flight Dynamics & Control: course materials*.
> University of Bristol. CC BY 4.0.

## Software: MIT

```
MIT License

Copyright (c) 2026 Steve Bullock, University of Bristol

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

This covers `models/`, `scripts/`, `docs/applets/`, `docs/javascripts/`,
`docs/stylesheets/course.css`, `docs/**/code/`, and the configuration in
`zensical.toml` and `package.json`.

**Attribution is not optional here either.** MIT requires the copyright notice
above to be kept in all copies or substantial portions, so reusing this code
means carrying that notice — in a `LICENSE` or `THIRD-PARTY-NOTICES` file, in
an About box, or in the source file header. That is the attribution, and it is
a condition of the licence rather than a courtesy.

If you publish work that this code helped produce, cite the teaching material
attribution above as well. That part is a courtesy.

## What neither licence covers

Nothing below is ours to license.

| Excluded | Why | Where |
|---|---|---|
| University of Bristol and Bristol Flight Lab names, logos, wordmarks and visual identity | University brand assets and trade marks. Neither CC BY nor MIT grants trade mark rights | `docs/assets/brand/logo-bristol*.svg`, `edge-*.svg`, and the branding rules in `docs/stylesheets/flightlab.css` |
| Quanser materials — laboratory guides, Simulink models, QUARC software and licence files | Third-party copyright, and the QUARC licences are confidential | `private/quanser/`, which git ignores |
| Assessment material — briefs, marking schemes, per-student parameters, previous years' coursework | Not published, and some of it is third-party | `private/`, which git ignores |
| University of Bristol marking criteria, policies and guidance | University documents, under their own terms | quoted in `ASSESSMENT.md` |
| MathWorks material — MATLAB, Simulink, Onramp courses, toolbox documentation | Third-party, used under the University's licence | referenced throughout |
| Third-party libraries | Their own licences apply | `node_modules/`, `requirements.txt`, and anything loaded from a CDN |
| Quotations, figures and data from published work | Copyright of their authors, used by citation | cited at the point of use |

If you reuse this material, remove the University branding and the Flight Lab
identity, or replace them with your own. The content is yours to use; the
institution's marks are not.

## Third-party notices

The site is built with [Zensical](https://zensical.org) and the slides with
[Marp](https://marp.app), each under its own licence. Python and JavaScript
dependencies are listed in `requirements.txt` and `package.json` and are
licensed by their authors.
