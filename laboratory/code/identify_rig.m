%[text] # Identify the rig in front of you
%[text] One recording, taken from the ground, tells you everything the rest of the unit needs about this machine: how hard it pushes, how fast it swings, how quickly it stops, and how much of the voltage budget is spent just holding the arm up.
%[text] You do it twice. First by hand, reading three numbers off a plot, because that is the thing you should be able to do when the toolbox is not there. Then with `fit_second_order`, which is the same calculation written down once. The point of doing both is to find out whether you believe the automatic one.
%[text] ## How to use this
%[text] **Run one section at a time**, with *Run Section*, not *Run All*.
%[text] - In the laboratory: start the model with the arm **resting on the floor**, step Elevation Input, let it settle, stop the model, and save with `save_recording`. Then run this on that file. \
%[text] - Away from the rig: it picks up the sample recording that comes with these files, so you can walk through it before you ever touch the machine. \
%[text] - There are four rigs. This describes **the one you recorded**, and nothing else does. \
clear; close all

file = pick_recording();
load(file, 'inputTime', 'input', 'outputTime', 'output');
fprintf('Recording: %s\n', file);
%%
%[text] ## Look at it first
%[text] Before any fitting. A model fitted to a recording nobody looked at is a model of whatever went wrong while it was being taken.
figure
subplot(2,1,1)
plot(inputTime, input, 'LineWidth', 1.2); grid on
ylabel('Elevation Input'); title('What you asked for')
subplot(2,1,2)
plot(outputTime, output, 'LineWidth', 1.2); grid on
xlabel('Time (s)'); ylabel('Elevation (deg)'); title('What it did')
%[text] Two things to check before you go on. Does the trace start flat, or was the arm already swinging when the recording began? And does it settle by the end, or is it still moving when the record stops? Either one makes the numbers below wrong in a way no amount of arithmetic recovers.
%%
%[text] ## By hand: the gain
%[text] The steady gain is how far it moved, divided by the step that moved it. Degrees per volt.
u  = interp1(inputTime, input, outputTime, 'previous', 'extrap');
i0 = find(abs(diff(u)) > 1e-6, 1) + 1;        % where the step happened
dt = median(diff(outputTime));

before  = mean(output(1 : max(1, min(round(0.5/dt), i0-1))));   % the tared start
settled = mean(output(round(0.9*numel(output)) : end));
dV      = mean(u(i0+5 : end)) - mean(u(1 : max(i0-1, 1)));

K_hand = (settled - before) / dV;
fprintf('started at %.2f deg, settled at %.2f deg, for %.2f V\n', before, settled, dV);
fprintf('  ->  K = %.2f deg/V\n', K_hand);
%[text] **Where it started from is worth a quarter of your gain**, so it is worth doing deliberately.
%[text] The obvious move is to average the whole stretch before the step. Look at that stretch on the plot above: if the arm is already swinging, the mean of a partial oscillation is wherever the swing happened to be cut off, and it is not the trim.
%[text] The encoder is zeroed against the floor at the start of the record, so take the start of the record. It is also what you would read off the plot with a ruler, which matters more than a cleverer estimator.
swing = max(output(1:max(i0-1,1))) - min(output(1:max(i0-1,1)));
if swing > 0.5
    fprintf(2, ['  NOTE: the arm was already swinging %.1f deg before the step.\n' ...
                '  Averaging that stretch instead would have given K = %.2f.\n'], ...
            swing, (settled - mean(output(1:max(i0-1,1)))) / dV);
end
%%
%[text] ## By hand: the frequency
%[text] The spacing of the peaks gives the **damped** natural frequency. `islocalmax` is base MATLAB, so this runs wherever you are; `findpeaks` would want Signal Processing Toolbox.
t   = outputTime(i0:end) - outputTime(i0);
y   = output(i0:end);
osc = y - settled;

pk = find(islocalmax(osc, 'MinSeparation', 2, 'SamplePoints', t));
pk = pk(abs(osc(pk)) > 0.10 * max(abs(osc)));   % above the encoder's noise floor

P  = mean(diff(t(pk)));
wd = 2*pi / P;
fprintf('%d peaks, period %.2f s  ->  omega_d = %.3f rad/s\n', numel(pk), P, wd);
%%
%[text] ## By hand: the damping
%[text] Each swing is smaller than the one before by the same factor. The log of that ratio, per cycle, is the **log decrement**, and the damping ratio follows from it.
%[text] Drag the slider to choose how many peaks to use. Use the early ones. Once the swing is down to a few tenths of a degree the encoder's resolution takes over, the "peaks" are noise, and noise does not decay: keep including them and you will drag your damping towards zero. Watch that happen.
nPeaks = 4 %[control:slider:np01]{"position":[10,11]}

nUse  = min(max(2, nPeaks), numel(pk));
a     = abs(osc(pk(1:nUse)));
delta = log(a(1) / a(end)) / (nUse - 1);
zeta_hand = delta / sqrt(4*pi^2 + delta^2);
wn_hand   = wd / sqrt(1 - zeta_hand^2);

fprintf('%d of %d peaks: log decrement %.4f  ->  zeta = %.4f, wn = %.3f rad/s\n', ...
    nUse, numel(pk), delta, zeta_hand, wn_hand);

