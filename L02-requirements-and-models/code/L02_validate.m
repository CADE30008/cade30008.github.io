%[text] # Does your model describe the rig, and for how long?
%[text] You fitted three numbers to a recording. This asks the next question: put the model and the recording on the same axes, and look at what is left over.
%[text] ## How to use this
%[text] **Run one section at a time**, with *Run Section*, not *Run All*.
%[text] - Where there are sliders, drag them. The section re-runs as you move, so the plot and the numbers under it follow the slider. \
%[text] - The recording is the laboratory's own. If you have one of your own in this folder, this picks it up instead. \
%[text] - You need a model to compare. Run **identify\_rig** first, or let this fall back to the worked example. \
clear; close all

[file, isSample] = L02_pick_recording();
rec = load(file);
t_raw = rec.outputTime(:);
y_raw = rec.output(:);
u_raw = interp1(rec.inputTime(:), double(rec.input(:)), t_raw, 'previous', 0);

% Everything below is measured from the step, so find it.
k = find(abs(diff(u_raw)) > 0.1, 1, 'first');
t = t_raw(k+1:end) - t_raw(k+1);
y = y_raw(k+1:end);
stepV = u_raw(k+1) - u_raw(k);

% The model has to be the one fitted to THIS recording, or the residual is
% mostly the difference between two machines. Your own recording goes with your
% own fit; the shipped sample goes with the shipped model, so ask for 'shared'
% and ignore any rig_plant.json you wrote from a different rig.
if isSample
    plant = heli_plant('shared');
    whose = 'the shared model, which is the one fitted to this sample';
else
    plant = heli_plant();
    whose = 'your fit, which came from this recording';
end

fprintf('Recording: %s, %.0f s at %.0f Hz, stepped %.1f V\n', ...
    file, t(end), 1/mean(diff(t)), stepV);
fprintf('Model: K = %.2f deg/V, wn = %.3f rad/s, zeta = %.3f  (%s)\n', ...
    plant.K, plant.wn, plant.zeta, whose);
%%
%[text] ## Start the model where the arm actually was
%[text] The arm in the sample recording was already swinging when the step arrived. That is a defect in the data, and the check at the end of Part 1 is there to catch it: plot every trace before you leave the room, and take it again if the arm is moving. If you are running your own recording and it starts steady, this section costs you nothing and changes nothing.
%[text] A recording like the sample can still be read, because the model's response splits into the part the step drives and the part the initial state drives, and the second is *linear in that state*, so two unknowns fall out by least squares. Treat it as a repair.
%[text] The window below is what the initial state is fitted over. Drag it and watch the rest of the record change.
fitWindow = 10 %[control:slider:win02]{"position":[13,15]}

G = tf(plant.K*plant.wn^2, [1, 2*plant.zeta*plant.wn, plant.wn^2]);
sys = ss(G);

forced = lsim(sys, stepV*ones(size(t)), t, [0; 0]);
basis = [lsim(sys, zeros(size(t)), t, [1; 0]), ...
         lsim(sys, zeros(size(t)), t, [0; 1])];
inWindow = t <= fitWindow;
x0 = basis(inWindow, :) \ (y(inWindow) - forced(inWindow));
model = forced + basis*x0;

resid = y - model;
span = plant.K * stepV;

figure
subplot(3, 1, [1 2])
plot(t, y, 'k-', t, model, 'r--', 'LineWidth', 1.2); grid on
xlim([0 60]); ylabel('Elevation (deg)')
legend('measured', 'your model', 'Location', 'southeast')
title(sprintf('Fitted over the first %g s', fitWindow))
subplot(3, 1, 3)
plot(t, resid, 'LineWidth', 1); grid on
xlim([0 60]); xlabel('Time since the step (s)'); ylabel('Residual (deg)')

fprintf('\nResidual, as a percentage of the %.2f deg the step asked for:\n', span);
for w = [10 30 60]
    in = t <= w;
    fprintf('  first %2d s: %4.1f%%   peak %.2f deg\n', ...
        w, 100*rms(resid(in))/span, max(abs(resid(in))));
end
%%
%[text] ## A residual has a shape, and the shape names the error
%[text] Read the bottom panel rather than the number above it. Three shapes, three different faults:
%[text] - **Flat and noisy.** Nothing systematic left. The model is as good as the measurement. \
%[text] - **A slow drift in one direction.** The gain is out, or the trim moved during the recording. \
%[text] - **An oscillation at the signal's own frequency, growing with time.** The *frequency* is out. The two start together, drift apart by a little each cycle, and after enough cycles they are in antiphase and the residual is as big as the signal. \
%[text] The third is what this one does, so the natural frequency is the number to doubt. That is not a failure of your arithmetic: the next section is where it comes from.
%%
%[text] ## The period is not one number
%[text] A linear model has one natural frequency, whatever the amplitude. Measure the rig's period one cycle at a time and see whether it has one.
final = mean(y(t > t(end)-5));
dev = y - final;
cross = t(find(dev(1:end-1) < 0 & dev(2:end) >= 0));
quantum = min(diff(unique(y)));

