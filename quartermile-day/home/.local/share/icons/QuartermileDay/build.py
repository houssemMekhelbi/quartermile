#!/usr/bin/env python3
"""Generate the QuartermileDay icon theme next to this file (Quarter Mile day).

scalable/  64-unit SVGs. Folders are body-blue panels with the twin stripes (and
           their pinstripes) running down the right side, a deeper back panel
           with a square tab, and one white mark for the special folders.
           Documents are white timeslips: a square-toothed (perforated) upper
           edge and printed rows with dotted leaders; one mark for the type
           (a deep-blue band on PDF, a striped blue picture on images). Devices
           are asphalt boxes in a chrome line with one white staged bulb. The
           trash is a chrome-lined drum. No status colour is used, except the
           red bulb on the full trash.
16/        sidebar size: plain square-capped line icons in the muted colour.
Anything not drawn here falls through to Adwaita.
Run: python3 build.py   (then gtk-update-icon-cache runs by itself)
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "QuartermileDay"

GROUND, PANEL, RAISED, LINE = "#F2EFE6", "#F8F6F0", "#E4DFD1", "#CFCABC"
BLUE, DEEP, EDGE, RED = "#1E7FD6", "#145A9C", "#0E3F73", "#E5342B"
WHITE, SHEET, SHEET_EDGE, INK, RULE = "#F3F1EA", "#FFFFFF", "#8B887C", "#101113", "#8C9198"
CHROME, BOX, BULB = "#B9BEC6", "#17191C", "#F3F1EA"
SIDE = "#5A5F66"


def svg64(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">{body}</svg>\n'


def write(rel, content, names):
    for name in names:
        path = ROOT / rel / f"{name}.svg"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def stroke(d, color=WHITE, w=2.6):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="square" stroke-linejoin="miter"/>'


# ---- folders: body panels with the stripes ------------------------------------------------
# marks are drawn around (24, 40): the stripes own the right side of the panel
MARKS = {
    None: "",
    "home": stroke("M14 41 L24 32 L34 41 M17 39.5 V51 H31 V39.5", WHITE, 2.8),
    "documents": "".join(stroke(f"M15 {y} H{x}", WHITE, 2.8) for y, x in ((33, 33), (40, 33), (47, 27))),
    "downloads": stroke("M24 30 V45 M17.5 39 L24 45.5 L30.5 39 M15 52 H33", WHITE, 2.8),
    "music": stroke("M20 47 V33 H31 V45", WHITE, 2.6) + f'<circle cx="17.5" cy="47.5" r="3.2" fill="{WHITE}"/><circle cx="28.5" cy="45.5" r="3.2" fill="{WHITE}"/>',
    "pictures": f'<path d="M14 51 L21 41 L25.5 46.5 L29 43 L34 51 Z" fill="{WHITE}"/><circle cx="31" cy="34" r="3" fill="{WHITE}"/>',
    "videos": f'<path d="M19 32 L32 41 L19 50 Z" fill="{WHITE}"/>',
    "desktop": f'<rect x="14" y="32" width="20" height="14" fill="none" stroke="{WHITE}" stroke-width="2.6"/>' + stroke("M19 51.5 H29", WHITE, 2.6),
    "templates": f'<rect x="15" y="32" width="18" height="18" fill="none" stroke="{WHITE}" stroke-width="2.4" stroke-dasharray="3.4 3.4"/>',
    "share": stroke("M18 41.5 L30 35 M18 41.5 L30 48.5", WHITE, 1.8) + "".join(f'<circle cx="{x}" cy="{y}" r="3.4" fill="{WHITE}"/>' for x, y in ((18, 41.5), (30, 34.5), (30, 48.5))),
    "remote": stroke("M24 32 a9 9.5 0 1 0 0.01 0 M15 41.5 H33 M24 32 C19 36.5 19 46.5 24 51 M24 32 C29 36.5 29 46.5 24 51", WHITE, 1.7),
}


def folder(kind=None):
    stripes = "".join(f'<rect x="{x}" y="19" width="{w}" height="38" fill="{WHITE}"/>' for x, w in ((38.5, 1.3), (42, 7), (51, 7), (60.2, 1.3)))
    body = (f'<path d="M4 9 Q4 6 7 6 H26 L32 13 H61 Q64 13 64 16 V24 H4 Z" fill="{DEEP}"/>'
            f'<rect x="4" y="19" width="60" height="38" rx="3" fill="{BLUE}"/>' + stripes
            + f'<rect x="4.5" y="19.5" width="59" height="37" rx="2.5" fill="none" stroke="{EDGE}" stroke-width="1"/>'
            f'<path d="M6 21 H62" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="1"/>' + MARKS[kind])
    return svg64(body)


FOLDERS = {
    None: ["folder", "inode-directory", "folder-open", "folder-drag-accept", "folder-visiting"],
    "home": ["user-home", "folder-home"],
    "documents": ["folder-documents"],
    "downloads": ["folder-download"],
    "music": ["folder-music"],
    "pictures": ["folder-pictures"],
    "videos": ["folder-videos"],
    "templates": ["folder-templates"],
    "share": ["folder-publicshare"],
    "desktop": ["user-desktop"],
    "remote": ["folder-remote", "network-workgroup"],
}
for kind, names in FOLDERS.items():
    write("scalable/places", folder(kind), names)
    if kind is None:
        write("scalable/mimetypes", folder(kind), names)
for kind, names in FOLDERS.items():
    write("scalable/places", folder(kind), names)
    if kind is None:
        write("scalable/mimetypes", folder(kind), names)


# ---- documents: timeslips -------------------------------------------------------------------
def sheet():
    # square-toothed upper edge: the perforation of a slip torn off a roll
    d = "M10 60 V3 " + " ".join(f"H{14 + 4 * k}" + (f" V{6 if k % 2 == 0 else 3}" if k < 10 else "") for k in range(11)) + " V60 Z"
    return (f'<path d="{d}" fill="{SHEET}" stroke="{SHEET_EDGE}" stroke-width="1"/>'
            f'<path d="M13 10.5 H51" stroke="{RULE}" stroke-width="1" stroke-dasharray="1.5 2.5"/>')


def row(y, x2=30, x3=42):
    """a printed row: legend, dotted leader, value"""
    return (f'<path d="M15 {y} H{x2}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{x2 + 3} {y} H{x3 - 3}" stroke="{RULE}" stroke-width="1.5" stroke-dasharray="1.2 2.4"/>'
            f'<path d="M{x3} {y} H49" stroke="{INK}" stroke-width="2.2"/>')


def lines(ys):
    return "".join(row(y, 30 - 4 * (i % 3), 42 - 3 * (i % 2)) for i, y in enumerate(ys))


def cheq(x, y, cols, rows, c, color):
    return "".join(f'<rect x="{x + i * c}" y="{y + k * c}" width="{c}" height="{c}" fill="{color}"/>'
                   for k in range(rows) for i in range(cols) if (i + k) % 2 == 0)


DOC_MARKS = {
    None: row(19),
    "text": lines([19, 26, 33, 40]) + f'<path d="M15 47 H49" stroke="{INK}" stroke-width="1"/>' + row(54, 24, 40),
    "script": stroke("M16 20 L22 25 L16 30", DEEP, 2.6) + stroke("M26 31 H38", INK, 2.4) + lines([40, 47, 54]),
    "code": stroke("M24 19 L17 27 L24 35", DEEP, 2.6) + stroke("M40 19 L47 27 L40 35", DEEP, 2.6) + lines([44, 51]),
    "exec": f'<rect x="15" y="17" width="34" height="24" fill="{INK}"/>' + cheq(15, 17, 8, 2, 4.25, SHEET) + stroke("M21 34 H31", SHEET, 2.4) + lines([48, 55]),
    "image": (f'<rect x="15" y="17" width="34" height="28" fill="{BLUE}"/><rect x="36" y="17" width="4" height="28" fill="{WHITE}"/>'
              f'<rect x="42" y="17" width="4" height="28" fill="{WHITE}"/><rect x="15" y="17" width="34" height="28" fill="none" stroke="{INK}" stroke-width="1.4"/>' + lines([52])),
    "pdf": lines([19, 26]) + f'<rect x="10.5" y="33" width="43" height="16" fill="{DEEP}"/>'
           f'<text x="32" y="45.5" text-anchor="middle" font-family="Bungee" font-size="12" letter-spacing="0.5" fill="{WHITE}">PDF</text>' + row(55, 24, 40),
    "audio": "".join(f'<rect x="{16 + 5 * i}" y="{31 - h / 2}" width="3" height="{h}" fill="{DEEP}"/>' for i, h in enumerate((8, 16, 24, 12, 20, 10, 16))) + lines([49, 55]),
    "video": f'<rect x="15" y="17" width="34" height="26" fill="{INK}"/><path d="M27 23 L39 30 L27 37 Z" fill="{SHEET}"/>' + lines([50]),
    "archive": f'<rect x="28" y="7" width="8" height="53" fill="{DEEP}"/>' + cheq(28, 12, 2, 8, 4, WHITE) + f'<rect x="24.5" y="47" width="15" height="9" fill="{SHEET}" stroke="{INK}" stroke-width="2"/>',
    "grid": stroke("M15 20 H49 M15 28 H49 M15 36 H49 M15 44 H49 M15 52 H49 M26 17 V55 M38 17 V55", RULE, 1.5),
    "slide": f'<rect x="15" y="17" width="34" height="20" fill="{DEEP}"/>' + stroke("M32 37 V46 M25 47 H39", INK, 2.2) + lines([54]),
    "font": stroke("M19 52 L32 19 L45 52 M24 42 H40", INK, 2.8),
}
DOCUMENTS = {
    None: ["application-x-generic", "unknown", "empty"],
    "text": ["text-x-generic", "text-plain", "x-office-document", "text-markdown", "text-x-readme"],
    "script": ["text-x-script", "application-x-shellscript", "text-x-python", "text-x-makefile"],
    "exec": ["application-x-executable", "application-x-sharedlib"],
    "image": ["image-x-generic"],
    "audio": ["audio-x-generic"],
    "video": ["video-x-generic"],
    "archive": ["package-x-generic", "application-x-archive", "application-zip", "application-x-compressed-tar", "application-x-tar"],
    "pdf": ["application-pdf"],
    "code": ["text-html", "application-json", "text-x-csrc", "text-x-c++src", "text-x-javascript"],
    "grid": ["x-office-spreadsheet"],
    "slide": ["x-office-presentation"],
    "font": ["font-x-generic"],
}
for kind, names in DOCUMENTS.items():
    write("scalable/mimetypes", svg64(sheet() + DOC_MARKS[kind]), names)
for kind, names in DOCUMENTS.items():
    write("scalable/mimetypes", svg64(sheet() + DOC_MARKS[kind]), names)


# ---- devices and trash -----------------------------------------------------------------
def box(x, y, w, h, r=3):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{BOX}" stroke="{CHROME}" stroke-width="1.8"/>'


def led(cx, cy):
    """a white staged bulb: the device exists"""
    return f'<circle cx="{cx}" cy="{cy}" r="3" fill="{BULB}"/><circle cx="{cx}" cy="{cy}" r="4.4" fill="none" stroke="{CHROME}" stroke-width="1"/>'


def pair(x, y, h):
    """the twin stripes, small"""
    return f'<rect x="{x}" y="{y}" width="3" height="{h}" fill="{BLUE}"/><rect x="{x + 5}" y="{y}" width="3" height="{h}" fill="{BLUE}"/>'


DRIVE = box(8, 21, 48, 23) + pair(14, 22, 21) + led(46, 32.5)
write("scalable/devices", svg64(DRIVE), ["drive-harddisk", "drive-harddisk-system", "drive-multidisk"])
REMOVABLE = f'<rect x="25" y="8" width="14" height="14" fill="{RAISED}" stroke="{CHROME}" stroke-width="1.8"/>' + box(18, 20, 28, 37) + pair(23, 21, 35) + led(37, 46)
write("scalable/devices", svg64(REMOVABLE), ["drive-removable-media", "drive-harddisk-usb", "media-removable", "media-flash"])
OPTICAL = (f'<circle cx="32" cy="32" r="21.5" fill="{BOX}" stroke="{CHROME}" stroke-width="1.8"/>'
           f'<circle cx="32" cy="32" r="13" fill="none" stroke="{BLUE}" stroke-width="3"/>' + led(32, 32))
write("scalable/devices", svg64(OPTICAL), ["drive-optical", "media-optical"])
COMPUTER = box(9, 10, 46, 32) + pair(15, 11, 30) + stroke("M32 42.5 V52 M23 54 H41", CHROME, 2.2) + led(44, 26)
write("scalable/devices", svg64(COMPUTER), ["computer", "video-display"])
BIN = (f'<path d="M14 14 H50 V57 Q50 60 47 60 H17 Q14 60 14 57 Z" fill="{RAISED}" stroke="{CHROME}" stroke-width="2"/>'
       + stroke("M10 14 H54", CHROME, 2.4) + stroke("M26 13 V7 H38 V13", CHROME, 2)
       + f'<path d="M14 29 H50 M14 45 H50" stroke="{SIDE}" stroke-width="1.6"/>')
write("scalable/places", svg64(BIN), ["user-trash"])
write("scalable/places", svg64(BIN + f'<circle cx="49" cy="11" r="5" fill="{RED}" stroke="{GROUND}" stroke-width="1.5"/>'), ["user-trash-full"])


# ---- 16px sidebar: plain line icons ------------------------------------------------------
SYM = {
    "home": '<path d="M2 8 L8 2.5 L14 8"/><path d="M4 7 V14 H12 V7"/>',
    "desktop": '<rect x="2" y="3" width="12" height="8"/><path d="M6 14 H10"/>',
    "documents": '<path d="M4 2 H10 L13 5 V14 H4 Z"/><path d="M6.5 8 H10.5 M6.5 11 H9.5"/>',
    "downloads": '<path d="M8 2 V11"/><path d="M4 7.5 L8 11.5 L12 7.5"/><path d="M3 14 H13"/>',
    "music": '<path d="M5.5 12.5 V3.5 L12.5 2.5 V11.5"/><circle cx="4" cy="12.5" r="1.6"/><circle cx="11" cy="11.5" r="1.6"/>',
    "pictures": '<path d="M2 13 L6 7 L9 10.5 L11 8.5 L14 13 Z"/><circle cx="11.5" cy="4.5" r="1.2"/>',
    "videos": '<path d="M5 3 V13 L13 8 Z"/>',
    "templates": '<rect x="2.5" y="2.5" width="11" height="11" stroke-dasharray="2.2 2"/>',
    "share": '<circle cx="4" cy="8" r="1.6"/><circle cx="12" cy="3.8" r="1.6"/><circle cx="12" cy="12.2" r="1.6"/><path d="M5.4 7.2 L10.6 4.6 M5.4 8.8 L10.6 11.4"/>',
    "folder": '<path d="M2 4 H6.5 L8 5.5 H14 V13 H2 Z"/>',
    "recent": '<circle cx="8" cy="8" r="6"/><path d="M8 4.5 V8 L10.5 9.5"/>',
    "trash": '<path d="M3 4.5 H13"/><path d="M6 4.5 V2.5 H10 V4.5"/><path d="M4.5 4.5 L5.5 14 H10.5 L11.5 4.5"/>',
    "bookmark": '<path d="M4 2 H12 V14 L8 10.5 L4 14 Z"/>',
    "drive": '<rect x="2" y="5" width="12" height="6"/><path d="M10.5 8 H11.5"/>',
    "removable": '<rect x="4.5" y="5" width="7" height="9"/><path d="M6 5 V2 H10 V5"/>',
    "optical": '<circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="1.5"/>',
    "computer": '<rect x="2" y="2.5" width="12" height="8"/><path d="M5 14 H11 M8 10.5 V14"/>',
    "network": '<circle cx="8" cy="8" r="6"/><path d="M2 8 H14 M8 2 C5 5 5 11 8 14 M8 2 C11 5 11 11 8 14"/>',
}


def sym16(key):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none" '
            f'stroke="{SIDE}" stroke-width="1.3" stroke-linecap="square" stroke-linejoin="miter">{SYM[key]}</svg>\n')


SIDEBAR = {
    "places": {
        "home": ["user-home", "folder-home", "go-home"], "desktop": ["user-desktop"], "documents": ["folder-documents"],
        "downloads": ["folder-download"], "music": ["folder-music"], "pictures": ["folder-pictures"],
        "videos": ["folder-videos"], "templates": ["folder-templates"], "share": ["folder-publicshare"],
        "folder": ["folder", "inode-directory", "folder-open", "folder-drag-accept", "folder-visiting"],
        "recent": ["document-open-recent", "folder-recent"], "trash": ["user-trash", "user-trash-full"],
        "bookmark": ["user-bookmarks", "bookmark-new"], "network": ["folder-remote", "network-workgroup", "network-server"],
    },
    "devices": {
        "drive": ["drive-harddisk", "drive-harddisk-system", "drive-multidisk"],
        "removable": ["drive-removable-media", "drive-harddisk-usb", "media-removable", "media-flash"],
        "optical": ["drive-optical", "media-optical"], "computer": ["computer", "video-display"],
    },
}
for ctx, groups in SIDEBAR.items():
    for key, names in groups.items():
        write(f"16/{ctx}", sym16(key), names)

(ROOT / "index.theme").write_text(f"""[Icon Theme]
Name={NAME}
Comment=Quarter Mile day: body-blue panels with the twin stripes for folders, white timeslips for documents, plain 16px line icons
Inherits=Adwaita,hicolor
Example=folder

Directories=16/places,16/devices,scalable/places,scalable/mimetypes,scalable/devices

[16/places]
Size=16
Context=Places
Type=Fixed

[16/devices]
Size=16
Context=Devices
Type=Fixed

[scalable/places]
Size=64
MinSize=20
MaxSize=512
Context=Places
Type=Scalable

[scalable/mimetypes]
Size=64
MinSize=16
MaxSize=512
Context=MimeTypes
Type=Scalable

[scalable/devices]
Size=64
MinSize=20
MaxSize=512
Context=Devices
Type=Scalable
""")
subprocess.run(["gtk-update-icon-cache", "-f", "-t", str(ROOT)], check=False,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"{NAME} icons written to {ROOT}")
