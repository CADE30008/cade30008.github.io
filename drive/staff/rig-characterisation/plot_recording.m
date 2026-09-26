function plot_recording(file)
%PLOT_RECORDING  Look at a recording before you fit anything to it.
%
%   plot_recording('trim-2V.mat')
%   plot_recording            the newest .mat here
%
% A model fitted to a recording nobody looked at is a model of whatever went
% wrong during the recording. Three things to check are in the laboratory
% notes for Part 1; this is what you check them on.

if nargin < 1 || isempty(file)
    d = dir('*.mat');
    d = d(~startsWith({d.name}, {'.', 'my_model'}));
    if isempty(d); error('plot_recording:none', 'No .mat recordings in this folder.'); end
    [~, i] = max([d.datenum]);
    file = d(i).name;
    fprintf('Showing the newest: %s\n', file);
end

d = load(file);
need = {'inputTime', 'input', 'outputTime', 'output'};
missing = need(~isfield(d, need));
if ~isempty(missing)
    error('plot_recording:badFile', ...
        '%s has no %s. Was it saved with save_recording?', file, strjoin(missing, ', '));
end

figure
yyaxis left
plot(d.outputTime, d.output, 'LineWidth', 1.3)
ylabel('Elevation (deg)')
yyaxis right
plot(d.inputTime, d.input, 'LineWidth', 1.2)
ylabel('Input (V)')
xlabel('Time (s)'); grid on
title(file, 'Interpreter', 'none')

if isfield(d, 'pitch') && isfield(d, 'travel')
    figure
    plot(d.pitchTime, d.pitch, d.travelTime, d.travel, 'LineWidth', 1.2)
    grid on; xlabel('Time (s)'); ylabel('Angle (deg)')
    legend('pitch', 'travel', 'Location', 'best')
    title([file ': the other two axes'], 'Interpreter', 'none')
end
end

% tracking: status=draft version=0 assisted=true
