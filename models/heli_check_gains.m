function result = heli_check_gains(folder, opts)
%HELI_CHECK_GAINS  Check submitted PID gains, and choose what to fly.
%
%   heli_check_gains(submitDir)                 check every submission
%   heli_check_gains(submitDir, Round = 1)      check, then say what to fly
%   r = heli_check_gains(submitDir, K = 0.0912) override the fitted plant
%
% This is the thing standing between a room full of arithmetic and a machine
% flying in front of it. Point it at the MATLAB Drive folder that syncs to this
% machine. It reads every .json and .csv in there, checks each set of gains
% against the envelope below, and prints a report.
%
% Two rules, both deliberate:
%
%   Refuse, never clamp.  Gains outside the envelope are rejected and their
%   owner told which limit they missed. Nothing is quietly adjusted into range:
%   a student whose gains were changed without being told learns the wrong
%   lesson, and the room watches a flight that was not theirs.
%
%   Refuse to invent a plant, but run on a provisional one.  With no model at
%   all it stops. With a provisional K it runs and says so in the banner, every
%   time, so nobody mistakes the report for a measured one. Those are different
%   situations: a provisional K still catches the gains that are obviously
%   unsafe, and refusing outright would stop a session rather than degrade it.
%
% Nothing is ever written back into the folder it read. That folder is shared
% with the cohort, so a file listing whose gains passed would publish exactly
% what the alias was protecting. Use the returned struct, or save it yourself
% somewhere else.
%
% The three rounds week 1 runs:
%
%   Round 1   a spread, not the best: the most aggressive, the most sluggish
%             and the most integral accepted submissions. Cause and effect
%             before any good answer.
%   Round 2   the cohort's average, checked like any other submission. It is
%             often worse than most of its parts, and it is not guaranteed
%             safe just because its ingredients were.
%   Round 3   the best few, by settling time then damping then gentleness.

arguments
    folder (1,:) char
    opts.Round (1,1) double {mustBeMember(opts.Round, [0 1 2 3])} = 0
    opts.K (1,1) double = NaN
end

env   = envelope();
plant = plantGain(opts.K);
K     = plant.K;

fprintf('Elevation model: K = %.4g rad/(V s^2), %s', K, plant.source);
if ~isempty(plant.measured); fprintf(', measured %s', plant.measured); end
fprintf('\n');
fprintf(['Envelope: Routh margin %.2f, damping >= %.2f, gain -%.1fx/+%.1fx, ' ...
         'PM >= %.0f deg,\n          peak <= %.1f V, settle <= %.0f s\n\n'], ...
    env.routhMargin, env.dampingMin, env.gainDownMin, env.gainUpMin, ...
    env.phaseMarginMin, env.voltagePeakMax, env.settleMaxS);

[subs, unreadable] = readSubmissions(folder);
if isempty(subs)
    fprintf(2, 'No submissions found in %s\n', folder);
    result = struct('accepted', [], 'rejected', []);
    return
end

for i = 1:numel(subs)
    subs(i) = evaluateOne(subs(i), K, env);
end

ok  = subs(arrayfun(@(s) isempty(s.reasons), subs));
bad = subs(arrayfun(@(s) ~isempty(s.reasons), subs));
[~, order] = sort(arrayfun(@(s) score(s), ok));
ok = ok(order);

fprintf('%d submission(s): %d accepted, %d rejected\n\n', numel(subs), numel(ok), numel(bad));
for i = 1:numel(ok)
    fprintf('  OK   %-22s Kp=%-7.4g Ki=%-7.4g Kd=%-7.4g  settle %4.1f s, zeta %.2f, peak %.1f V\n', ...
        ok(i).who, ok(i).kp, ok(i).ki, ok(i).kd, ...
        ok(i).metrics.settleS, ok(i).metrics.damping, ok(i).metrics.peakVolts);
