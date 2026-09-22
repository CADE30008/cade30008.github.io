function results = run_all_student_code()
%RUN_ALL_STUDENT_CODE  Run everything a student runs, and report what broke.
%
%   run_all_student_code
%
% Exercises both student bundles exactly as handed out, in the order a student
% meets them, and prints one line per step.
%
% This is the part of the laboratory pass that does not need the rig, so it is
% automated: bench time should not be spent watching scripts finish. The two
% interactive pieces it cannot check are in the README.
%
% Note on how it is written. Every student script opens with `clear`, which
% wipes the local variables of whatever function called it. So nothing here
% keeps state across a script's execution: the folder is changed and restored
% by the loop below, which `clear` cannot reach, and the helpers hold nothing.
% Getting this wrong made all five scripts look broken when they were fine.

here = fileparts(mfilename('fullpath'));
W = 'w01-design-cycle';
L = 'lab-quanser';

% lab1_fit needs something to fit.
labDir = fullfile(here, L);
if isempty(dir(fullfile(labDir, '*.mat')))
    src = fullfile(here, W, 'data', 'elevation-step.mat');
    if isfile(src)
        copyfile(src, fullfile(labDir, 'sample.mat'));
        fprintf('(copied a sample recording into %s so lab1_fit has one)\n', L);
    end
end

steps = {
    W, 'w01: s1_identify (fit the model)',         @(d) runScript(d, 's1_identify')
    W, 'w01: my_model.mat was written',            @(d) assertFile(fullfile(d, 'my_model.mat'))
    W, 'w01: s2_tune (three ways to tune)',        @(d) runScript(d, 's2_tune')
    W, 'w01: submit_gains accepts good gains',     @(d) mustContain('u = submit_gains(0.71, 0.59, 0.91, ''Preflight'');', 'forms.cloud.microsoft')
    W, 'w01: submit_gains refuses bad gains',      @(d) mustContain('submit_gains(7.4, 1.07, 15.2, ''Preflight'');', 'NOT submitted')
    L, 'lab: lab1_fit (fit your recordings)',      @(d) runScript(d, 'lab1_fit')
    L, 'lab: lab2_3dof (three axes, three loops)', @(d) runScript(d, 'lab2_3dof')
    L, 'lab: lab3_statespace (LQR)',               @(d) runScript(d, 'lab3_statespace')
    };

fprintf('\n%-44s %-8s %s\n', 'step', 'result', 'seconds');
fprintf('%s\n', repmat('-', 1, 72));
results = struct('step', {}, 'ok', {}, 'secs', {}, 'msg', {});
for i = 1:size(steps, 1)
    folder = fullfile(here, steps{i,1});
    home = pwd;
    t0 = tic;
    try
        cd(folder); addpath(folder);
        steps{i,3}(folder);
        ok = true; msg = '';
    catch e
        ok = false; msg = e.message;
    end
    cd(home);
    warning('off', 'MATLAB:rmpath:DirNotFound');
    rmpath(folder);
    warning('on', 'MATLAB:rmpath:DirNotFound');
    secs = toc(t0);
    results(end+1) = struct('step', steps{i,2}, 'ok', ok, 'secs', secs, 'msg', msg); %#ok<AGROW>
    fprintf('%-44s %-8s %6.1f\n', steps{i,2}, tf(ok), secs);
end

close all force
bad = ~[results.ok];
fprintf('%s\n', repmat('-', 1, 72));
fprintf('%d of %d ran. Total %.0f s.\n', nnz(~bad), numel(results), sum([results.secs]));
if any(bad)
    fprintf(2, '\nBROKEN, and students will hit these:\n');
    for r = results(bad)
        fprintf(2, '  %s\n      %s\n', r.step, strtrim(regexprep(r.msg, '\s+', ' ')));
    end
    fprintf(2, '\nSend me the lines above.\n');
else
    fprintf('\nEverything a student runs, runs. Two left, both by hand:\n');
    fprintf('  1. tune_sliders  - does the window open, do the sliders move,\n');
    fprintf('                     does the verdict change as you drag them?\n');
    fprintf('  2. submit_gains  - does the printed link open a form with your\n');
    fprintf('                     four values already in the boxes?\n');
end
end


function runScript(d, name)
%RUNSCRIPT  Run a student script by full path. Keeps no state: see the header.
evalc(sprintf('run(''%s'')', fullfile(d, [name '.m'])));
end


function assertFile(p)
if ~isfile(p); error('run_all:noFile', '%s was not created', p); end
end


function mustContain(cmd, needle)
%MUSTCONTAIN  Run a command and check what it printed.
out = evalc(cmd);
if ~contains(out, needle)
    error('run_all:missing', 'output did not contain "%s"', needle);
end
end


function s = tf(ok)
if ok; s = 'ok'; else; s = 'FAILED'; end
end
