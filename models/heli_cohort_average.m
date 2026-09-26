function avg = heli_cohort_average(flights, plant, env)
%HELI_COHORT_AVERAGE  Round 2: the room's average, checked like any other set.
%
%   avg = heli_cohort_average(flights)
%   avg = heli_cohort_average(flights, heli_plant, heli_envelope)
%
% flights is the table collate_gains returns, or any table with Kp, Ki and Kd
% in it. The average is taken over the sets that passed, because the question
% round 2 asks is what happens when you average designs that were each safe.
% Including the refused ones would answer a different and duller question.
%
% Which sets passed is decided here, by heli_check_one, and not read off a
% verdict column. A list typed in by hand when the form has failed carries
% whatever verdict was typed with it, and an average that quietly included a
% set the envelope refused would not be the average of safe designs at all.
%
% Returns a struct: kp, ki, kd, n, ok, why, metrics, and spread, the standard
% deviation of each gain across the sets averaged.
%
% The average gets the same heli_check_one every submission got. It can fail
% when every input passed: the gains that fly are not a convex set, so the
% midpoint of two acceptable designs need not be acceptable. When it fails it
% is refused like anything else. Nothing is nudged back into range to make the
% round work, and not flying it is the lesson.

arguments
    flights table
    plant struct = heli_plant()
    env struct = heli_envelope()
end

need = {'Kp', 'Ki', 'Kd'};
missing = need(~ismember(need, flights.Properties.VariableNames));
if ~isempty(missing)
    error('heli_cohort_average:badTable', ...
        ['The flight list has no %s.\nPass the table collate_gains returns.'], ...
        strjoin(missing, ', '));
end

flew = false(height(flights), 1);
for i = 1:height(flights)
    flew(i) = heli_check_one(flights.Kp(i), flights.Ki(i), flights.Kd(i), plant, env);
end
avg = struct('kp', NaN, 'ki', NaN, 'kd', NaN, 'n', nnz(flew), ...
             'ok', false, 'why', "", 'metrics', struct(), ...
             'spread', [NaN NaN NaN]);

if avg.n == 0
    avg.why = "nothing passed, so there is nothing to average";
    return
end

g = [flights.Kp(flew), flights.Ki(flew), flights.Kd(flew)];
avg.kp = mean(g(:,1));
avg.ki = mean(g(:,2));
avg.kd = mean(g(:,3));
if avg.n > 1
    avg.spread = std(g, 0, 1);
else
    avg.spread = [0 0 0];
end

[avg.ok, avg.why, avg.metrics] = heli_check_one(avg.kp, avg.ki, avg.kd, plant, env);
end

% tracking: status=draft version=0 assisted=true
