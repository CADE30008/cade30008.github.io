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


% This rig first, unless the caller asked for the shared one. There are four
% rigs in the laboratory and they do not share a model, so a file written here
% by identify_rig describes the machine you measured.
%
% The exception is a verdict about what will fly. In the first session everyone
% flies ONE rig and the gains are checked centrally against the model fitted
% from it that morning, so a local check against your own fit can pass
% something the submission then refuses. Ask for 'shared' wherever the question
% is what the hardware will do rather than what your model will do.
if nargin && (ischar(override) || isstring(override))
    if ~strcmpi(override, 'shared')
        error('heli_plant:badOption', ...
              'The only option is ''shared''. You passed ''%s''.', override);
    end
    p = fromShipped();
    return
end

if nargin && ~isempty(override)
    p = override;
    p = requireFields(p, 'the struct you passed');
    return
end

if isfile('rig_plant.json')
    p = jsondecode(fileread('rig_plant.json'));
    p = requireFields(p, 'rig_plant.json');
    return
end

p = fromShipped();
end


function p = fromShipped()
%FROMSHIPPED  The model fitted from the rig everyone flies, ignoring any local file.
here = fileparts(mfilename('fullpath'));
candidates = { fullfile(here, 'elevation_plant.json'), ...
               fullfile(here, '..', 'docs', 'L01-design-cycle', 'code', 'elevation_plant.json') };
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
