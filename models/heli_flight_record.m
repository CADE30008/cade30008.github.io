function row = heli_flight_record(file, entry)
%HELI_FLIGHT_RECORD  Append one flight to the session's record.
%
%   heli_flight_record(file, entry)
%
% One row per set of gains put on the rig, holding what the model predicted
% next to what the rig did. That pairing is the only thing the session
% produces that cannot be reconstructed afterwards: the gains are in the form
% export, the predictions come back out of heli_check_one, and the overshoot
% and settling time somebody read off the screen exist nowhere else.
%
% entry is a struct. Everything is optional except round, label, name and the
% three gains; anything absent is written blank.
%
%   round                      1, 2 or 3
%   label                      why this set is being flown
%   name                       the display name, never a University account
%   kp, ki, kd
%   verdict                    'fly' or 'hold'
%   predicted_overshoot_pct, predicted_settle_s, predicted_damping,
%   predicted_pm_deg, predicted_peak_V
%   flew                       'yes', 'no' or 'refused'
%   actual_overshoot_pct, actual_settle_s
%   note
%
% The file is a CSV, written a row at a time and flushed each time, so a
% MATLAB that falls over at minute 105 costs the flight in progress and
% nothing before it. Read it back with readtable.
%
% Where it may not be written:
%
%   a folder called submit/, which the whole cohort can read. A file in there
%   listing whose gains flew publishes what the display name was protecting.
%
%   anywhere inside this repository. Submitted gains and the names attached to
%   them are student work, and student work does not enter it, not in docs/,
%   not in private/, not ignored.
%
% Returns the row as a one-line table.

arguments
    file (1,:) char
    entry struct
end

fields = {'round', 'label', 'name', 'kp', 'ki', 'kd', 'verdict', ...
          'predicted_overshoot_pct', 'predicted_settle_s', 'predicted_damping', ...
          'predicted_pm_deg', 'predicted_peak_V', 'flew', ...
          'actual_overshoot_pct', 'actual_settle_s', 'note'};
required = {'round', 'label', 'name', 'kp', 'ki', 'kd'};
absent = required(~isfield(entry, required));
if ~isempty(absent)
    error('heli_flight_record:incomplete', ...
        'The entry has no %s.', strjoin(absent, ', '));
end

file = heli_expand_path(file);
folder = fileparts(file);
if isempty(folder); folder = pwd; end
refuseSharedFolder(folder);
refuseInsideRepository(folder);
if ~isfolder(folder)
    error('heli_flight_record:noFolder', 'No such folder:\n    %s', folder);
end

row = table('Size', [1 numel(fields) + 1], ...
    'VariableTypes', [{'string'}, repmat({'string'}, 1, numel(fields))], ...
    'VariableNames', [{'when'}, fields]);
row.when = string(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
for f = fields
    row.(f{1}) = asText(entry, f{1});
end

% Everything is written as text on purpose. Half these columns are blank
% while the session runs, and a column of numbers with blanks in it comes
% back from readtable as NaN in some rows and "" in others depending on what
% the first row happened to hold.
started = isfile(file);
if started
    writetable(row, file, 'WriteMode', 'append', 'WriteVariableNames', false);
else
    writetable(row, file, 'WriteMode', 'overwrite', 'WriteVariableNames', true);
end
end


function s = asText(entry, name)
%ASTEXT  One field as text, blank when it is absent or not a number.
if ~isfield(entry, name); s = ""; return; end
v = entry.(name);
if isempty(v); s = ""; return; end
if isnumeric(v) || islogical(v)
    if ~isfinite(v); s = ""; else; s = string(sprintf('%.6g', double(v))); end
else
    s = strtrim(string(v));
end
end


function refuseSharedFolder(folder)
%REFUSESHAREDFOLDER  Never write into the folder the cohort can read.
parts = split(string(strrep(folder, '\', '/')), '/');
if any(lower(parts) == "submit")
    error('heli_flight_record:sharedFolder', ...
        ['That path goes through a folder called submit:\n    %s\n' ...
         'The whole cohort can read it, and a list of whose gains flew would\n' ...
         'publish exactly what the display name was there to protect.'], folder);
end
end


function refuseInsideRepository(folder)
%REFUSEINSIDEREPOSITORY  Keep student work out of the course repository.
%
% The repository is found from this file rather than from the working
% directory, so it is this repository that is refused and not whichever other
% checkout the lecturer's home directory happens to contain.
repo = fileparts(fileparts(mfilename('fullpath')));
here = normalise(folder);
if startsWith(here, normalise(repo))
    error('heli_flight_record:insideRepository', ...
        ['%s is inside the course repository.\n' ...
         'Submitted gains and the names on them are student work, and student\n' ...
         'work does not go in here. Give a folder outside it, next to the form\n' ...
         'export:\n    fly_rounds(export, Out = "~/Downloads")'], folder);
end
end


function p = normalise(folder)
%NORMALISE  An absolute path ending in a separator, so a prefix test is exact.
%
% Without the trailing separator, ".../cade30008.github.io-notes" reads as
% being inside ".../cade30008.github.io".
p = string(heli_expand_path(folder));
if ~endsWith(p, filesep); p = p + filesep; end
end

% tracking: status=draft version=0