fprintf('\n cycle start   period    wd      swing\n');
for i = 1:numel(cross)-1
    in = t >= cross(i) & t < cross(i+1);
    swing = max(abs(dev(in)));
    if swing < 10*quantum        % below this the peaks are the encoder, not the arm
        break
    end
    T = cross(i+1) - cross(i);
    fprintf('   %6.2f s  %6.3f  %6.4f  %5.2f deg\n', cross(i), T, 2*pi/T, swing);
end
%[text] The period falls as the swing decays, so the frequency rises.
%[text] **Check it before you believe it.** Those periods are gaps between crossings of the final value, so they are only as good as your estimate of the final value. Peak-to-peak and trough-to-trough timings do not use it at all.
pk = L02_gaps(t, y);
tr = L02_gaps(t, -y);
fprintf('\n peak to peak     %s\n', sprintf('%6.3f', pk(1:min(5, end))));
fprintf(' trough to trough %s\n', sprintf('%6.3f', tr(1:min(5, end))));
%[text] Three ways of measuring it, one trend. So the machine really does take longer over a wide swing than over a narrow one, and a linear model cannot do that at any setting of $K$, $\\omega_n$ and $\\zeta$.
%[text] Do not read the last decimal place of the peak timings. The signal is quantised to about 0.09 degrees, so a peak has a flat top and which sample you call the peak is a choice; a different smoothing moves these by a few hundredths. The fall is in all three, which is the part that is real.
%[text] **Why** it does it is not settled in this laboratory, and you do not need it settled to act. A fit is a claim about one amplitude, and about the trim it was taken at, whichever explanation turns out to be right.
%%
%[text] ## Say what your model is good for
%[text] Write the three things a model has to carry with it, in your own words, before you design anything against it:
%[text] - **Over what time, or what frequencies.** Here, the first ten seconds. \
%[text] - **Over what amplitude, and about what trim.** Here, swings of a few degrees about the trim it was fitted at. \
%[text] - **How far out it is inside that range.** Here, the residual percentage printed above. \
%[text] A model with those three attached is a model somebody else can use. Without them it is three numbers and a hope.
%[text] The second one is the hardest to write honestly from a single recording, because one recording was taken at one trim and one step size. If you have the two extra runs from the end of Part 1, run this script on each of them and see how much of the range they let you claim.

function g = L02_gaps(t, y)
%L02_GAPS  Times between successive peaks of y, in seconds.
%
% Written out rather than called from findpeaks, because that is in the Signal
% Processing Toolbox and these files are meant to run with the Control System
% Toolbox alone.
dt = mean(diff(t));
ys = movmean(y, max(3, 2*round(0.1/dt) + 1));   % 0.2 s, odd, to centre cleanly
k = find([false; ys(2:end-1) > ys(1:end-2) & ys(2:end-1) >= ys(3:end); false]);
keep = k(1);
for i = 2:numel(k)
    if t(k(i)) - t(keep(end)) >= 4.0        % at most one peak per 4 s
        keep(end+1) = k(i);                 %#ok<AGROW>
    elseif ys(k(i)) > ys(keep(end))
        keep(end) = k(i);
    end
end
g = diff(t(keep));
end


function [file, isSample] = L02_pick_recording()
%L02_PICK_RECORDING  Your newest recording here, or the laboratory's sample.
%
% 'sample-' is in the filter and has to be. The Drive folder ships the sample
% as sample-elevation-step.mat and it sits in the same place your own
% recordings do, so without that prefix it is picked as yours: isSample comes
% back false, the shipped sample is compared against whatever rig_plant.json
% you fitted on a different machine, and the residual is a comparison between
% two rigs rather than a statement about either. Measured, that reads 34.6%
% where this page says 2.8%.
isSample = true;
d = dir('*.mat');
d = d(~startsWith({d.name}, {'.', 'my_', 'rig_', 'uav-', 'sample-'}));
if ~isempty(d)
    [~, i] = max([d.datenum]);
    file = d(i).name;
    isSample = false;
    return
end
here = fileparts(mfilename('fullpath'));
for c = {'sample-elevation-step.mat', ...
         fullfile(here, '..', '..', 'w01-design-cycle', 'data', 'elevation-step.mat')}
    if isfile(c{1})
        file = c{1};
        fprintf(2, 'No recording of your own here, so this is the sample.\n');
        return
    end
end
error(['No recordings here and no sample either. Save one at the rig with ' ...
       'save_recording, or copy the sample in from the data folder.']);
end

%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline"}
%---
%[control:slider:win02]
%   data: {"defaultValue":10,"label":"fit window (s)","max":60,"min":2,"run":"Section","runOn":"ValueChanging","step":1}
%---
