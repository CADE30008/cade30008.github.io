s = tf('s');
G = 40 / (s*(s + 2)*(s + 10));   % pitch attitude / elevator (rad/rad)
Kp0 = 2.03; Ki0 = 0.678; Kd0 = 0.661; N = 10;
t = linspace(0, 10, 5001);

% Part (a): the lecture design
[pm, wc, uPeak] = evaluate(1.0, G, Kp0, Ki0, Kd0, N, t);
fprintf('k = 1.00: PM %.1f deg, wc %.2f rad/s, peak elevator %.1f deg\n', pm, wc, uPeak)

% Part (b): largest k with PM >= 50 deg and peak elevator <= 15 deg
best = [];
for k = 0.30:0.01:1.49
    [pm, wc, uPeak, os] = evaluate(k, G, Kp0, Ki0, Kd0, N, t);
    if pm >= 50 && uPeak <= 15
        best = [k, pm, wc, uPeak, os];
    end
end
fprintf('best k = %.2f: PM %.1f deg, wc %.2f rad/s, peak elevator %.1f deg, overshoot %.1f %%\n', best)

function [pm, wc, uPeak, os] = evaluate(k, G, Kp0, Ki0, Kd0, N, t)
    % Scale all three gains by k; return PM, crossover, peak elevator, overshoot.
    Kp = k*Kp0; Ki = k*Ki0; Kd = k*Kd0;
    C = pid(Kp, Ki, Kd, Kd/(N*Kp));
    Cr = pid(Kp, Ki);                    % derivative on measurement
    [~, pm, ~, wc] = margin(C*G);
    uPeak = 10 * max(abs(step(Cr * feedback(1, C*G), t)));   % deg, 10 deg step
    info = stepinfo(Cr * feedback(G, C));   % relative to the final value, 1
    os = info.Overshoot;
end
