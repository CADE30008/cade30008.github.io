%[text] # The case: a pitch model, and a flight-test record that disagrees with it
%[text] You have been handed a pitch model for a small fixed-wing aircraft, derived from its geometry and its aerodynamic data. You have also been handed two flight-test records. Your job is not to decide whether the model is right. It is to say **what it is good for**, in numbers somebody else can act on, and then to write the requirements a pitch controller has to meet inside that.
%[text] ## How to use this
%[text] **Run one section at a time**, with *Run Section*, not *Run All*. Where there are sliders, drag them.
%[text] The flight-test records are **synthetic**: generated from an aircraft that is deliberately not the handed-over model, by `models/L02_requirements_models.py` in the course repository. Read that file *after* you have done the work here, not before.
%[text] ## The test card
%[text] Each record is 60 s of elevator, pitch rate and pitch attitude, logged at 50 Hz. The elevator does two things:
%[text] - a **3-2-1-1**, four held segments of 3, 2, 1 and 1 seconds, alternating in sign. It puts energy over about a decade of frequency around the fast pitching motion. \
%[text] - then a **pulse held for three seconds and released**, which is how you excite a slow mode. \
%[text] The two records fly the same card at two sizes: 2 degrees of elevator, and 8.
clear; close all

data = L02_load_flight_test();
small = data.small;
large = data.large;

% Which record the sections below work on. Change it to `large` and run the
% whole thing again: the example sheet asks you to.
rec = small;
amp = max(abs(rec.elevator));

% The handed-over model, elevator (deg) to pitch rate (deg/s) and to attitude
% (deg). Pitch rate lags the elevator with a 0.5 s time constant and a gain of
% 2, the servo lags by 0.1 s, and attitude is the integral of pitch rate.
s = tf('s');
Gq = 40/((s + 2)*(s + 10));
Gtheta = 40/(s*(s + 2)*(s + 10));

figure
subplot(2, 1, 1)
plot(rec.t, rec.elevator, 'LineWidth', 1.2); grid on
ylabel('Elevator (deg)'); title(sprintf('The %g° test card', amp))
subplot(2, 1, 2)
plot(rec.t, rec.q, 'LineWidth', 1); grid on
xlabel('Time (s)'); ylabel('Pitch rate (deg/s)')
%%
%[text] ## Overlay, then look at what is left
%[text] Simulate the handed-over model with the elevator that was actually flown, and subtract. The number underneath is the residual's rms as a percentage of the pitch rate **the model says** the input will produce, which is its steady gain times the input amplitude. Normalise by the aircraft's own gain instead and you are dividing by the thing you are trying to find out.
%[text] Two windows matter and they say different things. The **3-2-1-1**, up to 10 s, tests the fast motion. **After the release**, from 24 s, tests what the aircraft does when nothing is driving it.
% 'foh' is named rather than left to lsim's own choice, because it is what the
% script that generated the records used. Simulate the model one way and the
% aircraft another and the difference between the two integrators appears in
% the residual, where you would read it as the model being wrong.
qm = lsim(Gq, rec.elevator, rec.t, [], 'foh');
resid = rec.q - qm;
span = dcgain(Gq)*amp;

figure
subplot(3, 1, [1 2])
plot(rec.t, rec.q, 'k-', rec.t, qm, 'r--', 'LineWidth', 1.1); grid on
ylabel('Pitch rate (deg/s)'); legend('flight test', 'handed-over model')
title(sprintf('The %g° record against the handed-over model', amp))
subplot(3, 1, 3)
plot(rec.t, resid, 'LineWidth', 1); grid on
xlabel('Time (s)'); ylabel('Residual (deg/s)')

fast = rec.t <= 10;
slow = rec.t >= 24;
fprintf('Residual, as a percentage of the %.2f deg/s the model predicts:\n', span);
fprintf('  over the 3-2-1-1   %4.1f%%\n', 100*rms(resid(fast))/span);
fprintf('  after the release  %4.1f%%   peak %.2f deg/s\n', ...
    100*rms(resid(slow))/span, max(abs(resid(slow))));
