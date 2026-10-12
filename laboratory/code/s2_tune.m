%[text] # Tune a controller for the model you fitted
%[text] Three ways, in order: by feel, by design, and by function. Do them in that order. The point is not to arrive at gains, it is to arrive at gains you can defend when somebody asks why.
%[text] ## How to use this
%[text] **Run one section at a time**, with *Run Section*, not *Run All*. Each section builds on the one above, and most of them are something to look at before you move on.
%[text] - Where there are sliders, drag them. The section re-runs as you move, so the plot and the verdict under it follow the slider. \
%[text] - Output appears underneath the code that made it. \
%[text] - Run **identify\_rig** first. It writes `rig_plant.json`, which is the model this reads. \
clear; close all

% heli_plant reads rig_plant.json if identify_rig has written one here, and
% the worked example otherwise. So this is the machine you measured, and the
% check at the bottom of this script is against the same one.
if ~isfile('rig_plant.json')
    error(['No rig_plant.json in this folder. Run identify_rig first: it ' ...
           'fits the recording and writes the model this reads.']);
end
plant = heli_plant();
K = plant.K; wn = plant.wn; zeta = plant.zeta;
G = tf(K*wn^2, [1, 2*zeta*wn, wn^2]);

fprintf('Your model: K = %.2f deg/V, wn = %.3f rad/s, zeta = %.3f\n', K, wn, zeta);
%%
%[text] ## What one knob does
%[text] Proportional gain alone, swept. Watch the two things that happen and the one that does not.
figure
hold on
for kp = [0.5 2 10]
    step(feedback(kp*G, 1), 80)
end
hold off; grid on; legend('K_p = 0.5', 'K_p = 2', 'K_p = 10', 'Location', 'southeast')
title('Proportional gain alone')
%[text] Close a proportional loop and the characteristic polynomial is
%[text] $$s^2 + 2\\zeta\\omega_n s + \\omega_n^2(1 + KK_p)$$
%[text] $K_p$ is not in the coefficient of $s$. So the real part of the poles cannot move: the oscillation gets faster, the damping ratio falls, and the settling time stays where it was. More gain buys a worse response and not one second of settling.
%[text] It also never goes unstable, whatever you set. That matters for the next section.
%%
%[text] ## Why Ziegler-Nichols has nothing to bite on here
%[text] The tuning rule you may have met works by turning $K_p$ up until the loop oscillates steadily, then reading off that ultimate gain and its period.
%[text] There is no such gain for this plant. The coefficient of $s$ is $2\\zeta\\omega_n$, which is positive and has no $K_p$ in it, so every positive $K_p$ leaves a stable loop. Check it:
kps = logspace(-2, 4, 200);
worst = arrayfun(@(g) max(real(pole(feedback(g*G, 1)))), kps);
fprintf('\nKp from %.2g to %.2g: worst pole real part is always %.4f\n', ...
    kps(1), kps(end), max(worst));
fprintf('Stable at every one of them, so there is no ultimate gain to find.\n');
%[text] The open-loop rule does not apply either: it wants an S-shaped step response to measure a delay and a slope from, and this one oscillates.
%[text] Notice what that means. A tuning rule is fitted to a class of plants, and outside that class it does not degrade gracefully, it simply has no input. Recognising when a method does not apply is part of the method.
%%
%[text] ## Level 1: by feel
%[text] Drag the three sliders and watch the response redraw. Do this before you compute anything.
%[text] Start with all three low. Raise $K_d$ until the oscillation calms. Raise $K_p$ until it gets there in reasonable time. Raise $K_i$ until the gap to the target closes. Then push each one too far and notice what it costs you.
%[text] The verdict underneath is taken against the rig's own fitted model, not against yours. It has to be: if your fit came out optimistic, gains that look fine here would be refused at submission, or worse, flown against a machine they were never checked against.
Kp = 2 %[control:slider:kp01]{"position":[6,7]}
Ki = 0.5 %[control:slider:ki01]{"position":[6,9]}
Kd = 1 %[control:slider:kd01]{"position":[6,7]}

figure
step(feedback(pid(Kp, Ki, Kd)*G, 1), 0:0.05:30)
grid on; title(sprintf('K_p = %.2f,  K_i = %.2f,  K_d = %.2f', Kp, Ki, Kd))

[ok_feel, why_feel] = heli_check_one(Kp, Ki, Kd, heli_plant('shared'));
fprintf('envelope: %s %s\n', string(ok_feel), why_feel);
%%
%[text] ## Level 2: by design
%[text] Feel does not scale and does not transfer. Decide where you want the poles and solve for the gains that put them there.
%[text] With PID the characteristic polynomial is
%[text] $$s^3 + (2\\zeta\\omega_n + K\\omega_n^2 K_d)s^2 + (\\omega_n^2 + K\\omega_n^2 K_p)s + K\\omega_n^2 K_i$$
%[text] Ask for a dominant pair at $\\zeta_c$, $\\omega_c$ and a real pole at $-p$:
%[text] $$(s^2 + 2\\zeta_c\\omega_c s + \\omega_c^2)(s + p)$$
%[text] Match the coefficients and the three gains fall out. That is three equations and three unknowns, and you can do it on paper.
%[text] These three sliders move the poles you are asking for, not the gains. Watch the gains follow, and watch the voltage the check reports: a faster $\\omega_c$ is a request for more volts, and the demand path saturates not far above the trim.
zc = 0.7 %[control:slider:zc01]{"position":[6,9]}
wc = 0.8 %[control:slider:wc01]{"position":[6,9]}
p  = 2.5 %[control:slider:p01]{"position":[6,9]}

