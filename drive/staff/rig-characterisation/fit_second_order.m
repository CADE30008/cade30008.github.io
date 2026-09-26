function fit = fit_second_order(varargin)
%FIT_SECOND_ORDER  Fit K, omega_n and zeta to a measured elevation step.
%
%   fit = fit_second_order('rig-data/step-2V.csv')
%   fit = fit_second_order(t, u, y)                 vectors, degrees and volts
%   fit = fit_second_order(..., 'Plot', false)
%
% The model is the one the laboratory has always fitted to this rig:
%
%     G(s) = K * wn^2 / (s^2 + 2*zeta*wn*s + wn^2)       degrees per volt
%
% a stable, lightly damped second order. The arm sits at a trim elevation set
% by the motor voltage, and a disturbance leaves it swinging slowly about that
% trim before settling back.
%
% Three numbers, three measurements, each one a thing you can do by hand with a
% ruler on a plot:
%
%   K      where it settles, divided by the step that took it there
%   wn     the period of the swinging, corrected for damping
%   zeta   how much smaller each swing is than the one before
%
% `tfest` does all three in one line and is the right tool once you trust the
% answer. Reach the floor first: a fit you can argue with beats one that
% arrived from a function.
%
% Returns a struct with K, wn, zeta, the damped frequency, the period, the trim
% it settled at, and how well the model reproduces the data.

% ---- arguments, either a file or three vectors --------------------------
if nargin >= 3 && isnumeric(varargin{1})
    [t, u, y] = deal(varargin{1}(:), varargin{2}(:), varargin{3}(:));
    rest = varargin(4:end);
    label = 'vectors';
else
    file = varargin{1};
    rest = varargin(2:end);
    [t, u, y] = readRecording(file);
    label = file;
end
p = inputParser;
p.addParameter('Plot', true, @(x) islogical(x) || isnumeric(x));
p.parse(rest{:});
doPlot = logical(p.Results.Plot);

% ---- the step -----------------------------------------------------------
moved = find(abs(diff(u)) > 1e-6);
if isempty(moved)
    error('fit_second_order:noStep', 'The input never changes in %s.', label);
end
i0 = moved(1) + 1;
% The trim it started from, taken from the beginning of the record where the
% encoder was zeroed. Averaging the whole pre-step stretch is tempting and
% wrong: if the arm was already swinging, and it usually is, the mean of a
% partial cycle is wherever that cycle happened to stop. This is also what a
% student reads off the plot, which matters more than a cleverer estimator.
dt = median(diff(t));
head = max(1, round(0.5 / dt));
before = mean(y(1 : min(head, max(i0 - 1, 1))));
preSwing = max(y(1 : max(i0 - 1, 1))) - min(y(1 : max(i0 - 1, 1)));
dV = mean(u(min(i0 + 5, numel(u)) : end)) - mean(u(1 : max(i0 - 1, 1)));
if abs(dV) < 1e-6
    error('fit_second_order:noDrive', 'The step is %.3g V, which is no drive at all.', dV);
end

tt = t(i0:end) - t(i0);
yy = y(i0:end);

% ---- K, from where it ends up ------------------------------------------
tail = yy(max(1, end - round(0.1 * numel(yy))) : end);
settled = mean(tail);
K = (settled - before) / dV;

% ---- wn and zeta, from the swinging ------------------------------------
osc = yy - settled;
minSep = max(3, round(0.05 * numel(tt)));
pk = localPeaks(osc, minSep, 0.02 * max(abs(osc)));
fit = struct('K', K, 'wn', NaN, 'zeta', NaN, 'wd', NaN, 'period', NaN, ...
             'trim_deg', settled, 'step_V', dV, 'n_peaks', numel(pk), ...
             'fit_percent', NaN, 'source', label);

if numel(pk) < 2
    warning('fit_second_order:noOscillation', ...
        ['Fewer than two peaks in %s, so the frequency and damping cannot be ' ...
         'read.\nEither the step was too small to excite it, or the arm is ' ...
         'trimmed somewhere with no oscillation in it.'], label);
