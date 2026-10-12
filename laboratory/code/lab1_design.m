%[text] # Design a controller for the model you fitted
%[text] No rig in this part, and that is the point. You cannot turn a knob until it looks right, so you have to decide what right means first and then defend it.
%[text] ## How to use this
%[text] **Run one section at a time**, with *Run Section*, not *Run All*. Each section builds on the one above.
%[text] - Where there are sliders, drag them. The section re-runs as you move, so the plot and the verdict under it follow the slider. \
%[text] - Output appears underneath the code that made it. \
%[text] - Run **identify\_rig** or **lab1\_fit** first. Either writes `rig_plant.json`, which this reads. \
clear; close all

if ~isfile('rig_plant.json')
    error(['No rig_plant.json here. Run identify_rig on one recording, or ' ...
           'lab1_fit on all of them: either writes the model this reads.']);
end
m = jsondecode(fileread('rig_plant.json'));
plant = struct('K', m.K, 'wn', m.wn, 'zeta', m.zeta);
G = tf(plant.K * plant.wn^2, [1, 2*plant.zeta*plant.wn, plant.wn^2]);

fprintf('Your model: K = %.3f deg/V, wn = %.3f rad/s, zeta = %.4f\n', ...
    plant.K, plant.wn, plant.zeta);

%%
%[text] ## Your requirement
%[text] The numbers you and your group argued about and wrote down, **before any design**. Set them to what you agreed.
%[text] The step stays at 7.5 degrees. That is the figure the envelope check uses, so keeping it means the prediction below and the flight check are talking about the same manoeuvre.
%[text] Steady-state error is not here. With integral action it is zero by construction, so a requirement on it tests nothing about your design. If you want it to mean something, require it of a design with no integrator.
req.stepDeg      = 7.5;
req.overshootMax = 20 %[control:slider:ovr01]{"position":[20,22]}
req.settleMax    = 8 %[control:slider:set01]{"position":[20,21]}
req.voltMax      = 6 %[control:slider:vlt01]{"position":[20,21]}

%%
%[text] ## Level 1: by feel
%[text] Three sliders and a live response. Not a design method, and not meant to be: it is how you find out what each term does, so that the numbers in level 2 mean something when you choose them.
%[text] Move one at a time. Push each until it misbehaves, and note which way.
%[text] The response is against **your** fit, because exploring your own measurement is the point here. The verdict is against your fit too, which is right in the laboratory and is not what happens in the lecture: there, everyone flies one rig and the check is against that machine. Part 3 is where the two meet.
Kp = 2 %[control:slider:kp01]{"position":[6,7]}
Ki = 0.5 %[control:slider:ki01]{"position":[6,9]}
Kd = 1 %[control:slider:kd01]{"position":[6,7]}

figure
step(feedback(pid(Kp, Ki, Kd)*G, 1), 0:0.05:30)
grid on; title(sprintf('K_p = %.2f,  K_i = %.2f,  K_d = %.2f', Kp, Ki, Kd))

[ok_feel, why_feel] = heli_check_one(Kp, Ki, Kd, plant, heli_envelope());
fprintf('envelope: %s %s\n', string(ok_feel), why_feel);

%%
%[text] ## Level 2: by design
%[text] Feel does not scale and does not transfer. Decide where you want the poles and solve for the gains that put them there.
%[text] With PID the characteristic polynomial is
%[text] $$s^3 + (2\\zeta\\omega_n + K\\omega_n^2 K_d)s^2 + (\\omega_n^2 + K\\omega_n^2 K_p)s + K\\omega_n^2 K_i$$
%[text] Ask for a dominant pair at $\\zeta_c$, $\\omega_c$ and a real pole at $-p$:
%[text] $$(s^2 + 2\\zeta_c\\omega_c s + \\omega_c^2)(s + p)$$
%[text] Match the coefficients and the three gains fall out. Three equations, three unknowns, and you can do it on paper.

%[text] These sliders move the poles you are asking for, not the gains. Watch the gains follow, and watch the voltage in the table below: a faster $\\omega_c$ is a request for more volts, and the demand path saturates not far above the trim.
zc = 0.7 %[control:slider:zc01]{"position":[6,9]}
wc = 0.8 %[control:slider:wc01]{"position":[6,9]}
p  = 2.5 %[control:slider:p01]{"position":[6,9]}

a = plant.K * plant.wn^2;
design.Kd = (2*zc*wc + p - 2*plant.zeta*plant.wn) / a;
design.Kp = (wc^2 + 2*zc*wc*p - plant.wn^2) / a;
design.Ki = (wc^2 * p) / a;

%%
%[text] ## Level 3: by function
%[text] `pidtune` picks gains for a target bandwidth with a sensible margin. It is the tool you would reach for anyway, and now you have something to check it against.

Cauto = pidtune(G, 'PID');
auto = struct('Kp', Cauto.Kp, 'Ki', Cauto.Ki, 'Kd', Cauto.Kd);

