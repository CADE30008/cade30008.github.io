%% All three axes at once
% Three separate loops treat the coupling as a nuisance to be worked around.
% State feedback treats it as information.
%
% This is where the second half of the unit is going, so you are meeting it
% early and without the theory. Run it, compare it with your three loops, and
% come back to it later.

clear; close all
m = heli3d_model();
A = m.A; B = m.B; C = m.C;

%% Full state feedback
% One matrix, six states, two inputs. No loops, no cascade, no assumption that
% one axis is faster than another.

fprintf('controllable: %d of 6, so every pole can be placed anywhere\n', ...
    rank(ctrb(A,B)));

%% Choose by weighting, not by pole position
% With six poles and two inputs there are too many choices to make by hand.
% LQR turns the choice into a statement about what you care about:
%
%   minimise  integral of  x' Q x  +  u' R u
%
% Q penalises being in the wrong place, R penalises the effort of fixing it.
% Raise R and the controller gets gentler.

Q = diag([100, 1, 100, 10, 1, 10]);   % elevation and travel matter most
R = 0.05 * eye(2);                    % and volts are not free

K = lqr(A, B, Q, R);
fprintf('\ngain matrix K is %d by %d:\n', size(K,1), size(K,2));
disp(round(K, 3));

cl = ss(A - B*K, B, C, zeros(3,2));
fprintf('closed-loop poles:\n');
damp(cl)

%% Two motors, three angles, and what that means for what you can ask for
% Before commanding anything, ask what steady states exist.
%
% In steady state travel is only still if its acceleration is zero, and travel
% accelerates from pitch. So a steady travel angle requires *pitch = 0*. You
% cannot hold elevation, pitch and travel at three independently chosen
% values, because you have two motors and the third angle is spoken for.
%
% That is not a limitation of the controller. It is what the machine is.

Ct = C([1 3], :);                    % elevation and travel: what you may ask for
nu = size(B, 2);
M  = [A, B; Ct, zeros(2, nu)];
fprintf('\n[A B; C 0] is %d by %d, rank %d\n', size(M,1), size(M,2), rank(M));

sol = M \ [zeros(6, 2); eye(2)];
Nx = sol(1:6, :);
Nu = sol(7:end, :);

%% Does it fly?
% Command 10 degrees of elevation and 30 degrees of travel.

ref = [deg2rad(10); deg2rad(30)];
cl  = ss(A - B*K, B*(Nu + K*Nx), C, zeros(3, 2));

t = 0:0.01:25;
u = repmat(ref', numel(t), 1);
y = lsim(cl, u, t);

figure
plot(t, rad2deg(y), 'LineWidth', 1.4); grid on
yline(10, ':'); yline(30, ':');
xlabel('Time (s)'); ylabel('Angle (deg)')
legend('elevation', 'pitch', 'travel', 'Location', 'east')
title('State feedback, elevation and travel commanded')

fprintf('after %g s:  elevation %.2f deg (asked %g), travel %.2f deg (asked %g)\n', ...
    t(end), rad2deg(y(end,1)), 10, rad2deg(y(end,3)), 30);
fprintf('pitch settles to %.3f deg, which it has to\n', rad2deg(y(end,2)));
fprintf('peak pitch on the way: %.1f deg\n', max(abs(rad2deg(y(:,2)))));

%%
% Watch the pitch trace. Nothing asked for pitch, and it moves a long way
% anyway, because pitch is how the controller makes travel happen. It returns
% to zero at the end because it has to. Your three separate loops had to be
% told to use pitch that way; this one worked it out from the model.

%% What it costs
% The motor voltages, which is the part to be sceptical about.

x = lsim(ss(A - B*K, B*(Nu + K*Nx), eye(6), zeros(6,2)), u, t);
v = (Nu + K*Nx) * u' - K * x';       % [front; back], volts about the operating point
front = v(1,:) + m.params.Vop;
back  = v(2,:) + m.params.Vop;

figure
plot(t, front, t, back, 'LineWidth', 1.3); grid on
yline(m.params.Vmax, 'r--'); yline(0, 'r--');
xlabel('Time (s)'); ylabel('Motor voltage (V)')
legend('front', 'back', 'limit', 'Location', 'northeast')
title('What the amplifier is asked for')

fprintf('\npeak front %.1f V, peak back %.1f V, against a %.0f V limit\n', ...
    max(abs(front)), max(abs(back)), m.params.Vmax);
if max([abs(front), abs(back)]) > m.params.Vmax
    fprintf(2, 'This design saturates. It is not the design you would be testing.\n');
    fprintf(2, 'Raise R and try again: bigger R buys a gentler controller.\n');
else
    fprintf('Inside the amplifier, so the linear model is at least self-consistent.\n');
end

%%
% Even when the voltages fit, be sceptical. This model has no motor
% saturation, no friction and no encoder noise, and it is linearised about
% level while you are commanding 30 degrees of travel.

%% Fix it, the way the weighting is meant to be used
% R is the price of effort. The design above set it at 0.05, which says volts
% are nearly free, and the amplifier disagreed. Put the price up.

R2 = 1.0 * eye(2);
K2 = lqr(A, B, Q, R2);
sol2 = M \ [zeros(6, 2); eye(2)];
Nx2 = sol2(1:6, :); Nu2 = sol2(7:end, :);

x2 = lsim(ss(A - B*K2, B*(Nu2 + K2*Nx2), eye(6), zeros(6,2)), u, t);
v2 = (Nu2 + K2*Nx2) * u' - K2 * x2';
front2 = v2(1,:) + m.params.Vop;
back2  = v2(2,:) + m.params.Vop;
y2 = (C * x2')';

fprintf('\nR = 0.05:  peak %.1f V, elevation settles in %.1f s\n', ...
    max([abs(front), abs(back)]), settleTime(t, y(:,1), ref(1)));
fprintf('R = 1.00:  peak %.1f V, elevation settles in %.1f s\n', ...
    max([abs(front2), abs(back2)]), settleTime(t, y2(:,1), ref(1)));

figure
plot(t, front2, t, back2, 'LineWidth', 1.3); grid on
yline(m.params.Vmax, 'r--'); yline(0, 'r--');
xlabel('Time (s)'); ylabel('Motor voltage (V)')
legend('front', 'back', 'limit', 'Location', 'northeast')
title('After putting the price of effort up')

%%
% That is the trade, and it is the same one the first session was about. You
% did not buy the amplifier headroom with cleverness; you bought it with
% settling time. The only question is whether the requirement you wrote down
% can live with the slower number.
%
% If it cannot, the answer is not a better weighting. It is a bigger
% amplifier, a lighter arm, or a requirement somebody can defend.

%% Compare, and decide
% Put this next to your three-loop design and ask:
%
% * which settles sooner, and which asks for more volts?
% * which would you rather debug at the rig at half past four?
% * which one can you explain to somebody who has not done this unit?
%
% There is no single right answer, and the coursework does not want one. It
% wants the comparison, made against a requirement you wrote down first.


function ts = settleTime(t, y, target)
%SETTLETIME  Last time outside a 2% band, or Inf if it never settles.
out = find(abs(y - target) > 0.02 * abs(target));
if isempty(out) || out(end) + 1 >= numel(t)
    ts = Inf;
else
    ts = t(out(end));
end
end
