function compare_envelope(outFile)
%COMPARE_ENVELOPE  Dump this machine's verdicts so Python's can be diffed.
%
%   compare_envelope                       writes envelope-matlab.json here
%   compare_envelope('/tmp/out.json')
%
% There are two implementations of the same envelope, one in MATLAB for the
% room and one in Python for the repository, and they must never disagree.
% Cross-checking them is not optional: a set of gains accepted by one and
% refused by the other means somebody's flight depends on which tool was run.
%
% Run this, then scripts/compare_envelope.py, which reads both and reports
% every row where the verdicts differ.

if nargin < 1 || isempty(outFile)
    outFile = fullfile(fileparts(mfilename('fullpath')), 'envelope-matlab.json');
end

% Spread deliberately: comfortable designs, each limit's own failure mode,
% and the gains that were the fallback while the plant was a double
% integrator.
sets = [ ...
    0.71 0.59 0.91      % the fallback
    0.59 0.59 0.85
    0.82 0.59 0.96
    0.36 0.38 0.79
    7.13 0.20 12.6      % the old fallback: saturates the amplifier
    1.00 50.0 1.00      % integral action far too high
    0.10 0.01 0.10      % far too sluggish
    5.00 1.00 5.00
    2.00 0.50 2.00
    0.50 2.00 0.50
    60.0 1.00 1.00      % over the per-gain limit
    0.71 0.59 0.00 ];   % zero derivative

p = heli_plant();
out = struct('plant', p, 'rows', []);
rows = cell(size(sets,1), 1);
for i = 1:size(sets,1)
    [ok, why, m] = heli_check_one(sets(i,1), sets(i,2), sets(i,3), p);
    r = struct('kp', sets(i,1), 'ki', sets(i,2), 'kd', sets(i,3), ...
               'ok', logical(ok), 'why', char(why), 'metrics', m);
    rows{i} = r;
    fprintf('Kp=%6.2f Ki=%6.2f Kd=%6.2f  %-8s %s\n', ...
        sets(i,1), sets(i,2), sets(i,3), string(ok), char(why));
end
out.rows = rows;
fid = fopen(outFile, 'w');
fwrite(fid, jsonencode(out, 'PrettyPrint', true));
fclose(fid);
fprintf('\nwrote %s\n', outFile);
end

% tracking: status=draft version=0 assisted=true
