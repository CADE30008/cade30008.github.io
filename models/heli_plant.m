function p = heli_plant(override)
%HELI_PLANT  The fitted elevation model: K (deg/V), wn (rad/s), zeta.
%
%   p = heli_plant                 read elevation_plant.json
%   p = heli_plant(struct(...))    use these numbers instead
%
% Second order, not the double integrator Quanser's own linearisation gives.
% Their model is taken about level, where gravity stiffness is exactly zero;
% the rig is flown about a trim, and there it oscillates. See
% models/quanser_elevation.py for the provenance and the open question.
%
% There is deliberately no built-in default. Gains checked against a guessed
% plant produce a report that reads exactly like a real one.

if nargin && ~isempty(override)
    p = override;
    p = requireFields(p, 'the struct you passed');
    return
end

here = fileparts(mfilename('fullpath'));
candidates = { fullfile(here, 'elevation_plant.json'), ...
               fullfile(here, '..', 'docs', 'w01-design-cycle', 'code', 'elevation_plant.json') };
for i = 1:numel(candidates)
    if isfile(candidates{i})
        p = jsondecode(fileread(candidates{i}));
        p = requireFields(p, candidates{i});
        return
    end
end
error('heli_plant:noModel', ...
    ['No fitted elevation model found. Expected one of:\n  %s\n  %s\n' ...
     'Fit the rig''s own step response with fit_second_order and write K, wn\n' ...
     'and zeta into that file.'], candidates{1}, candidates{2});
end


function p = requireFields(p, where)
%REQUIREFIELDS  Refuse a model that is missing pieces or physically wrong.
need = {'K', 'wn', 'zeta'};
missing = need(~isfield(p, need));
if ~isempty(missing)
    error('heli_plant:incomplete', ...
        ['%s has no %s.\nA model carrying only K is the old double-integrator\n' ...
         'form. The plant is second order now: refit with fit_second_order.'], ...
        where, strjoin(missing, ', '));
end
if ~(p.K > 0) || ~(p.wn > 0)
    error('heli_plant:badValues', '%s: K and wn must both be positive.', where);
end
if ~(p.zeta > 0 && p.zeta < 1)
    error('heli_plant:badDamping', ...
        ['%s: zeta is %g, outside (0, 1).\nThe fitted axis is underdamped; a ' ...
         'value outside that range means the fit failed.'], where, p.zeta);
end
end
