function t1_fit_this_rig(file)
%T1_FIT_THIS_RIG  Fit the rig in front of you, and say whether to trust it.
%
%   t1_fit_this_rig('my-recording.mat')
%   t1_fit_this_rig            the newest .mat in this folder
%
% Test 1 of the laboratory pass. Everything downstream is checked against
% these three numbers, so this one comes first.

if nargin < 1 || isempty(file)
    d = dir('*.mat');
    d = d(~startsWith({d.name}, '.'));
    if isempty(d); error('No .mat files here. Save one with s_save first.'); end
    [~, i] = max([d.datenum]);
    file = d(i).name;
    fprintf('Using the newest recording: %s\n', file);
end

f = fit_second_order(file);

fprintf('\n------------------------------------------------------------\n');
fprintf('  K    = %.3f deg/V\n', f.K);
fprintf('  wn   = %.3f rad/s\n', f.wn);
fprintf('  zeta = %.4f\n', f.zeta);
fprintf('------------------------------------------------------------\n');

ref = struct('K', 3.4, 'wn', 1.0, 'zeta', 0.06);
d = @(a, b) 100 * abs(a - b) / b;
fprintf('\nAgainst the stored laboratory fit (3.40 / 1.00 / 0.060):\n');
fprintf('  K    %+6.1f%%\n', d(f.K, ref.K) * sign(f.K - ref.K));
fprintf('  wn   %+6.1f%%\n', d(f.wn, ref.wn) * sign(f.wn - ref.wn));
fprintf('  zeta %+6.1f%%\n', d(f.zeta, ref.zeta) * sign(f.zeta - ref.zeta));

big = d(f.K, ref.K) > 15 || d(f.wn, ref.wn) > 15;
if big
    fprintf(2, ['\nMore than 15%% out on K or wn. That is worth a second\n' ...
                'recording before it goes into the envelope: it is either a\n' ...
                'real change in the rig or a bad record.\n']);
else
    fprintf('\nClose enough to the stored fit to use either.\n');
end

fprintf(['\nIf you are happy with it, write it into elevation_plant.json in\n' ...
         'the repository, then run:\n' ...
         '    .venv/bin/python scripts/sync_student_code.py\n']);

fprintf('\nSEND ME: these three numbers, and whether the fitter warned about\n');
fprintf('the arm already swinging.\n');
end

% tracking: status=draft version=0
