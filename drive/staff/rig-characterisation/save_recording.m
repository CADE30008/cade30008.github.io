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

% A record that does not start near zero is a later segment of a run that
% began earlier. Stopping a QUARC model does not unload it, so the clock keeps
% going: start it again and the scopes carry on from where they were, and the
% workspace holds only this segment. Anything you did in an earlier one, a
% step included, is not in the file.
%
% Worth catching here rather than at a fit. Here you are still at the rig.
t0 = vars.outputTime(1);
dt = median(diff(vars.outputTime));
if t0 > 5 * dt
    fprintf(2, ['\nWARNING: this record starts at %.2f s, not 0.\n\n' ...
                'It is a later part of a run that began earlier, because the\n' ...
                'model was still loaded and its clock kept going. Whatever you\n' ...
                'did before %.2f s, including any step, is not in this file.\n\n' ...
                'Unload the model (QUARC > Unload), start it again so the clock\n' ...
                'resets, and take the recording in one go.\n\n'], t0, t0);
end

save(file, '-struct', 'vars');
n = numel(vars.outputTime);
fprintf('Saved %s: %d samples, %.2f to %.2f s, from %s\n', ...
    file, n, vars.outputTime(1), vars.outputTime(end), strjoin(found, ', '));
end
