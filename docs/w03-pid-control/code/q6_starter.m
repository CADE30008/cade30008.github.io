s = tf('s');
G = 40 / (s*(s + 2)*(s + 10));   % pitch attitude / elevator (rad/rad)
Kp = 2.03; Ki = 0.678; Kd = 0.661; N = 10;   % the lecture's PID design

C = pid(Kp, Ki, Kd, Kd/(N*Kp));  % full controller: sets the loop
Cr = pid(Kp, Ki);                % the reference sees P and I only
Tref = Cr * feedback(G, C);      % reference to attitude
Tu = Cr * feedback(1, C*G);      % reference to elevator

[~, Pm, ~, Wcp] = margin(C*G);
fprintf('PM = %.1f deg at %.2f rad/s\n', Pm, Wcp)

t = linspace(0, 10, 5001);
u = step(Tu, t) * 10;            % elevator (deg) for a 10 deg step
fprintf('peak elevator = %.1f deg\n', max(abs(u)))

% (b) Scale Kp, Ki and Kd by the same factor k and search for the largest k
%     meeting the requirements. Your code here.

% tracking: status=draft version=0 assisted=true
