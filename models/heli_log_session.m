function out = heli_log_session(logsout, label, dataDir)
%HELI_LOG_SESSION  Turn a flight into a file students can fit a model to.
%
%   heli_log_session(logsout, 'open-loop-attempt')
%   heli_log_session(logsout, 'step-2V', DATA_DIR)
%
% Writes two files into the session's MATLAB Drive data folder:
%
%   <label>.mat   time, input and elevation, as plain vectors
%   <label>.csv   the same thing, for anyone not using MATLAB
%
% and prints a one-line summary so you can see from the front of the room
% whether the run is worth handing out before you hand it out.
%
% Both are written **view only** material. Nothing here touches submit/, which
% the whole cohort can read: a file of ours landing in there would be
% indistinguishable from a student's own work.
%
% The CSV exists because a student whose MATLAB is broken at 10 past the hour
% still has to be able to do the activity. It is the same data, not a summary.

arguments
    logsout
    label (1,:) char
    dataDir (1,:) char = ''
end

% Defaulting to the base workspace's DATA_DIR cannot be done in the arguments
% block itself, so it happens here.
if isempty(dataDir)
    if ~evalin('base', 'exist(''DATA_DIR'', ''var'')')
        error('heli_log_session:noDataDir', ...
            ['No DATA_DIR in the workspace. Run heli_demo_setup first, or pass ' ...
             'the folder\nas the third argument.']);
    end
    dataDir = evalin('base', 'DATA_DIR');
end

if ~isfolder(dataDir)
    error('heli_log_session:noFolder', ...
        ['Data folder does not exist:\n    %s\nMake it, and share it view-only, ' ...
         'before the session.'], dataDir);
end

t    = getSignal(logsout, 'elevation').Time;
elev = getSignal(logsout, 'elevation').Data;
volt = getSignal(logsout, 'voltage').Data;

if numel(t) < 10
    error('heli_log_session:tooShort', ...
        'Only %d samples. Did the run actually start?', numel(t));
end

% Elevation is logged in radians and handed out in degrees. Students read a
% plot before they read a variable name, and a plot in radians invites a
% factor-of-57 error that survives all the way to the fitted gain.
elev = rad2deg(elev(:));
t    = t(:);
volt = volt(:);

stem   = matlab.lang.makeValidName(label);
matOut = fullfile(dataDir, [stem '.mat']);
csvOut = fullfile(dataDir, [stem '.csv']);

time_s        = t;
input_V       = volt;
elevation_deg = elev;
recorded      = datetime('now', Format = 'yyyy-MM-dd HH:mm');
save(matOut, 'time_s', 'input_V', 'elevation_deg', 'recorded');
writetable(table(t, volt, elev, ...
    VariableNames = {'time_s', 'input_V', 'elevation_deg'}), csvOut);

% A quick look at what was captured, so a bad run is caught here rather than
% by 190 people trying to fit a model to it.
settled = mean(elev(max(1, end - round(0.05 * numel(elev))) : end));
fprintf('%s: %.1f s, %d samples at %.0f Hz\n', label, t(end) - t(1), numel(t), ...
    1 / median(diff(t)));
fprintf('  elevation %+.2f to %+.2f deg, settling near %+.2f\n', ...
    min(elev), max(elev), settled);
fprintf('  input %+.2f to %+.2f V\n', min(volt), max(volt));
if max(elev) - min(elev) < 1
    fprintf(2, '  WARNING: under 1 degree of movement. Nothing to identify here.\n');
end
fprintf('  -> %s\n  -> %s\n', matOut, csvOut);

out = struct('mat', matOut, 'csv', csvOut, 'samples', numel(t), ...
    'span_deg', max(elev) - min(elev), 'settled_deg', settled);
end


function s = getSignal(logsout, name)
%GETSIGNAL  Fetch one logged signal, and say plainly when it is missing.
try
    s = logsout.getElement(name).Values;
catch
    available = strjoin(string(logsout.getElementNames()), ', ');
    error('heli_log_session:noSignal', ...
        ['No logged signal called "%s".\nThe model must log elevation and ' ...
         'voltage under those names.\nFound: %s'], name, available);
end
end
