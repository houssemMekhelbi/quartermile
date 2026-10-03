#!/usr/bin/env python3
"""Generate the Quarter Mile night art: everything that is an image rather than CSS.

  ~/.config/hypr/quartermile-night/wallpaper.svg, wallpaper.png   1920x1080: a hood seen from above, filling the
        screen: body paint with metallic flake, the twin stripes (with their pinstripes) running
        top to bottom clearly right of the centre, two tapering creases, one floodlight band that
        steps where it crosses the creases, two hood pins. The left is kept calm for windows.
        night: body blue with stripe-white stripes; day: body white with body-blue stripes.
  ~/.config/hypr/quartermile-night/lock-board.png   900x430 the lock's scoreboard: chrome frame, black face,
        the ELAPSED / HRS : MIN legends and the chequer band (the time and the date are hyprlock labels)
  ~/.config/hypr/quartermile-night/lock-tree.png    260x910 the starting tree on its post, staged lights lit
  ~/.config/hypr/quartermile-night/lock-field.png   520x56 the password plate: a staged bulb in its housing, the stripes across its right end
  ~/.config/waybar/quartermile-night/pod-left.png, pod-right.png   60x32 the solid end of the stripes and the
        two-column chequer strip that finishes it; pod-stripes.png 8x32 the faint stripes behind the labels
  ~/.config/waybar/quartermile-night/ws-<state>.png  20x24 tree bulbs: empty (unlit outline), occupied (white),
        active (amber: on another monitor), focused (green), urgent (red); ws.css picks them
  ~/.config/gtk-3.0/quartermile-night/crumb-cheq.png  Thunar path separator: a small chequer

Deterministic; edit and re-run (needs rsvg-convert and the theme's fonts):  python3 build-art.py
"""

import os
import subprocess
from pathlib import Path

CONF = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
HYPR = CONF / "hypr/quartermile-night"
BAR = CONF / "waybar/quartermile-night"
GTK = CONF / "gtk-3.0/quartermile-night"

GROUND, PANEL, LINE, RING, MUTED, TEXT = "#101113", "#17191C", "#31353C", "#5B616A", "#9AA0A8", "#F3F1EA"
FACE, STRIPE, PIT, BULB = "#101113", "#F3F1EA", "#0A0B0C", "#F3F1EA"
CHROME, CHROME_HI, CHROME_LO, CHROME_T = "#B9BEC6", "#FFFFFF", "#5B616A", "#B9BEC6"
AMBER, GREEN, RED = "#FFB02E", "#35C759", "#E5342B"
BOARD, BOARD_TEXT, BOARD_MUTED, LOCK_FIELD = "#0A0B0C", "#F3F1EA", "#9AA0A8", "#101113"
STRIPE_FAINT = 0.065

# wallpaper colours per variant
WALL = dict(
    night=dict(body=("#11508D", "#1A70C0", "#1E7FD6", "#155FA6"), stripe=("#E4E3DD", "#F3F1EA", "#FFFFFF", "#F3F1EA", "#DDDCD6"),
               fall="#061A30", fall_op=(0.55, 0.10, 0.0, 0.50), crease_lit="#A9D6FF", crease_dark="#03101F", crease_op=(0.42, 0.30, 0.42, 0.30),
               band="#FFFFFF", band_op=(0.28, 0.40, 0.20), flake="0.86 0.94 1", flake_op=0.6, grain="0 0.05 0.12", grain_a=0.22,
               pin_shadow="#04101E", pin_shadow_op=0.55, loop="#B9BEC6"),
    day=dict(body=("#DAD6CA", "#ECE8DD", "#F2EFE6", "#E2DED2"), stripe=("#1A6FBC", "#1E7FD6", "#3A95E6", "#1E7FD6", "#1868B2"),
             fall="#6B6555", fall_op=(0.30, 0.05, 0.0, 0.26), crease_lit="#FFFFFF", crease_dark="#6B6555", crease_op=(0.85, 0.22, 0.30, 0.70),
             band="#FFFFFF", band_op=(0.55, 0.70, 0.40), flake="1 1 1", flake_op=0.5, grain="0.35 0.32 0.25", grain_a=0.10,
             pin_shadow="#3A362C", pin_shadow_op=0.40, loop="#7D848D"),
)
K = WALL["night"]


