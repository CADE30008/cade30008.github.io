function save_rig(K, wn, zeta, cal, fromFile)
%SAVE_RIG  Write this rig's model and calibration beside your recordings.
%
%   save_rig(K, wn, zeta, cal, 'step-2V.mat')
%
% Two files, because two different things read them:
%
%   rig_plant.json        heli_plant reads it, so every check and every
%                         simulation is against the machine you measured
%   rig_calibration.mat   heli_envelope reads it, for the voltage head-room
%
% There are four rigs in the laboratory and they do not share a model. The
% repository ships one fitted plant as a worked example; a file written here
% describes the machine in front of you and takes precedence over it.

arguments
    K (1,1) double
    wn (1,1) double
    zeta (1,1) double
    cal (1,1) struct
    fromFile (1,:) char = ''
end

if ~(K > 0) || ~(wn > 0) || ~(zeta > 0 && zeta < 1)
    error('save_rig:badFit', ...
        ['Refusing to save K=%g, wn=%g, zeta=%g. The fitted axis is ' ...
         'underdamped and pushes the arm up, so all three should be ' ...
         'positive and zeta below 1. Check the fit before saving it.'], K, wn, zeta);
end

plant = struct('K', K, 'wn', wn, 'zeta', zeta, ...
               'fittedFrom', fromFile, 'when', cal.when);
fid = fopen('rig_plant.json', 'w');
if fid < 0
    error('save_rig:cannotWrite', 'Cannot write rig_plant.json in %s', pwd);
end
closer = onCleanup(@() fclose(fid));
fprintf(fid, '%s\n', jsonencode(plant, 'PrettyPrint', true));

fprintf('\n  rig_plant.json        K = %.3f, wn = %.3f, zeta = %.4f\n', K, wn, zeta);

% The calibration is held back when it disagrees sharply with the rig as
% measured by hand, because it decides how much voltage a controller may ask
% for and writing it is how a design gets refused or allowed.
%
% The open question: a recording's Elevation Input starts at zero with the arm
% resting on the floor, so the value it settles at is the input holding it at
% that elevation. Read that way this sample implies a trim of 20 V and 5 V of
% head-room. Measured by hand at the rig on 22 September, with the arm level,
% it was 16.4 V and 8.6 V. Those cannot both describe the same machine at the
% same operating point, and until somebody says which reading is the absolute
% Elevation Input, writing either one silently is worse than writing neither.
REFERENCE_TRIM = 16.4;
if abs(cal.vElevTrim - REFERENCE_TRIM) > 2
    fprintf(2, ['  rig_calibration.mat   NOT written\n\n' ...
        '  This recording implies Velev trims at %.2f V, leaving %.2f V.\n' ...
        '  Measured by hand at the rig it was %.1f V, leaving %.1f V.\n\n' ...
        '  Those are too far apart to choose between here, and the number\n' ...
        '  decides how much voltage your controller is allowed. Until it is\n' ...
        '  settled the checks use the reference rig, which they will say so.\n' ...
        '  Tell a demonstrator what this recording gave.\n'], ...
        cal.vElevTrim, cal.headroom, REFERENCE_TRIM, 25 - REFERENCE_TRIM);
    return
end

save('rig_calibration.mat', '-struct', 'cal');
fprintf('  rig_calibration.mat   trim %.2f V, head-room %.2f V\n', ...
    cal.vElevTrim, cal.headroom);
fprintf('\n  Keep both with the recordings they came from. A set of gains\n');
fprintf('  checked against another rig is not checked at all.\n');
end
