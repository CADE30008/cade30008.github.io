%HELI_DEMO_SETUP  Workspace parameters for the week 1 Quanser demonstration.
%
% Run this once before opening the model. Every block in the model reads its
% settings from the variables below rather than carrying numbers of its own,
% so the limits can be read, reviewed and changed here instead of by clicking
% through dialogs with a room watching.
%
%   >> heli_demo_setup
%   >> open_system('heli_demo')
%
% The model itself is built by hand from the existing laboratory file. What
% this script fixes is everything that makes it safe and repeatable:
% saturations, joystick scaling and the logging that feeds the students' data.
%
% Hardware figures are from the Quanser 3-DOF Helicopter Laboratory Guide; the
% envelope is the one scripts/gains.py enforces, so the two cannot disagree.

%% Timing ---------------------------------------------------------------
Ts          = 0.002;          % s, controller sample time (500 Hz)
Ts_log      = 0.01;           % s, logging decimated to 100 Hz: enough to see
                              % a 6 s oscillation, small enough to hand out

%% Amplifier and motors -------------------------------------------------
K_AMP       = 3;              % VoltPAQ-X2 gain
VMAX_DAC    = 10;             % V, DAQ card output limit
VMAX_AMP    = 24;             % V, peak motor voltage

% The controller output rides on top of Vop, the voltage that holds the arm
% level, so the usable swing is NOT symmetric about zero. Saturate on the
% total, not on the increment, or the limit is wrong in one direction.
Vop         = 8.0;            % V, trim. Set this from the rig on the day.
                              % Matches heli_envelope's vOp. Quanser publish
                              % about 7.5; 8 keeps the headroom conservative.
V_MIN       = 0;              % V, never drive a motor backwards in the room
V_MAX       = min(VMAX_AMP, VMAX_DAC * K_AMP);   % V, 24

%% Travel limits --------------------------------------------------------
% Refuse, never clamp, is the rule for *gains*. These are different: they are
% the physical envelope of the rig, and hitting them is a normal part of an
% open-loop flight attempt going wrong in front of everybody.
ELEV_MIN    = deg2rad(-27.5); % rad, arm on the lower stop
ELEV_MAX    = deg2rad( 30.0); % rad
PITCH_LIM   = deg2rad( 45.0); % rad, either side
RATE_LIM    = deg2rad( 45.0); % rad/s, on the commanded elevation

%% Joysticks ------------------------------------------------------------
% Two controllers, so a volunteer flies with one hand on each and the room can
% see that it takes both. Quanser's own block is
%   quarc_library/Devices/Peripherals/Target/Game Controller
% with the controller index as its first parameter.
JOY_COLLECTIVE = 1;           % controller index: both motors together
JOY_DIFFERENTIAL = 2;         % controller index: one against the other

JOY_DEADZONE   = 0.08;        % fraction of full travel ignored around centre;
                              % cheap sticks drift, and a drifting stick looks
                              % like a control problem from the back of a room
JOY_GAIN_COLL  = 2.0;         % V per unit stick, added to both motors
JOY_GAIN_DIFF  = 1.5;         % V per unit stick, added to one and subtracted
                              % from the other
JOY_RATE_LIM   = 8.0;         % V/s, so a stick slammed to its stop does not
                              % arrive at the motor as a step

%% Controller envelope --------------------------------------------------
% Mirrors models/quanser_elevation.py and scripts/gains.py. Anything flown has
% already passed these; they are repeated in the model as a last line.
GAIN_MAX    = 50;
ERR_INT_SAT = 7.5;            % integrator anti-windup limit

%% Where the session's files go ----------------------------------------
% Set DRIVE_ROOT to the MATLAB Drive folder that syncs to this machine. The
% layout is the one in teaching/matlab-drive.md; nothing here writes into
% submit/, which the whole cohort can read.
home = getenv('HOME');
if isempty(home); home = getenv('USERPROFILE'); end
DRIVE_ROOT  = fullfile(home, 'MATLAB Drive', 'CADE30008', '2026-27', 'w01-design-cycle');
DATA_DIR    = fullfile(DRIVE_ROOT, 'data');     % view only, handed out
SUBMIT_DIR  = fullfile(DRIVE_ROOT, 'submit');   % writable, never written to

fprintf('heli_demo_setup: Ts %.0f Hz, log %.0f Hz, V in [%.1f, %.1f] about Vop %.1f\n', ...
    1/Ts, 1/Ts_log, V_MIN, V_MAX, Vop);
fprintf('  elevation %+.1f to %+.1f deg, pitch +/-%.0f deg, joysticks %d and %d\n', ...
    rad2deg(ELEV_MIN), rad2deg(ELEV_MAX), rad2deg(PITCH_LIM), ...
    JOY_COLLECTIVE, JOY_DIFFERENTIAL);
if ~isfolder(DATA_DIR)
    fprintf(2, '  NOTE: %s does not exist yet. Make it before the session.\n', DATA_DIR);
end
