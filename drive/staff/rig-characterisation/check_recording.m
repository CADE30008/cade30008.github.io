function check_recording(file)
%CHECK_RECORDING  Say what is wrong with a recording, before you fit to it.
%
%   check_recording('level-datum.mat')
%   check_recording               the newest .mat here
%
% Run this when a fit refuses, or before you leave the laboratory. It reads
% what is in the file and reports the things that stop a fit working, in the
% order they usually go wrong.

if nargin < 1 || isempty(file)
    d = dir('*.mat');
    d = d(~startsWith({d.name}, {'.', 'my_model', 'rig_calibration'}));
    if isempty(d); error('check_recording:none', 'No recordings in this folder.'); end
    [~, i] = max([d.datenum]); file = d(i).name;
    fprintf('Newest recording: %s\n', file);
end

d = load(file);
fprintf('\n%s\n%s\n', file, repmat('-', 1, numel(file)));

need = {'inputTime', 'input', 'outputTime', 'output'};
missing = need(~isfield(d, need));
if ~isempty(missing)
    fprintf(2, 'Missing: %s\n', strjoin(missing, ', '));
    fprintf(2, 'Was this saved with save_recording?\n');
    return
end

u = d.input(:); t = d.inputTime(:);
y = d.output(:); ty = d.outputTime(:);
dt = median(diff(ty));
fprintf('  %d samples of input, %d of output\n', numel(u), numel(y));
fprintf('  runs %.2f to %.2f s  (%.1f s at %.0f Hz)\n', ty(1), ty(end), ty(end)-ty(1), 1/dt);

% 1. Did the run start at zero time, or has the front been thrown away?
if ty(1) > 2*dt
    fprintf(2, '\n  The record starts at %.2f s, not 0.\n', ty(1));
    fprintf(2, ['  This is a later part of a run that began earlier. Stopping a\n' ...
                '  QUARC model does not unload it: it stays on the rig with its\n' ...
                '  clock going, so starting again carries on from where it was,\n' ...
                '  and the scopes hand over only this segment.\n\n' ...
                '  Anything you did before %.2f s is not in this file.\n\n' ...
                '  QUARC > Unload, start again so the clock resets, and take the\n' ...
                '  recording in one go. Run check_scopes if you want to rule out\n' ...
                '  the scopes dropping data as well.\n'], ty(1));
end

% 2. Is there a step in there at all?
lo = min(u); hi = max(u);
fprintf('\n  input goes from %.3f to %.3f', lo, hi);
if hi - lo < 1e-6
    fprintf(2, '\n\n  The input never changes: it is %.3f for the whole run.\n', lo);
    fprintf(2, ['\n  Three ways that happens:\n' ...
                '    1. It was already at %.3f when the model started. Start the\n' ...
                '       run first, let it settle, and change it while recording.\n' ...
                '    2. The change was made before logging began, or after the\n' ...
                '       run had finished.\n' ...
                '    3. The step was in an earlier run segment, if the record\n' ...
                '       does not start at 0 above.\n'], lo);
    return
end
k = find(abs(diff(u)) > 1e-6, 1);
fprintf(', stepping at %.2f s\n', t(k+1));

% 3. Enough of the run before and after to be usable?
before = t(k+1) - t(1);
after  = t(end) - t(k+1);
fprintf('  %.1f s before the step, %.1f s after\n', before, after);
if before < 1
    fprintf(2, '  Under a second before the step. The starting trim is a guess.\n');
end
if after < 20
    fprintf(2, '  Under 20 s after it. That is not enough swings to read damping.\n');
end

% 4. Was it steady before the step?
pre = y(ty < t(k+1));
if numel(pre) > 10
    swing = max(pre) - min(pre);
    fprintf('  moved %.2f deg before the step', swing);
    if swing > 0.5
        fprintf(2, '  <- still swinging. Let it settle a full minute.\n');
    else
        fprintf(' (settled)\n');
    end
end

% 5. Did it do anything afterwards?
post = y(ty >= t(k+1));
fprintf('  moved %.2f deg after it\n', max(post) - min(post));
if max(post) - min(post) < 1
    fprintf(2, '  Barely moved. Was the amplifier on?\n');
end
fprintf('\n');
end

% tracking: status=draft version=0
