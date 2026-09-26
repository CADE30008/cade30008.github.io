// Run Python in the browser, for code blocks marked as runnable.
//
// Wrap a Python code block in <div class="py-runnable" markdown> ... </div> to
// give it a "Run in your browser" button. The first press downloads Pyodide,
// the standard Python interpreter compiled to WebAssembly, together with NumPy,
// SciPy, Matplotlib and python-control. Later runs on any page reuse them, and
// the browser caches the download. Printed output appears under the code, and
// any Matplotlib figures are drawn as images.
//
// Nothing is sent to a server: the code runs entirely on the student's device.
const PYODIDE_VERSION = "314.0.7";
const PYODIDE_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

let pyodideReady = null;

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = resolve;
    script.onerror = () => reject(new Error(`could not load ${src}`));
    document.head.appendChild(script);
  });
}

function getPyodide(status) {
  if (!pyodideReady) {
    pyodideReady = (async () => {
      status("Downloading Python. This happens once, and can take a minute on a slow connection…");
      await loadScript(PYODIDE_URL + "pyodide.js");
      const py = await loadPyodide({ indexURL: PYODIDE_URL });
      status("Loading NumPy, SciPy and Matplotlib…");
      await py.loadPackage(["micropip", "numpy", "scipy", "matplotlib"]);
      status("Installing python-control…");
      await py.pyimport("micropip").install("control");
      // Draw figures off-screen, and make plt.show() a no-op: figures are
      // collected after each run and shown as images instead.
      py.runPython(`
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.show = lambda *args, **kwargs: None
`);
      return py;
    })();
    pyodideReady.catch(() => { pyodideReady = null; });   // allow a retry
  }
  return pyodideReady;
}

async function run(block, output, button) {
  const code = block.querySelector("pre code").textContent;
  const log = document.createElement("pre");
  output.replaceChildren(log);
  output.hidden = false;
  const status = (message) => { log.textContent = message; };
  button.disabled = true;

  try {
    const py = await getPyodide(status);
    log.textContent = "";
    const write = (line) => { log.textContent += line + "\n"; };
    py.setStdout({ batched: write });
    py.setStderr({ batched: write });
    py.runPython(`plt.close("all")`);

    try {
      await py.runPythonAsync(code);
    } catch (err) {
      // sys.exit() is a normal way for a script to stop; anything else is an error.
      if (!String(err.message || err).includes("SystemExit")) write(String(err.message || err));
    }

    // Exporting figures can raise library deprecation warnings that say nothing
    // about the student's code, so they are kept out of the output.
    const figures = py.runPython(`
import io, base64, warnings
_figures = []
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for _n in plt.get_fignums():
        _buffer = io.BytesIO()
        plt.figure(_n).savefig(_buffer, format="png", dpi=110, bbox_inches="tight")
        _figures.append(base64.b64encode(_buffer.getvalue()).decode())
plt.close("all")
_figures
`).toJs();
    for (const data of figures) {
      const img = new Image();
      img.src = `data:image/png;base64,${data}`;
      img.alt = "Figure drawn by the code above";
      output.append(img);
    }
  } catch (err) {
    log.textContent += `\nPython could not run in this browser: ${err.message || err}`;
  } finally {
    button.disabled = false;
    button.textContent = "Run again";
  }
}

// Add buttons on first load and after instant navigation swaps page content.
document$.subscribe(() => {
  for (const block of document.querySelectorAll(".py-runnable:not([data-ready])")) {
    block.dataset.ready = "";
    const button = document.createElement("button");
    button.type = "button";
    button.className = "md-button md-button--primary py-run";
    button.textContent = "Run in your browser";
    const output = document.createElement("div");
    output.className = "py-output";
    output.hidden = true;
    output.setAttribute("aria-live", "polite");
    button.addEventListener("click", () => run(block, output, button));
    block.append(button, output);
  }
});

// tracking: status=draft version=0
