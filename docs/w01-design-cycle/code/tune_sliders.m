function tune_sliders(K, wn, zeta)
%TUNE_SLIDERS  Three sliders, a step response, and the envelope's verdict.
%
%   tune_sliders                    uses the fitted model in elevation_plant.json
%   tune_sliders(K, wn, zeta)       uses your own fit
%
% Built with uifigure rather than as Live Script controls so that it works the
% same on a laptop and in MATLAB Online, and so that the verdict can update
% with the plot. Live Script sliders are fine too: Insert > Control, bound to
% kp, ki and kd.
%
% Two models are in play, on purpose.
%
% The *response* is simulated against whatever model you pass in, because that
% is your fit and exploring it is the point.
%
% The *verdict* is always taken against the model fitted from the rig on the
% day, which is what submit_gains and the rig-side tool use. It has to be. If
% your fit came out high, gains that look fine against it would be refused at
% submission, or worse, flown against a machine they were never checked
% against. The panel says which model each number came from.

official = heli_plant();
if nargin < 3
    K = official.K; wn = official.wn; zeta = official.zeta;
end
mine = struct('K', K, 'wn', wn, 'zeta', zeta);
env  = heli_envelope();

f = uifigure('Name', 'Tune the elevation loop', 'Position', [100 100 980 560]);
g = uigridlayout(f, [2 2], 'ColumnWidth', {300, '1x'}, 'RowHeight', {'1x', 120});

panel = uipanel(g, 'Title', 'Gains');
panel.Layout.Row = 1; panel.Layout.Column = 1;
pg = uigridlayout(panel, [6 1], 'RowHeight', repmat({'fit'}, 1, 6));

s = struct();
[s.kp, s.kpLabel] = addSlider(pg, 'K_p  proportional', 0, 5, 0.7);
[s.kd, s.kdLabel] = addSlider(pg, 'K_d  derivative (damping)', 0, 5, 0.9);
[s.ki, s.kiLabel] = addSlider(pg, 'K_i  integral (removes the gap)', 0, 3, 0.6);

ax = uiaxes(g);
ax.Layout.Row = 1; ax.Layout.Column = 2;

verdict = uitextarea(g, 'Editable', 'off', 'FontName', 'Menlo');
verdict.Layout.Row = 2; verdict.Layout.Column = [1 2];

redraw();
s.kp.ValueChangedFcn = @(~,~) redraw();
s.kd.ValueChangedFcn = @(~,~) redraw();
s.ki.ValueChangedFcn = @(~,~) redraw();
s.kp.ValueChangingFcn = @(~,e) live(e, 'kp');
s.kd.ValueChangingFcn = @(~,e) live(e, 'kd');
s.ki.ValueChangingFcn = @(~,e) live(e, 'ki');

    function live(e, which)
        % Update the labels while dragging; recompute on release, because the
        % envelope check simulates and is too slow for every mouse move.
        switch which
            case 'kp', s.kpLabel.Text = sprintf('K_p  proportional  =  %.2f', e.Value);
            case 'kd', s.kdLabel.Text = sprintf('K_d  derivative  =  %.2f', e.Value);
            case 'ki', s.kiLabel.Text = sprintf('K_i  integral  =  %.2f', e.Value);
        end
    end

    function redraw()
        kp = s.kp.Value; kd = s.kd.Value; ki = s.ki.Value;
        s.kpLabel.Text = sprintf('K_p  proportional  =  %.2f', kp);
        s.kdLabel.Text = sprintf('K_d  derivative  =  %.2f', kd);
        s.kiLabel.Text = sprintf('K_i  integral  =  %.2f', ki);

        G = tf(K*wn^2, [1, 2*zeta*wn, wn^2]);
        t = linspace(0, 30, 1500);
        ref = min(env.cmdRateDegS * t, env.stepDeg);

        cla(ax);
        if kp <= 0 || ki <= 0 || kd <= 0
            verdict.Value = {'Every gain has to be above zero before there is'; ...
                             'anything to simulate.'};
            plot(ax, t, ref, 'k--'); grid(ax, 'on');
            return
        end

        Tf = kd / (env.derivativeFilterN * kp);
        C  = tf([kp*Tf + kd, kp + ki*Tf, ki], [Tf, 1, 0]);
        C1 = tf([kp, ki], [1, 0]);
        L  = C * G;
        y  = lsim(minreal(G*C1/(1+L), [], false), ref, t);

        plot(ax, t, ref, 'k--', 'LineWidth', 1.1); hold(ax, 'on');
        plot(ax, t, y, 'LineWidth', 1.6); hold(ax, 'off');
        grid(ax, 'on');
        xlabel(ax, 'Time (s)'); ylabel(ax, 'Elevation (deg)');
        legend(ax, 'demand', 'response', 'Location', 'southeast');
        ylim(ax, [-2, max(14, 1.3*max(y))]);

        [ok, why, m] = heli_check_one(kp, ki, kd, official, env);
        lines = {sprintf('Kp = %.3f    Ki = %.3f    Kd = %.3f', kp, ki, kd)};
        lines{end+1} = sprintf(['plot: your fit, K=%.2f wn=%.2f zeta=%.3f   |   ' ...
            'verdict: the rig''s, K=%.2f wn=%.2f zeta=%.3f'], ...
            mine.K, mine.wn, mine.zeta, official.K, official.wn, official.zeta);
        lines{end+1} = line1(m, env);
        if ok
            lines{end+1} = 'INSIDE THE ENVELOPE. submit_gains will accept this.';
            ax.Title.String = 'Inside the envelope';
        else
            lines{end+1} = sprintf('OUTSIDE: %s', why);
            ax.Title.String = 'Outside the envelope';
        end
        verdict.Value = lines;
    end
end


function txt = line1(m, env)
%LINE1  The four numbers the envelope actually cares about.
part = {};
if isfield(m, 'damping')
    part{end+1} = sprintf('damping %.2f (>= %.2f)', m.damping, env.dampingMin);
end
if isfield(m, 'phase_margin')
    part{end+1} = sprintf('PM %.0f deg (>= %g)', m.phase_margin, env.phaseMarginMin);
end
if isfield(m, 'peak_volts')
    part{end+1} = sprintf('peak %.1f V (<= %.1f)', m.peak_volts, env.voltagePeakMax);
end
if isfield(m, 'settle_s')
    part{end+1} = sprintf('settles %.1f s (<= %g)', m.settle_s, env.settleMaxS);
end
if isempty(part); txt = ''; else; txt = strjoin(part, '   '); end
end


function [sl, lbl] = addSlider(parent, name, lo, hi, val)
%ADDSLIDER  A labelled slider, with the label showing the value.
lbl = uilabel(parent, 'Text', name, 'FontWeight', 'bold');
sl  = uislider(parent, 'Limits', [lo hi], 'Value', val);
end

% tracking: status=draft version=0 assisted=true
