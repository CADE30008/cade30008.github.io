% L03_ttail_case.m — the T-tail case from Lecture 3.
%
% Duc Nguyen's script, as he runs it in the lecture. A pitch model whose short
% period and phugoid sit two decades apart: tune a PI against the short period
% alone and it is a good controller, put the same PI on the full dynamics and
% the loop is unstable.
%
% The deck shows Duc's own plots. The handout's are redrawn in the site's
% style by models/L03_ttail_case.py, which writes out the same two transfer
% functions and the same gains by hand: change one below and that script has
% to change with it, or the two stop agreeing.

close all; clear
s = tf('s');

%% Pitch response: short period, phugoid, and combined dynamics
sp = (s+0.5877)/ (s^2+1.127*s+1.862);
pg = (s+0.02662) / (s^2+0.01579*s+0.01475);
ol_full = sp*pg;

figure(1); % step responses
subplot(311); step(sp,'b'); xlim([0 150]); title('Short period');
subplot(312); step(pg,'r'); xlim([0 150]); title('Phugoid');
subplot(313); step(ol_full,'k'); xlim([0 150]); title('Combined');

%% PI controller
PI = 2.2 + 8.3/s;
cl_sp = feedback(PI*sp,1); % closed-loop short-period model only
cl_sys_ol = feedback(PI*ol_full,1); % Closed-loop full dynamics

figure(2); % short-period open- and closed-loop step response
subplot(211); step(sp); title('Short-period open loop');
subplot(212); step(cl_sp); title('Short-period with PI'); 

figure(3) % full dynamics closed-loop step response
step(cl_sys_ol); title('Full dynamics with PI')

% Frequency responses
figure(4); margin(PI*sp); xlim([10^-3 10^2]); title('Short period with PI')
figure(5); margin(PI*ol_full); xlim([10^-3 10^2]); title('Full dynamics with PI')

%% Root locus
PI_rl = (2.2 + 8.3/s)/2.2; % divide both sides by the Kp gain 

figure(4);
subplot(121); rlocus(PI_rl*sp); xlim([-8 1]); ylim([-4 4]); title('Short period with PI')
subplot(122); rlocus(PI_rl*ol_full); xlim([-8 1]); ylim([-4 4]); title('Short period and phugoid with PI')