else
    P = mean(diff(tt(pk)));
    wd = 2 * pi / P;

    % Damping, from peaks that are actually signal. The encoder quantises at a
    % few tenths of a degree, and once the swing is down to that the "peaks"
    % are noise: including them drags the damping towards zero, because noise
    % does not decay.
    a = abs(osc(pk));
    keep = a > 0.10 * a(1);
    if nnz(keep) >= 2
        a = a(keep); pk = pk(keep);
    end
    n = numel(a) - 1;
    delta = log(a(1) / a(end)) / n;                 % log decrement per cycle
    zeta = delta / sqrt(4 * pi^2 + delta^2);
    fit.wd = wd; fit.period = P; fit.zeta = zeta;
    fit.wn = wd / sqrt(1 - zeta^2);

    % How much of the measured movement the fitted model actually reproduces.
    sys = tf(K * fit.wn^2, [1, 2 * zeta * fit.wn, fit.wn^2]);
    yhat = before + lsim(sys, u(i0:end) - mean(u(1:max(i0-1,1))), tt);
    fit.fit_percent = 100 * (1 - norm(yy - yhat) / norm(yy - mean(yy)));
end

fprintf('\n%s\n', label);
fprintf('  step %+.2f V, from %+.2f to %+.2f deg  ->  K = %.3f deg/V\n', ...
    dV, before, settled, K);
if preSwing > 0.5
    fprintf(2, ['  NOTE: the arm was already swinging %.1f deg before the step, so\n' ...
                '  the starting trim is uncertain and K with it. Let it settle first.\n'], ...
            preSwing);
end
if ~isnan(fit.wn)
    fprintf('  %d peaks, period %.2f s  ->  wd = %.3f, zeta = %.3f, wn = %.3f rad/s\n', ...
        numel(pk), fit.period, fit.wd, fit.zeta, fit.wn);
    fprintf('  the fitted model reproduces %.0f%% of the movement\n', fit.fit_percent);
end

if doPlot && ~isnan(fit.wn)
    figure; plot(tt, yy, 'LineWidth', 1.3); hold on
    plot(tt, yhat, '--', 'LineWidth', 1.4);
    plot(tt(pk), yy(pk), 'o', MarkerSize = 5); hold off
    grid on; xlabel('Time since step (s)'); ylabel('Elevation (deg)');
    legend('measured', sprintf('K=%.2f, \\omega_n=%.2f, \\zeta=%.3f', ...
        K, fit.wn, fit.zeta), 'peaks used', Location = 'southeast');
    title(sprintf('%s: second-order fit', label), Interpreter = 'none');
end
end


function idx = localPeaks(x, minSep, minHeight)
%LOCALPEAKS  Peak indices, without needing Signal Processing Toolbox.
%
% findpeaks would do this in one line, but it is not in base MATLAB and these
% files have to run in MATLAB Online for students who have whatever their
% licence gives them. Highest first, then anything too close to an accepted
% peak is dropped, which is what MinPeakDistance does.
x = x(:);
rising  = [false; x(2:end-1) > x(1:end-2) & x(2:end-1) >= x(3:end); false];
cand = find(rising & x > minHeight);
if isempty(cand); idx = []; return; end
[~, order] = sort(x(cand), 'descend');
cand = cand(order);
idx = [];
for c = cand'
    if all(abs(idx - c) >= minSep); idx(end+1) = c; end %#ok<AGROW>
end
idx = sort(idx);
end


function [t, u, y] = readRecording(file)
%READRECORDING  What heli_log_session writes, in either format.
if ~isfile(file)
    error('fit_second_order:noFile', 'No such recording:\n    %s', file);
end
[~, ~, ext] = fileparts(file);
if strcmpi(ext, '.mat')
    d = load(file);
    if all(isfield(d, {'time_s', 'input_V', 'elevation_deg'}))
        t = d.time_s(:); u = d.input_V(:); y = d.elevation_deg(:);
    elseif all(isfield(d, {'inputTime', 'input', 'outputTime', 'output'}))
        % The laboratory's own s_save.m layout.
        t = d.outputTime(:); y = d.output(:);
        u = interp1(d.inputTime(:), d.input(:), t, 'previous', 'extrap');
    else
        error('fit_second_order:badMat', ...
            'Unrecognised variables in %s: %s', file, strjoin(fieldnames(d)', ', '));
    end
else
    tbl = readtable(file);
    low = lower(tbl.Properties.VariableNames);
    need = {'time_s', 'input_v', 'elevation_deg'};
    if ~all(ismember(need, low))
        error('fit_second_order:badCsv', ...
            'Expected time_s, input_V, elevation_deg in %s. Found: %s', ...
            file, strjoin(tbl.Properties.VariableNames, ', '));
    end
    pick = @(w) tbl{:, find(strcmp(low, w), 1)};
    t = pick('time_s'); u = pick('input_v'); y = pick('elevation_deg');
end
end

% tracking: status=draft version=0
