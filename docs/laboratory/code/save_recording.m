function file = save_recording(name)
%SAVE_RECORDING  Save what the rig just logged, under a name you choose.
%
%   save_recording('trim-2V')
%   save_recording('part3-designed')
%
% Run this after a Simulink run has finished, with the model's logged signals
% still in the workspace.
%
% Replaces the laboratory's `s_save`, which does the same job but always
% writes to `d_Part1.mat`. Part 1 asks you for several recordings at different
% trims, and with a fixed filename each one overwrites the last, which you
% find out about later when you have one recording and three labels.
%
% Works after either model. It saves whichever signals are there:
%
%   part1_identify   inputTime, input, outputTime, output
%   part3_validate   the same, plus demand, pitch and travel
%
% The variable names are the laboratory's own, so `fit_second_order`,
% `lab1_fit` and the rest read these files without knowing where they came
% from.

arguments
    name (1,:) char
end

% Pairs of [logged struct in the workspace, what to call it in the file].
% elevData is Part 1's name for the elevation signal; outputData is Part 3's.
wanted = { 'inputData',  'inputTime',  'input'
           'elevData',   'outputTime', 'output'
           'outputData', 'outputTime', 'output'
           'demandData', 'demandTime', 'demand'
           'pitchData',  'pitchTime',  'pitch'
           'travelData', 'travelTime', 'travel' };

vars = struct();
found = {};
for i = 1:size(wanted, 1)
    src = wanted{i,1};
    if ~evalin('base', sprintf('exist(''%s'', ''var'')', src))
        continue
    end
    s = evalin('base', src);
    if ~isstruct(s) || ~isfield(s, 'time') || ~isfield(s, 'signals')
        continue
    end
    vars.(wanted{i,2}) = s.time;
    vars.(wanted{i,3}) = s.signals.values;
    found{end+1} = src; %#ok<AGROW>
end

if ~isfield(vars, 'inputTime') || ~isfield(vars, 'outputTime')
    error('save_recording:nothingLogged', ...
        ['No logged signals in the workspace.\n\n' ...
         'This reads what the Simulink model leaves behind, so run the model\n' ...
         'first and let it finish. If it did run, check the scopes are still\n' ...
         'set to log to the workspace.\n\n' ...
         'Looked for: %s'], strjoin(wanted(:,1)', ', '));
end

[~, stem, ext] = fileparts(name);
if isempty(ext); ext = '.mat'; end
file = [stem ext];
if isfile(file)
    error('save_recording:exists', ...
        ['%s already exists, and overwriting a recording you cannot retake\n' ...
         'without going back to the rig is not something this will do quietly.\n' ...
         'Choose another name, or delete that one first.'], file);
end

save(file, '-struct', 'vars');
n = numel(vars.(   'outputTime'));
fprintf('Saved %s: %d samples over %.1f s, from %s\n', ...
    file, n, vars.outputTime(end) - vars.outputTime(1), strjoin(found, ', '));
end
