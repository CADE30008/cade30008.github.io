function [ok, why, m] = heli_check_one(kp, ki, kd, plant, env)
%HELI_CHECK_ONE  One set of gains against the flight envelope.
%
%   [ok, why, m] = heli_check_one(kp, ki, kd)
%   [ok, why, m] = heli_check_one(kp, ki, kd, heli_plant, heli_envelope)
%
% The single MATLAB implementation of the envelope. collate_gains and
% heli_check_gains both call it, so a set of gains cannot be accepted by one
% and refused by the other. It is kept in step with scripts/gains.py, and
% models/compare_envelope.m checks that the two agree.
%
% Returns ok, a one-line reason when it is false, and a struct of metrics.
%
% Every check is a refusal, never a clamp. Nothing is quietly moved into
% range: a student whose gains were changed without being told learns the
% wrong lesson, and the room watches a flight that was not theirs.

if nargin < 4 || isempty(plant); plant = heli_plant(); end
if nargin < 5 || isempty(env);   env   = heli_envelope(); end

m = struct();
K = plant.K; wn = plant.wn; z = plant.zeta;

% 1. Finite, positive, and inside the per-gain limits.
named = struct('Kp', kp, 'Ki', ki, 'Kd', kd);
for g = ["Kp" "Ki" "Kd"]
    v = named.(g);
    if ~isfinite(v);        ok = false; why = g + " is not a finite number"; return; end
    if v <= 0;              ok = false; why = g + " must be greater than zero"; return; end
    if v > env.gainMax;     ok = false; why = g + " is above the limit of " + env.gainMax; return; end
end

% 2. Routh, on the polynomial this plant actually has:
%
%   s^3 + (2 zeta wn + K wn^2 Kd) s^2 + (wn^2 + K wn^2 Kp) s + K wn^2 Ki
%
% The condition a student checks on paper is a2*a1 > a0. This is NOT
% K*Kd*Kp > Ki, which is Routh for the double integrator and was used here
% while that was the assumed plant. It is a different inequality, and it
% accepts gains this plant will not fly.
a2 = 2*z*wn + K*wn^2*kd;
a1 = wn^2 + K*wn^2*kp;
a0 = K*wn^2*ki;
m.routh_ratio = (a2*a1)/a0;
if m.routh_ratio <= 1
    ok = false; why = sprintf('unstable: Routh needs a2*a1 > a0, ratio is %.2f', m.routh_ratio); return
elseif m.routh_ratio < env.routhMargin
    ok = false; why = sprintf('too close to unstable: Routh ratio %.2f, below %.2f', ...
        m.routh_ratio, env.routhMargin); return
end

% 3. The loop. Derivative acts on the measurement, not the error, which is
%    what the rig does and what the handout calls rate feedback. The loop
%    transfer is the same either way, so poles and margins are unchanged;
%    only the reference paths differ.
G  = tf(K*wn^2, [1, 2*z*wn, wn^2]);
Tf = kd / (env.derivativeFilterN * kp);          % proper, so the demand is finite
C  = tf([kp*Tf + kd, kp + ki*Tf, ki], [Tf, 1, 0]);
C1 = tf([kp, ki], [1, 0]);                       % what the reference may see
L  = C * G;
T  = feedback(L, 1);

p = pole(T);
m.max_real_pole = max(real(p));
if m.max_real_pole >= 0
    ok = false; why = 'closed loop is unstable'; return
end
osc = p(abs(imag(p)) > 1e-9);
if isempty(osc)
    m.damping = 1;
else
    m.damping = min(-real(osc) ./ abs(osc));
end
if m.damping < env.dampingMin
    ok = false; why = sprintf('too oscillatory: damping %.3f below %.2f', ...
        m.damping, env.dampingMin); return
end

[~, pm] = margin(L);
m.phase_margin = pm;
if ~isfinite(pm) || pm < env.phaseMarginMin
    ok = false; why = sprintf('phase margin %.1f deg below %g', pm, env.phaseMarginMin); return
end

% 4. What the motors are asked for, against the demand as the rig receives
%    it: rate-limited at Quanser's own CMD_RATE_LIMIT, not a step. A step
%    asks the derivative term to differentiate a discontinuity.
t   = linspace(0, env.settleMaxS * 1.5, 4000);
ref = min(env.cmdRateDegS * t, env.stepDeg);
v   = lsim(minreal(C1 / (1 + L), [], false), ref, t);
m.peak_volts = max(abs(v));
if m.peak_volts > env.voltagePeakMax
    ok = false; why = sprintf('demands %.1f V for a %g deg step, above the %.1f V we allow', ...
        m.peak_volts, env.stepDeg, env.voltagePeakMax); return
end

sgn = sign(v(abs(v) > 0.02 * max(m.peak_volts, 1e-9)));
m.reversals = nnz(diff(sgn) ~= 0);
if m.reversals > env.reversalsMax
    ok = false; why = sprintf('motor demand changes sign %d times, above %d', ...
        m.reversals, env.reversalsMax); return
end

% 5. Settling, to 2% of the demand.
y  = lsim(minreal(G * C1 / (1 + L), [], false), ref, t);
out = find(abs(y - env.stepDeg) > 0.02 * env.stepDeg);
if isempty(out) || out(end) + 1 >= numel(t)
    m.settle_s = Inf;
else
    m.settle_s = t(out(end));
end
if m.settle_s > env.settleMaxS
    ok = false; why = sprintf('takes %.1f s to settle, over the %g s limit', ...
        m.settle_s, env.settleMaxS); return
end

ok = true; why = "";
end
