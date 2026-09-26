// Maths for the PID tuner applet: plant model, loop frequency response,
// stability margins and a time-domain simulation with actuator limits.
//
// A classic script with no dependencies, exposed as globalThis.PidCore. It is
// deliberately not an ES module: browsers refuse to load modules from file://
// pages, and the applet must work when a deck is opened from disk, offline.
// scripts/test-applets.mjs loads this same file in Node and checks it against
// the numbers from models/pitch.py.
(() => {
"use strict";

/** Pitch attitude from elevator: 40 / (s (s + 2) (s + 10)). */
const PITCH = { num: [40], den: [1, 12, 20, 0] };

// ---------------------------------------------------------------- complex
const cx = (re, im = 0) => ({ re, im });
const add = (a, b) => cx(a.re + b.re, a.im + b.im);
const mul = (a, b) => cx(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re);
const div = (a, b) => {
  const d = b.re * b.re + b.im * b.im;
  return cx((a.re * b.re + a.im * b.im) / d, (a.im * b.re - a.re * b.im) / d);
};
const polyval = (p, z) => p.reduce((acc, c) => add(mul(acc, z), cx(c)), cx(0));

/** Smallest derivative filter time constant the simulation will use (s). */
const TF_MIN = 0.004;

/** Derivative filter time constant: Tf = Td / N, with Td = Kd / Kp. */
function filterTime(g) {
  if (!g.kd) return 0;
  return Math.max(g.kd / (g.n * Math.max(g.kp, 1e-3)), TF_MIN);
}

/** C(jw) for C(s) = Kp + Ki/s + Kd s / (Tf s + 1). */
function controllerAt(g, w) {
  const jw = cx(0, w);
  let c = cx(g.kp);
  if (g.ki) c = add(c, div(cx(g.ki), jw));
  if (g.kd) {
    const tf = filterTime(g);
    c = add(c, div(mul(cx(g.kd), jw), add(mul(cx(tf), jw), cx(1))));
  }
  return c;
}

/** Log-spaced frequencies. */
function logspace(a, b, n) {
  return Array.from({ length: n }, (_, i) => 10 ** (a + ((b - a) * i) / (n - 1)));
}

/** Magnitude (dB) and unwrapped phase (deg) of L(jw) = C(jw) G(jw). */
function loopResponse(g, plant = PITCH, w = logspace(-2, 3, 800)) {
  const mag = [];
  const phase = [];
  let prev = null;
  let offset = 0;
  for (const wi of w) {
    const z = cx(0, wi);
    const L = mul(controllerAt(g, wi), div(polyval(plant.num, z), polyval(plant.den, z)));
    mag.push(20 * Math.log10(Math.hypot(L.re, L.im)));
    let ph = (Math.atan2(L.im, L.re) * 180) / Math.PI;
    if (prev !== null) {
      while (ph + offset - prev > 180) offset -= 360;
      while (ph + offset - prev < -180) offset += 360;
    } else if (ph > 0) {
      offset = -360;   // integrators start the phase below zero
    }
    prev = ph + offset;
    phase.push(prev);
  }
  return { w, mag, phase };
}

const interpLog = (w, y, i, target) => {
  // log-frequency interpolation of where y crosses `target` between i-1 and i
  const f = (target - y[i - 1]) / (y[i] - y[i - 1]);
  return 10 ** (Math.log10(w[i - 1]) + f * (Math.log10(w[i]) - Math.log10(w[i - 1])));
};
const interpAt = (w, y, i, wx) => {
  const f = (Math.log10(wx) - Math.log10(w[i - 1])) / (Math.log10(w[i]) - Math.log10(w[i - 1]));
  return y[i - 1] + f * (y[i] - y[i - 1]);
};

/**
 * Gain and phase margins from the first 0 dB crossing and the first -180 deg
 * crossing. Adequate for the minimum-phase plants used here.
 */
function margins(resp) {
  const { w, mag, phase } = resp;
  let wc = null, pm = null, w180 = null, gmDb = Infinity;
  for (let i = 1; i < w.length; i++) {
    if (wc === null && mag[i - 1] >= 0 && mag[i] < 0) {
      wc = interpLog(w, mag, i, 0);
      pm = 180 + interpAt(w, phase, i, wc);
    }
    if (w180 === null && phase[i - 1] > -180 && phase[i] <= -180) {
      w180 = interpLog(w, phase, i, -180);
      gmDb = -interpAt(w, mag, i, w180);
    }
  }
  const stable = (pm === null || pm > 0) && gmDb > 0;
  return { wc, pm, w180, gmDb, gm: 10 ** (gmDb / 20), stable };
}

// ------------------------------------------------------------ simulation
function companion(plant) {
  // Controllable canonical form of a strictly proper transfer function.
  const lead = plant.den[0];
  const den = plant.den.map((c) => c / lead);
  const n = den.length - 1;
  const num = Array(n - plant.num.length).fill(0).concat(plant.num.map((c) => c / lead));
  const a = den.slice(1).reverse();      // a0 ... a_{n-1}
  const b = num.slice().reverse();       // b0 ... b_{n-1}
  return { n, a, b };
}

/**
 * Simulate a reference step (and optionally an input disturbance step).
 *
 * opts: { gains: {kp, ki, kd, n}, plant, step, dStep, tDist, uMax,
 *         antiWindup, dOnError, tEnd, dt }
 * Returns { t, y, u, r } arrays; angles in the same units as `step`.
 */
function simulate(opts) {
  const g = opts.gains;
  const { n, a, b } = companion(opts.plant || PITCH);
  const r = opts.step;
  const uMax = opts.uMax ?? Infinity;
  const tEnd = opts.tEnd ?? 10;
  const dt = opts.dt ?? 2e-3;
  const tf = filterTime(g) || 1;
  const steps = Math.round(tEnd / dt);

  const out = (x) => b.reduce((acc, bi, i) => acc + bi * x[i], 0);
  const law = (x, xi, xf) => {
    const y = out(x);
    const e = r - y;
    const sig = opts.dOnError ? e : -y;
    const D = g.kd ? (g.kd * (sig - xf)) / tf : 0;
    const uRaw = g.kp * e + g.ki * xi + D;
    const u = Math.max(-uMax, Math.min(uMax, uRaw));
    return { y, e, sig, u, uRaw };
  };
  const deriv = (x, xi, xf, t) => {
    const c = law(x, xi, xf);
    const d = opts.dStep && t >= (opts.tDist ?? 0) ? opts.dStep : 0;
    const dx = new Array(n);
    for (let i = 0; i < n - 1; i++) dx[i] = x[i + 1];
    dx[n - 1] = c.u + d - a.reduce((acc, ai, i) => acc + ai * x[i], 0);
    const hold = opts.antiWindup && c.u !== c.uRaw && Math.sign(c.e) === Math.sign(c.uRaw);
    return { dx, dxi: hold ? 0 : c.e, dxf: g.kd ? (c.sig - xf) / tf : 0 };
  };

  let x = new Array(n).fill(0), xi = 0, xf = 0;
  const T = [], Y = [], U = [];
  const axpy = (v, k, h) => v.map((vi, i) => vi + h * k[i]);
  for (let k = 0; k <= steps; k++) {
    const t = k * dt;
    const c = law(x, xi, xf);
    T.push(t); Y.push(c.y); U.push(c.u);
    if (!Number.isFinite(c.y) || Math.abs(c.y) > 1e6) break;   // diverged
    if (k === steps) break;
    const k1 = deriv(x, xi, xf, t);
    const k2 = deriv(axpy(x, k1.dx, dt / 2), xi + (dt / 2) * k1.dxi, xf + (dt / 2) * k1.dxf, t + dt / 2);
    const k3 = deriv(axpy(x, k2.dx, dt / 2), xi + (dt / 2) * k2.dxi, xf + (dt / 2) * k2.dxf, t + dt / 2);
    const k4 = deriv(axpy(x, k3.dx, dt), xi + dt * k3.dxi, xf + dt * k3.dxf, t + dt);
    x = x.map((xv, i) => xv + (dt / 6) * (k1.dx[i] + 2 * k2.dx[i] + 2 * k3.dx[i] + k4.dx[i]));
    xi += (dt / 6) * (k1.dxi + 2 * k2.dxi + 2 * k3.dxi + k4.dxi);
    xf += (dt / 6) * (k1.dxf + 2 * k2.dxf + 2 * k3.dxf + k4.dxf);
  }
  return { t: T, y: Y, u: U, r };
}

/** Rise time (10-90%), overshoot (%) and 2% settling time of a step response. */
function stepMetrics(sim, tUntil = Infinity) {
  const { t, y, r } = sim;
  let t10 = null, t90 = null, peak = -Infinity, tsIdx = 0, last = 0;
  for (let i = 0; i < t.length && t[i] <= tUntil; i++) {
    const v = y[i] / r;
    if (t10 === null && v >= 0.1) t10 = t[i];
    if (t90 === null && v >= 0.9) t90 = t[i];
    peak = Math.max(peak, v);
    if (Math.abs(v - 1) > 0.02) tsIdx = i;
    last = i;
  }
  return {
    riseTime: t10 !== null && t90 !== null ? t90 - t10 : null,
    overshoot: Math.max(0, (peak - 1) * 100),
    settlingTime: tsIdx < last ? t[tsIdx + 1] : null,
  };
}

globalThis.PidCore = {
  PITCH, TF_MIN, filterTime, controllerAt, logspace, loopResponse, margins, simulate, stepMetrics,
};
})();

// tracking: status=draft version=0 assisted=true