%[text] Neither number on its own tells you anything. The residual's **shape** does, and the next two sections take the two windows in turn.
%%
%[text] ## After the release: a mode the model does not have
%[text] From 24 s nothing is driving the aircraft, so the model predicts nothing. The record does not agree. Measure what it is doing.
slow = rec.t >= 24;
r = resid(slow) - mean(resid(slow));
ts = rec.t(slow);

% Smooth before counting crossings. The gyro noise crosses zero hundreds of
% times a minute and has nothing to do with the aircraft.
rs = L02_zero_phase(ts, r, 1.0);
cross = ts(find(rs(1:end-1) < 0 & rs(2:end) >= 0));

figure
plot(ts, r, '-', ts, rs, '-', 'LineWidth', 1.2); grid on
xlabel('Time (s)'); ylabel('Residual (deg/s)')
legend('residual', 'below 1 rad/s', 'Location', 'southeast')
title('What is left after the elevator is released')

fprintf('\nUpward zero crossings at: %s\n', sprintf('%.1f ', cross));
if numel(cross) > 1
    T = mean(diff(cross));
    fprintf('Period about %.1f s, so %.2f rad/s, amplitude about %.2f deg/s\n', ...
        T, 2*pi/T, max(abs(rs)));
end
fprintf('The rate gyro contributes about 0.04 deg/s rms, so this is not noise.\n');
%[text] A slow, lightly damped oscillation in pitch rate, with the controls fixed. You have met it in the flight dynamics half of this unit, and the handed-over model has no such mode: it has two real poles and an integrator, so it cannot oscillate at all.
%[text] **A residual with a frequency in it is a missing mode.** That is the most useful thing a residual ever tells you, and it is invisible in any single fit percentage.
%%
%[text] ## Over the 3-2-1-1: wrong above a frequency, not wrong everywhere
%[text] The residual during the fast manoeuvre is larger, and it is not a missing mode: it is the model's shape. Find out *where* in frequency it goes wrong by throwing away everything above a cut-off and comparing what is left.
%[text] Drag the cut-off down from 10 rad/s and watch the residual fall. The frequency where it stops falling is the edge of the band you may design in.
cutoff = 2.0 %[control:slider:wc02]{"position":[10,13]}

qf  = L02_zero_phase(rec.t, rec.q, cutoff);
qmf = L02_zero_phase(rec.t, qm,    cutoff);
fast = rec.t <= 10;

figure
plot(rec.t(fast), qf(fast), 'k-', rec.t(fast), qmf(fast), 'r--', 'LineWidth', 1.3)
grid on; xlabel('Time (s)'); ylabel('Pitch rate below the cut-off (deg/s)')
legend('flight test', 'handed-over model', 'Location', 'southeast')
title(sprintf('Everything below %.1f rad/s', cutoff))

fprintf('\nBelow %.1f rad/s the residual over the 3-2-1-1 is %.1f%%\n', ...
    cutoff, 100*rms(qf(fast) - qmf(fast))/span);
%[text] The filter is a second-order Butterworth run forwards and then backwards, so it delays nothing. Delaying one trace and not the other would show up as a residual and you would blame the aircraft for it.
%%
%[text] ## How hard you push it changes the gain
%[text] A linear model has one gain. Take the steady pitch rate during the first, longest segment of the 3-2-1-1 in each record, and divide by the elevator that produced it.
for rec = {small, large}
    d = rec{1};
    steady = d.t >= 4 & d.t <= 5;
    amp = max(abs(d.elevator));
    fprintf('%4.1f deg of elevator: %.2f deg/s, so %.3f (deg/s)/deg\n', ...
        amp, mean(d.q(steady)), mean(d.q(steady))/amp);
