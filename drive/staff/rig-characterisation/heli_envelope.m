function e = heli_envelope(cal)
%
%   heli_envelope          uses rig_calibration.mat in this folder, if there is one
%   heli_envelope(cal)     uses the calibration you pass
%
% The one per-rig number is the trim: how much of the demand range goes on
% holding the arm up before the controller gets any. Run level_rig on the
% machine in front of you and this picks it up. Without it, the reference
% rig's figure is used, which is the right order and the wrong rig.
%HELI_ENVELOPE  What we are willing to fly in a room with 190 people in it.
%
% Kept in step with Envelope in models/quanser_elevation.py. Change one and
% change the other, then run models/compare_envelope.m.

if nargin < 1 || isempty(cal)
    cal = struct([]);
    if isfile('rig_calibration.mat')
        cal = load('rig_calibration.mat');
    end
end

e = struct( ...
    'gainMax',            50, ...    % each gain, same limit on all three
    'routhMargin',        1.15, ...  % a2*a1 must beat a0 by this factor
    'dampingMin',         0.15, ...  % of the dominant closed-loop pole pair
    'phaseMarginMin',     20, ...    % degrees
    'derivativeFilterN',  10, ...    % derivative filter, Tf = Kd/(N Kp)
    'stepDeg',            7.5, ...   % the guide's standard elevation step
    'cmdRateDegS',        45, ...    % Quanser's own CMD_RATE_LIMIT, in deg/s
    'reversalsMax',       6, ...     % sign changes of the demand in one step
    'settleMaxS',         12, ...    % a flight nobody wants to watch
    'vElevSat',           25, ...   % V, the saturation Velev passes through
    'vElevTrim',          16.4, ... % V, what Velev sits at with the arm level
    'vMotorSat',          24, ...   % V, the per-motor saturation
    'safety',             0.7);     % of the headroom, kept back

% What the controller may ask for, in the units it works in.
%
% Everything here is in **Elevation Input units**, because that is what the
% fitted K is per: K = 3.4 deg/V came from stepping Elevation Input from 0 to
% 2. The signal path, measured at the rig on 22 September:
%
%   Elevation Input + elev offset (18)  ->  Velev
%   Velev  ->  saturate +/-25  ->  voltage calculations
%          ->  summed and halved with the elevation motor demand
%          ->  u_front, u_back  ->  saturate +/-24  ->  gain 1/3 to the DAC
%
% An Elevation Input of -1.6 holds the arm level, so Velev trims at 16.4 and
% each motor sits at about 8.2 V. That is the operating voltage, and it agrees
% with the 7.5 Quanser publish.
%
% Two limits could bind, and it is not the one you would expect:
%
%   Velev saturation     25 - 16.4            =  8.6
%   motor saturation     (24 - 8.2) x 2       = 31.6
%
% **Velev binds, at 8.6.** The motors have plenty of room; the demand
% saturates long before they do. This file previously worked the budget out
% from the motor rail alone, 0.7*(24-8) = 11.2, which is 1.9 times what is
% actually available, so designs were accepted that would have clipped.
if isfield(cal, 'vElevTrim') && isfinite(cal.vElevTrim)
    e.vElevTrim  = cal.vElevTrim;
    e.trimSource = 'measured on this rig';
else
    e.trimSource = 'the reference rig, not this one: run level_rig';
end

upVelev  = e.vElevSat - e.vElevTrim;
upMotor  = (e.vMotorSat - e.vElevTrim / 2) * 2;
e.voltagePeakMax = e.safety * min(upVelev, upMotor);

% Kept for anything that still reads them.
e.vMax = e.vMotorSat;
e.vOp  = e.vElevTrim / 2;
end

% tracking: status=draft version=0 assisted=true
