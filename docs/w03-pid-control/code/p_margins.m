s = tf('s');
G = 40 / (s*(s + 2)*(s + 10));   % pitch attitude / elevator (rad/rad)

Kp = 1;
[Gm, Pm, Wcg, Wcp] = margin(Kp*G);
fprintf('GM = %.2f at %.2f rad/s, PM = %.1f deg at %.2f rad/s\n', Gm, Wcg, Pm, Wcp)

% tracking: status=draft version=0
