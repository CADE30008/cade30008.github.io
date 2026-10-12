function cal = rig_calibration(elevInputAtLevel, angleAtLevel)
%RIG_CALIBRATION  What this rig costs to hold up, from one steady reading.
%
%   cal = rig_calibration(-1.6)         Elevation Input that held it steady
%   cal = rig_calibration(-1.6, 27.4)   and how far above the floor that was
%
% Every rig is a little different: the counterweight sits where somebody last
% put it, and the arm has its own friction. So each group measures the one in
% front of them and everything afterwards is taken from that.
%
% This used to be a separate levelling step, holding the arm level by hand and
% reading off the input that held it. It does not need to be. The end of any
% step recording is the arm sitting still under a constant input, which is the
% same measurement about the trim the model is fitted at, and it costs nothing
% extra to take.

arguments
    elevInputAtLevel (1,1) double
    angleAtLevel (1,1) double = NaN
end

% Fixed by the laboratory wiring, and not yours to change.
ELEV_OFFSET = 18;
VELEV_SAT   = 25;

cal = struct( ...
    'elevInputAtLevel', elevInputAtLevel, ...
    'angleAtLevel',     angleAtLevel, ...
    'elevOffsetBlock',  ELEV_OFFSET, ...
    'vElevSat',         VELEV_SAT, ...
    'vElevTrim',        ELEV_OFFSET + elevInputAtLevel, ...
    'headroom',         VELEV_SAT - (ELEV_OFFSET + elevInputAtLevel), ...
    'when',             char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm')));
end
