function m = heli3d_model()
%HELI3D_MODEL  Linearised state-space model of the whole machine.
%
%   m = heli3d_model
%
% Six states, two inputs, three measured outputs:
%
%   x = [elevation; pitch; travel; elevation rate; pitch rate; travel rate]
%   u = [front motor voltage; back motor voltage]
%   y = [elevation; pitch; travel]
%
% Angles in radians here, because the model is written in radians. Convert on
% the way out if you want degrees, and be consistent about it.
%
% This is the manufacturer's linearisation, taken about level flight, from
% their published physical constants. Read what it says before you use it:
%
%   B(4,:) is the same for both motors, so elevation comes from their SUM.
%   B(5,:) is equal and opposite, so pitch comes from their DIFFERENCE.
%   B(6,:) is zero, so travel is not commanded at all.
%   A(6,2) is not zero, so travel accelerates because of PITCH.
%
% That last pair is the coupling, and it is the whole difficulty of flying
% three axes: to go somewhere you tilt, and tilting is also how you stop.
%
% A(4,1) is zero, so there is no restoring term on elevation and this model
% makes that axis a double integrator. That is a consequence of linearising
% about level, where gravity stiffness is exactly zero. Measured about a trim
% the same axis oscillates, which is why the single-axis work uses a fitted
% second order instead. Both are right about the point they describe.

p = params();

A = zeros(6);
A(1,4) = 1;                 % d/dt elevation = elevation rate
A(2,5) = 1;                 % d/dt pitch     = pitch rate
A(3,6) = 1;                 % d/dt travel    = travel rate
A(6,2) = (2*p.m_f*p.La - p.m_w*p.Lw) * p.g / ...
         (2*p.m_f*p.La^2 + 2*p.m_f*p.Lh^2 + p.m_w*p.Lw^2);

B = zeros(6,2);
be = p.La * p.Kf / (p.m_w*p.Lw^2 + 2*p.m_f*p.La^2);
bp = 0.5 * p.Kf / (p.m_f * p.Lh);
B(4,:) = [ be,  be];        % elevation: the sum
B(5,:) = [ bp, -bp];        % pitch:     the difference

C = [eye(3), zeros(3)];
D = zeros(3,2);

m = struct('A', A, 'B', B, 'C', C, 'D', D, 'params', p, ...
    'states', {{'elevation','pitch','travel','elev rate','pitch rate','travel rate'}}, ...
    'inputs', {{'front motor (V)','back motor (V)'}}, ...
    'outputs', {{'elevation (rad)','pitch (rad)','travel (rad)'}});
m.sys = ss(A, B, C, D, ...
    'StateName', m.states, 'InputName', m.inputs, 'OutputName', m.outputs);
end


function p = params()
%PARAMS  The rig's published physical constants.
%
% Manufacturer's figures for this machine. Lengths are given in inches in the
% original and converted here, which is why they look like they do.
p.Kf  = 0.1188;             % propeller force-thrust constant, N/V
p.m_h = 1.15;               % helicopter body, kg
p.m_w = 1.87;               % counterweight, kg
p.m_f = p.m_h / 2;          % front propeller assembly, kg
p.Lh  = 7.0  * 0.0254;      % pitch pivot to each motor, m
p.La  = 26.0 * 0.0254;      % elevation pivot to body, m
p.Lw  = 18.5 * 0.0254;      % elevation pivot to counterweight, m
p.g   = 9.81;
p.Vop = 7.5;                % volts that hold the arm up
p.Vmax = 24;                % what the amplifier can deliver
end