end
if ~isempty(ok) && ~isempty(bad); fprintf('\n'); end
for i = 1:numel(bad)
    fprintf(2, '  NO   %-22s Kp=%-7.4g Ki=%-7.4g Kd=%-7.4g\n', ...
        bad(i).who, bad(i).kp, bad(i).ki, bad(i).kd);
    for r = 1:numel(bad(i).reasons)
        fprintf(2, '         %s\n', bad(i).reasons(r));
    end
end
for i = 1:numel(unreadable)
    fprintf(2, '  ??   %s\n', unreadable(i));
end

if opts.Round > 0
    fprintf('\n');
    flyRound(ok, opts.Round, K, env);
end

result = struct('accepted', ok, 'rejected', bad, 'unreadable', {unreadable}, 'K', K);
end


% ---------------------------------------------------------------- envelope

function env = envelope()
%ENVELOPE  What we are willing to fly with 190 people in the room.
%
% Mirrors models/quanser_elevation.py exactly. If one changes, change both:
% two tools disagreeing about what is safe is worse than either being wrong.
V_MAX = 24.0;                 % V, peak the amplifier can deliver
V_OP  = 8.0;                  % V, provisional operating point
env = struct( ...
    'gainMax',        50, ...
    'routhMargin',    1.15, ...   % K*Kd*Kp must beat Ki by this
    'dampingMin',     0.15, ...
    'gainDownMin',    1.5, ...    % may lose a third of the loop gain
    'gainUpMin',      2.0, ...    % may double it
    'phaseMarginMin', 20, ...     % deg
    'voltagePeakMax', 0.7 * (V_MAX - V_OP), ...
    'reversalsMax',   6, ...
    'settleMaxS',     12, ...
    'stepDeg',        7.5, ...    % the guide's standard elevation step
    'filterN',        10);        % derivative filter, so the demand is finite
end


function plant = plantGain(override)
%PLANTGAIN  The elevation model, and where it came from.
%
% Matches models/quanser_elevation.py exactly, which is the point: two tools
% disagreeing about which plant to filter against is worse than either being
% wrong on its own.
%
% It refuses when there is **nothing**, and runs-but-declares when the value is
% provisional. Those are different situations. A provisional K still rejects
% the gains that are obviously unsafe, and the banner says on every run what it
% was checked against, so nobody mistakes the report for a measured one. A hard
% refusal here would stop the session rather than degrade it.
%
% In order of preference: an explicit K, this session's fit, then the file.
if ~isnan(override)
    plant = struct('K', override, 'source', 'passed in explicitly', 'measured', '');
    return
end
if evalin('base', 'exist(''K_fitted'', ''var'')')
    plant = struct('K', evalin('base', 'K_fitted'), ...
        'source', 'fitted in this session (K_fitted)', 'measured', datestr(now, 'yyyy-mm-dd'));
    return
end

here = fileparts(mfilename('fullpath'));
path = fullfile(here, 'elevation_plant.json');
if ~isfile(path)
    error('heli_check_gains:noPlant', ...
        ['No fitted elevation model at\n    %s\nRecord a step response from ' ...
         'the rig, fit K, and write it there as\n  {"K": <rad/(V s^2)>, ' ...
         '"source": "...", "measured": "YYYY-MM-DD"}\nThere is deliberately no ' ...
         'default: gains must never be checked against a guessed plant.'], path);
end
d = jsondecode(fileread(path));
for key = ["K" "source" "measured"]
    if ~isfield(d, key)
        error('heli_check_gains:noPlant', 'elevation_plant.json has no ''%s''', key);
    end
end
if ~(d.K > 0)
    error('heli_check_gains:noPlant', ...
        'elevation_plant.json: K must be positive, got %g', d.K);
end
plant = struct('K', double(d.K), 'source', char(d.source), 'measured', char(d.measured));
end


% ------------------------------------------------------------------ input

function [subs, unreadable] = readSubmissions(folder)
%READSUBMISSIONS  Every .json and .csv in the folder, one struct each.
if ~isfolder(folder)
    error('heli_check_gains:noFolder', 'No such folder:\n    %s', folder);