%%
%[text] ## Do they meet what you asked for?
%[text] Both designs, against your requirement and against the flight envelope.
%[text] The prediction comes from heli_check_one, which is the same code that decides whether your gains are allowed on the rig. That is deliberate: a design checked here against one simulation and refused there by another would teach nothing except that the tools disagree.
%[text] It takes the derivative from the measured rate rather than the error, which is how Part 2 tells you to wire it. On the error, the demand's own ramp goes straight through Kd and asks the amplifier for voltage it does not have.

env = heli_envelope();
names = {'by design', 'by pidtune'};
sets = {design, auto};

fprintf('\n%-11s %6s %6s %6s | %9s %8s %7s | %s\n', ...
    'method', 'Kp', 'Ki', 'Kd', 'overshoot', 'settles', 'peak V', 'envelope');
for i = 1:numel(sets)
    g = sets{i};
    [ok, why, r] = heli_check_one(g.Kp, g.Ki, g.Kd, plant, env);
    fprintf('%-11s %6.3f %6.3f %6.3f | %8.1f%% %7.1fs %6.1fV | %s\n', ...
        names{i}, g.Kp, g.Ki, g.Kd, r.overshoot_pct, r.settle_s, r.peak_volts, ...
        ternary(ok, 'passes', char(why)));

    fails = {};
    if r.overshoot_pct > req.overshootMax
        fails{end+1} = sprintf('overshoot %.1f%% over your %g%%', r.overshoot_pct, req.overshootMax); %#ok<SAGROW>
    end
    if r.settle_s > req.settleMax
        fails{end+1} = sprintf('settles in %.1f s, over your %g s', r.settle_s, req.settleMax); %#ok<SAGROW>
    end
    if r.peak_volts > req.voltMax
        fails{end+1} = sprintf('asks %.1f V, over your %g V', r.peak_volts, req.voltMax); %#ok<SAGROW>
    end
    if isempty(fails)
        fprintf('%-11s   meets your requirement\n', '');
    else
        fprintf('%-11s   misses it: %s\n', '', strjoin(fails, '; '));
    end
end

%%
%[text] Expect the two to disagree, and work out why before you pick one. They are answering different questions: yours placed the poles where you said, and `pidtune` chose a bandwidth it thought was safe near a plant that rings at about 1 rad/s.
%[text] If one of them asks for more voltage than the envelope allows, that is the most useful failure in this part. Say in your report which requirement you would relax to fix it, and what that costs.

%%
%[text] ## Does it survive your own uncertainty?
%[text] lab1_fit told you how much your recordings disagree. The rig on the day will not be at the mean of your fits, so a design that only works there is a design that works nowhere in particular.
%[text] This re-checks your chosen gains against the extremes of your own spread.

choice = design;      % change to `auto` if that is the one you are taking

if isfield(m, 'fits') && numel(m.fits) > 1
    fields = {'K', 'K', 'wn', 'wn'};
    picks  = {'lowest', 'highest', 'lowest', 'highest'};
    fprintf('\nYour gains at the edges of your own fits:\n');
    for i = 1:numel(fields)
        f = fields{i};
        values = [m.fits.(f)];
        edge = plant;
        if strcmp(picks{i}, 'lowest')
            edge.(f) = min(values);
        else
            edge.(f) = max(values);
        end
        [ok, why, r] = heli_check_one(choice.Kp, choice.Ki, choice.Kd, edge, env);
        fprintf('  %-8s %-4s = %6.3f  ->  %s\n', picks{i}, f, edge.(f), ...
            ternary(ok, sprintf('%.1f%% overshoot, %.1f V', r.overshoot_pct, r.peak_volts), char(why)));
    end
    fprintf(['\nA set of gains that passes at the mean and fails at an edge is\n' ...
             'not ready. Either widen the margin or say in your report which\n' ...
             'edge you are betting against, and why.\n']);
else
    fprintf(['\nOnly one fit in rig_plant.json, so this cannot test your spread.\n' ...
             'Take several recordings next time you are at the rig: knowing how\n' ...
             'badly you know the machine is worth more than one careful fit.\n']);
end

%%
%[text] ## Take it to the rig
%[text] Saved for Part 3, with the requirement you are asking to be judged against.

Kp = choice.Kp; Ki = choice.Ki; Kd = choice.Kd; %#ok<NASGU>
save('my_gains.mat', 'Kp', 'Ki', 'Kd', 'req', 'plant');
fprintf('\nSaved my_gains.mat: Kp = %.3f, Ki = %.3f, Kd = %.3f\n', ...
    choice.Kp, choice.Ki, choice.Kd);
fprintf('Write down what you expect to see before you go back in.\n');
fprintf('Being wrong is fine. Not having predicted is not.\n');


function out = ternary(c, a, b)
out = b; if c; out = a; end
end

%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline"}
%---
%[control:slider:ovr01]
%   data: {"defaultValue":20,"label":"max overshoot %","max":60,"min":0,"run":"Section","runOn":"ValueChanging","step":1}
%---
%[control:slider:set01]
%   data: {"defaultValue":8,"label":"settle within (s)","max":20,"min":1,"run":"Section","runOn":"ValueChanging","step":0.5}
%---
%[control:slider:vlt01]
%   data: {"defaultValue":6,"label":"peak demand (V)","max":12,"min":1,"run":"Section","runOn":"ValueChanging","step":0.5}
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
