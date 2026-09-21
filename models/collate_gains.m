function flights = collate_gains(file, opts)
%COLLATE_GAINS  Turn the form's export into a flight list.
%
%   flights = collate_gains('~/Downloads/responses.xlsx')
%   collate_gains(file, 'Plant', 3.4)          override the fitted gain
%   collate_gains(file, 'Keep', 'all')         every submission, not the last
%
% Reads what Microsoft Forms exports, finds the four columns we care about
% whatever else the export carries, checks each set of gains against the same
% envelope the student was checked against, and returns them in the order they
% should be flown.
%
% One person, one flight. Students resubmit while they tune, so by default only
% each person's last submission survives. Identity comes from the email the
% form records; if the form was left open to anonymous responses there is no
% email, and the display name is used instead, which means two students who
% pick the same alias collapse into one. The report says when that happened.
%
% Returns a table: order, name, Kp, Ki, Kd, zeta, verdict, why.

arguments
    file (1,:) char
    opts.Plant struct = struct([])
    opts.Keep (1,:) char {mustBeMember(opts.Keep, {'last','all'})} = 'last'
end

if ~isfile(file)
    error('collate_gains:noFile', 'No such export:\n    %s', file);
end
% Columns are located before the file is read, not after, because readtable
% decides a column of mostly-numbers is a double column and quietly turns
% "Kp = 6.2" into NaN on the way in. By the time the table exists the text a
% student actually typed is gone, and with it any chance of telling them what
% was wrong with it. The four answer columns are forced to text and parsed
% here; everything else, the timestamps especially, keeps its natural type.
iopts = detectImportOptions(file, 'VariableNamingRule', 'preserve');
names = iopts.VariableNames;
col = struct( ...
    'name',  findColumn(names, {'display name', 'displayname', 'name'}, true), ...
    'kp',    findColumn(names, {'kp'}, false), ...
    'ki',    findColumn(names, {'ki'}, false), ...
    'kd',    findColumn(names, {'kd'}, false), ...
    'email', findColumn(names, {'email', 'username', 'user name'}, true), ...
    'time',  findColumn(names, {'completion time', 'submitted', 'last modified time'}, true));

asText = {col.kp, col.ki, col.kd};
if ~isempty(col.name); asText{end+1} = col.name; end
iopts = setvartype(iopts, asText, 'string');
raw = readtable(file, iopts);
if isempty(raw)
    error('collate_gains:empty', 'The export has no rows in it at all.');
end

n = height(raw);
name = strings(n,1); kp = nan(n,1); ki = nan(n,1); kd = nan(n,1);
typed = strings(n,3);
for i = 1:n
    name(i) = cellText(raw, col.name, i);
    kp(i) = cellNumber(raw, col.kp, i);
    ki(i) = cellNumber(raw, col.ki, i);
    kd(i) = cellNumber(raw, col.kd, i);
    typed(i,:) = [cellText(raw, col.kp, i), cellText(raw, col.ki, i), ...
                  cellText(raw, col.kd, i)];
end
blank = name == "";
name(blank) = "(no name given)";

% Who each row belongs to. Email when the form recorded one, because two
% students can and will both call themselves Maverick.
if isempty(col.email)
    who = lower(strtrim(name));
    identity = 'display name';
else
    who = strings(n,1);
    for i = 1:n; who(i) = lower(strtrim(cellText(raw, col.email, i))); end
    identity = 'email';
end

order = (1:n)';
if ~isempty(col.time)
    t = raw.(col.time);
    if isdatetime(t); [~, order] = sort(t); end
end

keep = order;
if strcmp(opts.Keep, 'last')
    seen = containers.Map('KeyType','char','ValueType','double');
    for i = order'                        % oldest first, so later overwrites
        seen(char(who(i))) = i;
    end
    keep = sort(cell2mat(values(seen)))';
end

if isempty(opts.Plant)
    plant = heli_plant();
else
    plant = heli_plant(opts.Plant);
end
env = heli_envelope();
fprintf('\nPlant: K = %g deg/V, wn = %g rad/s, zeta = %g\n', ...
    plant.K, plant.wn, plant.zeta);

rows = cell(0, 8);
for i = keep'
    [ok, why, m] = checkOne(kp(i), ki(i), kd(i), plant, env, typed(i,:));
    if isfield(m, 'damping'); zeta = m.damping; else; zeta = NaN; end
    rows(end+1, :) = {numel(rows)+1, name(i), kp(i), ki(i), kd(i), zeta, ...
                      string(ternary(ok, "fly", "hold")), string(why)}; %#ok<AGROW>