end
subs = struct('who', {}, 'kp', {}, 'ki', {}, 'kd', {}, ...
              'source', {}, 'reasons', {}, 'metrics', {});
unreadable = strings(0);

files = [dir(fullfile(folder, '*.json')); dir(fullfile(folder, '*.csv'))];
for f = files'
    path = fullfile(f.folder, f.name);
    try
        rows = readRows(path);
    catch e
        unreadable(end+1) = string(f.name) + ": unreadable (" + e.message + ")"; %#ok<AGROW>
        continue
    end
    for r = 1:numel(rows)
        row = rows{r};
        [kp, ki, kd, okRow] = pullGains(row);
        if ~okRow
            unreadable(end+1) = string(f.name) + ": needs kp, ki and kd as numbers"; %#ok<AGROW>
            continue
        end
        subs(end+1) = struct( ...
            'who', pullName(row, f.name), 'kp', kp, 'ki', ki, 'kd', kd, ...
            'source', f.name, 'reasons', strings(0), 'metrics', struct()); %#ok<AGROW>
    end
end
end


function rows = readRows(path)
[~, ~, ext] = fileparts(path);
if strcmpi(ext, '.json')
    d = jsondecode(fileread(path));
    if isstruct(d) && numel(d) > 1
        rows = num2cell(d(:))';
    elseif iscell(d)
        rows = d(:)';
    else
        rows = {d};
    end
else
    t = readtable(path, TextType = 'string');
    rows = arrayfun(@(i) table2struct(t(i, :)), 1:height(t), UniformOutput = false);
end
end


function [kp, ki, kd, ok] = pullGains(row)
%PULLGAINS  kp/ki/kd, whatever case they were written in.
kp = NaN; ki = NaN; kd = NaN; ok = false;
if ~isstruct(row); return; end
f = fieldnames(row);
low = lower(f);
get = @(want) row.(f{find(strcmp(low, want), 1)});
if all(ismember({'kp', 'ki', 'kd'}, low))
    try
        kp = double(get('kp')); ki = double(get('ki')); kd = double(get('kd'));
        ok = isscalar(kp) && isscalar(ki) && isscalar(kd);
    catch
        ok = false;
    end
end
end


function who = pullName(row, fallback)
who = '';
if isstruct(row)
    f = fieldnames(row); low = lower(f);
    for want = {'name', 'alias'}
        i = find(strcmp(low, want{1}), 1);
        if ~isempty(i) && (ischar(row.(f{i})) || isstring(row.(f{i})))
            who = strtrim(char(row.(f{i})));
            if ~isempty(who); return; end
        end
    end
end
[~, who] = fileparts(fallback);
end


% ------------------------------------------------------------- evaluation

function s = evaluateOne(s, K, env)
%EVALUATEONE  Fill in s.reasons and s.metrics. Every check is a refusal.
s.metrics = struct('routhRatio', NaN, 'damping', NaN, 'gainDown', NaN, ...
    'gainUp', NaN, 'phaseMargin', NaN, 'peakVolts', NaN, 'reversals', NaN, ...
    'settleS', NaN);

% 1. Finite, strictly positive, and inside the per-gain ceiling. On a double
%    integrator a non-positive gain is not a gentle controller, it is an
%    unstable one.
names = {'Kp', 'Ki', 'Kd'}; vals = [s.kp, s.ki, s.kd];
for i = 1:3
    if ~isfinite(vals(i))
        s.reasons(end+1) = names{i} + " is not a finite number";
    elseif vals(i) <= 0
        s.reasons(end+1) = sprintf('%s must be greater than 0, got %g', names{i}, vals(i));
    elseif vals(i) > env.gainMax
        s.reasons(end+1) = sprintf('%s above the %g limit, got %g', names{i}, env.gainMax, vals(i));
    end
end
if ~isempty(s.reasons); return; end