figure
plot(t, osc, 'LineWidth', 1.1); hold on
plot(t(pk(1:nUse)), osc(pk(1:nUse)), 'o', 'MarkerSize', 8, 'LineWidth', 1.5)
plot(t(pk(nUse+1:end)), osc(pk(nUse+1:end)), 'x', 'MarkerSize', 7)
hold off; grid on; xlabel('Time since the step (s)'); ylabel('Swing about the trim (deg)')
legend('measured', 'peaks you are using', 'peaks you are ignoring')
%%
%[text] ## Does it reproduce the measurement?
%[text] Three numbers read off a plot. Put them back through the model and overlay the result on the data. This is the step people skip.
G_hand = tf(K_hand * wn_hand^2, [1, 2*zeta_hand*wn_hand, wn_hand^2]);
y_hand = before + lsim(G_hand, u - mean(u(1:max(i0-1,1))), outputTime);

figure
plot(outputTime, output, 'LineWidth', 1.3); hold on
plot(outputTime, y_hand, '--', 'LineWidth', 1.4); hold off
grid on; xlabel('Time (s)'); ylabel('Elevation (deg)')
legend('measured', sprintf('by hand: K=%.2f, \\omega_n=%.2f, \\zeta=%.3f', ...
    K_hand, wn_hand, zeta_hand), 'Location', 'southeast')
title('Your fit, against the rig')
%%
%[text] ## The same thing, automatically
%[text] `fit_second_order` does what you just did: tared start, peak spacing, log decrement. **It is the same function `lab1_fit` runs over a whole folder of recordings**, so when you fit ten of them later, each one is this calculation.
%[text] It should agree with you. Where it does not, one of you is wrong and it is worth knowing which.
auto = fit_second_order(file, 'Plot', false);

fprintf('\n%-10s %8s %8s %8s\n', '', 'K', 'wn', 'zeta');
fprintf('%-10s %8.3f %8.3f %8.4f\n', 'by hand', K_hand, wn_hand, zeta_hand);
fprintf('%-10s %8.3f %8.3f %8.4f\n', 'automatic', auto.K, auto.wn, auto.zeta);
fprintf('%-10s %7.1f%% %7.1f%% %7.1f%%\n', 'apart', ...
    100*abs(K_hand-auto.K)/auto.K, 100*abs(wn_hand-auto.wn)/auto.wn, ...
    100*abs(zeta_hand-auto.zeta)/auto.zeta);
%[text] A few per cent on $K$ and $\\omega_n$ is ordinary. A large gap on $\\zeta$ usually means the two of you kept different peaks, which is the slider above, and is the honest reason damping is the least certain of the three.
%%
%[text] ## What the arm costs to hold up
%[text] The same recording gives this, and it is why there is no separate levelling step any more. At the end of the record the arm is sitting still at some elevation under a constant Elevation Input. That input is what the loop spends just holding the thing up, and whatever is left is what your controller gets to use.
elevInputSteady = mean(u(i0+5 : end));
cal = rig_calibration(elevInputSteady, settled - before);

fprintf('Holding it there takes %+.2f on Elevation Input.\n', cal.elevInputAtLevel);
fprintf('So Velev trims at %.2f V, leaving %.2f V of head-room\n', ...
    cal.vElevTrim, cal.headroom);
fprintf('before the demand path saturates at %g V.\n', cal.vElevSat);

if cal.headroom < 4
    fprintf(2, ['That is not much room. Check the counterweight: if the arm is\n' ...
                'heavy at the rotor end, the loop spends its budget holding it\n' ...
                'up. Ask a demonstrator before going on.\n']);
end
%%
%[text] ## Write this rig down
%[text] Saved beside your recordings, and **everything downstream reads it from there**: the response you simulate, the envelope your gains are checked against, and the verdict when you submit.
%[text] There are four rigs and they are not the same. Keep these files with the recordings they came from, and do not carry them to another machine.
save_rig(K_hand, wn_hand, zeta_hand, cal, file);
%[text] Now go to **lab1\_design**, or in the first session to **s2\_tune**, and design something.

function file = pick_recording()
%PICK_RECORDING  The newest recording here, or the sample if there is none.
d = dir('*.mat');
% 'sample-' too. The Drive folder ships the sample beside your own
% recordings, so without it the sample is picked as yours and the
% "No recording of your own here" notice never fires: you would be
% fitting the laboratory's recording believing it was your rig's.
d = d(~startsWith({d.name}, {'.', 'my_', 'rig_', 'sample-', 'uav-'}));
if isempty(d)
    file = 'sample-elevation-step.mat';
    if ~isfile(file)
        error(['No recordings here and no sample either. Save one at the rig ' ...
               'with save_recording, or copy the sample in from the data folder.']);
    end
    fprintf(2, 'No recording of your own here, so this is the sample.\n');
    return
end
[~, i] = max([d.datenum]);
file = d(i).name;
end

%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline"}
%---
%[control:slider:np01]
%   data: {"defaultValue":4,"label":"peaks to use","max":12,"min":2,"run":"Section","runOn":"ValueChanging","step":1}
%---
