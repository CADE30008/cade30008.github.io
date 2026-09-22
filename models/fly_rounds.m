function record = fly_rounds(source, opts)
%FLY_ROUNDS  Drive the three rounds of flying, one set of gains at a time.
%
%   fly_rounds                                  the newest export in ~/Downloads
%   fly_rounds('~/Downloads/responses.xlsx')
%   fly_rounds(flights)                         a table collate_gains returned
%   fly_rounds(export, From = 2)                pick up at round 2
%   fly_rounds(export, Out = '~/Downloads')     where the flight record goes
%
% This is the one thing to run at the lectern. It reads the form export,
% builds the flight list, works out the three rounds, and then goes through
% them a set at a time: whose gains are up, what the model says it will do,
% a pause while you fly it, and three questions about what it actually did.
%
% Each screen holds one set of gains and nothing else, so there is no place in
% it to lose your position, and it says at the top which round it is and how
% far through. Press ENTER to fly, s to skip, q to stop. Stopping is safe:
% every flight is written to the record as it happens, and From picks the
% round to start from.
%
%   Round 1   the extremes: the most aggressive, the most sluggish and the
%             most integral of the sets that passed
%   Round 2   the average of the sets that passed, checked like any other
%             submission and refused if it fails
%   Round 3   the best few, fastest first
%
% Display names only. The University accounts the form records are read by
% collate_gains to tell one person's submissions from another's and are never
% put on this screen.
%
% What it does not do: fly anything. It does not talk to QUARC, the rig or
% Simulink. You type the gains into the model as you always would; this reads
% the export, decides the order, and holds the numbers to compare afterwards.

arguments
    source = ''
    opts.From (1,1) double {mustBeMember(opts.From, [1 2 3])} = 1
    opts.Out (1,:) char = ''
    opts.Answers (1,:) string = strings(1,0)
end

RULE = repmat('=', 1, 64);
THIN = repmat('-', 1, 64);

% ---- the flight list ----------------------------------------------------
[flights, exportFile] = resolveFlights(source);
plant = heli_plant();
env   = heli_envelope();
plan  = buildPlan(flights, plant, env);
out   = recordFile(opts.Out, exportFile);

% ---- what is about to happen -------------------------------------------
fprintf('\n%s\n  THE ROOM''S GAINS, IN THREE ROUNDS\n%s\n\n', RULE, RULE);
fprintf('  plant   K %.2f deg/V   wn %.2f rad/s   zeta %.3f\n', ...
    plant.K, plant.wn, plant.zeta);
fprintf('  trim    %s\n', env.trimSource);
fprintf('  budget  %.1f V peak for a %g deg demand\n\n', ...
    env.voltagePeakMax, env.stepDeg);
for r = 1:3
    inRound = plan([plan.round] == r);
    fprintf('  round %d  %-22s %d set(s)', r, roundName(r), numel(inRound));
    refused = nnz(~[inRound.ok]);
    if refused > 0; fprintf('   %d refused', refused); end
    fprintf('\n');
end
fprintf('\n  record  %s\n', out);
if opts.From > 1
    fprintf('  starting at round %d\n', opts.From);
end
fprintf('\n');

% ---- the rounds ---------------------------------------------------------
ai = 1;                                   % where we are in a scripted rehearsal
rows = cell(0, 1);
k = find([plan.round] >= opts.From, 1);
if isempty(k)
    fprintf(2, 'Nothing to fly from round %d onwards.\n', opts.From);
    record = table();
    return
end

while k <= numel(plan)
    item = plan(k);
    nth  = nnz([plan(1:k).round] == item.round);
    ofN  = nnz([plan.round] == item.round);

    showSet(item, nth, ofN, env, RULE);

    if ~item.ok
        [~, ai] = askLine('ENTER to go on      q stop here', opts.Answers, ai, THIN);
        rows{end+1} = logFlight(out, item, 'refused', NaN, NaN, ''); %#ok<AGROW>
        k = k + 1;
        continue
    end

    [answer, ai] = askLine('ENTER to fly it     s skip      q stop here', ...
        opts.Answers, ai, THIN);
    switch lower(answer)
        case 'q'
            fprintf('\n  Stopped at round %d, set %d.\n', item.round, nth);
            fprintf('  To pick up here:  fly_rounds(..., From = %d)\n\n', item.round);
            break
        case 's'
            rows{end+1} = logFlight(out, item, 'no', NaN, NaN, 'skipped'); %#ok<AGROW>
        otherwise
            [over, settle, note, ai] = askActuals(item, opts.Answers, ai, THIN);
            saySoFar(item, over, settle);
            rows{end+1} = logFlight(out, item, 'yes', over, settle, note); %#ok<AGROW>
    end
    k = k + 1;
end

