%% Tune a controller for the model you fitted
% Three ways, in order: by feel, by design, and by function. Do them in that
% order. The point is not to arrive at gains, it is to arrive at gains you can
% defend when somebody asks why.
%
% You need |my_model.mat| from *s1_identify*.

clear; close all
load('my_model.mat')                  % K, wn, zeta
G = tf(K*wn^2, [1, 2*zeta*wn, wn^2]);

fprintf('Your model: K = %.2f deg/V, wn = %.3f rad/s, zeta = %.3f\n', K, wn, zeta);

%% What one knob does
% Proportional gain alone, swept. Watch the two things that happen and the one
% that does not.

figure
hold on
for kp = [0.5 2 10]
    step(feedback(kp*G, 1), 80)
end
hold off; grid on; legend('K_p = 0.5', 'K_p = 2', 'K_p = 10', 'Location', 'southeast')
title('Proportional gain alone')

%%
% Close a proportional loop and the characteristic polynomial is
%
% $$s^2 + 2\zeta\omega_n s + \omega_n^2(1 + KK_p)$$
%
% $K_p$ is not in the coefficient of $s$. So the real part of the poles cannot
% move: the oscillation gets faster, the damping ratio falls, and the settling
% time stays where it was. More gain buys a worse response and not one second
% of settling.
%
% It also never goes unstable, whatever you set. That matters for the next
% section.

%% Why Ziegler-Nichols has nothing to bite on here
% The tuning rule you may have met works by turning $K_p$ up until the loop
% oscillates steadily, then reading off that ultimate gain and its period.
%
% There is no such gain for this plant. The coefficient of $s$ is
% $2\zeta\omega_n$, which is positive and has no $K_p$ in it, so every
% positive $K_p$ leaves a stable loop. Check it:

kps = logspace(-2, 4, 200);
worst = arrayfun(@(g) max(real(pole(feedback(g*G, 1)))), kps);
fprintf('\nKp from %.2g to %.2g: worst pole real part is always %.4f\n', ...
    kps(1), kps(end), max(worst));
fprintf('Stable at every one of them, so there is no ultimate gain to find.\n');

%%
% The open-loop rule does not apply either: it wants an S-shaped step response
% to measure a delay and a slope from, and this one oscillates.
%
% Notice what that means. A tuning rule is fitted to a class of
% plants, and outside that class it does not degrade gracefully, it simply has
% no input. Recognising when a method does not apply is part of the method.

%% Level 1: by feel
% Open the slider tool, and get a feel for what each gain does before you
% compute anything.
%
%   tune_sliders(K, wn, zeta)
%
% Start with all three low. Raise $K_d$ until the oscillation calms. Raise
% $K_p$ until it gets there in reasonable time. Raise $K_i$ until the gap to
% the target closes. Then notice what raising each one too far costs you.

tune_sliders(K, wn, zeta);

%% Level 2: by design
% Feel does not scale and does not transfer. Decide where you want the poles
% and solve for the gains that put them there.
%
% With PID the characteristic polynomial is
%
% $$s^3 + (2\zeta\omega_n + K\omega_n^2 K_d)s^2 + (\omega_n^2 + K\omega_n^2 K_p)s + K\omega_n^2 K_i$$
%
% Ask for a dominant pair at $\zeta_c$, $\omega_c$ and a real pole at $-p$:
%
% $$(s^2 + 2\zeta_c\omega_c s + \omega_c^2)(s + p)$$
%
% Match the coefficients and the three gains fall out. That is three equations
% and three unknowns, and you can do it on paper.

zc = 0.7;     % damping you want
wc = 0.8;     % speed you want, rad/s
p  = 2.5;     % the third pole, well left of the pair

% Those three numbers are a starting point, not an answer. Try wc = 1.0 and
% watch what the check says about volts: the demand path saturates at 8.6 V
% above the trim, and asking for a faster loop is asking for more of it. The
% limit is what the rig can actually deliver, not a rule somebody invented.

a  = K * wn^2;
Kd_design = (2*zc*wc + p - 2*zeta*wn) / a;
Kp_design = (wc^2 + 2*zc*wc*p - wn^2) / a;
Ki_design = (wc^2 * p) / a;

fprintf('\nBy design: Kp = %.3f, Ki = %.3f, Kd = %.3f\n', ...
    Kp_design, Ki_design, Kd_design);

C_design = pid(Kp_design, Ki_design, Kd_design);
S = stepinfo(feedback(C_design*G, 1));
fprintf('  overshoot %.1f%%, settles in %.1f s\n', S.Overshoot, S.SettlingTime);

%% Level 3: by function
% |pidtune| chooses gains to hit a target bandwidth with a sensible margin. It
% is the tool you would actually reach for, and now you have something to check
% it against.

C_auto = pidtune(G, 'PID');
fprintf('\nBy pidtune: Kp = %.3f, Ki = %.3f, Kd = %.3f\n', ...
    C_auto.Kp, C_auto.Ki, C_auto.Kd);
S2 = stepinfo(feedback(C_auto*G, 1));
fprintf('  overshoot %.1f%%, settles in %.1f s\n', S2.Overshoot, S2.SettlingTime);

%%
% Ask it for a particular crossover and watch what happens near the plant's own
% resonance. At $\omega_c$ = 1 rad/s, which is where this plant rings, the
% tuner backs right off and hands you something that takes eight minutes.

for wc_try = [1 3 8]
    Ct = pidtune(G, 'PID', wc_try);
    St = stepinfo(feedback(Ct*G, 1));
    fprintf('  wc = %g:  Kp = %6.3f, Ki = %6.3f, Kd = %6.3f  ->  settles in %.1f s\n', ...
        wc_try, Ct.Kp, Ct.Ki, Ct.Kd, St.SettlingTime);
end

%%
% Compare the two designs.

figure
step(feedback(C_design*G, 1), 20); hold on
step(feedback(C_auto*G, 1), 20); hold off
grid on; legend('by design', 'pidtune', 'Location', 'southeast')
title('Your design against the function''s')

%% The one the function cannot know about
% Run both through the check that decides what actually flies.

fprintf('\n--- your design ---\n');
[ok_d, why_d] = heli_check_one(Kp_design, Ki_design, Kd_design);
fprintf('%s %s\n', string(ok_d), why_d);

fprintf('\n--- pidtune ---\n');
[ok_a, why_a] = heli_check_one(C_auto.Kp, C_auto.Ki, C_auto.Kd);
fprintf('%s %s\n', string(ok_a), why_a);

%%
% Read that carefully, because it is the whole session in one result.
%
% |pidtune| gives the better-damped loop: look at the damping ratio and the
% phase margin. It settles in much the same time as yours and overshoots more,
% so it is not better at everything. And it is refused outright, because it
% asks the motors for more volts than the amplifier has.
%
% The function was not wrong. It optimised for the specification it was given,
% and the amplifier was not in it. Nothing you can do inside the loop fixes a
% specification that left something out.
%
% Which of the two would you defend in a design review? That is the question
% the coursework asks, and there is more than one defensible answer.

%% Check it, then submit
% |submit_gains| runs the same checks and only then gives you a link with your
% numbers in it.

submit_gains(Kp_design, Ki_design, Kd_design, 'your name here');

% tracking: status=draft version=0
