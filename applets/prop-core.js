// The proportional loop on the rig's elevation axis, as maths with no drawing
// in it, so scripts/test-applets.mjs can check it against the numbers
// models/L01_proportional_limit.py writes into models/L01_numbers.json.
//
// The plant is the measured elevation axis:
//
//   G(s) = K wn^2 / (s^2 + 2 zeta wn s + wn^2)
//
// Close a proportional loop around it and the characteristic polynomial is
//
//   s^2 + 2 zeta wn s + wn^2 (1 + K Kp)
//
// Kp is absent from the coefficient of s. That one fact is the whole applet:
// the constant term rises with gain and the s term does not, so the natural
// frequency is multiplied by sqrt(1 + K Kp) and the damping ratio divided by
// it. Their product, which is the decay rate and the real part of the poles,
// does not move at all.
(function (root) {
  "use strict";

  // Kept in step with docs/laboratory/code/elevation_plant.json. The test
  // compares these against the Python's own copy and fails if they drift.
  var PLANT = { K: 3.4, wn: 1.0, zeta: 0.06 };

  function closedLoop(kp, plant) {
    var p = plant || PLANT;
    var f = Math.sqrt(1 + p.K * kp);
    var zeta = p.zeta / f;
    var wn = p.wn * f;
    var wd = wn * Math.sqrt(1 - zeta * zeta);
    return {
      zeta: zeta,
      wn: wn,
      wd: wd,
      // Real part of the closed-loop poles, and the rate the envelope decays
      // at. zeta * wn = p.zeta * p.wn for every gain, which is the point.
      decay: zeta * wn,
      poleReal: -zeta * wn,
      poleImag: wd,
      // Peak overshoot of a second-order step, as a percentage.
      overshoot: 100 * Math.exp(-Math.PI * zeta / Math.sqrt(1 - zeta * zeta)),
      // Time for the envelope to fall inside a 2% band.
      settling: -Math.log(0.02 * Math.sqrt(1 - zeta * zeta)) / (zeta * wn),
      // What a proportional loop leaves behind: 1/(1 + K Kp) of the demand.
      ssError: 100 / (1 + p.K * kp),
      dcGain: (p.K * kp) / (1 + p.K * kp)
    };
  }

  // Unit-step response, solved rather than simulated: the closed loop is a
  // standard second order and there is nothing to integrate.
  function stepResponse(kp, t, plant) {
    var c = closedLoop(kp, plant);
    var out = new Float64Array(t.length);
    for (var i = 0; i < t.length; i++) {
      var env = Math.exp(-c.decay * t[i]);
      out[i] = c.dcGain * (1 - env * (Math.cos(c.wd * t[i]) +
                                      (c.decay / c.wd) * Math.sin(c.wd * t[i])));
    }
    return out;
  }

  // The characteristic polynomial's coefficients, s^2 + b s + c.
  //
  //   b = 2 zeta wn, which has no Kp in it
  //   c = wn^2 (1 + K Kp), which is the only place Kp appears
  //
  // Returned rather than formatted, so the applet can line the numbers up
  // under the symbols and the test can check them.
  function charEq(kp, plant) {
    var p = plant || PLANT;
    var c = closedLoop(kp, p);
    return {
      a: 1,
      b: 2 * p.zeta * p.wn,          // = 2 * the decay rate, at every gain
      c: p.wn * p.wn * (1 + p.K * kp)
    };
  }

  // The locus the poles trace as the gain runs from zero upwards: a vertical
  // line, which is the thing worth seeing move.
  function poleLocus(kpMax, n, plant) {
    var pts = [];
    for (var i = 0; i <= n; i++) {
      var kp = kpMax * Math.pow(i / n, 2);     // dense where the action is
      var c = closedLoop(kp, plant);
      pts.push({ kp: kp, re: c.poleReal, im: c.poleImag });
    }
    return pts;
  }

  root.PropCore = { PLANT: PLANT, closedLoop: closedLoop, charEq: charEq,
                    stepResponse: stepResponse, poleLocus: poleLocus };
})(typeof globalThis !== "undefined" ? globalThis : this);