% ---- what happened ------------------------------------------------------
if isempty(rows)
    record = table();
else
    record = vertcat(rows{:});
end
fprintf('\n%s\n  %d flight(s) recorded\n%s\n', RULE, height(record), RULE);
if ~isempty(record)
    disp(record(:, {'round', 'name', 'flew', ...
        'predicted_overshoot_pct', 'actual_overshoot_pct', ...
        'predicted_settle_s', 'actual_settle_s'}));
end
fprintf('  %s\n\n', out);
end


% =================================================== reading the flight list

function [flights, exportFile] = resolveFlights(source)
%RESOLVEFLIGHTS  A table from whatever was passed, or found.
if istable(source)
    flights = source;
    exportFile = '';
    return
end

exportFile = char(source);
if isempty(exportFile)
    exportFile = newestExport();
    fprintf('Using the newest export in Downloads:\n    %s\n', exportFile);
end
flights = collate_gains(exportFile);
end


function file = newestExport()
%NEWESTEXPORT  The most recent Forms export sitting in Downloads.
%
% Typing a path at a lectern with a room watching is how a session loses two
% minutes to a spelling mistake, so with no argument this guesses and says out
% loud what it guessed. It only ever looks at Downloads, and it never guesses
% between an export and something else: the name has to contain "response".
home = getenv('HOME');
if isempty(home); home = getenv('USERPROFILE'); end
folder = fullfile(home, 'Downloads');
d = [dir(fullfile(folder, '*response*.xlsx')); dir(fullfile(folder, '*response*.csv'))];
d = d(~startsWith({d.name}, {'.', '~$'}));
if isempty(d)
    error('fly_rounds:noExport', ...
        ['No form export found in\n    %s\n' ...
         'Looked for a .xlsx or .csv with "response" in the name. Export the\n' ...
         'responses, or pass the path:\n' ...
         '    fly_rounds(''/path/to/responses.xlsx'')'], folder);
end
[~, i] = max([d.datenum]);
file = fullfile(d(i).folder, d(i).name);
end


function out = recordFile(given, exportFile)
%RECORDFILE  Where the flight record goes.
%
% Beside the export by default, because that folder is already where this
% session's student data lives and it is not shared with the cohort.
% heli_flight_record refuses a submit/ folder and refuses the repository, so
% a wrong answer here stops rather than leaking.
if ~isempty(given)
    folder = heli_expand_path(given);
elseif ~isempty(exportFile)
    folder = fileparts(heli_expand_path(exportFile));
else
    folder = pwd;
end
out = fullfile(folder, sprintf('flight-record-%s.csv', ...
    char(datetime('now', 'Format', 'yyyy-MM-dd'))));
end


% ========================================================== building the plan

function plan = buildPlan(flights, plant, env)
%BUILDPLAN  The three rounds, in the order they are flown.
%
% Metrics are recomputed here rather than carried out of collate_gains, which
% returns damping and the verdict and not the rest. It is the same
% heli_check_one on the same plant, so a set cannot be accepted by one and
% refused by the other; what it adds is settling time, peak volts and the
% predicted overshoot, which are what round 1 is chosen on and what the rig is
% compared against afterwards.
needed = {'name', 'Kp', 'Ki', 'Kd', 'verdict'};
absent = needed(~ismember(needed, flights.Properties.VariableNames));
if ~isempty(absent)
    error('fly_rounds:badTable', ...
        ['The flight list has no %s.\nPass the table collate_gains returns, ' ...
         'or the export itself.'], strjoin(absent, ', '));
end

n = height(flights);
m = cell(n, 1);
ok = false(n, 1);
for i = 1:n
    [ok(i), ~, m{i}] = heli_check_one(flights.Kp(i), flights.Ki(i), flights.Kd(i), ...
        plant, env);
end
flew = find(ok(:) & string(flights.verdict) == "fly");

plan = emptyPlan();

% ---- round 1, the extremes ---------------------------------------------
if isempty(flew)
    % The run sheet's fallback, flown as the lecturer's own and labelled as
    % such. It is checked here rather than assumed: if the plant moved this
    % morning, these are not safe either and the screen has to say so.
    [fok, fwhy, fm] = heli_check_one(0.71, 0.59, 0.91, plant, env);
    plan(end+1) = mkItem(1, 'the fallback, mine and not yours', ...
        'NOBODY''S GAINS PASSED', 0.71, 0.59, 0.91, fok, fwhy, fm);
