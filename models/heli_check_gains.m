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
    opts.K = []
end

env   = envelope();
plant = plantGain(opts.K);
K     = plant.K;   % deg/V, for the banner only

fprintf('Elevation model: K = %.4g deg/V, wn = %.4g rad/s, zeta = %.4g\n', ...
    plant.K, plant.wn, plant.zeta);
fprintf('  %s\n', plant.source);
if isfield(plant, 'measured') && ~isempty(plant.measured)
    fprintf('  measured %s\n', plant.measured);
end
fprintf(['Envelope: Routh margin %.2f, damping >= %.2f, PM >= %.0f deg,\n' ...
         '          peak <= %.1f V for a %g deg demand at %g deg/s, settle <= %.0f s\n\n'], ...
    env.routhMargin, env.dampingMin, env.phaseMarginMin, ...
    env.voltagePeakMax, env.stepDeg, env.cmdRateDegS, env.settleMaxS);

[subs, unreadable] = readSubmissions(folder);
if isempty(subs)
    fprintf(2, 'No submissions found in %s\n', folder);
    result = struct('accepted', [], 'rejected', []);
    return
end

for i = 1:numel(subs)
    subs(i) = evaluateOne(subs(i), plant, env);
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
    flyRound(ok, opts.Round, plant, env);
end

result = struct('accepted', ok, 'rejected', bad, 'unreadable', {unreadable}, 'K', K);
end


% ---------------------------------------------------------------- envelope

function env = envelope()
%ENVELOPE  What we are willing to fly with 190 people in the room.
%
% Delegates to heli_envelope, which is the single definition and is mirrored
% by Envelope in models/quanser_elevation.py. This used to be a second copy,
% and a second copy is how the two ended up describing different plants.
env = heli_envelope();
end


function plant = plantGain(override)
%PLANTGAIN  The fitted elevation model, or one passed in.
%
%   heli_check_gains(folder)                 elevation_plant.json
%   heli_check_gains(folder, 'K', struct(...))  these numbers
%
% Delegates to heli_plant. The name is kept because callers use it; the model
% it returns is second order now, with K, wn and zeta, not a lone gain.
if isstruct(override)
    plant = heli_plant(override);
elseif isnumeric(override) && isscalar(override) && ~isnan(override)
    error('heli_check_gains:scalarK', ...
        ['A bare K is the old double-integrator model. Pass a struct with K,\n' ...
         'wn and zeta, or leave it out to read elevation_plant.json.']);
else
    plant = heli_plant();
end
end


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
function s = evaluateOne(s, plant, env)
%EVALUATEONE  Fill in s.reasons and s.metrics. Every check is a refusal.
%
% The envelope itself is heli_check_one, which is also what the students' own
% submit_gains runs and what collate_gains applies to the form export. This
% file used to carry its own copy, built on G = K/s^2 with Routh as
% K*Kd*Kp > Ki, and that copy went wrong when the plant became second order.
% Three implementations of one envelope is two too many.
%
% scripts/compare_envelope.py checks this against the Python side.

[ok, why, m] = heli_check_one(s.kp, s.ki, s.kd, plant, env);

s.metrics = struct( ...
    'routhRatio',  valueOr2(m, 'routh_ratio'), ...
    'damping',     valueOr2(m, 'damping'), ...
    'phaseMargin', valueOr2(m, 'phase_margin'), ...
    'peakVolts',   valueOr2(m, 'peak_volts'), ...
    'reversals',   valueOr2(m, 'reversals'), ...
    'settleS',     valueOr2(m, 'settle_s'), ...
    'gainDown',    NaN, ...
    'gainUp',      NaN);

% gainDown and gainUp are no longer tested. They existed because the double
% integrator's PID loop was conditionally stable, so a Bode gain margin read
% below 1 for every good design and the honest question was how far the gain
% could move in both directions. The second-order loop is not conditionally
% stable: a working design stays stable over a factor of a thousand either
% way, checked by sweeping, so the test never binds and reporting a number
% that always passes would be worse than reporting none.

if ~ok
    s.reasons(end+1) = string(why);
end
end


function v = valueOr2(m, name)
%VALUEOR2  A metric if the check got far enough to compute it.
if isfield(m, name); v = m.(name); else; v = NaN; end
end


function v = score(s)
%SCORE  Rank accepted gains: fast, then well damped, then gentle.
%
% heli_score is the definition; this only renames the fields, because the
% metrics struct here uses settleS where heli_check_one returns settle_s.
v = heli_score(struct('settle_s',   s.metrics.settleS, ...
                      'damping',    s.metrics.damping, ...
                      'peak_volts', s.metrics.peakVolts));
end


% --------------------------------------------------------------- the room

function flyRound(ok, round, plant, env)
%FLYROUND  What to fly, and in what order.
%
% Round 2 takes the plant because it checks a set of gains nobody submitted.
% It used to be handed K, the scalar, which is not what evaluateOne wants, and
% the round fell over with "Unrecognized function or variable 'plant'" the
% first time it was run against a folder rather than read.
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
        avg = evaluateOne(avg, plant, env);
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

% tracking: status=draft version=0
