function v = heli_score(m)
%HELI_SCORE  Rank gains that have already passed: fast, then damped, then gentle.
%
%   v = heli_score(m)     m is the metrics struct heli_check_one returns
%
% Lower is better. Only ever applied to gains that passed every check, so this
% is a preference between safe designs and not a safety judgement. It decides
% the order of round 3 and nothing else.
%
% Mirrored by score() in scripts/gains.py. It was a local copy in
% heli_check_gains as well, until round 3 needed it in a third place.

settle  = pick(m, 'settle_s',   1e9);
damping = pick(m, 'damping',    0.7);
peak    = pick(m, 'peak_volts', 0);

v = settle + 2.0 * max(0, 0.7 - damping) * 10 + 0.05 * peak;
end


function v = pick(m, name, fallback)
if isfield(m, name) && isfinite(m.(name))
    v = m.(name);
else
    v = fallback;
end
end

% tracking: status=draft version=0 assisted=true
