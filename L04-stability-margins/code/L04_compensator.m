%[text] # Shape the loop: four numbers, and what each one does
%[text] The aircraft is the one from Lecture 3: a T-tail whose short period and phugoid sit two decades apart. The PI below was tuned against the short period alone, and on the full dynamics it is unstable.
%[text] Your job is the four corner frequencies of a lead-lag compensator. Everything else is written for you.
clear; close all
s = tf('s');

%[text] ## The aircraft, and the controller that failed
sp = (s + 0.5877) / (s^2 + 1.127*s + 1.862);     % short period
pg = (s + 0.02662) / (s^2 + 0.01579*s + 0.01475); % phugoid
G  = sp * pg;                                     % the whole aircraft
C  = 2.2 + 8.3/s;                                 % week 3's PI

[Gm, Pm] = margin(C*G);
fprintf('No compensator:  GM %6.1f dB   PM %6.1f deg\n', 20*log10(Gm), Pm);

%[text] Negative margins, and the closed loop is unstable. That is where we start.

%[text] ## Your compensator
%[text] A lag in series with a lead. Each is one zero over one pole:
%[text] $$ K(s) = \left(\frac{s/a_1 + 1}{s/b_1 + 1}\right)\left(\frac{s/a_2 + 1}{s/b_2 + 1}\right) $$
%[text] **Put the four corner frequencies in.** Lag first: `a1` above `b1`. Then the lead: `a2` below `b2`.
a1 = 0.11 %[control:slider:a1]{"position":[6,10],"min":0.01,"max":1,"step":0.01}
b1 = 0.01 %[control:slider:b1]{"position":[6,10],"min":0.001,"max":0.5,"step":0.001}
a2 = 0.11 %[control:slider:a2]{"position":[6,10],"min":0.01,"max":1,"step":0.01}
b2 = 15 %[control:slider:b2]{"position":[6,8],"min":1,"max":60,"step":1}

K = ((s/a1 + 1)/(s/b1 + 1)) * ((s/a2 + 1)/(s/b2 + 1));
L = C * G * K;

[Gm, Pm, ~, Wcp] = margin(L);
fprintf('With compensator: GM %6.1f dB   PM %6.1f deg at %.2f rad/s\n', 20*log10(Gm), Pm, Wcp);

figure; margin(L); grid on
title('The compensated loop')

%[text] **Are both margins positive?** If not, look at which corner frequency is in the wrong place rather than changing all four.

%[text] ## What it did to the closed loop
cl_before = feedback(C*G, 1);
cl_after  = feedback(L, 1);

figure
step(cl_after, 10); grid on
title('Closed loop with the compensator')

%[text] **Now try the lead pole at 50 instead of 15.** Change `b2` above and run this section again. What happened to the phase margin, and what happened to the step?