else
    % Aggression is read off settling time, which is a proxy and worth
    % knowing is one. On the fixture the fastest set is also the one with the
    % least damping and the most overshoot, so the label and the flight
    % agree; the set asking for the most volts was the best damped of the
    % seven, so peak demand would have put "the most aggressive" on screen
    % above the tidiest design in the room. Same choice as heli_check_gains.
    settle = cellfun(@(x) fieldOr(x, 'settle_s', Inf), m(flew));
    ki     = flights.Ki(flew);
    [~, fast]  = min(settle);
    [~, slow]  = max(settle);
    [~, integ] = max(ki);
    wanted = [fast, slow, integ];
    labels = {'the most aggressive', 'the most sluggish', 'the most integral'};
    % One submission can be two of these at once. It is flown once and carries
    % both labels, or the name on the screen says the wrong thing about it.
    for j = unique(wanted, 'stable')
        i = flew(j);
        plan(end+1) = mkItem(1, strjoin(labels(wanted == j), ' and '), ...
            flights.name(i), flights.Kp(i), flights.Ki(i), flights.Kd(i), ...
            true, "", m{i}); %#ok<AGROW>
    end
end

% ---- round 2, the average ----------------------------------------------
avg = heli_cohort_average(flights, plant, env);
if avg.n > 0
    plan(end+1) = mkItem(2, sprintf('the average of the %d that passed', avg.n), ...
        'THE COHORT AVERAGE', avg.kp, avg.ki, avg.kd, avg.ok, avg.why, avg.metrics);
    plan(end).spread = avg.spread;
end

% ---- round 3, the best few ---------------------------------------------
if ~isempty(flew)
    [~, best] = sort(cellfun(@(x) heli_score(x), m(flew)));
    for j = 1:min(3, numel(best))
        i = flew(best(j));
        plan(end+1) = mkItem(3, sprintf('#%d of %d that passed', j, numel(flew)), ...
            flights.name(i), flights.Kp(i), flights.Ki(i), flights.Kd(i), ...
            true, "", m{i}); %#ok<AGROW>
    end
end

% Round 3 usually picks up something round 1 already flew. Say so on the
% screen instead of quietly flying the same gains twice with the clock at 108.
for a = 1:numel(plan)
    for b = 1:a-1
        same = isequal([plan(a).kp plan(a).ki plan(a).kd], ...
                       [plan(b).kp plan(b).ki plan(b).kd]);
        if same; plan(a).again = plan(b).round; break; end
    end
end
end


function p = emptyPlan()
p = struct('round', {}, 'label', {}, 'name', {}, 'kp', {}, 'ki', {}, 'kd', {}, ...
           'ok', {}, 'why', {}, 'm', {}, 'spread', {}, 'again', {});
end


function it = mkItem(round, label, name, kp, ki, kd, ok, why, m)
it = struct('round', round, 'label', label, 'name', char(name), ...
            'kp', kp, 'ki', ki, 'kd', kd, ...
            'ok', logical(ok), 'why', string(why), 'm', m, ...
            'spread', [], 'again', 0);
end


function v = fieldOr(s, name, fallback)
if isstruct(s) && isfield(s, name) && isfinite(s.(name))
    v = s.(name);
else
    v = fallback;
end
end


function s = roundName(r)
switch r
    case 1; s = 'the extremes';
    case 2; s = 'the cohort average';
    otherwise; s = 'the best few';
end
end


% ================================================================ the screen

function showSet(item, nth, ofN, env, RULE)
%SHOWSET  One set of gains, filling the window, and nothing else.
fprintf('\n\n%s\n', RULE);
fprintf(' ROUND %d   %-30s        set %d of %d\n', ...
    item.round, roundName(item.round), nth, ofN);
fprintf('%s\n\n', RULE);

fprintf('   %s\n', upper(item.name));
fprintf('   %s\n', item.label);
if ~isempty(item.spread)
    fprintf('   spread across them   Kp %.2f   Ki %.2f   Kd %.2f\n', ...
        item.spread(1), item.spread(2), item.spread(3));
end
fprintf('\n');
fprintf('      Kp  %-10.3g Ki  %-10.3g Kd  %-10.3g\n\n', item.kp, item.ki, item.kd);

if item.ok
    m = item.m;
    fprintf('   the model says     overshoot      %.0f %%\n', ...
        fieldOr(m, 'overshoot_pct', NaN));
    fprintf('                      settles in     %.1f s\n', ...
        fieldOr(m, 'settle_s', NaN));
    fprintf('                      damping        %.2f\n', ...
        fieldOr(m, 'damping', NaN));
    fprintf('                      phase margin   %.0f deg\n', ...
        fieldOr(m, 'phase_margin', NaN));
    fprintf('                      peak demand    %.1f V of the %.1f allowed\n', ...
        fieldOr(m, 'peak_volts', NaN), env.voltagePeakMax);
    if item.again > 0
        fprintf('\n   These already flew in round %d. Skip it if the clock is tight.\n', ...
            item.again);
    end
