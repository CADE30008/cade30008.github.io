function out = heli_log_session(source, label, dataDir)
%HELI_LOG_SESSION  Turn a flight into a file students can fit a model to.
%
%   heli_log_session([], 'open-loop-attempt')
%   heli_log_session([], 'step-2V', DATA_DIR)
%   heli_log_session(out.logsout, 'step-2V')
%
% Writes two files into the session's MATLAB Drive data folder:
%
%   <label>.mat   time, input and elevation, as plain vectors
%   <label>.csv   the same thing, for anyone not using MATLAB
%
% and prints a one-line summary so you can see from the front of the room
% whether the run is worth handing out before you hand it out.
%
% With [] as the first argument it reads what the laboratory models leave in
% the base workspace: the To Workspace structs inputData and elevData, or
% outputData, each with .time and .signals.values. That is how
% part1_identify and part3_validate log, so it is the normal call. Pass a
% Simulink.SimulationData.Dataset instead and it looks for elements called
% elevation and voltage.
%
% Units. Elevation comes back in **degrees**: the laboratory model brings it
% out as Elev(deg), and check_recording, fit_second_order and the students'
% own scripts all read degrees. This function used to convert from radians,
% which against a signal already in degrees is a factor of 57 in the fitted
% gain. Nothing converts now.
%
% The input column is Elevation Input, which is what the fitted K is per:
% K = 3.4 deg/V came from stepping Elevation Input from 0 to 2. It is not the
% motor voltage, and it is one offset block away from Velev. It keeps the name
% input_V because fit_second_order and the students' code read that name.
%
% Both files are written **view only** material. Nothing here touches a folder
% the cohort can write to, and submissions come back through the form rather
% than through a folder.
%
% The CSV exists because a student whose MATLAB is broken at 10 past the hour
% still has to be able to do the activity. It is the same data, not a summary.
%
% Not tested against the rig or QUARC. What is untested is whether the signal
% names below match a model nobody has run yet; the arithmetic underneath is
% tested against recordings in models/rig-data.

arguments
    source = []
    label (1,:) char = ''
    dataDir (1,:) char = ''
end

if isempty(label)
    error('heli_log_session:noLabel', ...
        'Give the run a name:  heli_log_session([], ''open-loop-attempt'')');
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

if isempty(source)
    [t, volt, elev] = fromWorkspace();
else
    [t, volt, elev] = fromDataset(source);
end

if numel(t) < 10
    error('heli_log_session:tooShort', ...
        'Only %d samples. Did the run actually start?', numel(t));
end

t = t(:); volt = volt(:); elev = elev(:);

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
fprintf('  input %+.2f to %+.2f\n', min(volt), max(volt));
if max(elev) - min(elev) < 1
    fprintf(2, '  WARNING: under 1 degree of movement. Nothing to identify here.\n');
end
if max(volt) - min(volt) < 1e-6
    fprintf(2, '  WARNING: the input never changes. There is no step to fit.\n');
end
fprintf('  -> %s\n  -> %s\n', matOut, csvOut);

out = struct('mat', matOut, 'csv', csvOut, 'samples', numel(t), ...
    'span_deg', max(elev) - min(elev), 'settled_deg', settled);
end


function [t, volt, elev] = fromWorkspace()
%FROMWORKSPACE  The To Workspace structs the laboratory models leave behind.
%
% elevData is Part 1's name for the elevation signal and outputData is Part
% 3's, which is the same split save_recording handles in the staff kit.
%
% Input and output are logged on their own clocks, so the input is resampled
% onto the output's time with a previous-value hold. It is a demand that steps
% and then sits still, so holding is right and interpolating would invent a
% ramp where the rig saw an edge.
in  = fetch({'inputData'});
el  = fetch({'elevData', 'outputData'});
t    = el.time(:);
elev = el.signals.values(:);
volt = interp1(in.time(:), in.signals.values(:), t, 'previous', 'extrap');
end


function s = fetch(names)
%FETCH  One To Workspace struct out of the base workspace, by any of its names.
for n = names
    if evalin('base', sprintf('exist(''%s'', ''var'')', n{1}))
        s = evalin('base', n{1});
        if isstruct(s) && isfield(s, 'time') && isfield(s, 'signals')
            return
        end
    end
end
error('heli_log_session:noSignal', ...
    ['Nothing called %s in the workspace, or it is not a logged signal.\n\n' ...
     'This reads what the Simulink model leaves behind, so run the model and\n' ...
     'let it finish first. If it did run, check the scopes are still set to\n' ...
     'log to the workspace.'], strjoin(names, ' or '));
end


function [t, volt, elev] = fromDataset(logsout)
%FROMDATASET  A Simulink.SimulationData.Dataset, for a model that logs that way.
[t, elev] = getSignal(logsout, 'elevation');
[~, volt] = getSignal(logsout, 'voltage');
end


function [t, y] = getSignal(logsout, name)
%GETSIGNAL  Fetch one logged signal, and say plainly when it is missing.
%
% The name is checked before the element is touched. Catching everything
% around the fetch and then blaming the name is how a Dataset holding plain
% timeseries, which have Time and Data where a logged Signal has Values, got
% reported as "no logged signal called elevation. Found: elevation".
available = string(logsout.getElementNames());
if ~any(available == string(name))
    error('heli_log_session:noSignal', ...
        ['No logged signal called "%s".\nThe model must log elevation and ' ...
         'voltage under those names.\nFound: %s'], name, strjoin(available, ', '));
end
e = logsout.getElement(name);
if isprop(e, 'Values') || isfield(e, 'Values'); e = e.Values; end
t = e.Time;
y = e.Data;
end

% tracking: status=draft version=0 assisted=true
