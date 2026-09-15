% PITCH_CHECK  Recompute the Lecture 2 design numbers in MATLAB.
%
% Reads the gains from models/pitch_numbers.json (written by models/pitch.py),
% recomputes every linear metric with the Control System Toolbox, and writes
% models/pitch_numbers_matlab.json. models/compare.py checks the two agree.
%
% Run from the repository root:
%   matlab -batch "run('models/pitch_check.m')"

here = fileparts(mfilename('fullpath'));
py = jsondecode(fileread(fullfile(here, 'pitch_numbers.json')));

s = tf('s');
G = 40 / (s * (s + 2) * (s + 10));      % pitch attitude / elevator, rad/rad
N = py.N;
step10 = deg2rad(10);
t = linspace(0, 8, 8001);

out = struct();
names = fieldnames(py.designs);
for k = 1:numel(names)
    d = py.designs.(names{k});
    if d.Kd > 0
        Tf = d.Kd / (N * d.Kp);
    else
        Tf = 0;
    end
    C = pid(d.Kp, d.Ki, d.Kd, Tf);      % Kp + Ki/s + Kd s/(Tf s + 1)
    Cr = pid(d.Kp, d.Ki);               % the reference sees P and I only
    L = C * G;
    [Gm, Pm, Wcg, Wcp] = margin(L);
    Tref = minreal(Cr * feedback(G, C), 1e-6);
    Tu = minreal(Cr * feedback(1, L), 1e-6);
    Tdist = minreal(feedback(G, C), 1e-6);
    info = stepinfo(Tref, 'SettlingTimeThreshold', 0.02, 'RiseTimeLimits', [0.1 0.9]);
    u = step(Tu, t) * step10;
    r.GM = Gm;
    r.GM_dB = 20 * log10(Gm);
    r.PM_deg = Pm;
    r.wc = Wcp;
    r.w180 = Wcg;
    r.rise_time = info.RiseTime;
    r.overshoot_pct = info.Overshoot;
    r.settling_time = info.SettlingTime;
    r.peak_elevator_deg_per_10deg_step = rad2deg(max(abs(u)));
    r.dist_final_per_unit = dcgain(Tdist);
    out.designs.(names{k}) = r;
end

% Derivative kick: filtered D acting on the error, PD design, 10 deg step.
d = py.designs.PD;
Cpd = pid(d.Kp, 0, d.Kd, d.Kd / (N * d.Kp));
uerr = step(feedback(Cpd, G), linspace(0, 1, 10001)) * step10;
out.kick.peak_elevator_deg_D_on_error = rad2deg(max(abs(uerr)));

fid = fopen(fullfile(here, 'pitch_numbers_matlab.json'), 'w');
fprintf(fid, '%s\n', jsonencode(out, 'PrettyPrint', true));
fclose(fid);
fprintf('Wrote %s\n', fullfile(here, 'pitch_numbers_matlab.json'));