% 2. The condition students can check by hand, with margin for a rig that is
%    not exactly the fitted model.
ratio = K * s.kd * s.kp / s.ki;
s.metrics.routhRatio = ratio;
if ratio <= 1
    s.reasons(end+1) = sprintf('unstable: needs K*Kd*Kp > Ki, but the ratio is %.2f', ratio);
    return
elseif ratio < env.routhMargin
    s.reasons(end+1) = sprintf(['too close to unstable: K*Kd*Kp beats Ki by only ' ...
        '%.2f, and we fly nothing below %.2f'], ratio, env.routhMargin);
end

% 3. Closed loop. The derivative is filtered, or the demand on the motors is
%    an impulse and cannot be computed at all.
s_ = tf('s');
Tf = s.kd / (env.filterN * s.kp);
C  = s.kp + s.ki / s_ + s.kd * s_ / (1 + Tf * s_);
G  = K / s_^2;
L  = C * G;
T  = feedback(L, 1);

p = pole(T);
if max(real(p)) >= 0
    s.reasons(end+1) = "closed loop is unstable: a pole is on or right of the imaginary axis";
    return
end
osc = p(abs(imag(p)) > 1e-9);
if ~isempty(osc)
    zeta = min(-real(osc) ./ abs(osc));
    s.metrics.damping = zeta;
    if zeta < env.dampingMin
        s.reasons(end+1) = sprintf('too oscillatory: damping %.3f below %.2f', ...
            zeta, env.dampingMin);
    end
end

% How far the loop gain may move in BOTH directions. Not the Bode gain margin:
% this loop is conditionally stable, so that number is below 1 for every good
% design and testing it against a floor rejects everything.
[down, up] = gainRange(L);
s.metrics.gainDown = down; s.metrics.gainUp = up;
if down < env.gainDownMin
    s.reasons(end+1) = sprintf(['only tolerates the loop gain dropping by %.2fx ' ...
        '(needs %.1fx); this loop goes unstable when gain falls'], down, env.gainDownMin);
end
if up < env.gainUpMin
    s.reasons(end+1) = sprintf('only tolerates the loop gain rising by %.2fx (needs %.1fx)', ...
        up, env.gainUpMin);
end

[~, pm] = margin(L);
s.metrics.phaseMargin = pm;
if ~isfinite(pm) || pm < env.phaseMarginMin
    s.reasons(end+1) = sprintf('phase margin %.1f deg below %g', pm, env.phaseMarginMin);
end

% 4. What the motors are actually asked to do. A design can be perfectly
%    stable on paper and still slam the amplifier into its rails.
step = deg2rad(env.stepDeg);
t = linspace(0, env.settleMaxS * 1.5, 4000);
v = step * step_(feedback(C, G), t);
peak = max(abs(v));
s.metrics.peakVolts = peak;
if peak > env.voltagePeakMax
    s.reasons(end+1) = sprintf('demands %.1f V for a %g deg step, above the %.1f V we allow', ...
        peak, env.stepDeg, env.voltagePeakMax);
end

sgn = sign(v(abs(v) > 0.02 * max(peak, 1e-9)));
reversals = sum(diff(sgn) ~= 0);
s.metrics.reversals = reversals;
if reversals > env.reversalsMax
    s.reasons(end+1) = sprintf(['motor demand changes sign %d times; the rig''s ' ...
        'guide warns against this above %d'], reversals, env.reversalsMax);
end

% 5. Settling, to 2%. Room time is finite and so is everyone's patience.
y = step * step_(T, t);
outside = find(abs(y - step) > 0.02 * step);
if isempty(outside) || outside(end) >= numel(t)
    settle = Inf;
else
    settle = t(outside(end));
end
s.metrics.settleS = settle;
if settle > env.settleMaxS
    s.reasons(end+1) = sprintf('takes %.1f s to settle, over the %g s limit', ...
        settle, env.settleMaxS);
end
end