def render(svg, out, keep=False):
    out.parent.mkdir(parents=True, exist_ok=True)
    src = out.with_suffix(".svg")
    src.write_text(svg)
    subprocess.run(["rsvg-convert", "-o", str(out), str(src)], check=True)
    if not keep:
        src.unlink()


# ---- wallpaper -------------------------------------------------------------------
def wallpaper():
    W, H = 1920, 1080
    CX = 1330                                # centre of the stripe pair
    SW, GAP, PIN, PGAP = 150, 20, 7, 18      # stripe width, gap between the two, pinstripe width, its distance
    TOP, BOT = 575, 455                      # half width of the raised centre section at the cowl and at the nose
    xs = [(CX - GAP / 2 - SW, SW), (CX + GAP / 2, SW), (CX - GAP / 2 - SW - PGAP - PIN, PIN), (CX + GAP / 2 + SW + PGAP, PIN)]
    stripes = "".join(f'<rect x="{x:.0f}" y="-10" width="{w}" height="{H + 20}" fill="url(#st)"/>' for x, w in xs)

    def pin(x, y):
        return (f'<ellipse cx="{x + 7}" cy="{y + 12}" rx="30" ry="28" fill="{K["pin_shadow"]}" opacity="{K["pin_shadow_op"]}" filter="url(#soft)"/>'
                f'<circle cx="{x}" cy="{y}" r="27" fill="url(#chr)" stroke="#2A2F36" stroke-width="1.2"/>'
                f'<circle cx="{x}" cy="{y}" r="17" fill="url(#chr2)" stroke="#3A4048" stroke-width="1"/>'
                f'<circle cx="{x}" cy="{y}" r="5.5" fill="#1B1E22"/>'
                f'<path d="M{x - 30},{y + 7} H{x + 50}" stroke="{K["pin_shadow"]}" stroke-opacity="0.45" stroke-width="7" stroke-linecap="round" filter="url(#soft2)"/>'
                f'<path d="M{x - 34},{y} H{x + 46}" stroke="#7D848D" stroke-width="4" stroke-linecap="round"/>'
                f'<path d="M{x - 33},{y - 0.8} H{x + 45}" stroke="#EEF1F4" stroke-width="1.6" stroke-linecap="round"/>'
                f'<circle cx="{x + 52}" cy="{y}" r="6" fill="none" stroke="{K["loop"]}" stroke-width="2.4"/>')

    b0, b1, b2 = K["band_op"]
    band = (f'<ellipse cx="1040" cy="350" rx="1300" ry="60" fill="{K["band"]}" opacity="{b0}" filter="url(#band)"/>'
            f'<ellipse cx="1180" cy="338" rx="950" ry="7" fill="{K["band"]}" opacity="{b1}" filter="url(#band2)"/>'
            f'<ellipse cx="1000" cy="414" rx="1000" ry="3" fill="{K["band"]}" opacity="{b2}" filter="url(#band2)"/>')
    body, st, f, c = K["body"], K["stripe"], K["fall_op"], K["crease_op"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="body" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{body[0]}"/><stop offset="0.30" stop-color="{body[1]}"/><stop offset="0.69" stop-color="{body[2]}"/><stop offset="1" stop-color="{body[3]}"/></linearGradient>
<linearGradient id="fall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{K["fall"]}" stop-opacity="{f[0]}"/><stop offset="0.16" stop-color="{K["fall"]}" stop-opacity="{f[1]}"/><stop offset="0.62" stop-color="{K["fall"]}" stop-opacity="{f[2]}"/><stop offset="1" stop-color="{K["fall"]}" stop-opacity="{f[3]}"/></linearGradient>
<linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{st[0]}"/><stop offset="0.2" stop-color="{st[1]}"/><stop offset="0.34" stop-color="{st[2]}"/><stop offset="0.5" stop-color="{st[3]}"/><stop offset="1" stop-color="{st[4]}"/></linearGradient>
<linearGradient id="chr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.45" stop-color="{CHROME}"/><stop offset="1" stop-color="#5C636C"/></linearGradient>
<linearGradient id="chr2" x1="1" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#F4F6F8"/><stop offset="0.5" stop-color="#9AA0A8"/><stop offset="1" stop-color="#4A5058"/></linearGradient>
<filter id="band" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="46"/></filter>
<filter id="band2" x="-20%" y="-400%" width="140%" height="900%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="crease" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="9"/></filter>
<clipPath id="inner"><path d="M{CX - TOP + 8},-20 L{CX + TOP - 8},-20 L{CX + BOT - 8},{H + 20} L{CX - BOT + 8},{H + 20} Z"/></clipPath>
<clipPath id="outer"><path d="M-20,-20 L{CX - TOP + 8},-20 L{CX - BOT + 8},{H + 20} L-20,{H + 20} Z M{CX + TOP - 8},-20 L{W + 20},-20 L{W + 20},{H + 20} L{CX + BOT - 8},{H + 20} Z"/></clipPath>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>
<filter id="soft2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="flake" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.35" numOctaves="1" seed="7"/><feColorMatrix values="0 0 0 0 {K["flake"].split()[0]}  0 0 0 0 {K["flake"].split()[1]}  0 0 0 0 {K["flake"].split()[2]}  2.6 2.6 0 0 -2.95"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 {K["grain"].split()[0]}  0 0 0 0 {K["grain"].split()[1]}  0 0 0 0 {K["grain"].split()[2]}  0 0 0 {K["grain_a"]} 0"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#body)"/>
<g filter="url(#crease)">
<path d="M{CX - TOP},-20 L{CX - BOT},{H + 20}" stroke="{K["crease_lit"]}" stroke-opacity="{c[0]}" stroke-width="16" fill="none"/>
<path d="M{CX - TOP + 26},-20 L{CX - BOT + 26},{H + 20}" stroke="{K["crease_dark"]}" stroke-opacity="{c[1]}" stroke-width="22" fill="none"/>
<path d="M{CX + TOP},-20 L{CX + BOT},{H + 20}" stroke="{K["crease_dark"]}" stroke-opacity="{c[2]}" stroke-width="26" fill="none"/>
<path d="M{CX + TOP - 26},-20 L{CX + BOT - 26},{H + 20}" stroke="{K["crease_lit"]}" stroke-opacity="{c[3]}" stroke-width="14" fill="none"/>
</g>
<rect width="{W}" height="{H}" filter="url(#flake)" opacity="{K["flake_op"]}"/>
<rect width="{W}" height="{H}" filter="url(#grain)"/>
{stripes}
<rect x="{CX - 340}" y="0" width="680" height="{H}" filter="url(#grain)" opacity="0.35"/>
<rect width="{W}" height="{H}" fill="url(#fall)"/>
<g clip-path="url(#outer)"><g transform="rotate(-1.6 960 350)">{band}</g></g>
<g clip-path="url(#inner)"><g transform="translate(0 -46) rotate(-1.6 960 350)">{band}</g></g>
{pin(930, 952)}{pin(1730, 952)}
</svg>'''
    render(svg, HYPR / "wallpaper.png", keep=True)


# ---- helpers ---------------------------------------------------------------------
def chequer(x, y, cols, rows, c, color, first=True):
    """cols x rows cells of size c; the upper-left cell is filled when `first`."""
    return "".join(f'<rect x="{x + i * c}" y="{y + j * c}" width="{c}" height="{c}" fill="{color}"/>'
                   for j in range(rows) for i in range(cols) if ((i + j) % 2 == 0) == first)


def stripes_h(w, h, color, opacity=1.0):
    """The twin stripes running along a 32px pod face: pinstripe, stripe, gap, stripe, pinstripe."""
    rows = ((2, 1), (5, 9), (18, 9), (29, 1))
    return "".join(f'<rect x="0" y="{y}" width="{w}" height="{t}" fill="{color}" fill-opacity="{opacity}"/>' for y, t in rows)


def svg(w, h, body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{CHROME_DEFS}{defs}</defs>{body}</svg>'


CHROME_DEFS = (f'<linearGradient id="chrome" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CHROME_HI}"/>'
               f'<stop offset="0.45" stop-color="{CHROME}"/><stop offset="1" stop-color="#4A5058"/></linearGradient>'
               f'<linearGradient id="chromev" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CHROME_HI}"/>'
               f'<stop offset="0.4" stop-color="{CHROME}"/><stop offset="1" stop-color="{CHROME_LO}"/></linearGradient>')


# ---- bar ---------------------------------------------------------------------------
def bar():
    solid, c, h = 44, 8, 32
    left = stripes_h(solid, h, STRIPE) + chequer(solid, 0, 2, 4, c, STRIPE, True)
    right = f'<g transform="translate({2 * c} 0)">{stripes_h(solid, h, STRIPE)}</g>' + chequer(0, 0, 2, 4, c, STRIPE, False)
    render(svg(solid + 2 * c, h, left), BAR / "pod-left.png")
    render(svg(solid + 2 * c, h, right), BAR / "pod-right.png")
    render(svg(8, h, stripes_h(8, h, STRIPE, STRIPE_FAINT)), BAR / "pod-stripes.png")


def bulb(cx, cy, r, color, glow):
    g = f'<circle cx="{cx}" cy="{cy}" r="{r + 1.5}" fill="{color}" opacity="0.75" filter="url(#g)"/>' if glow else ""
    return (g + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
            f'<circle cx="{cx - r * 0.3:.2f}" cy="{cy - r * 0.32:.2f}" r="{r * 0.34:.2f}" fill="#FFFFFF" opacity="0.8"/>')


def workspaces():
    """20x24 per state, the same image for every slot. The bulbs sit in the black housing (#workspaces),
    so they keep their colours in both variants. The glow is baked in: GTK3 shadows stop at the box."""
    blur = '<filter id="g" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.2"/></filter>'
    states = {
        "empty": f'<circle cx="10" cy="12" r="5.75" fill="#FFFFFF" fill-opacity="0.03" stroke="{CHROME_LO}" stroke-width="1.5"/>',
        "occupied": bulb(10, 12, 6.5, BULB, False),
        "active": bulb(10, 12, 6.5, AMBER, True),
        "focused": bulb(10, 12, 7.5, GREEN, True),
        "urgent": bulb(10, 12, 6.5, RED, True),
    }
    css = ["/* Generated by ~/.config/hypr/quartermile-night/build-art.py: the tree bulb for every state (the same in every slot). */"]
    ids = lambda suffix: ",\n".join(f"#custom-ws-{n}{suffix}" for n in range(1, 11))
    for state, body in states.items():
        render(svg(20, 24, body, blur), BAR / f"ws-{state}.png")
    # order matters: a focused slot carries .active and .focused, so .focused comes last
    for state in ("occupied", "empty", "active", "urgent", "focused"):
        css.append(f'{ids("" if state == "occupied" else "." + state)} {{ background-image: url("ws-{state}.png"); }}')
    (BAR / "ws.css").write_text("\n".join(css) + "\n")


def crumb():
    render(svg(10, 18, chequer(2, 3, 2, 4, 3, RING, True)), GTK / "crumb-cheq.png")


# ---- lock ------------------------------------------------------------------------
def lock():
    # scoreboard: 900x430, chrome frame 4px, black face; the time and the date are labels on top of it
    w, h = 900, 430
    body = (f'<rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="url(#chrome)"/>'
            f'<rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="10" fill="{BOARD}"/>'
            f'<text x="40" y="42" font-family="Courier Prime" font-size="15" letter-spacing="3" fill="{BOARD_MUTED}">ELAPSED</text>'
            f'<text x="{w - 40}" y="42" text-anchor="end" font-family="Courier Prime" font-size="15" letter-spacing="3" fill="{BOARD_MUTED}">HRS : MIN</text>'
            + chequer(40, 340, 82, 2, 10, CHROME, True))
    render(svg(w, h, body), HYPR / "lock-board.png")

    # the tree: post, pre-stage and stage pairs lit white (locked = staged), three ambers, green, red unlit
    w, h, cx = 260, 910, 130
    blur = '<filter id="tg" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="9"/></filter>'
    o = (f'<rect x="{cx - 8}" y="18" width="16" height="{h - 18}" fill="{PIT}" stroke="#3A4048" stroke-width="1"/>'
         f'<rect x="{cx - 20}" y="0.75" width="40" height="22" rx="4" fill="{PIT}" stroke="url(#chrome)" stroke-width="1.5"/>')
    y = 40
    for _ in range(2):
        o += f'<rect x="{cx - 112}" y="{y}" width="224" height="44" rx="8" fill="{PIT}" stroke="#3A4048" stroke-width="1.5"/>'
        for bx in (cx - 84, cx - 50, cx + 50, cx + 84):
            o += (f'<circle cx="{bx}" cy="{y + 22}" r="14" fill="{BULB}" opacity="0.55" filter="url(#tg)"/>'
                  f'<circle cx="{bx}" cy="{y + 22}" r="10" fill="{BULB}" stroke="url(#chrome)" stroke-width="2"/>')
        y += 56
    y += 10
    for col in (AMBER, AMBER, AMBER, GREEN, RED):
        o += f'<rect x="{cx - 112}" y="{y}" width="224" height="84" rx="10" fill="{PIT}" stroke="#3A4048" stroke-width="1.5"/>'
        for bx in (cx - 62, cx + 62):
            o += (f'<circle cx="{bx}" cy="{y + 42}" r="31" fill="#050506" stroke="url(#chrome)" stroke-width="3"/>'
                  f'<circle cx="{bx}" cy="{y + 42}" r="26" fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-opacity="0.40" stroke-width="1.5"/>'
                  f'<path d="M{bx - 16},{y + 30} A20,20 0 0 1 {bx + 4},{y + 20}" fill="none" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="3" stroke-linecap="round"/>')
        y += 96
    render(svg(w, h, o, blur), HYPR / "lock-tree.png")

    # the password plate: staged bulb at the left, the twin stripes across the right end
    w, h = 520, 56
    sx = w - 24 - 39
    blur = '<filter id="g" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.5"/></filter>'
    body = (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="4.5" fill="{LOCK_FIELD}" fill-opacity="0.96" stroke="{CHROME_T}"/>'
            + "".join(f'<rect x="{sx + dx}" y="1" width="{sw}" height="{h - 2}" fill="{STRIPE}"/>' for dx, sw in ((0, 1.5), (5.5, 12), (21.5, 12), (37.5, 1.5)))
            + f'<rect x="12" y="{h / 2 - 12}" width="30" height="24" rx="4" fill="{PIT}" stroke="{CHROME_LO}" stroke-width="1"/>'
            + bulb(27, h / 2, 6, BULB, True))
    render(svg(w, h, body, blur), HYPR / "lock-field.png")


if __name__ == "__main__":
    wallpaper()
    bar()
    workspaces()
    crumb()
    lock()
    print("art written under", CONF)