else
    fprintf('   ***  REFUSED. DO NOT FLY THIS ONE.  ***\n\n');
    fprintf('   %s\n', wrapAt(char(item.why), 58, '   '));
    if item.round == 2
        fprintf('\n   Every set that went into this average passed that same\n');
        fprintf('   check. The average did not. Say that, and move on.\n');
    end
end
end


function saySoFar(item, over, settle)
%SAYSOFAR  The model's two numbers against the two just typed in.
p_over   = fieldOr(item.m, 'overshoot_pct', NaN);
p_settle = fieldOr(item.m, 'settle_s', NaN);
fprintf('\n   model  %s overshoot, %s\n', pct(p_over), secs(p_settle));
fprintf('   rig    %s overshoot, %s\n\n', pct(over), secs(settle));
end


function s = pct(v)
if isfinite(v); s = sprintf('%.0f %%', v); else; s = 'overshoot not read'; end
end


function s = secs(v)
if isfinite(v); s = sprintf('settles in %.1f s', v); else; s = 'never settles'; end
end


function out = wrapAt(txt, width, indent)
%WRAPAT  Break a refusal across lines, so it is not cut off on a projector.
words = strsplit(strtrim(txt));
out = ''; line = '';
for w = words
    if isempty(line)
        line = w{1};
    elseif numel(line) + numel(w{1}) + 1 <= width
        line = [line ' ' w{1}]; %#ok<AGROW>
    else
        out = [out line newline indent]; %#ok<AGROW>
        line = w{1};
    end
end
out = [out line];
end


% ================================================================= the asking

function [txt, ai] = askLine(prompt, answers, ai, THIN)
%ASKLINE  One question, and the answer typed back.
%
% The only part of this file that reads a keyboard, so it is the only part
% that cannot be run under matlab -batch. Answers is a scripted list of
% replies, which is how the walk-through is rehearsed and tested; in the room
% it is empty and every answer comes from the keyboard.
fprintf('\n%s\n %s\n%s\n', THIN, prompt, THIN);
if ai <= numel(answers)
    txt = char(answers(ai));
    ai = ai + 1;
    fprintf('> %s\n', txt);
else
    if ~isempty(answers)
        % A rehearsal that ran out of script. Carry on with blanks rather
        % than blocking, so the rest of the walk-through still gets checked.
        txt = '';
        fprintf('> \n');
    else
        txt = input('> ', 's');
    end
end
txt = strtrim(char(txt));
end


function [over, settle, note, ai] = askActuals(item, answers, ai, THIN)
%ASKACTUALS  What the rig did, while the numbers are still on the screen.
fprintf('\n%s\n %s is up:   Kp %.3g   Ki %.3g   Kd %.3g\n', ...
    THIN, upper(item.name), item.kp, item.ki, item.kd);
fprintf(' the model said %s overshoot, settling in %s\n%s\n', ...
    pct(fieldOr(item.m, 'overshoot_pct', NaN)), ...
    secs(fieldOr(item.m, 'settle_s', NaN)), THIN);

[over, ai]   = askNumber('overshoot you saw, %      ENTER to leave it blank', ...
    answers, ai, THIN);
[settle, ai] = askNumber('settling time to 2%, s    ENTER if it never settled', ...
    answers, ai, THIN);
[note, ai]   = askLine('anything to remember      ENTER for none', answers, ai, THIN);
end


function [x, ai] = askNumber(prompt, answers, ai, THIN)
%ASKNUMBER  A number, or blank. Anything else is asked again rather than lost.
while true
    [txt, ai] = askLine(prompt, answers, ai, THIN);
    if isempty(txt); x = NaN; return; end
    x = str2double(regexprep(txt, '[%s\s]', ''));
    if isfinite(x); return; end
    fprintf(' "%s" is not a number. Type one, or press ENTER to leave it out.\n', txt);
end
end


% ================================================================ the record

function row = logFlight(out, item, flew, over, settle, note)
%LOGFLIGHT  One row, written now rather than at the end.
entry = struct( ...
    'round', item.round, 'label', item.label, 'name', item.name, ...
    'kp', item.kp, 'ki', item.ki, 'kd', item.kd, ...
    'verdict', ternary(item.ok, 'fly', 'hold'), ...
    'predicted_overshoot_pct', fieldOr(item.m, 'overshoot_pct', NaN), ...
    'predicted_settle_s',      fieldOr(item.m, 'settle_s', NaN), ...
    'predicted_damping',       fieldOr(item.m, 'damping', NaN), ...
    'predicted_pm_deg',        fieldOr(item.m, 'phase_margin', NaN), ...
    'predicted_peak_V',        fieldOr(item.m, 'peak_volts', NaN), ...
    'flew', flew, ...
    'actual_overshoot_pct', over, 'actual_settle_s', settle, ...
    'note', note);
row = heli_flight_record(out, entry);
end


function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