function y = step_(sys, t)
%STEP_  Unit step response on a given time vector, as a plain column.
y = step(sys, t);
y = y(:);
end


function [down, up] = gainRange(L, lo, hi, n)
%GAINRANGE  How far the loop gain can be scaled, down and up, and stay stable.
%
% Swept rather than read off a Bode crossing, because this loop is
% conditionally stable and the crossing answers a different question.
arguments
    L
    lo (1,1) double = 1e-3
    hi (1,1) double = 1e3
    n  (1,1) double = 400
end
isStable = @(a) max(real(pole(feedback(a * L, 1)))) < 0;
if ~isStable(1); down = 1; up = 1; return; end
alphas = logspace(log10(lo), log10(hi), n);
i = find(alphas >= 1, 1);

down = Inf;
for a = flip(alphas(1:i-1))
    if ~isStable(a); down = 1 / a; break; end
end
up = Inf;
for a = alphas(i:end)
    if ~isStable(a); up = a; break; end
end
end


function v = score(s)
%SCORE  Rank accepted gains: fast, then well damped, then gentle.
%
% Only ever applied to gains that already passed, so this is a preference
% between safe designs and not a safety judgement.
settle  = valueOr(s.metrics.settleS, 1e9);
damping = valueOr(s.metrics.damping, 0.7);
peak    = valueOr(s.metrics.peakVolts, 0);
v = settle + 2.0 * max(0, 0.7 - damping) * 10 + 0.05 * peak;
end


function v = valueOr(x, fallback)
if isnan(x); v = fallback; else; v = x; end
end


% --------------------------------------------------------------- the room

function flyRound(ok, round, K, env)
%FLYROUND  What to fly, and in what order.
if isempty(ok)
    fprintf(2, 'Nothing accepted, so there is nothing to fly. Say so, and why.\n');
    return
end

switch round
    case 1
        % A spread, not the best. Cause and effect before any good answer.
        [~, fast]  = min(arrayfun(@(s) s.metrics.settleS, ok));
        [~, slow]  = max(arrayfun(@(s) s.metrics.settleS, ok));
        [~, integ] = max(arrayfun(@(s) s.ki, ok));
        wanted = [fast, slow, integ];
        labels = {'most aggressive', 'most sluggish', 'most integral'};
        % One submission can win two of these. Fly it once, but carry both
        % labels, or the caption on screen says the wrong thing about it.
        fprintf('Round 1 - the extremes, chosen to misbehave:\n');
        for idx = unique(wanted, 'stable')
            label = strjoin(labels(wanted == idx), ' and ');
            show(ok(idx), label);
        end

    case 2
        % The average of safe gains is not guaranteed safe. That is the point.
        avg = struct('who', sprintf('the cohort''s average of %d', numel(ok)), ...
            'kp', mean([ok.kp]), 'ki', mean([ok.ki]), 'kd', mean([ok.kd]), ...
            'source', '(computed)', 'reasons', strings(0), 'metrics', struct());
        avg = evaluateOne(avg, K, env);
        fprintf('Round 2 - the average of every accepted submission:\n');
        if isempty(avg.reasons)
            show(avg, 'the average');
        else
            fprintf(2, '  ** the average FAILS: %s\n', avg.reasons(1));
            fprintf('  Say this out loud. The average of safe designs is not safe by\n');
            fprintf('  construction, and that is worth more than a clean flight.\n');
        end

    case 3
        fprintf('Round 3 - the best few:\n');
        for j = 1:min(3, numel(ok))
            show(ok(j), sprintf('#%d', j));
        end
end
end


function show(s, label)
fprintf('  %-16s %-22s Kp=%-7.4g Ki=%-7.4g Kd=%-7.4g', label, s.who, s.kp, s.ki, s.kd);
if isfield(s.metrics, 'settleS') && ~isnan(s.metrics.settleS)
    fprintf('  settle %.1f s, zeta %.2f', s.metrics.settleS, s.metrics.damping);
end
fprintf('\n');
end