a  = K * wn^2;
Kd_design = (2*zc*wc + p - 2*zeta*wn) / a;
Kp_design = (wc^2 + 2*zc*wc*p - wn^2) / a;
Ki_design = (wc^2 * p) / a;

fprintf('\nBy design: Kp = %.3f, Ki = %.3f, Kd = %.3f\n', ...
    Kp_design, Ki_design, Kd_design);

C_design = pid(Kp_design, Ki_design, Kd_design);
S = stepinfo(feedback(C_design*G, 1));
fprintf('  overshoot %.1f%%, settles in %.1f s\n', S.Overshoot, S.SettlingTime);
%%
%[text] ## Level 3: by function
%[text] `pidtune` chooses gains to hit a target bandwidth with a sensible margin. It is the tool you would actually reach for, and now you have something to check it against.
C_auto = pidtune(G, 'PID');
fprintf('\nBy pidtune: Kp = %.3f, Ki = %.3f, Kd = %.3f\n', ...
    C_auto.Kp, C_auto.Ki, C_auto.Kd);
S2 = stepinfo(feedback(C_auto*G, 1));
fprintf('  overshoot %.1f%%, settles in %.1f s\n', S2.Overshoot, S2.SettlingTime);
%[text] Ask it for a particular crossover and watch what happens near the plant's own resonance. At $\\omega_c$ = 1 rad/s, which is where this plant rings, the tuner backs right off and hands you something that takes eight minutes.
for wc_try = [1 3 8]
    Ct = pidtune(G, 'PID', wc_try);
    St = stepinfo(feedback(Ct*G, 1));
    fprintf('  wc = %g:  Kp = %6.3f, Ki = %6.3f, Kd = %6.3f  ->  settles in %.1f s\n', ...
        wc_try, Ct.Kp, Ct.Ki, Ct.Kd, St.SettlingTime);
end
%%
%[text] Compare the two designs.
figure
step(feedback(C_design*G, 1), 20); hold on
step(feedback(C_auto*G, 1), 20); hold off
grid on; legend('by design', 'pidtune', 'Location', 'southeast')
title('Your design against the function''s')
%%
%[text] ## The one the function cannot know about
%[text] Run both through the check that decides what actually flies.
fprintf('\n--- your design ---\n');
[ok_d, why_d] = heli_check_one(Kp_design, Ki_design, Kd_design, heli_plant('shared'));
fprintf('%s %s\n', string(ok_d), why_d);

fprintf('\n--- pidtune ---\n');
[ok_a, why_a] = heli_check_one(C_auto.Kp, C_auto.Ki, C_auto.Kd, heli_plant('shared'));
fprintf('%s %s\n', string(ok_a), why_a);
%%
%[text] Read that carefully, because it is the whole session in one result.
%[text] `pidtune` gives the better-damped loop: look at the damping ratio and the phase margin. It settles in much the same time as yours and overshoots more, so it is not better at everything. And it is refused outright, because it asks the motors for more volts than the amplifier has.
%[text] The function was not wrong. It optimised for the specification it was given, and the amplifier was not in it. Nothing you can do inside the loop fixes a specification that left something out.
%[text] Which of the two would you defend in a design review? That is the question the coursework asks, and there is more than one defensible answer.
%%
%[text] ## Check it, then submit
%[text] `submit_gains` runs the same checks and only then gives you a link with your numbers in it.
submit_gains(Kp_design, Ki_design, Kd_design, 'your name here');

%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline"}
%---
%[control:slider:kp01]
%   data: {"defaultValue":2,"label":"Kp","max":20,"min":0,"run":"Section","runOn":"ValueChanging","step":0.1}
%---
%[control:slider:ki01]
%   data: {"defaultValue":0.5,"label":"Ki","max":5,"min":0,"run":"Section","runOn":"ValueChanging","step":0.05}
%---
%[control:slider:kd01]
%   data: {"defaultValue":1,"label":"Kd","max":10,"min":0,"run":"Section","runOn":"ValueChanging","step":0.05}
%---
%[control:slider:zc01]
%   data: {"defaultValue":0.7,"label":"zeta_c","max":1,"min":0.1,"run":"Section","runOn":"ValueChanging","step":0.05}
%---
%[control:slider:wc01]
%   data: {"defaultValue":0.8,"label":"omega_c","max":3,"min":0.2,"run":"Section","runOn":"ValueChanging","step":0.05}
%---
%[control:slider:p01]
%   data: {"defaultValue":2.5,"label":"third pole","max":10,"min":0.5,"run":"Section","runOn":"ValueChanging","step":0.1}
%---
