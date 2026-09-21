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
    opts.Plant (1,1) double = NaN
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

K = plantGain(opts.Plant);

rows = cell(0, 8);
for i = keep'
    [ok, why, zeta] = checkGains(kp(i), ki(i), kd(i), K, typed(i,:));
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
flat = lower(regexprep(names, '[^a-zA-Z0-9]', ''));
for w = wanted
    hit = find(strcmp(flat, regexprep(lower(w{1}), '[^a-zA-Z0-9]', '')), 1);
    if ~isempty(hit); c = names{hit}; return; end
end
if optional; c = ''; return; end
error('collate_gains:noColumn', ...
    ['No column named %s in the export. Found: %s\n' ...
     'The four questions must be named Display name, Kp, Ki and Kd.'], ...
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


function K = plantGain(override)
%PLANTGAIN  The fitted elevation gain, or the provisional one.
if ~isnan(override); K = override; return; end
here = fileparts(mfilename('fullpath'));
f = fullfile(here, '..', 'docs', 'w01-design-cycle', 'code', 'elevation_plant.json');
if isfile(f)
    d = jsondecode(fileread(f));
    if isfield(d, 'K') && isfinite(d.K) && d.K > 0; K = d.K; return; end
end
K = 3.4;
fprintf(2, ['Using the provisional plant gain K = %.2f. Pass ''Plant'' with the\n' ...
            'value fitted in the session to check against what was actually flown.\n'], K);
end


function [ok, why, zeta] = checkGains(kp, ki, kd, K, typed)
%CHECKGAINS  The envelope, stated the same way the student was told it.
%
% A rejection quotes what the student actually typed. "Kp is not a number"
% sends you to the spreadsheet to work out why; quoting the text tells you at
% a glance whether to say "decimal point, please" or something else.
GAIN_MAX = 50; ROUTH = 1.15; ZETA_MIN = 0.15;
zeta = NaN;
named = struct('Kp', kp, 'Ki', ki, 'Kd', kd);
order = ["Kp" "Ki" "Kd"];
for j = 1:3
    g = order(j);
    v = named.(g);
    if ~isfinite(v)
        ok = false;
        if typed(j) == ""
            why = g + " was left blank";
        else
            why = string(sprintf('%s is not a number: "%s"', g, typed(j)));
        end
        return
    end
    if v <= 0; ok = false; why = g + " must be above zero"; return; end
    if v > GAIN_MAX; ok = false; why = g + " is above the limit of " + GAIN_MAX; return; end
end
ratio = K * kd * kp / ki;
if ratio <= 1
    ok = false; why = sprintf('unstable: K*Kd*Kp/Ki = %.2f', ratio); return
elseif ratio < ROUTH
    ok = false; why = sprintf('too close to unstable: ratio %.2f', ratio); return
end
p = roots([1, K*kd, K*kp, K*ki]);
osc = p(abs(imag(p)) > 1e-9);
if isempty(osc)
    zeta = 1;
else
    [~, j] = max(real(osc));
    zeta = -real(osc(j)) / abs(osc(j));
end
if zeta < ZETA_MIN
    ok = false; why = sprintf('too lightly damped: zeta = %.3f', zeta); return
end
ok = true; why = "";
end


function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
