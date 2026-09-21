%% Identify the elevation axis
% You have a recording of the rig: a step in motor voltage, and the elevation
% that followed. By the end of this script you will have a model of it, fitted
% two ways, and a view on whether to believe either.
%
% Work down the file. Run one section at a time with *Run Section*, not the
% whole thing at once, because the point is what each step shows you.

clear; close all
load('../data/elevation-step.mat')     % inputTime, input, outputTime, output

%% Look at it first
% Before any fitting. A model fitted to a recording you have not looked at is
% a model of whatever went wrong during the recording.

figure
plot(outputTime, output, 'LineWidth', 1.3); hold on
plot(inputTime, input, 'LineWidth', 1.2); hold off
grid on
xlabel('Time (s)'); ylabel('Elevation (deg)  /  Input (V)')
legend('measured elevation', 'motor voltage', 'Location', 'southeast')
title('The rig''s own step response')

%%
% Three things to read off that plot, and write down before you compute
% anything:
%
% * roughly where it starts, and where it ends up;
% * roughly how long one oscillation takes;
% * roughly how many swings before you would call it finished.

%% By hand: the gain
% The steady gain is how far it moved, divided by the step that moved it.
% Degrees per volt.

u = interp1(inputTime, input, outputTime, 'previous', 'extrap');
i0 = find(abs(diff(u)) > 1e-6, 1) + 1;          % where the step happened
dt = median(diff(outputTime));

% Where it started from. This looks like a detail and is worth 25% of your
% gain, so it is worth doing deliberately.
%
% The obvious move is to average the whole stretch before the step. Try it on
% this recording and you get -1.55 deg. But look at that stretch on the plot:
% the arm is already swinging, through 4.2 degrees, because somebody nudged it
% and it takes a minute to stop. The mean of a partial oscillation is wherever
% that oscillation happened to be cut off, and it is not the trim.
%
% The encoder was zeroed against a datum at the start of the record, so take
% the start of the record. It is also what you would read off the plot with a
% ruler, which matters more than a cleverer estimator.
head    = max(1, round(0.5 / dt));              % first half second
before  = mean(output(1 : min(head, max(i0-1, 1))));
settled = mean(output(round(0.9*numel(output)) : end));
dV      = mean(u(i0+5 : end)) - mean(u(1 : max(i0-1, 1)));

K_hand = (settled - before) / dV;
fprintf('started at %.2f deg, settled at %.2f deg, for %.2f V\n', before, settled, dV);
fprintf('  ->  K = %.2f deg/V\n', K_hand);

pre_swing = max(output(1:max(i0-1,1))) - min(output(1:max(i0-1,1)));
if pre_swing > 0.5
    fprintf(2, ['  NOTE: the arm was already swinging %.1f deg before the step.\n' ...
                '  Averaging that whole stretch instead of the tared start would\n' ...
                '  have given K = %.2f.\n'], pre_swing, ...
            (settled - mean(output(1:max(i0-1,1)))) / dV);
end

%% By hand: the frequency
% The period of the oscillation gives the *damped* natural frequency. Find the
% peaks, take the average spacing.
%
% |findpeaks| needs Signal Processing Toolbox. This does it with |islocalmax|,
% which is in base MATLAB, so the script runs wherever you are.

t   = outputTime(i0:end) - outputTime(i0);
y   = output(i0:end);
osc = y - settled;

pk  = find(islocalmax(osc, 'MinSeparation', 2, 'SamplePoints', t));
pk  = pk(abs(osc(pk)) > 0.10 * max(abs(osc)));   % ignore the encoder's noise floor

P       = mean(diff(t(pk)));
omega_d = 2*pi / P;
fprintf('%d peaks, period %.2f s  ->  omega_d = %.3f rad/s\n', numel(pk), P, omega_d);

%% By hand: the damping
% Each swing is smaller than the one before by the same factor. The log of
% that ratio, per cycle, is the *log decrement*, and the damping ratio follows.
%
% Use the early peaks. Once the swing is down to a few tenths of a degree the
% encoder's resolution takes over and the "peaks" are noise, which does not
% decay and will drag your damping towards zero.

a     = abs(osc(pk));
n     = numel(a) - 1;
delta = log(a(1) / a(end)) / n;
zeta_hand  = delta / sqrt(4*pi^2 + delta^2);
omega_hand = omega_d / sqrt(1 - zeta_hand^2);

fprintf('log decrement %.4f  ->  zeta = %.3f, omega_n = %.3f rad/s\n', ...
    delta, zeta_hand, omega_hand);

%% Does it reproduce the measurement?
% Three numbers read off a plot. Put them back through the model and overlay
% the result on the data. This is the step people skip.

G_hand = tf(K_hand * omega_hand^2, [1, 2*zeta_hand*omega_hand, omega_hand^2]);
y_hand = before + lsim(G_hand, u - mean(u(1:max(i0-1,1))), outputTime);

figure
plot(outputTime, output, 'LineWidth', 1.3); hold on
plot(outputTime, y_hand, '--', 'LineWidth', 1.4); hold off
grid on
xlabel('Time (s)'); ylabel('Elevation (deg)')
legend('measured', sprintf('by hand: K=%.2f, \\omega_n=%.2f, \\zeta=%.3f', ...
    K_hand, omega_hand, zeta_hand), 'Location', 'southeast')
title('Your fit, against the rig')

%% Now the professional version
% |tfest| fits a transfer function of whatever order you ask for, from the
% data, in one line. It uses System Identification Toolbox.
%
% Reach the floor before the ceiling. A fit you got by hand is one you can
% argue with; a fit that arrived from a function is one you can only accept.
% You now have something to check it against.

data  = iddata(output - before, u - mean(u(1:max(i0-1,1))), ...
               median(diff(outputTime)));
G_est = tfest(data, 2, 0);                 % two poles, no zeros

[wn_est, zeta_est] = damp(G_est);
K_est = dcgain(G_est);
fprintf('\n  by hand : K = %.2f, omega_n = %.3f, zeta = %.3f\n', ...
    K_hand, omega_hand, zeta_hand);
fprintf('  tfest   : K = %.2f, omega_n = %.3f, zeta = %.3f   (fit %.0f%%)\n', ...
    K_est, wn_est(1), zeta_est(1), G_est.Report.Fit.FitPercent);

%%
% They should be close. Where they differ, the question is not which function
% is better but which of your three readings moved: the steady value, the peak
% spacing, or how many peaks you kept.

figure
compare(data, G_est); grid on
title('tfest, against the rig')

%% Write your model down
% Everything after this uses these three numbers. Save them.

K = K_hand; wn = omega_hand; zeta = zeta_hand;      % or the tfest ones, if you prefer
save('my_model.mat', 'K', 'wn', 'zeta');
fprintf('\nSaved K = %.3f, wn = %.3f, zeta = %.3f to my_model.mat\n', K, wn, zeta);

%%
% *Compare with the person next to you before you move on.* You will not have
% the same numbers, and that is the exercise rather than a failure of it.
