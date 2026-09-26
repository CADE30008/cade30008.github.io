// Show that a capped code block scrolls.
//
// Wrapping a code block in <div class="code-scroll" markdown> caps its height
// (course.css), which keeps a long script from pushing the page away. On its
// own that is a trap: macOS and iOS hide scrollbars until something scrolls, so
// a capped block looks like a short one and the reader never sees the rest.
//
// For each capped block that really does overflow, this marks the code as a
// labelled region the keyboard can reach and scroll, and adds a hint and a fade
// at the foot. Both disappear once the reader reaches the end, and come back if
// they scroll up. A block short enough to fit is left alone.
const NEAR_END = 4;                       // px; rounding on zoomed displays
const LANGUAGES = { matlab: "MATLAB", python: "Python", text: "Output", bash: "Shell" };

function language(box) {
  const name = [...box.classList].find((c) => c.startsWith("language-"))?.slice(9);
  if (!name) return "Code";
  return LANGUAGES[name] ?? name[0].toUpperCase() + name.slice(1);
}

function setUp(code) {
  const box = code.closest(".highlight");
  if (!box || code.scrollHeight <= code.clientHeight + NEAR_END) return;

  box.classList.add("code-scroll--scrollable");
  code.tabIndex = 0;                      // so it can be scrolled from the keyboard
  code.setAttribute("role", "region");
  code.setAttribute("aria-label", `${language(box)} listing, scrollable`);

  const hint = document.createElement("span");
  hint.className = "code-scroll__hint";
  hint.setAttribute("aria-hidden", "true");   // the label already says it scrolls
  hint.textContent = "Scroll for more";
  box.append(hint);

  const update = () => {
    const atEnd = code.scrollTop + code.clientHeight >= code.scrollHeight - NEAR_END;
    box.classList.toggle("code-scroll--end", atEnd);
  };
  code.addEventListener("scroll", update, { passive: true });
  update();
}

// On first load, and after instant navigation swaps the page content.
document$.subscribe(() => {
  for (const code of document.querySelectorAll(".code-scroll .highlight pre > code:not([data-scroll-ready])")) {
    code.dataset.scrollReady = "";
    setUp(code);
  }
});

// tracking: status=draft version=0 assisted=true
