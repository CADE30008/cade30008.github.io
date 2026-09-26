%% Three axes, three loops
% One axis at a time was the easy version. This is the machine.
%
% You have two motor voltages and three angles to control, and one of the
% three cannot be commanded at all. The way round that is a cascade: command
% pitch, and let travel follow.
%
% Run one section at a time.

clear; close all
m = heli3d_model();
A = m.A; B = m.B;

%% What the model says before you design anything
% Read the structure out of the matrices rather than taking it on trust.

fprintf('eigenvalues: '); fprintf('%.3f ', eig(A)); fprintf('\n');
fprintf('elevation from the sum:        B(4,:) = [%.4f %.4f]\n', B(4,1), B(4,2));
fprintf('pitch from the difference:     B(5,:) = [%.4f %.4f]\n', B(5,1), B(5,2));
fprintf('travel not commanded:          B(6,:) = [%.4f %.4f]\n', B(6,1), B(6,2));
fprintf('travel accelerates from pitch: A(6,2) = %.4f\n', A(6,2));
fprintf('controllable: %d of 6\n', rank(ctrb(A,B)));

%%
% Six poles at the origin. Nothing in this model pulls any axis back towards
% anywhere, which is what "linearised about level" costs you: the gravity
% stiffness you measured on the elevation axis is exactly zero at level, so it
% is absent here.
%
% It is still controllable, so there is nothing stopping you.

%% Change coordinates to what you can actually command
% Work in the sum and the difference rather than in front and back voltages.
% Nothing is lost and the loops separate.
%
%   u_sum  = Vf + Vb   ->  elevation
%   u_diff = Vf - Vb   ->  pitch

T = [0.5 0.5; 0.5 -0.5];            % [Vf; Vb] = T * [u_sum; u_diff]
Bt = B * T;
fprintf('\nafter the change of variables:\n');
fprintf('  elevation from u_sum:  %.4f\n', Bt(4,1));
fprintf('  pitch from u_diff:     %.4f\n', Bt(5,2));
fprintf('  cross terms:           %.2e, %.2e\n', Bt(4,2), Bt(5,1));

%%
% The cross terms are zero. In these coordinates elevation and pitch are two
% independent double integrators, and each is a single-input problem you have
% already solved once.

Ke = Bt(4,1);           % rad/(V s^2), elevation from the summed voltage
Kp_pitch = Bt(5,2);     % rad/(V s^2), pitch from the difference
Ktrav = A(6,2);         % rad/s^2 per rad of pitch

%% The elevation loop
% This model is linearised about level, which makes elevation a double
% integrator. A double integrator cannot be stabilised by proportional
% feedback at any gain, so the derivative term is not a refinement here.

s = tf('s');
G_elev = Ke / s^2;

zc = 0.8; wc = 1.2;                 % what you want
kd_e = 2*zc*wc / Ke;
kp_e = wc^2 / Ke;
C_elev = kd_e*s + kp_e;
fprintf('\nelevation: Kp = %.2f, Kd = %.2f\n', kp_e, kd_e);

figure
step(feedback(C_elev*G_elev, 1), 10); grid on
title('Elevation loop')

%% The pitch loop, fast
% Pitch is the inner loop of the travel cascade, so it has to be several times
% faster than the loop wrapped around it or the two will argue.

G_pitch = Kp_pitch / s^2;
zp = 0.8; wp = 8.0;                 % fast, for the reason checked below
kd_p = 2*zp*wp / Kp_pitch;
kp_p = wp^2 / Kp_pitch;
C_pitch = kd_p*s + kp_p;
fprintf('pitch:     Kp = %.2f, Kd = %.2f   (wn = %.1f rad/s)\n', kp_p, kd_p, wp);

%% The travel loop, slow
% Travel is commanded by asking for pitch. Treat the closed pitch loop as
% roughly unity for frequencies well below its bandwidth, and the travel plant
% is then A(6,2)/s^2 from commanded pitch.

T_pitch = feedback(C_pitch*G_pitch, 1);
G_trav  = Ktrav / s^2;

zt = 0.9; wt = 0.8;
kd_t = 2*zt*wt / Ktrav;
kp_t = wt^2 / Ktrav;

%%
% Look at the signs. |Ktrav| is negative, so those gains come out negative,
% which is correct and looks wrong. Positive pitch drives travel one way, and
% the sign has to come back somewhere. Getting this wrong is the most common
% reason a travel loop runs away on the first attempt, and it is a sign error
% rather than a tuning problem.

fprintf('travel:    Kp = %.2f, Kd = %.2f   (note the sign)\n', kp_t, kd_t);

C_trav = kd_t*s + kp_t;
L_trav = C_trav * T_pitch * G_trav;
figure
step(feedback(L_trav, 1), 30); grid on
title('Travel loop, through the closed pitch loop')

%%
% Check the separation you assumed. The cascade only works if the inner loop
% is fast enough that the outer one can treat it as "already there", and the
% rule of thumb is a factor of four in bandwidth.
%
% This is a check worth making rather than assuming. The first attempt at
% these numbers used a pitch loop at 6 rad/s and a travel loop at 1.2, which
% comes out at 3.3 and fails: the two loops would have been arguing with each
% other, and the step response above would have been optimistic about a design
% that did not hold together. Slowing travel to 0.8 rad/s and raising pitch to
% 8 fixes it.

fprintf('\npitch loop bandwidth: %.2f rad/s\n', bandwidth(T_pitch));
fprintf('travel loop bandwidth: %.2f rad/s\n', bandwidth(feedback(L_trav,1)));
ratio = bandwidth(T_pitch) / bandwidth(feedback(L_trav,1));
fprintf('ratio: %.1f  (want 4 or more)  -> %s\n', ratio, ...
    string(ratio >= 4).replace("true","the cascade holds").replace("false","TOO CLOSE, redesign"));

%% What this costs in volts
% Both loops drive the same two motors. Elevation uses the sum, pitch the
% difference, and the actual voltages are what the amplifier sees.
%
%   Vf = (u_sum + u_diff)/2 + Vop
%   Vb = (u_sum - u_diff)/2 + Vop
%
% Work out the worst case for the manoeuvre you intend, and check it against
% the amplifier before you go anywhere near the rig. A design that saturates
% one motor is not the design you tested.

fprintf('\noperating point %.1f V, amplifier limit %.0f V\n', ...
    m.params.Vop, m.params.Vmax);
fprintf('headroom per motor: %.1f V up, %.1f V down\n', ...
    m.params.Vmax - m.params.Vop, m.params.Vop);

% tracking: status=draft version=0 assisted=true
