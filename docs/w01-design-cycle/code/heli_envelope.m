function e = heli_envelope()
%HELI_ENVELOPE  What we are willing to fly in a room with 190 people in it.
%
% Kept in step with Envelope in models/quanser_elevation.py. Change one and
% change the other, then run models/compare_envelope.m.

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
    'vMax',               24, ...    % V the amplifier can deliver
    'vOp',                8);        % V that holds the arm at trim

% The controller may use what is left once the operating point is paid for,
% with a third held back because the rig's own K is a fit and not a constant.
e.voltagePeakMax = 0.7 * (e.vMax - e.vOp);
end
