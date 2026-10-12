function url = gain_form_url(kp, ki, kd, displayName)
%GAIN_FORM_URL  The submission form, with your gains already filled in.
%
%   url = gain_form_url(7.4, 1.07, 15.2, 'Red Baron')
%
% Returns a link to the unit's submission form with all four boxes already
% filled. You still press Submit yourself, so you get to see what is being
% sent under your name before it goes.
%
% The name you give is the name on screen when your gains are flown. An alias
% is fine, and a good one is encouraged. Your University account is recorded by
% the form separately and is never shown to the room.
%
% Called by submit_gains, which checks the gains first. Call it directly only
% if you want the link without the checks.

arguments
    kp (1,1) double
    ki (1,1) double
    kd (1,1) double
    displayName (1,:) char
end

cfg = formConfig();

% Six significant figures. The form stores text, and a gain pasted in as
% 7.4000000000000004 is the same controller but reads like false precision.
q = { cfg.fields.display_name, strtrim(displayName)
      cfg.fields.kp,           num2str(kp, '%.6g')
      cfg.fields.ki,           num2str(ki, '%.6g')
      cfg.fields.kd,           num2str(kd, '%.6g') };

parts = "id=" + encode(cfg.form_id);
for i = 1:size(q, 1)
    parts(end+1) = string(q{i,1}) + "=" + encode(q{i,2}); %#ok<AGROW>
end
url = char(cfg.base + "?" + join(parts, "&"));
end


function e = encode(s)
%ENCODE  Percent-encode for a query string.
%
% urlencode writes a space as "+", which is legal in a query string and which
% Microsoft Forms does render as a space. It is percent-encoded here anyway,
% because "+" survives one copy-paste through a chat window or a slide and
% then arrives as a literal plus in somebody's name.
e = string(strrep(urlencode(s), '+', '%20'));
end


function cfg = formConfig()
%FORMCONFIG  Read gain_form.json from beside this file.
%
% The form's field identifiers live in JSON rather than in this function so
% that next year's form is a config change. The JSON says how to regenerate
% them.
here = fileparts(mfilename('fullpath'));
f = fullfile(here, 'gain_form.json');
if ~isfile(f)
    error('gain_form_url:noConfig', ...
        ['gain_form.json is missing. It should sit beside this file, in\n    %s\n' ...
         'Re-download the week 1 code folder.'], here);
end
cfg = jsondecode(fileread(f));
need = {'display_name', 'kp', 'ki', 'kd'};
missing = need(~isfield(cfg.fields, need));
if ~isempty(missing)
    error('gain_form_url:badConfig', ...
        'gain_form.json has no field id for: %s', strjoin(missing, ', '));
end
cfg.base = string(cfg.base);
end