end
fprintf('The model says %.3f (deg/s)/deg, whatever the input.\n', dcgain(Gq));
%[text] The bigger input gets less out of each degree of elevator. A control surface at a large deflection is less effective than the same surface at a small one, which no linear model can represent and every aircraft does.
%[text] So the model's claim has an amplitude on it as well as a frequency.
%%
%[text] ## Write the bound down
%[text] Three lines, and they are the deliverable. Fill in your own numbers from the sections above.
%[text] - **Frequencies.** Usable from about the slow mode's frequency up to the cut-off where the residual stopped falling. Below the slow mode the model misses a whole oscillation; above the cut-off it has the wrong shape. \
%[text] - **Amplitude.** Up to the elevator deflection at which the measured gain is still within your tolerance of the model's. \
%[text] - **How far out, inside that.** The band-limited residual percentage. \
%[text] A model with those three attached can be designed against by somebody who was not in the room. Without them it is a transfer function and a hope.
%%
%[text] ## Now the requirement, and whether you are allowed to ask for it
%[text] A time-domain requirement is also a statement about frequency, whether or not it is written that way. The overshoot fixes the damping ratio, the settling time then fixes the natural frequency, and that frequency is where the closed loop will be working.
%[text] Drag the settling time. The overshoot is fixed at 10% here; change it in the code if you want to see what it costs.
settle = 3.0 %[control:slider:ts02]{"position":[10,13]}
overshootPct = 10;

zeta = -log(overshootPct/100) / sqrt(pi^2 + log(overshootPct/100)^2);
wn = 4/(zeta*settle);                       % 2% band
T = tf(wn^2, [1, 2*zeta*wn, wn^2]);
[~, PM, ~, wgc] = margin(T/(1 - T));        % the loop gain behind that closed loop

fprintf('\nSettle to 2%% in %.1f s with %d%% overshoot:\n', settle, overshootPct);
fprintf('  zeta %.3f, so wn %.2f rad/s\n', zeta, wn);
fprintf('  as a loop gain: crossover %.2f rad/s, phase margin %.1f deg\n', wgc, PM);
%[text] Put that $\\omega_n$ beside the band you just wrote down. Inside it, you have a requirement you can design to on a model you can defend. Outside it, you have asked for something the evidence does not support, and there are two honest responses: relax the requirement, or go and fly more test points.
%[text] What you may not do is design there anyway and report the simulation.
%[text] The crossover and the phase margin are the same requirement in the form the design work wants it in. They are in the handout; you do not need them today.

function data = L02_load_flight_test()
%L02_LOAD_FLIGHT_TEST  The two records, from here or from the lecture's data folder.
here = fileparts(mfilename('fullpath'));
for c = {'uav-doublets.mat', ...
         fullfile(here, '..', '..', 'L02-requirements-and-models', 'data', ...
                  'uav-doublets.mat')}
    if isfile(c{1})
        data = load(c{1});
        for f = {'small', 'large'}
            d = data.(f{1});
            data.(f{1}) = struct('t', d.t(:), 'elevator', d.elevator(:), ...
                                 'q', d.q(:), 'theta', d.theta(:));
        end
        return
    end
end
error(['uav-doublets.mat is not in this folder. Download it from the ' ...
       'lecture page and put it beside this file.']);
end


function y = L02_zero_phase(t, x, wc)
%L02_ZERO_PHASE  Second-order Butterworth, run forwards then backwards.
F = tf(wc^2, [1, sqrt(2)*wc, wc^2]);
y = flipud(lsim(F, flipud(lsim(F, x, t, [], 'foh')), t, [], 'foh'));
end

%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline"}
%---
%[control:slider:wc02]
%   data: {"defaultValue":2,"label":"cut-off (rad/s)","max":10,"min":0.3,"run":"Section","runOn":"ValueChanging","step":0.1}
%---
%[control:slider:ts02]
%   data: {"defaultValue":3,"label":"settling time (s)","max":6,"min":1,"run":"Section","runOn":"ValueChanging","step":0.1}
%---
