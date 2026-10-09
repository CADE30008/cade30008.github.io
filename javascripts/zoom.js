// Let a reader open any figure at its own size.
//
// Handouts are read in a 44rem column, and a good deal of what goes in them is
// a plot with axis labels or a block diagram with text in it. At column width
// those are legible; at a glance they are not, and a reader who wants to look
// properly has no way to. The term map and the week chart were linked to
// themselves by hand for exactly that reason, which is the pattern this
// generalises: every content image becomes a link to its own file.
//
// A link rather than a lightbox, deliberately. There is no overlay to dismiss,
// nothing to trap the keyboard, no state to get wrong when instant navigation
// swaps the page under it, and it degrades to an ordinary image when script
// does not run. The browser's own image view already does panning and zooming
// better than anything written here would.
//
// New tab, because the alternative is losing your place in a handout you were
// halfway through. links.js makes the same choice for links that leave the
// site, and says so in the tooltip for the same reason: an unannounced new tab
// is disorienting for anyone using a screen reader or a keyboard.
//
// Images already wrapped by an author are left where they are and given the
// same tooltip and cursor, so the two cases behave alike.

// Rendered figures only. The header logo, the nav icons and anything the theme
// draws are furniture, not content a reader would want to inspect.
const SCOPE = ".md-content .md-typeset";

function dress(a, img) {
  a.classList.add("zoomable");
  a.target = "_blank";
  a.rel = [a.rel, "noopener"].join(" ").trim();
  if (!a.title) {
    const name = decodeURIComponent(new URL(a.href, location.href).pathname.split("/").pop());
    a.title = `Opens ${name} at full size, in a new tab`;
  }
  // The alt text belongs to the image and describes the picture. The link
  // needs its own name or a screen reader reads the alt twice, once as the
  // link and once as its content.
  if (!a.getAttribute("aria-label")) {
    a.setAttribute("aria-label", img.alt ? `Full size: ${img.alt.slice(0, 80)}` : "Open the full-size image");
  }
}

document$.subscribe(() => {
  for (const img of document.querySelectorAll(`${SCOPE} img:not([data-zoom-ready])`)) {
    img.dataset.zoomReady = "";
    const src = img.getAttribute("src");
    if (!src) continue;

    const parent = img.closest("a");
    if (parent) {
      // An author already linked it. Only treat it as a zoom if the link goes
      // to the picture itself; a figure used as a button to somewhere else is
      // not this.
      const href = new URL(parent.href, location.href).pathname;
      if (href === new URL(src, location.href).pathname) dress(parent, img);
      continue;
    }

    const a = document.createElement("a");
    // setAttribute rather than the .href property, which would resolve what it
    // is given. The build currently emits absolute srcs, so today there is
    // nothing to resolve; copying verbatim means a relative one keeps working
    // if that ever changes.
    a.setAttribute("href", src);
    img.replaceWith(a);
    a.appendChild(img);
    dress(a, img);
  }
});
