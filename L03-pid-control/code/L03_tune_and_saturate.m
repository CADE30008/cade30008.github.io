%[text] # Tune it, then push it until the actuator cannot keep up
%[text] You have tuned PID controllers before, in Design, Computing and Load Simulation: what each term does, steady-state error with P, PD and PID, Ziegler-Nichols, and matching the characteristic equation. None of that is repeated here.
%[text] This picks up where that stopped. You tune a controller for the pitch loop, meet the requirement, and then find out what happens when the elevator runs out of travel — which the linear analysis you used to design it does not model at all.
%[text] ## How to use this
%[text] **Run one section at a time**, with *Run Section*, not *Run All*. Drag the sliders: the section re-runs as you move them, so the plot and the numbers under it follow.
%[text] Work in pairs. The questions in bold are the point of the exercise; the code is only how you answer them.
clear; close all

%[text] ## 1 · The plant
%[text] The pitch attitude loop from the lecture, elevator to attitude. It is the same `G` the handout designs against, and the integrator in it is why a proportional controller alone leaves no steady-state error to a step but cannot damp what follows.
s = tf('s');
G = 40 / (s*(s + 2)*(s + 10));   % pitch attitude / elevator

figure; step(feedback(G, 1), 20); grid on
title('Closed loop with unity gain: the starting point')

%[text] **Before you tune anything, write down the overshoot and the settling time of that response.** You are about to claim an improvement and you need something to claim it over.

%[text] ## 2 · Your controller
%[text] Three sliders. The derivative term is filtered, because a pure derivative amplifies noise without limit; `N` sets how far up the filter lets it act.
Kp = 2.03 %[control:slider:kp01]{"position":[6,10],"min":0,"max":10,"step":0.01}
Ki = 0.678 %[control:slider:ki01]{"position":[6,11],"min":0,"max":3,"step":0.001}
Kd = 0.661 %[control:slider:kd01]{"position":[6,11],"min":0,"max":3,"step":0.001}
N  = 10;

C = pid(Kp, Ki, Kd, Kd/(N*Kp));
L = C*G;
cl = feedback(L, 1);

figure; step(cl, 30); grid on
title(sprintf('Closed loop: Kp %.2f, Ki %.3f, Kd %.3f', Kp, Ki, Kd))

info = stepinfo(cl);
[Gm, Pm, ~, Wcp] = margin(L);
fprintf('overshoot %5.1f %%   settling %5.2f s   phase margin %5.1f deg at %.2f rad/s\n', ...
        info.Overshoot, info.SettlingTime, Pm, Wcp);

%[text] **Find a setting that meets the requirement: overshoot under 10% and settled within 4 seconds.** Then look at the phase margin you got. Did you aim for it, or did it just happen?

%[text] ## 3 · The elevator has limits
%[text] Everything above assumed the elevator does whatever it is told. It does not: it has a travel limit, and the controller has no idea.
%[text] Command a step large enough to hit it, and simulate the loop with the limit in place.
lim_deg  = 20 %[control:slider:lim01]{"position":[12,14],"min":5,"max":40,"step":1}
step_deg = 25 %[control:slider:step01]{"position":[13,15],"min":1,"max":40,"step":1}

t = 0:0.01:30;
[y_lin, y_sat, u_sat] = pitch_with_limit(G, C, step_deg, lim_deg, t);

figure
subplot(211)
plot(t, y_lin, 'LineWidth', 1.2); hold on
plot(t, y_sat, 'LineWidth', 1.6); yline(step_deg, ':'); grid on
legend('No limit (what you designed)', 'With the limit', 'Location', 'southeast')
ylabel('Pitch (deg)'); title('The same controller, with and without the limit')
subplot(212)
plot(t, u_sat, 'LineWidth', 1.2); hold on
yline(lim_deg, 'r:'); yline(-lim_deg, 'r:'); grid on
ylabel('Elevator (deg)'); xlabel('Time (s)')

