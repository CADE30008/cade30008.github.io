// GoatCounter: how many people read which pages, and what sent them here.
//
// The only third-party script on the site. It sets no cookies, stores no IP
// address and builds no profile, so there is nothing to ask consent for. What
// comes back is the page, the day, the screen width, the country, and the
// referrer.
//
// The site uses navigation.instant, which swaps the page body rather than
// loading a new document, so GoatCounter's own on-load counter fires once a
// visit and never again. It still handles the first page, including the wait
// for a background tab to become visible; every page after that is counted
// here, from document$, the same hook mathjax.js uses.
//
// Only the first page of a visit reports a referrer. document.referrer keeps
// naming whatever sent the reader here for as long as the tab lives, so a
// student who arrives from Blackboard and reads six pages would otherwise be
// reported as six arrivals from Blackboard.
//
// count.js ignores localhost and private addresses, so `npm run serve` and
// `npm run preview:live` never reach the live figures. To keep your own
// reading out of them on the published site, load any page there with
// #toggle-goatcounter on the end, once per browser.

// The subdomain is the site code chosen when the site was registered at
// goatcounter.com. If it doesn't match, counts are posted into thin air and
// nothing anywhere says so.
const GOATCOUNTER = "https://cade30008.goatcounter.com/count";

const gc = document.createElement("script");
gc.async = true;
gc.src = "//gc.zgo.at/count.js";
gc.dataset.goatcounter = GOATCOUNTER;
document.head.appendChild(gc);

let counted = false;

document$.subscribe(() => {
  if (!counted) {
    counted = true;      // count.js counts the first page itself
    return;
  }
  if (!window.goatcounter || !window.goatcounter.count) return;
  window.goatcounter.count({
    path: location.pathname + location.search,
    referrer: "",
  });
});

// tracking: status=draft version=0 assisted=true
