function submit_gains(kp, ki, kd, displayName)
%SUBMIT_GAINS  Check your PID gains, then write them out for today's flights.
%
%   submit_gains(kp, ki, kd)                uses your MATLAB account name
%   submit_gains(kp, ki, kd, 'Red Baron')   uses a name of your choosing
%
% Run this from inside the shared "submit" folder in MATLAB Drive. It writes
% one small .json file there. That folder is readable by everyone on the unit,
% so **the name you give is the name the room sees on screen** when your gains
% are flown. An alias is fine. Your real identity is never shown.
%
% Before it writes anything it runs the same checks the rig-side tool runs, so
% you find out here rather than by not appearing in the flight list. The checks
% refuse; they never quietly adjust your numbers into range. A set of gains
% that was changed without telling you would teach you the wrong lesson, and
% the room would watch a flight that was not yours.
%
% The plant is the elevation axis, a double integrator:
%
%     G(s) = eps(s) / V(s) = K / s^2
%
% with K fitted from the rig's own step response earlier in the session.

arguments
    kp (1,1) double
    ki (1,1) double
    kd (1,1) double
    displayName (1,:) char = defaultName()
end

K        = plantGain();     % rad/(V s^2), from this session's fit
GAIN_MAX = 50;              % each gain, same limit on all three
ROUTH    = 1.15;            % K*Kd*Kp must beat Ki by this factor
ZETA_MIN = 0.15;            % of the dominant closed-loop pole pair

problems = strings(0);

% 1. Finite and strictly positive. On a double integrator a gain of zero or
%    less is not a gentle controller, it is an unstable one: with no damping
%    term in the plant, every one of the three has to pull its weight.
named = struct('Kp', kp, 'Ki', ki, 'Kd', kd);
for g = ["Kp" "Ki" "Kd"]
    v = named.(g);
    if ~isfinite(v)
        problems(end+1) = g + " is not a finite number";                    %#ok<AGROW>
    elseif v <= 0
        problems(end+1) = g + " must be greater than zero, got " + v;       %#ok<AGROW>
    elseif v > GAIN_MAX
        problems(end+1) = g + " must be at most " + GAIN_MAX + ", got " + v; %#ok<AGROW>
    end
end

% 2. Routh on s^3 + K*Kd*s^2 + K*Kp*s + K*Ki = 0. This loop is *conditionally
%    stable*: scale every gain by alpha and the condition becomes
%    alpha*K*Kd*Kp > Ki, so it is stable for large alpha and unstable for
%    small. Turning the gain down is what breaks it, which is the opposite of
%    the usual reflex.
if isempty(problems)
    ratio = K * kd * kp / ki;
    if ratio <= 1
        problems(end+1) = sprintf(['unstable: needs K*Kd*Kp > Ki, but the ratio ' ...
            'is %.2f'], ratio);
    elseif ratio < ROUTH
        problems(end+1) = sprintf(['too close to unstable: K*Kd*Kp beats Ki by ' ...
            'only %.2f, and we fly nothing under %.2f'], ratio, ROUTH);
    end
end

% 3. Damping of the dominant pair, so the arm does not spend the flight
%    ringing at the ceiling of its travel.
zeta = NaN;
if isempty(problems)
    poles = roots([1, K*kd, K*kp, K*ki]);
    cplx  = poles(abs(imag(poles)) > 1e-9);
    if ~isempty(cplx)
        dominant = cplx(imag(cplx) > 0);
        [~, i]   = max(real(dominant));
        p        = dominant(i);
        zeta     = -real(p) / abs(p);
        if zeta < ZETA_MIN
            problems(end+1) = sprintf(['too lightly damped: zeta = %.3f, and we ' ...
                'fly nothing under %.2f'], zeta, ZETA_MIN);
        end
    end
end

fprintf('\n  Kp = %-8.4g Ki = %-8.4g Kd = %-8.4g   (K = %.4g)\n', kp, ki, kd, K);
if ~isempty(problems)
    fprintf(2, '  NOT submitted. %d problem(s):\n', numel(problems));
    for i = 1:numel(problems)
        fprintf(2, '    - %s\n', problems(i));
    end
    fprintf('  Change the gains and run this again.\n\n');
    return
end

file = fullfile(pwd, "gains_" + matlab.lang.makeValidName(displayName) + ".json");
payload = struct('name', displayName, 'kp', kp, 'ki', ki, 'kd', kd);
fid = fopen(file, 'w');
if fid < 0
    error('submit_gains:cannotWrite', ...
        ['Could not write to\n    %s\nAre you inside the shared submit folder, ' ...
         'and is MATLAB Drive connected?'], pwd);
end
closeFile = onCleanup(@() fclose(fid));
fprintf(fid, '%s\n', jsonencode(payload, PrettyPrint = true));

fprintf('  Accepted');
if ~isnan(zeta); fprintf(', closed-loop zeta = %.2f', zeta); end
fprintf('.\n  Written as "%s" to\n    %s\n', displayName, file);
fprintf('  That name is what the room will see. Run again to overwrite it.\n\n');
end


function name = defaultName()
%DEFAULTNAME  Something recognisable, if no alias was given.
name = getenv('USER');
if isempty(name); name = getenv('USERNAME'); end
if isempty(name); name = 'anonymous'; end
end


function K = plantGain()
%PLANTGAIN  This session's fitted K, or a refusal.
%
% There is no fallback value on purpose. A flight report produced against an
% invented plant reads exactly like a real one, so the tool would rather stop.
if evalin('base', 'exist(''K_fitted'', ''var'')')
    K = evalin('base', 'K_fitted');
    return
end
error('submit_gains:noPlant', ...
    ['No fitted plant found. Run the system identification first, so that ' ...
     'K_fitted\nexists in the workspace. Do not guess a value: gains checked ' ...
     'against the wrong\nplant pass and then fly badly.']);
end
