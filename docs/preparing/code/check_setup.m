% Check your MATLAB and Simulink set-up for CADE30008.
%
% Run it in MATLAB on your own computer or in MATLAB Online. It should finish
% by printing "All checks passed", draw one step-response plot, and build and
% simulate a small Simulink model.

passed = true;

v = ver('MATLAB');
passed = report('MATLAB', true, sprintf('%s %s', v.Version, v.Release)) && passed;

hasControl = license('test', 'Control_Toolbox') && ~isempty(ver('control'));
passed = report('Control System Toolbox', hasControl) && passed;
hasSimulink = license('test', 'Simulink') && ~isempty(ver('simulink'));
passed = report('Simulink', hasSimulink) && passed;

if hasControl
    % The pitch-attitude loop from week 3, with a proportional gain of 1.
    G = tf(40, [1 12 20 0]);
    [gm, pm, ~, wc] = margin(G);
    ok = abs(pm - 43.21) < 0.05 && abs(wc - 1.559) < 0.005 && abs(gm - 6.0) < 0.01;
    passed = report('loop margins', ok, sprintf( ...
        'phase margin %.2f deg at %.3f rad/s, gain margin %.2f', pm, wc, gm)) && passed;

    % The closed loop follows a step with no steady-state error.
    T = feedback(G, 1);
    passed = report('closed loop', abs(dcgain(T) - 1) < 1e-9, ...
        sprintf('steady-state gain %.3f', dcgain(T))) && passed;

    figure
    step(T, 10)
    title('Set-up check: closed-loop step response')
    grid on
end

if hasSimulink
    % Build the same loop in Simulink and simulate it.
    mdl = 'cade30008_check';
    if bdIsLoaded(mdl)
        close_system(mdl, 0);
    end
    new_system(mdl);
    add_block('simulink/Sources/Step', [mdl '/Step'], 'Time', '0');
    add_block('simulink/Math Operations/Sum', [mdl '/Sum'], 'Inputs', '+-');
    add_block('simulink/Math Operations/Gain', [mdl '/Kp'], 'Gain', '1');
    add_block('simulink/Continuous/Transfer Fcn', [mdl '/G'], ...
        'Numerator', '40', 'Denominator', '[1 12 20 0]');
    add_block('simulink/Sinks/Out1', [mdl '/theta']);
    add_line(mdl, 'Step/1', 'Sum/1');
    add_line(mdl, 'Sum/1', 'Kp/1');
    add_line(mdl, 'Kp/1', 'G/1');
    add_line(mdl, 'G/1', 'theta/1');
    add_line(mdl, 'G/1', 'Sum/2');
    set_param(mdl, 'StopTime', '30', 'SaveOutput', 'on', 'OutputSaveName', 'yout', ...
        'SaveFormat', 'Dataset', 'ReturnWorkspaceOutputs', 'on');
    Simulink.BlockDiagram.arrangeSystem(mdl);

    out = sim(mdl);
    theta = out.yout{1}.Values.Data;
    passed = report('Simulink simulation', abs(theta(end) - 1) < 1e-3, ...
        sprintf('final pitch attitude %.3f', theta(end))) && passed;

    if usejava('desktop')
        open_system(mdl);   % leave it open to look at; close without saving
    else
        close_system(mdl, 0);
    end
end

if passed
    disp('All checks passed')
else
    disp('Some checks failed: see the lines marked FAIL')
end

function ok = report(label, ok, detail)
    if nargin < 3
        detail = '';
    end
    status = 'ok';
    if ~ok
        status = 'FAIL';
    end
    if isempty(detail)
        fprintf('[%s] %s\n', status, label);
    else
        fprintf('[%s] %s: %s\n', status, label, detail);
    end
end

% tracking: status=draft version=0
