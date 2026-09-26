function t2_fly_these(K, wn, zeta)
%T2_FLY_THESE  Gains to put on the rig, and what each should do.
%
%   t2_fly_these                 against the stored model
%   t2_fly_these(3.5, 1.02, 0.07)   against the fit you just took
%
% Test 2. Four sets, chosen so that if the rig agrees with the model you will
% see four clearly different things. If it does not, we find out now rather
% than at 13:40.

if nargin == 3
    plant = struct('K', K, 'wn', wn, 'zeta', zeta);
else
    plant = heli_plant();
end
env = heli_envelope();
fprintf('Checking against K=%.2f wn=%.2f zeta=%.3f\n\n', plant.K, plant.wn, plant.zeta);

sets = { 'the fallback',        0.71, 0.59, 0.91, 'should look tidy: settles about 6 s, small overshoot'
         'gentler',             0.36, 0.38, 0.79, 'slower, less overshoot, should still settle'
         'pidtune''s answer',   2.18, 1.01, 1.18, 'REFUSED on volts. Fly it anyway if you are willing: it should saturate and look worse than the model says'
         'too much integral',   0.50, 2.00, 0.50, 'REFUSED as unstable. Do not fly it. Listed so you can see the check catch it' };

for i = 1:size(sets,1)
    [ok, why, m] = heli_check_one(sets{i,2}, sets{i,3}, sets{i,4}, plant, env);
    fprintf('%-20s Kp=%.2f Ki=%.2f Kd=%.2f\n', sets{i,1}, sets{i,2}, sets{i,3}, sets{i,4});
    if ok
        fprintf('   ACCEPTED   damping %.2f, PM %.0f deg, peak %.1f V, settles %.1f s\n', ...
            m.damping, m.phase_margin, m.peak_volts, m.settle_s);
    else
        fprintf('   REFUSED    %s\n', why);
    end
    fprintf('   expect: %s\n\n', sets{i,5});
end

fprintf(['SEND ME: for the two accepted sets, the overshoot and settling time\n' ...
         'you actually saw, and whether the motors sounded like they were\n' ...
         'saturating. Those two numbers against the predictions above are the\n' ...
         'whole sim-against-hardware story for the session.\n']);
end

% tracking: status=draft version=0 assisted=true
