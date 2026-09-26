s = tf('s');
G = 40 / (s*(s + 2)*(s + 10));   % pitch attitude / elevator (rad/rad)

Kp = 2.03; Ki = 0.678; Kd = 0.661; N = 10;
C = pid(Kp, Ki, Kd, Kd/(N*Kp));  % full controller: sets the loop
Cr = pid(Kp, Ki);                % what the reference sees
Tref = Cr * feedback(G, C);      % D on measurement

[Gm, Pm, ~, Wcp] = margin(C*G);
S = stepinfo(Tref, 'SettlingTimeThreshold', 0.02);
fprintf('PM = %.1f deg at %.2f rad/s, GM = %.1f\n', Pm, Wcp, Gm)
fprintf('rise %.2f s, overshoot %.1f %%, settling %.2f s\n', ...
        S.RiseTime, S.Overshoot, S.SettlingTime)

% tracking: status=draft version=0 assisted=true