%[text] **Drag the step size up until the two traces separate.** At what commanded step does the limit start to matter? **Now drag it further.** The overshoot does not just get a little worse — say what it does instead.
%[text] **Why does the response stay past the target after the elevator has come out of saturation?** The answer is in the lower plot, and it is about what the integrator was doing while the elevator was stuck.

%[text] ## 4 · Stop the integrator winding up
%[text] The standard fix is to stop integrating while the actuator is saturated and the error would push it further in. Conditional integration, or clamping.
[~, y_clamp, u_clamp] = pitch_with_limit(G, C, step_deg, lim_deg, t, true);

figure
plot(t, y_sat, 'LineWidth', 1.2); hold on
plot(t, y_clamp, 'LineWidth', 1.6); yline(step_deg, ':'); grid on
legend('Limit, no anti-windup', 'Limit, conditional integration', 'Location', 'southeast')
ylabel('Pitch (deg)'); xlabel('Time (s)')
title('Clamping the integrator while the elevator is stuck')

fprintf('no anti-windup: overshoot %.1f %%\n', 100*(max(y_sat)-step_deg)/step_deg);
fprintf('clamped:        overshoot %.1f %%\n', 100*(max(y_clamp)-step_deg)/step_deg);

%[text] **Does clamping get you back to the response you designed?** Compare all three. It should not, quite, and the gap is the honest cost of an actuator that cannot do what the controller asked.
%[text] ## What to take away
%[text] - A linear design is a claim about small signals. The elevator's travel is the first thing that breaks it, and nothing in the Bode plot warned you. \
%[text] - An integrator with nowhere to put its output keeps integrating. That is windup, and the overshoot it causes arrives after the saturation has ended. \
%[text] - Anti-windup is a repair, not a design. The cheaper fix is often to ask for less: rate-limit the reference so the actuator never saturates.

function [y_lin, y_sat, u_sat] = pitch_with_limit(G, C, step_deg, lim_deg, t, clamp)
%PITCH_WITH_LIMIT  Step the pitch loop with and without an elevator limit.
%   Fixed-step Euler on the plant and a discrete PID, because a saturation
%   inside the loop is not a transfer function and cannot be stepped with
%   step(). clamp = true stops the integrator while the elevator is on its
%   stop and the error would drive it further in.
    if nargin < 6, clamp = false; end
    dt = t(2) - t(1);
    sysd = c2d(ss(G), dt);
    [Ad, Bd, Cd, Dd] = ssdata(sysd);
    [Kp, Ki, Kd, Tf] = piddata(C);

    run = @(limit, anti) deal_loop(Ad, Bd, Cd, Dd, Kp, Ki, Kd, Tf, dt, t, step_deg, limit, anti);
    [y_lin, ~] = run(inf, false);
    [y_sat, u_sat] = run(lim_deg, clamp);
end

function [y, u_log] = deal_loop(Ad, Bd, Cd, Dd, Kp, Ki, Kd, Tf, dt, t, ref, limit, anti)
    x = zeros(size(Ad, 1), 1);
    integ = 0; dstate = 0; y = zeros(size(t)); u_log = zeros(size(t));
    for k = 1:numel(t)
        out = Cd*x + Dd*0;
        e = ref - out;
        % Derivative on the measurement, not on the error: a step in the
        % reference is a step in the error, and differentiating it is the
        % kick the handout warns about. Filtered, because a pure derivative
        % amplifies noise without limit.
        if Tf > 0
            dstate = dstate + dt*(out - dstate)/Tf;
            dmeas = (out - dstate)/Tf;
        else
            dmeas = 0;
        end
        u_unsat = Kp*e + Ki*integ - Kd*dmeas;
        u = max(min(u_unsat, limit), -limit);
        % Integrate unless clamped against the stop in the direction that
        % would push it further in.
        winding = anti && (u ~= u_unsat) && (sign(e) == sign(u_unsat));
        if ~winding, integ = integ + dt*e; end
        y(k) = out; u_log(k) = u;
        x = Ad*x + Bd*u;
    end
end
