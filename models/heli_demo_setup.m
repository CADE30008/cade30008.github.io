%HELI_DEMO_SETUP  Workspace parameters for the open-loop flight attempt.
%
% Run this once before opening the model. Every block in the model reads its
% settings from the variables below rather than carrying numbers of its own,
% so the limits can be read, reviewed and changed here instead of by clicking
% through dialogs with a room watching.
%
%   >> heli_demo_setup
%   >> open_system('heli_demo')
%
% The model itself is built by hand from the laboratory's part1_identify. What
% this script fixes is everything that makes it safe and repeatable:
% saturations, joystick scaling and the logging that feeds the students' data.
%
% Nothing here has been run against the rig or against QUARC. The numbers come
% from heli_envelope, from the calibration level_rig writes, and from the
% Quanser 3-DOF Helicopter Laboratory Guide; what has not been checked is
% whether a model wired to them behaves as the comments say. The joystick
% block is the part with no evidence behind it at all.

%% Where the numbers come from ------------------------------------------
% The envelope is the single definition, so this file cannot describe a
% different rig from the one heli_check_one is refusing gains against.
env = heli_envelope();

%% Timing ---------------------------------------------------------------
Ts          = 0.002;          % s, controller sample time (500 Hz)
Ts_log      = 0.01;           % s, logging decimated to 100 Hz: enough to see
                              % a 6 s oscillation, small enough to hand out

%% The voltage path -----------------------------------------------------
% Measured at the rig on 22 September and written up in heli_envelope:
%
%   Elevation Input + ELEV_OFFSET  ->  Velev
%   Velev  ->  saturate +/-VELEV_SAT  ->  voltage calculations
%          ->  summed and halved with the elevation motor demand
%          ->  u_front, u_back  ->  saturate +/-VMOTOR_SAT  ->  1/K_AMP to the DAC
%
% Saturate the **total**, not the increment the controller adds. The
% controller's output rides on top of the trim that holds the arm level, so
% the usable swing is not symmetric about zero, and a limit applied to the
% increment is wrong in one direction.
ELEV_OFFSET = 18;             % the laboratory's fixed offset block
VELEV_SAT   = env.vElevSat;   % V, 25
VMOTOR_SAT  = env.vMotorSat;  % V, 24, per motor
K_AMP       = 3;              % VoltPAQ-X2 gain
VMAX_DAC    = 10;             % V, DAQ card output limit

VELEV_TRIM  = env.vElevTrim;  % V, what Velev sits at with the arm level
VOP         = env.vOp;        % V, so what each motor sits at

% Two limits could bind, and it is Velev, not the motor rail. The head-room
% above trim is VELEV_SAT - VELEV_TRIM, about 8.6 V, against (VMOTOR_SAT -
% VOP)*2, about 31.6. A budget worked out from the motor rail alone is nearly
% twice what the demand path will actually pass.
HEADROOM    = VELEV_SAT - VELEV_TRIM;
V_PEAK_MAX  = env.voltagePeakMax;   % V, the safety fraction of the head-room
V_MIN       = 0;              % V, never drive a motor backwards in the room
V_MAX       = min(VMOTOR_SAT, VMAX_DAC * K_AMP);   % V, 24

%% Travel limits --------------------------------------------------------
% Refuse, never clamp, is the rule for *gains*. These are different: they are
% the physical envelope of the rig, and hitting them is a normal part of an
% open-loop flight attempt going wrong in front of everybody.
%
% Degrees, not radians, because the laboratory model brings elevation out as
% Elev(deg) and everything downstream of it is in degrees. The names carry the
% unit so that a limit dropped into the wrong saturation block is visible in
% the dialog rather than a factor of 57 later.
%
% Both frames are here because they are easy to confuse and the confusion is
% 27 degrees wide. The travel figures are the guide's, about level. The
% encoder, though, is zeroed wherever the arm was when the model started, and
% the laboratory's Part 1 starts it resting on the floor, so the encoder reads
% about zero at the bottom stop and about +27 at level. level_rig measures
% that offset on the rig in front of you.
ELEV_BELOW_LEVEL_DEG = 27.5;  % down from level to the lower stop
ELEV_ABOVE_LEVEL_DEG = 30.0;  % up from level
PITCH_LIM_DEG        = 45.0;  % either side
RATE_LIM_DEG_S       = env.cmdRateDegS;   % 45, Quanser's own CMD_RATE_LIMIT

