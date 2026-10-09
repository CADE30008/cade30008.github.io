// Which copy of the site this is, in a fluorescent box over the top right of
// the header, so the dev site and the staged build are never taken for each
// other, or for the live one.
//
//   Local dev      npm run serve, and the review page's rendered pane: every
//                  page, unpublished ones included.
//   Local staged   npm run preview:live: the live build, exactly what a push
//                  would publish.
//
// Nothing shows on the public site, because the box needs a local address.
// The staged build says "staged" because scripts/build_live.py rewrites the
// BUILD line below in its own copy; this file always says "dev".
const BUILD = "staged";

(() => {
  const host = location.hostname;
  const local = ["localhost", "127.0.0.1", "::1", "[::1]"].includes(host) || host.endsWith(".localhost");
  if (!local) return;
  const show = () => {
    if (document.getElementById("which-site")) return;
    const box = document.createElement("div");
    box.id = "which-site";
    box.dataset.build = BUILD;
    box.textContent = BUILD === "staged" ? "Local staged · the live build" : "Local dev · every page";
    document.body.append(box);
  };
  show();
  // navigation.instant swaps the page without reloading it; put the box back
  // if a swap ever takes it away.
  if (window.document$) document$.subscribe(show);
})();
