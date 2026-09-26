%% Fit every recording you took, and compare them
% One fit tells you what the rig did once. Several fits tell you how well you
% know the rig, which is the number you actually need.
%
% Put your .mat files from the laboratory in this folder, then run this.

clear; close all

files = dir('*.mat');
files = files(~startsWith({files.name}, 'my_model'));
if isempty(files)
    error(['No .mat recordings in this folder.\n' ...
           'Copy the files you saved with s_save into here first.']);
end
fprintf('Found %d recording(s).\n', numel(files));

%% Fit each one

fits = struct('file', {}, 'K', {}, 'wn', {}, 'zeta', {}, 'trim', {});
for i = 1:numel(files)
    try
        f = fit_second_order(files(i).name, 'Plot', false);
    catch e
        fprintf(2, '  skipped %s: %s\n', files(i).name, e.message);
        continue
    end
    if isnan(f.wn)
        fprintf(2, '  skipped %s: no oscillation to read\n', files(i).name);
        continue
    end
    fits(end+1) = struct('file', files(i).name, 'K', f.K, 'wn', f.wn, ...
                         'zeta', f.zeta, 'trim', f.trim_deg); %#ok<SAGROW>
end

if numel(fits) < 1
    error('Nothing fitted. Look at the messages above.');
end

%% How much do they disagree?

fprintf('\n%-28s %8s %8s %8s %8s\n', 'file', 'K', 'wn', 'zeta', 'trim');
for i = 1:numel(fits)
    fprintf('%-28s %8.3f %8.3f %8.4f %8.2f\n', ...
        fits(i).file, fits(i).K, fits(i).wn, fits(i).zeta, fits(i).trim);
end

spread = @(v) (max(v) - min(v)) / mean(v) * 100;
if numel(fits) > 1
    fprintf('\nspread across your recordings:\n');
    fprintf('  K     %.1f%%\n', spread([fits.K]));
    fprintf('  wn    %.1f%%\n', spread([fits.wn]));
    fprintf('  zeta  %.1f%%\n', spread([fits.zeta]));
end

%%
% Those percentages are the honest answer to "how well do you know this
% machine?", and they belong in your report. A controller designed against the
% mean of these fits has to survive anywhere in that range, because the rig on
% the day will not be at the mean.
%
% Expect the damping ratio to be the worst of the three. It depends on peak
% heights, and which peaks you keep changes it.

%% Does the trim matter?
% If you recorded at different trims, plot the natural frequency against them.
% Gravity stiffness on the arm goes as sin(elevation), so there is a real
% question about whether one model covers the whole range.

if numel(fits) > 2 && spread([fits.trim]) > 20
    figure
    plot([fits.trim], [fits.wn], 'o', 'MarkerSize', 8, 'LineWidth', 1.5);
    grid on
    xlabel('Trim elevation (deg)'); ylabel('\omega_n (rad/s)')
    title('Does the natural frequency move with the trim?')
    fprintf('\nYou have recordings at different trims. If wn moves with trim,\n');
    fprintf('every fit is local to where it was taken.\n');
else
    fprintf('\nAll at much the same trim, so this cannot answer the trim question.\n');
    fprintf('Worth taking a few at different elevations next time you are in.\n');
end

%% Take the model forward

K = mean([fits.K]); wn = mean([fits.wn]); zeta = mean([fits.zeta]);
save('my_model.mat', 'K', 'wn', 'zeta');
fprintf('\nSaved the mean: K = %.3f, wn = %.3f, zeta = %.4f\n', K, wn, zeta);
fprintf('Design against this, then check your design still works at the\n');
fprintf('extremes of the spread above.\n');

% tracking: status=draft version=0 assisted=true
