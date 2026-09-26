function check_scopes(model)
%CHECK_SCOPES  What every scope in a model is logging, and whether it is
%              throwing the beginning away.
%
%   check_scopes('part1_identify')
%   check_scopes                    whatever is open
%
% The setting this is really about is "Limit data points to last N", in the
% scope's View > Configuration Properties > Logging tab. With it on, a long
% run keeps only the tail, so a step early in the run is simply not in the
% file you saved, and the fit refuses with no clue why.
%
% Reading it here beats clicking through four scopes, and tells you the
% variable names at the same time.
%
% The decimation column is what the block is set to, and is not necessarily
% what you get. A recording taken from the rig on 22 September came back at
% 1000 Hz from scopes set to decimate by 49, so external mode appears to
% ignore it. Trust the sample count in the file over this column.

if nargin < 1 || isempty(model)
    open = find_system('type', 'block_diagram');
    open = setdiff(open, {'simulink'});
    if isempty(open); error('check_scopes:none', 'No model open. Pass a name.'); end
    model = open{1};
end
if ~bdIsLoaded(model); load_system(model); end

scopes = find_system(model, 'LookUnderMasks', 'all', 'FollowLinks', 'on', ...
                     'BlockType', 'Scope');
if isempty(scopes)
    fprintf('%s has no scopes.\n', model); return
end

fprintf('\n%s\n%s\n', model, repmat('-', 1, numel(model)));
fprintf('%-22s %-14s %-9s %-10s %s\n', 'scope', 'variable', 'logging', 'limited', 'decimation');
trouble = false;
for i = 1:numel(scopes)
    c = get_param(scopes{i}, 'ScopeConfiguration');
    name = get_param(scopes{i}, 'Name');
    name = regexprep(name, '\s+', ' ');
    if ~c.DataLogging
        fprintf('%-22s %-14s %-9s\n', name, '-', 'off');
        continue
    end
    lim = c.DataLoggingLimitDataPoints;
    limTxt = 'no';
    if lim
        limTxt = sprintf('last %g', c.DataLoggingMaxPoints);
        trouble = true;
    end
    fprintf('%-22s %-14s %-9s %-10s %g\n', name, c.DataLoggingVariableName, ...
        'on', limTxt, c.DataLoggingDecimation);
end

if trouble
    fprintf(2, ['\nAt least one scope keeps only the last N points. On a long run\n' ...
                'that throws the beginning away, including any step you made\n' ...
                'early on. Turn it off in View > Configuration Properties >\n' ...
                'Logging, or from here:\n\n']);
    fprintf(2, ['  for b = find_system(''%s'',''BlockType'',''Scope'')''\n' ...
                '      c = get_param(b{1},''ScopeConfiguration'');\n' ...
                '      c.DataLoggingLimitDataPoints = false;\n' ...
                '  end\n\n'], model);
else
    fprintf('\nNo scope is limiting its data. A short recording is not this.\n');
end
end

% tracking: status=draft version=0 assisted=true
