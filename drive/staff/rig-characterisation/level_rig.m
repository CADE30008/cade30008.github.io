function cal = level_rig(elevInputAtLevel, angleAtLevel)
%LEVEL_RIG  Find what this rig needs to sit level, and write it down.
%
%   level_rig(-1.6)          angle taken from the last logged sample
%   level_rig(-1.6, 27.4)    angle given by hand
%
% Every rig is a little different: the counterweight sits where somebody last
% put it, the arm has its own friction, and the encoder zeroes wherever the
% arm happened to be when the model started. So each group calibrates the one
% in front of them, and everything afterwards is measured from that.
%
% The procedure is in the laboratory notes for Part 1. In short: start the
% model with the arm **resting on the floor**, so the zero is a position the
% rig chooses rather than one you hold; raise Elevation Input until the arm
% sits level; **stop the model while it is sitting there**; then call this
% with the value that held it.
%
% Stopping first is not optional. The scopes hand elevData to the workspace
% when a run ends, not while it runs, so there is no angle to read until you
% have stopped. Stopping with the arm level leaves the level angle at the end
% of the record, which is what this takes.
%
% Writes rig_calibration.mat in the current folder. Two numbers come out of
% it, and both matter later:
%
%   elevInputAtLevel   what the loop has to hold just to stay up, which is
%                      subtracted from the head-room your controller gets
%   angleAtLevel       how far above the resting position level is, which is
%                      the offset between the encoder's zero and the datum
%                      your model is fitted about

arguments
    elevInputAtLevel (1,1) double
    angleAtLevel (1,1) double = NaN
end

if isnan(angleAtLevel)
    if ~evalin('base', 'exist(''elevData'', ''var'')')
        error('level_rig:noAngle', ...
            ['No elevation in the workspace, so the angle cannot be read.\n\n' ...
             'The scopes hand their data over when a run **ends**. Stop the\n' ...
             'model while the arm is sitting level, then run this again.\n\n' ...
             'Or give the angle yourself:  level_rig(%g, <angle>)'], elevInputAtLevel);
    end
    e = evalin('base', 'elevData');
    y = e.signals.values;
    % The end of the record is the moment you stopped, which is where the
    % arm was sitting level.
    tail = y(max(1, end - 99) : end);
    angleAtLevel = mean(tail);
    if max(tail) - min(tail) > 1.0
        fprintf(2, ['The arm was still moving %.1f deg over the last second of\n' ...
                    'the record. Let it settle before you stop, or the datum\n' ...
                    'is wherever the swing happened to be.\n'], ...
                max(tail) - min(tail));
    end
end

% The offset block is fixed by the laboratory and is not yours to change.
ELEV_OFFSET = 18;
VELEV_SAT   = 25;

cal = struct( ...
    'elevInputAtLevel', elevInputAtLevel, ...
    'angleAtLevel',     angleAtLevel, ...
    'elevOffsetBlock',  ELEV_OFFSET, ...
    'vElevTrim',        ELEV_OFFSET + elevInputAtLevel, ...
    'headroom',         VELEV_SAT - (ELEV_OFFSET + elevInputAtLevel), ...
    'when',             char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm')));

fprintf('\n  Elevation Input to hold level : %+.2f\n', cal.elevInputAtLevel);
fprintf('  Level is %+.1f deg above where it rested\n', cal.angleAtLevel);
fprintf('  So Velev trims at %.2f, and your controller has\n', cal.vElevTrim);
fprintf('  %.2f V of head-room before the demand saturates.\n\n', cal.headroom);

if cal.headroom < 4
    fprintf(2, ['That is not much room. Check the counterweight: if the arm is\n' ...
                'heavy at the rotor end, the loop spends its budget just holding\n' ...
                'the thing up. Ask a demonstrator before going on.\n\n']);
elseif cal.headroom > 12
    fprintf(2, ['That is more room than expected, which usually means the arm\n' ...
                'was not actually level. Check it by eye against the marker.\n\n']);
end

save('rig_calibration.mat', '-struct', 'cal');
fprintf('Saved rig_calibration.mat. Keep it with your recordings: the checks\n');
fprintf('use it, and a set of gains checked against the wrong rig is not\n');
fprintf('checked at all.\n');
end

% tracking: status=draft version=0 assisted=true
