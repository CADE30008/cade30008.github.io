function url = submit_gains(kp, ki, kd, displayName, opts)
%SUBMIT_GAINS  Check your PID gains, then get a link to submit them.
%
%   submit_gains(7.1, 0.6, 0.9)
%   submit_gains(7.1, 0.6, 0.9, 'Red Baron')
%   submit_gains(..., 'Open', false)        print the link, do not open it
%
% Checks your gains against the same envelope the rig-side tool uses, then
% opens the unit's submission form with all four boxes already filled in. You
% press Submit yourself, so you see what goes out under your name.
%
% It does not open a window when MATLAB is running with -batch, and 'Open',
% false stops it too. Automated checks call this function repeatedly, and a
% browser tab per call is somebody else's afternoon.
%
% The name you give is the name on screen when your gains are flown. An alias
% is fine, and a good one is encouraged. Your University account is recorded by
% the form separately and is never shown to the room.
%
% If your gains are outside the envelope you are told which limit they missed
% and no link is produced. Nothing is quietly adjusted into range: gains that
% were changed without telling you would put a flight on screen under your name
% that was not yours.
%
% The plant is the elevation axis, fitted from a measured step response:
%
%     G(s) = eps(s)/V(s) = K wn^2 / (s^2 + 2 zeta wn s + wn^2)
%
% stable, but so lightly damped that a disturbance takes about a minute to die
% away. Fitting K, wn and zeta is the first half of the session.

arguments
    kp (1,1) double
    ki (1,1) double
    kd (1,1) double
    displayName (1,:) char = defaultName()
    opts.Open (1,1) logical = ~batchStartupOptionUsed
end

plant = heli_plant();
env   = heli_envelope();

fprintf('\nChecking against the fitted elevation model:\n');
fprintf('  K = %g deg/V,  wn = %g rad/s,  zeta = %g\n', plant.K, plant.wn, plant.zeta);
if isfield(env, 'trimSource')
    fprintf('  trim %.1f V, %s\n', env.vElevTrim, env.trimSource);
end

[ok, why, m] = heli_check_one(kp, ki, kd, plant, env);

if isfield(m, 'damping')
    fprintf('\n  damping       %.3f   (needs %.2f or more)\n', m.damping, env.dampingMin);
end
if isfield(m, 'phase_margin')
    fprintf('  phase margin  %.1f deg (needs %g or more)\n', m.phase_margin, env.phaseMarginMin);
end
if isfield(m, 'peak_volts')
    fprintf('  peak demand   %.1f V   (allowed up to %.1f)\n', m.peak_volts, env.voltagePeakMax);
end
if isfield(m, 'settle_s')
    fprintf('  settles in    %.1f s   (allowed up to %g)\n', m.settle_s, env.settleMaxS);
end

if ~ok
    fprintf(2, '\n  NOT submitted: %s\n', why);
    fprintf(['\n  Nothing has been sent. Change your gains and run this again.\n' ...
             '  If you are stuck, more derivative gain buys damping, and more\n' ...
             '  proportional gain on its own does not.\n\n']);
    url = '';
    return
end

url = gain_form_url(kp, ki, kd, displayName);
fprintf('\n  Inside the envelope. Submitting as: %s\n', strtrim(displayName));
fprintf('\n  <a href="%s">Open the form with your gains filled in</a>\n', url);
fprintf('  (or copy this link)\n  %s\n\n', url);

if opts.Open
    try
        web(url, '-browser');
    catch
        % MATLAB Online may not be allowed to open a window. The printed link
        % above is the fallback, and it is printed first for that reason.
    end
end
end


function n = defaultName()
%DEFAULTNAME  Something to put on screen if they did not choose one.
[~, n] = system('whoami');
n = strtrim(n);
if isempty(n) || numel(n) > 24
    n = 'anonymous';
end
end

% tracking: status=draft version=0
