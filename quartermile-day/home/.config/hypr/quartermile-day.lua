-- Quarter Mile day look and feel.
-- The drag strip at day: the starting tree
-- carries every status, the twin stripes, the chequer and chrome carry the
-- structure. Windows are plain rectangles: a 1px border that runs along a
-- gradient on the focused window, a hairline on the others, one dark shadow
-- and no glow. Loaded after futuwwa.lua so these values win; behaviour and
-- binds stay there. The popups and helpers are shared by both Quarter Mile
-- variants (quartermile-*).

local C = {
    ground = "F2EFE6",
    line   = "CFCABC",
    a      = "1E7FD6",
    b      = "145A9C",
    c      = "145A9C",
    shadow = "15171A",
}

hl.config({
    general = {
        gaps_in     = 6,
        gaps_out    = 14,
        border_size = 1,
        col = {
            active_border   = {
                colors = { "rgb(" .. C.a .. ")", "rgb(" .. C.b .. ")", "rgb(" .. C.c .. ")" },
                angle  = 135,
            },
            inactive_border = "rgb(" .. C.line .. ")",
        },
    },

    decoration = {
        rounding       = 5,
        rounding_power = 2.0,

        active_opacity   = 1.0,
        inactive_opacity = 0.96,

        blur = {
            enabled           = true,
            size              = 8,
            passes            = 3,
            vibrancy          = 0.10,
            noise             = 0.01,
            new_optimizations = true,
            popups            = true,
        },

        glow = {
            enabled = false,
        },

        -- One dark shadow, a little below the window; status colours never glow here.
        shadow = {
            enabled        = true,
            range          = 24,
            render_power   = 3,
            offset         = { 0, 8 },
            color          = "rgba(" .. C.shadow .. "40)",
            color_inactive = "rgba(15171A22)",
        },
    },

    group = {
        col = {
            border_active   = "rgb(" .. C.b .. ")",
            border_inactive = "rgb(" .. C.line .. ")",
        },
    },

    misc = {
        disable_hyprland_logo    = true,
        disable_splash_rendering = true,
        background_color         = "rgb(" .. C.ground .. ")",
    },
})

-- Cursor: QuartermileDayTree (~/.local/share/icons/QuartermileDayTree, hyprcursor + XCursor).
-- On a live theme switch restore.sh runs `hyprctl setcursor` from gsettings.txt.
hl.env("HYPRCURSOR_THEME", "QuartermileDayTree")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("XCURSOR_THEME", "QuartermileDayTree")
hl.env("XCURSOR_SIZE", "24")

-- A config reload resets the cursor to the default theme; set it again.
local function quartermile_cursor()
    hl.exec_cmd("hyprctl setcursor QuartermileDayTree 24")
end
hl.on("hyprland.start", quartermile_cursor)
hl.on("config.reloaded", quartermile_cursor)

-- Launcher bind points at the Quarter Mile launcher; futuwwa.lua binds the Girih one.
hl.unbind("SUPER + D")
hl.bind("SUPER + D",
    hl.dsp.exec_cmd(os.getenv("HOME") .. "/.local/bin/quartermile-launcher"),
    { description = "Application launcher" })

-- Terminals draw their own glass (foot/alacritty/ghostty alpha) so text stays opaque.
hl.window_rule({
    name    = "quartermile-terminal-opaque",
    match   = { class = "^(foot|footclient|Alacritty|com.mitchellh.ghostty)$" },
    opacity = "1.0 override 1.0 override",
})

-- Blur behind layer surfaces: the bar, alert banners, launcher, notifications.
-- ignore_alpha keeps fully transparent parts of a layer unblurred.
hl.layer_rule({
    name         = "quartermile-bar-glass",
    match        = { namespace = "^hattin-" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "quartermile-launcher-glass",
    match        = { namespace = "^launcher$" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "quartermile-notify-glass",
    match        = { namespace = "^swaync" },
    blur         = true,
    ignore_alpha = 0.1,
})

-- Launcher: floating foot + fzf (~/.local/bin/quartermile-launcher).
hl.window_rule({
    name     = "quartermile-launcher",
    match    = { class = "^quartermile-launcher$" },
    float    = true,
    size     = "780 470",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

-- Taskwarrior popups from the waybar "yawm" module (~/.local/bin/quartermile-yawm).
hl.window_rule({
    name     = "quartermile-yawm",
    match    = { class = "^quartermile-yawm$" },
    float    = true,
    size     = "820 600",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

hl.window_rule({
    name     = "quartermile-yawm-add",
    match    = { class = "^quartermile-yawm-add$" },
    float    = true,
    size     = "720 240",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

local quartermile_popups = { "quartermile-launcher", "quartermile-yawm", "quartermile-yawm-add" }

-- Close every popup window except those of class `keep`.
-- hl.get_windows matches `class` exactly (no regex), so pass the plain name.
function quartermile_close_popups(keep)
    for _, class in ipairs(quartermile_popups) do
        if class ~= keep then
            for _, w in ipairs(hl.get_windows({ class = class })) do
                hl.dispatch(hl.dsp.window.close({ window = "address:" .. w.address }))
            end
        end
    end
end

function quartermile_close_launcher()
    quartermile_close_popups()
end

-- Close popups as soon as focus moves elsewhere.
hl.on("window.active", function(win)
    quartermile_close_popups(win and win.class)
end)
