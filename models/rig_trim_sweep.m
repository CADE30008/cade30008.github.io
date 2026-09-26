function results = rig_trim_sweep(files, opts)
%RIG_TRIM_SWEEP  Does the natural frequency depend on where the arm is trimmed?
%
%   rig_trim_sweep                       every trim-*.csv in models/rig-data
%   rig_trim_sweep("rig-data/*.csv")
%   rig_trim_sweep(["a.csv" "b.csv" "c.csv"])
%
% This analyses recordings. **It does not drive the rig**, deliberately: see
% "Taking the recordings" below. Fit each run, plot omega_n against the trim it
% settled at, and say which of the two models the data looks like.
%
% The question
% ------------
% Two models of the elevation axis disagree and one dataset cannot separate
% them. Quanser's own linearisation, taken about level, is a double integrator:
% no restoring term, no natural frequency at all. The laboratory's fit of the
% measured rig is a stable second order with omega_n near 1 rad/s. Both are
% defensible, because gravity stiffness on an arm goes as sin(elevation): zero
% at level, growing away from it.
%
%     omega_n constant across trims   the plant is linear over the working
%                                     range, and one fitted model serves it all
%
%     omega_n rising, as              the stiffness is geometric, every fit is
%     sqrt(sin(elevation))            local to its trim, and a controller
%                                     designed at one trim flies at another
%
% It decides something real: whether week 1 can hand students one model, and
% whether the gain envelope means what it says away from the trim it was set at.
%
% Part of it is already answered. In the laboratory's own recording the arm
% swings with a period of 5.85 s about the level datum and 6.02 s at +7 deg:
% the same frequency, within 3%. The geometric story in its strong form needs
% the period at level to grow without limit, so that form is out. Two trims
% seven degrees apart do not show omega_n is constant across the range, which
% is what this function is still for. Take the runs over 1 V to 3 V.
%
% Taking the recordings
% ---------------------
% By hand, at the rig, because that part cannot be tested anywhere else and
% untested code driving hardware in front of a class is a bad trade. Four or
% five runs, ten minutes:
%
%   1. Open the laboratory's `part1_identify.slx` and connect to the hardware as usual.
%   2. Set **Elevation Input** to your first voltage. Let the arm settle: give
%      it a full minute, because at zeta = 0.06 a disturbance rings for about
%      that long, and a swing left over from the last run lands in this one's
%      fit. The fitter warns you when that happens.
%   3. Nudge it: change Elevation Input by about +0.5 V, and leave it.
%   4. Record at least 40 s of the swing that follows.
%   5. Save with `s_save`, then copy the .mat into models/rig-data as
%      `trim-<volts>V-<date>.mat`.
%   6. Repeat at 1.0, 1.5, 2.0, 2.5, 3.0 V or thereabouts.
%
% Keep the runs that go wrong. A recording where the arm hit a stop is worth
% having when somebody asks why a fit moved.

arguments
    files = ""
    opts.Plot (1,1) logical = true
end

paths = resolveFiles(files);
if isempty(paths)
    error('rig_trim_sweep:noFiles', ...
        ['No recordings found. Put them in models/rig-data as trim-*.csv or\n' ...
         'trim-*.mat, or pass the paths explicitly. The procedure for taking\n' ...
         'them is in the help for this function.']);
end

results = struct('file', {}, 'trim_deg', {}, 'wn', {}, 'zeta', {}, 'K', {});
for i = 1:numel(paths)
    try
        f = fit_second_order(char(paths(i)), 'Plot', false);
    catch e
        fprintf(2, '  skipped %s: %s\n', paths(i), e.message);
        continue
    end
    if isnan(f.wn)
        fprintf(2, '  skipped %s: no oscillation to read\n', paths(i));
        continue
    end
    [~, nm, ext] = fileparts(paths(i));
    results(end+1) = struct('file', char(nm + ext), 'trim_deg', f.trim_deg, ...
        'wn', f.wn, 'zeta', f.zeta, 'K', f.K); %#ok<AGROW>
end

report(results, opts.Plot);
end


function paths = resolveFiles(files)
%RESOLVEFILES  A pattern, a list, or the default folder.
if isstring(files) && isscalar(files) && files == ""
    here = fileparts(mfilename('fullpath'));
    d = [dir(fullfile(here, 'rig-data', 'trim-*.csv'));
         dir(fullfile(here, 'rig-data', 'trim-*.mat'))];
elseif (isstring(files) || ischar(files)) && any(contains(string(files), '*'))
    d = dir(char(files));
else
    paths = string(files); return
end
paths = arrayfun(@(x) string(fullfile(x.folder, x.name)), d);
end


function report(r, doPlot)
%REPORT  The table, the plot, and the answer.
if numel(r) < 2
    fprintf(2, ['\n%d usable run(s). Two or more trims are needed to answer the\n' ...
                'question at all.\n'], numel(r));
    return
end

fprintf('\n%-30s %-12s %-11s %-8s %s\n', 'file', 'trim (deg)', 'wn (rad/s)', 'zeta', 'K');
for i = 1:numel(r)
    fprintf('%-30s %-12.2f %-11.3f %-8.3f %.2f\n', ...
        r(i).file, r(i).trim_deg, r(i).wn, r(i).zeta, r(i).K);
end

trim = [r.trim_deg]; wn = [r.wn];
spread = (max(wn) - min(wn)) / mean(wn);
fprintf('\nomega_n varies by %.0f%% over a trim range of %.1f degrees.\n', ...
    100 * spread, max(trim) - min(trim));

% How well each of the two stories fits, so the answer is not eyeballed.
flat = mean(wn);
rmsFlat = sqrt(mean((wn - flat).^2));
s = sqrt(max(sind(trim), 1e-9));
scale = (s(:) \ wn(:));                       % least squares through the origin
rmsGeom = sqrt(mean((wn - scale * s).^2));
fprintf('residual against a constant:        %.4f rad/s\n', rmsFlat);
fprintf('residual against sqrt(sin(trim)):   %.4f rad/s\n', rmsGeom);

if spread < 0.10
    fprintf(['\nUnder 10%%: it looks constant. The plant is linear over this range,\n' ...
             'one fitted model serves all of it, and the laboratory model is enough.\n']);
elseif rmsGeom < 0.6 * rmsFlat
    fprintf(['\nIt moves with trim, and sqrt(sin(trim)) fits it better than a constant\n' ...
             'does. The stiffness is geometric: every fit is local to its trim, and a\n' ...
             'controller designed at one trim is being flown at another.\n']);
else
    fprintf(['\nIt moves with trim, but not as sqrt(sin(trim)). Something else is\n' ...
             'going on. Worth more runs before drawing a conclusion.\n']);
end

if ~doPlot; return; end
figure;
plot(trim, wn, 'o', MarkerSize = 8, LineWidth = 1.5); hold on
tt = linspace(max(min(trim) - 1, 0.1), max(trim) + 1, 200);
plot(tt, scale * sqrt(sind(tt)), '--', LineWidth = 1.4);
yline(flat, ':', 'constant', LineWidth = 1.2);
hold off; grid on
xlabel('Trim elevation (deg)'); ylabel('\omega_n (rad/s)');
legend('measured', 'geometric: \propto sqrt(sin(trim))', 'linear: constant', ...
    Location = 'best');
title('Does the natural frequency depend on the trim?');
end

% tracking: status=draft version=0 assisted=true
