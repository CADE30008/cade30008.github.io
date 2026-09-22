function p = heli_expand_path(p)
%HELI_EXPAND_PATH  An absolute path, with a leading ~ expanded.
%
%   heli_expand_path('~/Downloads/responses.xlsx')
%   heli_expand_path('flights.csv')          -> relative to the current folder
%
% MATLAB's own file functions take a leading ~ on Unix, but string comparison
% between paths does not, and the checks in heli_flight_record are string
% comparisons. Resolving here means "~/Downloads" and "/Users/me/Downloads"
% are the same folder to every caller.
%
% The path does not have to exist. This is arithmetic on the text, not a
% question for the file system: `.` and `..` are left where they are, so do
% not build a security check on top of it.

p = char(p);
if isempty(p); p = pwd; return; end

if p(1) == '~'
    home = getenv('HOME');
    if isempty(home); home = getenv('USERPROFILE'); end
    if ~isempty(home)
        if numel(p) == 1
            p = home;
        elseif p(2) == '/' || p(2) == filesep
            p = fullfile(home, p(3:end));
        end
    end
end

if ~isAbsolute(p)
    p = fullfile(pwd, p);
end
end


function tf = isAbsolute(p)
if ispc
    tf = numel(p) >= 2 && (p(2) == ':' || strncmp(p, '\\', 2));
else
    tf = p(1) == '/';
end
end
