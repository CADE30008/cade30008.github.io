// Checks the applet maths (docs/applets/pid-core.js) against the numbers
// produced by models/pitch.py, so the interactive version and the handout
// always agree. Run with: node scripts/test-applets.mjs
import { readFileSync } from "node:fs";
import vm from "node:vm";

// pid-core.js is a classic browser script; run it and pick up globalThis.PidCore.
vm.runInThisContext(readFileSync(new URL("../docs/applets/pid-core.js", import.meta.url), "utf8"));
const { loopResponse, margins, simulate, stepMetrics } = globalThis.PidCore;

const nums = JSON.parse(readFileSync(new URL("../models/pitch_numbers.json", import.meta.url)));
const D2R = Math.PI / 180;
const peak = (a) => a.reduce((m, v) => Math.max(m, Math.abs(v)), 0);
let bad = 0;
function check(label, got, want, tol) {
  const ok = Number.isFinite(got) && Math.abs(got - want) <= tol;
  if (!ok) bad++;
  console.log(`${ok ? "ok " : "BAD"} ${label.padEnd(32)} applet ${Number(got).toFixed(3).padStart(9)}  python ${want.toFixed(3).padStart(9)}`);
}

for (const [name, d] of Object.entries(nums.designs)) {
  const g = { kp: d.Kp, ki: d.Ki, kd: d.Kd, n: nums.N };
  const m = margins(loopResponse(g));
  check(`${name} phase margin`, m.pm, d.PM_deg, 0.2);
  check(`${name} crossover`, m.wc, d.wc, 0.01);
  check(`${name} gain margin dB`, m.gmDb, d.GM_dB, 0.1);
  const sim = simulate({ gains: g, step: 10 * D2R, tEnd: 8 });
  const sm = stepMetrics(sim);
  check(`${name} overshoot %`, sm.overshoot, d.overshoot_pct, 0.3);
  check(`${name} rise time`, sm.riseTime, d.rise_time, 0.01);
  check(`${name} settling time`, sm.settlingTime, d.settling_time, 0.05);
  check(`${name} peak elevator deg`, peak(sim.u) / D2R, d.peak_elevator_deg_per_10deg_step, 0.1);
}

const pid = nums.designs.PID;
const gPid = { kp: pid.Kp, ki: pid.Ki, kd: pid.Kd, n: nums.N };
for (const [label, o] of [["linear", {}], ["saturated", { uMax: 20 * D2R }],
                          ["anti_windup", { uMax: 20 * D2R, antiWindup: true }]]) {
  const sm = stepMetrics(simulate({ gains: gPid, step: 25 * D2R, tEnd: 12, ...o }));
  check(`windup ${label} overshoot %`, sm.overshoot, nums.windup[label].overshoot_pct, 0.3);
  check(`windup ${label} settling`, sm.settlingTime, nums.windup[label].settling_time, 0.05);
}

const pd = nums.designs.PD;
const kick = simulate({ gains: { kp: pd.Kp, ki: 0, kd: pd.Kd, n: nums.N }, step: 10 * D2R, dOnError: true, tEnd: 1 });
check("kick peak elevator deg", peak(kick.u) / D2R, nums.kick.peak_elevator_deg_D_on_error, 0.5);

const unstable = margins(loopResponse({ kp: 6.5, ki: 0, kd: 0, n: 10 }));
check("Kp = 6.5 flagged unstable", unstable.stable ? 1 : 0, 0, 0);

console.log(bad ? `\n${bad} checks failed` : "\nall applet checks passed");
process.exit(bad ? 1 : 0);

// tracking: status=draft version=0