end
flights = cell2table(rows, 'VariableNames', ...
    {'order', 'name', 'Kp', 'Ki', 'Kd', 'zeta', 'verdict', 'why'});

flyable = flights.verdict == "fly";
flights = [flights(flyable, :); flights(~flyable, :)];
flights.order = (1:height(flights))';

fprintf('\n%d submission(s) from %d %s(s); %d set(s) fit to fly.\n', ...
    n, numel(unique(who)), identity, nnz(flyable));
if strcmp(opts.Keep, 'last') && n > numel(keep)
    fprintf('%d superseded by a later submission from the same %s.\n', ...
        n - numel(keep), identity);
end
if isempty(col.email)
    fprintf(2, ['NOTE: no email column, so submissions were matched on display\n' ...
                'name. Two people sharing an alias have been merged into one.\n']);
end
disp(flights);
end


function c = findColumn(names, wanted, optional)
%FINDCOLUMN  A column whose header matches, ignoring case and punctuation.
%
% The export's headers are the question text, verbatim, so "Kp" survives only
% as long as nobody improves the question to "Kp (proportional gain)". Each
% candidate term is tried exact, then as a prefix, then anywhere in the header,
% and the first term to match anything wins.
%
% The loops are this way round on purpose. A Microsoft Forms export carries the
% respondent's own "Name" column alongside our "Display name" question, so a
% pass that tried every term exactly before trying any term loosely would bind
% "name" to the wrong column the moment the question was reworded. The more
% specific term has to be exhausted first, not the stricter test.
flat = lower(regexprep(names, '[^a-zA-Z0-9]', ''));
want = cellfun(@(w) regexprep(lower(w), '[^a-zA-Z0-9]', ''), wanted, ...
               'UniformOutput', false);
tests = {@(f, w) strcmp(f, w), @(f, w) startsWith(f, w), @(f, w) contains(f, w)};
for k = 1:numel(want)
    for t = tests
        hit = find(cellfun(@(f) t{1}(f, want{k}), flat), 1);
        if ~isempty(hit); c = names{hit}; return; end
    end
end
if optional; c = ''; return; end
error('collate_gains:noColumn', ...
    ['No column named %s in the export.\nFound: %s\n' ...
     'The four questions should be Display name, Kp, Ki and Kd, in that order.'], ...
    strjoin(wanted, ' or '), strjoin(names, ', '));
end


function s = cellText(t, c, i)
if isempty(c); s = ""; return; end
v = t.(c)(i);
if iscell(v); v = v{1}; end
if ismissing(v); s = ""; else; s = strtrim(string(v)); end
end


function x = cellNumber(t, c, i)
%CELLNUMBER  A number out of a text answer, tolerating what people type.
%
% Students paste "Kp = 7.4" and " 7.4 " and both should work. A comma is the
% exception: "12,5" is twelve and a half to half the room and twelve thousand
% five hundred to a parser, and there is no way to tell which was meant. It is
% refused rather than guessed. A rejected submission costs one resubmission;
% a gain silently read as ten times its value gets flown.
s = cellText(t, c, i);
if s == ""; x = NaN; return; end
s = erase(s, [" ", "="]);
s = regexprep(s, '^[Kk][PpIiDd]', '');         % a leading "Kp", "Ki" or "Kd"
if contains(s, ",")
    x = NaN; return
end
x = str2double(s);
end


function [ok, why, m] = checkOne(kp, ki, kd, plant, env, typed)
%CHECKONE  heli_check_one, plus the one thing it cannot know.
%
% The envelope itself lives in heli_check_one, so this tool and the one the
% students run cannot drift apart. All this adds is quoting back what was
% actually typed when a field would not parse, which only the reader of the
% export has.
order = ["Kp" "Ki" "Kd"];
vals  = [kp ki kd];
for j = 1:3
    if ~isfinite(vals(j))
        ok = false; m = struct();
        if typed(j) == ""
            why = order(j) + " was left blank";
        else
            why = string(sprintf('%s is not a number: "%s"', order(j), typed(j)));
        end
        return
    end
end
[ok, why, m] = heli_check_one(kp, ki, kd, plant, env);
end


function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