cal = struct([]);
if isfile('rig_calibration.mat')
    cal = load('rig_calibration.mat');
end
if isfield(cal, 'angleAtLevel') && isfinite(cal.angleAtLevel)
    LEVEL_DEG = cal.angleAtLevel;         % where level sits in encoder units
else
    LEVEL_DEG = NaN;
end
ELEV_MIN_DEG = LEVEL_DEG - ELEV_BELOW_LEVEL_DEG;
ELEV_MAX_DEG = LEVEL_DEG + ELEV_ABOVE_LEVEL_DEG;

%% Joysticks ------------------------------------------------------------
% Two controllers, so a volunteer flies with one hand on each and the room can
% see that it takes both. Quanser's own block is
%   quarc_library/Devices/Peripherals/Target/Game Controller
% with the controller index as its first parameter.
%
% None of this has been on a rig. The scalings below are guesses at what makes
% the machine controllable enough to be worth failing at, and they are the
% first thing to change if the attempt is either impossible or too easy.
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
% Mirrors models/heli_check_one.m and scripts/gains.py. Anything flown has
% already passed these; they are repeated in the model as a last line.
GAIN_MAX    = env.gainMax;
ERR_INT_SAT = env.stepDeg;    % deg s, anti-windup limit on the integrator: a
                              % full step's worth of error for one second

%% Where the session's files go ----------------------------------------
% The layout is teaching/matlab-drive.md. DATA_DIR is the folder shared with
% the cohort view-only, and it is the only one this session writes to.
% Submissions come back through the form, not through a folder, so there is
% nothing here to write to and nothing to be careful about not writing to.
home = getenv('HOME');
if isempty(home); home = getenv('USERPROFILE'); end
DRIVE_ROOT  = fullfile(home, 'MATLAB-Drive', 'Teaching', 'cade30008-students');
DATA_DIR    = fullfile(DRIVE_ROOT, 'w01-design-cycle', 'data');

%% What was just set ----------------------------------------------------
fprintf('heli_demo_setup: Ts %.0f Hz, log %.0f Hz\n', 1/Ts, 1/Ts_log);
fprintf('  Velev trims at %.1f V, saturates at %.0f: %.1f V of head-room,\n', ...
    VELEV_TRIM, VELEV_SAT, HEADROOM);
fprintf('  of which %.1f V is the most a controller may ask for\n', V_PEAK_MAX);
fprintf('  trim from %s\n', env.trimSource);
if isnan(LEVEL_DEG)
    fprintf(2, ['  NO rig_calibration.mat in %s\n' ...
                '  The travel limits are %+.1f to %+.1f deg about LEVEL, and the\n' ...
                '  encoder zero is wherever the arm was when the model started.\n' ...
                '  Run level_rig before trusting ELEV_MIN_DEG and ELEV_MAX_DEG.\n'], ...
        pwd, -ELEV_BELOW_LEVEL_DEG, ELEV_ABOVE_LEVEL_DEG);
else
    fprintf('  level reads %+.1f deg on this rig''s encoder, so travel is\n', LEVEL_DEG);
    fprintf('  %+.1f to %+.1f deg as logged\n', ELEV_MIN_DEG, ELEV_MAX_DEG);
end
fprintf('  pitch +/-%.0f deg, demand rate limit %.0f deg/s\n', ...
    PITCH_LIM_DEG, RATE_LIM_DEG_S);
fprintf('  joysticks %d and %d\n', JOY_COLLECTIVE, JOY_DIFFERENTIAL);
if ~isfolder(DATA_DIR)
    fprintf(2, '  NOTE: %s does not exist yet. Make it before the session.\n', DATA_DIR);
end
