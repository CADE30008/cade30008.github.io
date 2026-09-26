// Say where a link goes, before the reader clicks it.
//
// Four kinds, and three of them are worked out from the address alone, so
// there is nothing for an author to remember and nothing to forget:
//
//   a page on this site           no marker — this is the ordinary case
//   a file on this site           a download glyph, because a click saves something
//   another site, for reference   a small outward arrow
//   another site, go there now    the same arrow, in brand red, and underlined
//
// Both of the kinds that leave the site also open in a new tab, so that a
// reader who follows a reference does not lose their place in a handout they
// were halfway through. The tooltip says so: opening a tab unannounced is
// disorienting for anyone using a screen reader or a keyboard.
//
// Only the last carries an author's judgement, so only the last is written by
// hand: put { .go } after the link, which attr_list turns into class="go".
//
//     Read the [Cube overview](https://ardupilot.org/...){ .go } before step 2.
//     The [connector naming](https://www.mattmillman.com/...) page explains why.
//
// Rule of thumb: .go means "stop reading this page, go there, come back". If
// the reader could skip it and lose nothing, leave it plain.
//
// The marker is drawn by CSS from the data-link attribute set here
// (stylesheets/course.css). Doing it in script rather than in a CSS selector
// on [href^="http"] buys two things: an absolute link to our own site is
// correctly treated as internal, and the tooltip can name the host, which is
// what tells a cautious reader whether to trust it.
const FILE = /\.(m|mlx|slx|mdl|py|ipynb|pdf|zip|csv|mat|txt)$/i;

function classify(a) {
  const href = a.getAttribute("href");
  if (!href || href.startsWith("#")) return null;         // same page
  let url;
  try {
    url = new URL(a.href);
  } catch {
    return null;                                          // mailto:, tel:, anything exotic
  }
  if (url.protocol !== "http:" && url.protocol !== "https:") return null;
  if (url.origin !== window.location.origin) return a.classList.contains("go") ? "go" : "away";
  if (a.classList.contains("go")) {
    console.warn(`links.js: { .go } is for links that leave the site, but ${href} stays on it`);
  }
  return FILE.test(url.pathname) ? "file" : null;
}

function describe(kind, url) {
  const host = url.host.replace(/^www\./, "");
  if (kind === "go") return `${host} — opens in a new tab; go there as part of this activity, then come back`;
  if (kind === "away") return `${host} — opens in a new tab; for reference, you don't have to follow it now`;
  return `Downloads ${decodeURIComponent(url.pathname.split("/").pop())}`;
}

// On first load, and after instant navigation swaps the page content. Scoped to
// .md-content because the footer is .md-typeset too, and its licence and
// attribution links are furniture, not things the reader is choosing between.
document$.subscribe(() => {
  for (const a of document.querySelectorAll(".md-content .md-typeset a[href]:not([data-link-ready])")) {
    a.dataset.linkReady = "";
    const kind = classify(a);
    if (!kind) continue;
    a.dataset.link = kind;
    if (kind === "away" || kind === "go") {
      a.target = "_blank";
      // noopener stops the new page reaching back through window.opener;
      // noreferrer keeps our reader's page out of the other site's logs.
      a.rel = [a.rel, "noopener", "noreferrer"]
        .join(" ").trim().split(/\s+/).filter((v, i, all) => all.indexOf(v) === i).join(" ");
    }
    if (!a.title) a.title = describe(kind, new URL(a.href));
  }
});

// tracking: status=draft version=0 assisted=true
