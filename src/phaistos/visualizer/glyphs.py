"""Universal Glyph Repertoire: Emoji, Vector SVG Silhouettes, and Unicode mappings for all 45 signs.

Provides reliable multi-mode rendering (Emoji+ID, Vector SVG, Unicode SMP)
to eliminate the missing-font 'four horizontal lines' issue across all platforms.
"""

from typing import Dict, Optional


GLYPH_REGISTRY: Dict[str, Dict[str, str]] = {
    "01": {
        "name": "PEDESTRIAN",
        "emoji": "🚶",
        "short_name": "Youth",
        "label": "01 🚶 Youth",
        "unicode_char": "𐇐",
        "unicode_hex": "0x101D0",
        "vector_svg": '<circle cx="16" cy="6" r="3" fill="currentColor"/><path d="M16 9v8l-4 8m4-8l4 8m-6-13l3 4 3-4" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>',
    },
    "02": {
        "name": "PLUMED HEAD",
        "emoji": "🪶",
        "short_name": "Plumed Head",
        "label": "02 🪶 Plumed",
        "unicode_char": "𐇑",
        "unicode_hex": "0x101D1",
        "vector_svg": '<path d="M12 28v-6c-3-2-4-5-4-9 0-5 3-9 8-9s8 4 8 9c0 4-1 7-4 9v6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 5l1-4m3 4l1-4m3 4l1-4m3 4l1-4m3 4l1-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="19" cy="12" r="1.5" fill="currentColor"/><path d="M17 18h4" stroke="currentColor" stroke-width="1.5"/>',
    },
    "03": {
        "name": "TATTOOED HEAD",
        "emoji": "👤",
        "short_name": "Tattooed Head",
        "label": "03 👤 Tattooed",
        "unicode_char": "𐇒",
        "unicode_hex": "0x101D2",
        "vector_svg": '<path d="M11 27v-5c-3-2-4-5-4-9 0-6 4-10 9-10s9 4 9 10c0 4-1 7-4 9v5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="13" cy="15" r="2" fill="currentColor"/><circle cx="18" cy="13" r="1.5" fill="currentColor"/>',
    },
    "04": {
        "name": "CAPTIVE",
        "emoji": "⛓️",
        "short_name": "Captive",
        "label": "04 ⛓️ Captive",
        "unicode_char": "𐇓",
        "unicode_hex": "0x101D3",
        "vector_svg": '<circle cx="16" cy="7" r="3" fill="currentColor"/><path d="M16 10v10l-4 8m4-8l4 8M11 16h10" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>',
    },
    "05": {
        "name": "CHILD",
        "emoji": "👶",
        "short_name": "Child",
        "label": "05 👶 Child",
        "unicode_char": "𐇔",
        "unicode_hex": "0x101D4",
        "vector_svg": '<circle cx="16" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 12v9m-4-6l4-3 4 3m-4 6l-3 6m3-6l3 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    },
    "06": {
        "name": "WOMAN",
        "emoji": "👩",
        "short_name": "Goddess",
        "label": "06 👩 Goddess",
        "unicode_char": "𐇕",
        "unicode_hex": "0x101D5",
        "vector_svg": '<circle cx="16" cy="6" r="3" fill="currentColor"/><path d="M12 11h8l-2 5h-4zM10 16h12l2 12H8z" fill="none" stroke="currentColor" stroke-width="1.8"/>',
    },
    "07": {
        "name": "BREAST",
        "emoji": "🍼",
        "short_name": "Breast",
        "label": "07 🍼 Breast",
        "unicode_char": "𐇖",
        "unicode_hex": "0x101D6",
        "vector_svg": '<path d="M6 24c2-9 6-16 10-16s8 7 10 16" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="16" cy="8" r="2" fill="currentColor"/>',
    },
    "08": {
        "name": "GAUNTLET",
        "emoji": "🥊",
        "short_name": "Gauntlet",
        "label": "08 🥊 Gauntlet",
        "unicode_char": "𐇗",
        "unicode_hex": "0x101D7",
        "vector_svg": '<path d="M10 28V14c0-3 2-6 6-6s6 3 6 6v14" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 18h12M10 23h12" stroke="currentColor" stroke-width="1.8"/>',
    },
    "09": {
        "name": "TIARA",
        "emoji": "🪖",
        "short_name": "Tiara",
        "label": "09 🪖 Tiara",
        "unicode_char": "𐇘",
        "unicode_hex": "0x101D8",
        "vector_svg": '<path d="M6 24h20L21 9l-5 5-5-5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
    },
    "10": {
        "name": "ARROW",
        "emoji": "🏹",
        "short_name": "Arrow",
        "label": "10 🏹 Arrow",
        "unicode_char": "𐇙",
        "unicode_hex": "0x101D9",
        "vector_svg": '<path d="M16 28V4m-5 7l5-7 5 7M11 26l5-4 5 4" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    },
    "11": {
        "name": "BOW",
        "emoji": "🏹",
        "short_name": "Bow",
        "label": "11 🏹 Bow",
        "unicode_char": "𐇚",
        "unicode_hex": "0x101DA",
        "vector_svg": '<path d="M10 4c10 4 10 20 0 24" fill="none" stroke="currentColor" stroke-width="2.5"/><line x1="10" y1="4" x2="10" y2="28" stroke="currentColor" stroke-width="1.5"/>',
    },
    "12": {
        "name": "SHIELD",
        "emoji": "🛡️",
        "short_name": "Shield",
        "label": "12 🛡️ Shield",
        "unicode_char": "𐇛",
        "unicode_hex": "0x101DB",
        "vector_svg": '<circle cx="16" cy="16" r="12" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="16" cy="16" r="3" fill="currentColor"/><circle cx="16" cy="9" r="1.5" fill="currentColor"/><circle cx="16" cy="23" r="1.5" fill="currentColor"/><circle cx="9" cy="16" r="1.5" fill="currentColor"/><circle cx="23" cy="16" r="1.5" fill="currentColor"/>',
    },
    "13": {
        "name": "CLUB",
        "emoji": "🪵",
        "short_name": "Club",
        "label": "13 🪵 Club",
        "unicode_char": "𐇜",
        "unicode_hex": "0x101DC",
        "vector_svg": '<path d="M14 28l-2-12c-1-4 1-9 4-11s6 2 5 6l-3 17z" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "14": {
        "name": "MANACLES",
        "emoji": "🔗",
        "short_name": "Manacles",
        "label": "14 🔗 Manacles",
        "unicode_char": "𐇝",
        "unicode_hex": "0x101DD",
        "vector_svg": '<circle cx="10" cy="16" r="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="22" cy="16" r="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15 16h2" stroke="currentColor" stroke-width="2"/>',
    },
    "15": {
        "name": "MATTOCK",
        "emoji": "⛏️",
        "short_name": "Adze",
        "label": "15 ⛏️ Adze",
        "unicode_char": "𐇞",
        "unicode_hex": "0x101DE",
        "vector_svg": '<path d="M8 8c5-3 12-3 16 2M16 8v20" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round"/>',
    },
    "16": {
        "name": "SAW",
        "emoji": "🔪",
        "short_name": "Knife",
        "label": "16 🔪 Knife",
        "unicode_char": "𐇟",
        "unicode_hex": "0x101DF",
        "vector_svg": '<path d="M12 28V6l6 4v14z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 10l3-2m-3 5l3-2m-3 5l3-2m-3 5l3-2" stroke="currentColor" stroke-width="1.5"/>',
    },
    "17": {
        "name": "LID",
        "emoji": "🏺",
        "short_name": "Pyxis Lid",
        "label": "17 🏺 Lid",
        "unicode_char": "𐇠",
        "unicode_hex": "0x101E0",
        "vector_svg": '<path d="M6 22c2-8 18-8 20 0z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M14 14V8h4v6" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "18": {
        "name": "BOOMERANG",
        "emoji": "📐",
        "short_name": "Angle",
        "label": "18 📐 Angle",
        "unicode_char": "𐇡",
        "unicode_hex": "0x101E1",
        "vector_svg": '<path d="M8 6l16 10L10 26" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    },
    "19": {
        "name": "CARPENTER'S ANGLE",
        "emoji": "🪵",
        "short_name": "Yoke",
        "label": "19 🪵 Yoke",
        "unicode_char": "𐇢",
        "unicode_hex": "0x101E2",
        "vector_svg": '<path d="M6 10h20M10 10v14M22 10v14" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
    },
    "20": {
        "name": "COLUMN",
        "emoji": "🪮",
        "short_name": "Comb",
        "label": "20 🪮 Comb",
        "unicode_char": "𐇣",
        "unicode_hex": "0x101E3",
        "vector_svg": '<path d="M6 8h20v6H6z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 14v12M12 14v12M16 14v12M20 14v12M24 14v12" stroke="currentColor" stroke-width="1.8"/>',
    },
    "21": {
        "name": "DOUBLE FLUTE",
        "emoji": "🪈",
        "short_name": "Aulos Flute",
        "label": "21 🪈 Flute",
        "unicode_char": "𐇤",
        "unicode_hex": "0x101E4",
        "vector_svg": '<path d="M12 4l-4 24M20 4l4 24" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="10" cy="16" r="1" fill="currentColor"/><circle cx="22" cy="16" r="1" fill="currentColor"/>',
    },
    "22": {
        "name": "DOUBLE MATTOCK",
        "emoji": "🌾",
        "short_name": "Sickle",
        "label": "22 🌾 Sickle",
        "unicode_char": "𐇥",
        "unicode_hex": "0x101E5",
        "vector_svg": '<path d="M16 28V10M8 8c5 5 11 5 16 0" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
    },
    "23": {
        "name": "COLUMN TREE",
        "emoji": "🌲",
        "short_name": "Cypress",
        "label": "23 🌲 Cypress",
        "unicode_char": "𐇦",
        "unicode_hex": "0x101E6",
        "vector_svg": '<path d="M16 28V6M16 6l-6 16h12z" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>',
    },
    "24": {
        "name": "ROSETTE",
        "emoji": "🌸",
        "short_name": "Rosette",
        "label": "24 🌸 Rosette",
        "unicode_char": "𐇧",
        "unicode_hex": "0x101E7",
        "vector_svg": '<circle cx="16" cy="16" r="4" fill="currentColor"/><path d="M16 4v8M16 20v8M4 16h8M20 16h8M7.5 7.5l5.7 5.7M18.8 18.8l5.7 5.7M7.5 24.5l5.7-5.7M18.8 13.2l5.7-5.7" stroke="currentColor" stroke-width="2"/>',
    },
    "25": {
        "name": "LILY",
        "emoji": "⚜️",
        "short_name": "Lily",
        "label": "25 ⚜️ Lily",
        "unicode_char": "𐇨",
        "unicode_hex": "0x101E8",
        "vector_svg": '<path d="M16 28V14M16 14c-4-6-9-4-10 1 3 0 7-3 10-1M16 14c4-6 9-4 10 1-3 0-7-3-10-1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    },
    "26": {
        "name": "OXEN HORN",
        "emoji": "⛵",
        "short_name": "Boat Galley",
        "label": "26 ⛵ Galley",
        "unicode_char": "𐇩",
        "unicode_hex": "0x101E9",
        "vector_svg": '<path d="M4 18c6 6 18 6 24-2-8 0-16 0-24 2z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 18V6l8 8" stroke="currentColor" stroke-width="1.8" fill="none"/>',
    },
    "27": {
        "name": "BULL HORN",
        "emoji": "🤘",
        "short_name": "Bull Horn",
        "label": "27 🤘 Horns",
        "unicode_char": "𐇪",
        "unicode_hex": "0x101EA",
        "vector_svg": '<path d="M8 8c1 8 5 14 8 14s7-6 8-14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>',
    },
    "28": {
        "name": "BULL'S LEG",
        "emoji": "🥩",
        "short_name": "Bull Leg",
        "label": "28 🥩 Bull Leg",
        "unicode_char": "𐇫",
        "unicode_hex": "0x101EB",
        "vector_svg": '<path d="M12 4h8l-3 14 3 6h-6l-2-7z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
    },
    "29": {
        "name": "CAT",
        "emoji": "🐱",
        "short_name": "Cat Head",
        "label": "29 🐱 Cat",
        "unicode_char": "𐇬",
        "unicode_hex": "0x101EC",
        "vector_svg": '<circle cx="16" cy="18" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M9 11L7 5l6 4M23 11l2-6-6 4" stroke="currentColor" stroke-width="2" fill="none"/><circle cx="13" cy="17" r="1.5" fill="currentColor"/><circle cx="19" cy="17" r="1.5" fill="currentColor"/>',
    },
    "30": {
        "name": "RAM",
        "emoji": "🐏",
        "short_name": "Ram Head",
        "label": "30 🐏 Ram",
        "unicode_char": "𐇭",
        "unicode_hex": "0x101ED",
        "vector_svg": '<circle cx="16" cy="17" r="8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 12c-4-4-5 3-1 4M20 12c4-4 5 3 1 4" stroke="currentColor" stroke-width="2" fill="none"/>',
    },
    "31": {
        "name": "EAGLE",
        "emoji": "🦅",
        "short_name": "Eagle",
        "label": "31 🦅 Eagle",
        "unicode_char": "𐇮",
        "unicode_hex": "0x101EE",
        "vector_svg": '<path d="M4 14c8-4 12-2 12 6 0-8 4-10 12-6-6 6-12 10-12 14 0-4-6-8-12-14z" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "32": {
        "name": "DOVE",
        "emoji": "🕊️",
        "short_name": "Dove",
        "label": "32 🕊️ Dove",
        "unicode_char": "𐇯",
        "unicode_hex": "0x101EF",
        "vector_svg": '<circle cx="10" cy="10" r="3" fill="currentColor"/><path d="M10 13c3 4 8 7 16 7-3-6-6-10-12-10z" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "33": {
        "name": "TUNNY",
        "emoji": "🐟",
        "short_name": "Fish",
        "label": "33 🐟 Fish",
        "unicode_char": "𐇰",
        "unicode_hex": "0x101F0",
        "vector_svg": '<path d="M6 16c6-6 16-6 22 0-6 6-16 6-22 0zM4 12l4 4-4 4z" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "34": {
        "name": "BEE",
        "emoji": "🐝",
        "short_name": "Bee",
        "label": "34 🐝 Bee",
        "unicode_char": "𐇱",
        "unicode_hex": "0x101F1",
        "vector_svg": '<ellipse cx="16" cy="18" rx="4" ry="7" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="16" cy="8" r="3" fill="currentColor"/><path d="M12 15c-5-4-6 2 0 4M20 15c5-4 6 2 0 4" stroke="currentColor" stroke-width="1.8" fill="none"/>',
    },
    "35": {
        "name": "PLANE TREE",
        "emoji": "🌿",
        "short_name": "Branch",
        "label": "35 🌿 Branch",
        "unicode_char": "𐇲",
        "unicode_hex": "0x101F2",
        "vector_svg": '<path d="M16 28V6M16 10l-6-3m6 8l-6-3m6 8l-6-3M16 10l6-3m-6 8l6-3m-6 8l6-3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    },
    "36": {
        "name": "OLIVE SPRAY",
        "emoji": "🌱",
        "short_name": "Olive Shoot",
        "label": "36 🌱 Shoot",
        "unicode_char": "𐇳",
        "unicode_hex": "0x101F3",
        "vector_svg": '<path d="M16 28V12c-4-4-2-8 0-8 2 0 4 4 0 8z" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "37": {
        "name": "PAPYRUS",
        "emoji": "🪜",
        "short_name": "Altar Podium",
        "label": "37 🪜 Altar",
        "unicode_char": "𐇴",
        "unicode_hex": "0x101F4",
        "vector_svg": '<path d="M8 26h16M10 20h12M12 14h8M14 8h4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>',
    },
    "38": {
        "name": "ROSETTE SHRINE",
        "emoji": "🏛️",
        "short_name": "Peak Shrine",
        "label": "38 🏛️ Shrine",
        "unicode_char": "𐇵",
        "unicode_hex": "0x101F5",
        "vector_svg": '<path d="M6 26h20M8 26V14h16v12M12 14V8h8v6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M14 10h4" stroke="currentColor" stroke-width="1.8"/>',
    },
    "39": {
        "name": "CHALICE",
        "emoji": "🏆",
        "short_name": "Chalice",
        "label": "39 🏆 Chalice",
        "unicode_char": "𐇶",
        "unicode_hex": "0x101F6",
        "vector_svg": '<path d="M8 8h16c0 6-3 10-8 10s-8-4-8-10zM16 18v8m-5 0h10" fill="none" stroke="currentColor" stroke-width="2"/>',
    },
    "40": {
        "name": "HIDE",
        "emoji": "📜",
        "short_name": "Animal Hide",
        "label": "40 📜 Hide",
        "unicode_char": "𐇷",
        "unicode_hex": "0x101F7",
        "vector_svg": '<path d="M8 6h16l-3 10 3 10H8l3-10z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
    },
    "41": {
        "name": "FLUTE VASE",
        "emoji": "🏺",
        "short_name": "Hydria Pitcher",
        "label": "41 🏺 Pitcher",
        "unicode_char": "𐇸",
        "unicode_hex": "0x101F8",
        "vector_svg": '<path d="M12 6h8l2 12-4 8h-4l-4-8z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 10c3 0 4 4 2 8" fill="none" stroke="currentColor" stroke-width="1.8"/>',
    },
    "42": {
        "name": "GRATER",
        "emoji": "🥢",
        "short_name": "Tally Grater",
        "label": "42 🥢 Grater",
        "unicode_char": "𐇹",
        "unicode_hex": "0x101F9",
        "vector_svg": '<path d="M10 6h12v20H10z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 10h1M18 10h1M13 16h1M18 16h1M13 22h1M18 22h1" stroke="currentColor" stroke-width="2"/>',
    },
    "43": {
        "name": "STRAINER",
        "emoji": "🔺",
        "short_name": "Strainer",
        "label": "43 🔺 Strainer",
        "unicode_char": "𐇺",
        "unicode_hex": "0x101FA",
        "vector_svg": '<path d="M16 6l10 18H6z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="16" cy="15" r="1" fill="currentColor"/><circle cx="13" cy="19" r="1" fill="currentColor"/><circle cx="19" cy="19" r="1" fill="currentColor"/>',
    },
    "44": {
        "name": "SMALL AXE",
        "emoji": "🪓",
        "short_name": "Labrys Axe",
        "label": "44 🪓 Labrys",
        "unicode_char": "𐇻",
        "unicode_hex": "0x101FB",
        "vector_svg": '<path d="M16 4v24M16 8c-6-3-8 3-2 6 6 3 2 9-2 6m4-12c6-3 8 3 2 6-6 3-2 9 2 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    },
    "45": {
        "name": "WAVY BAND",
        "emoji": "〰️",
        "short_name": "Water Wave",
        "label": "45 〰️ Wave",
        "unicode_char": "𐇽",
        "unicode_hex": "0x101FD",
        "vector_svg": '<path d="M6 12c3-4 6 4 9 0s6 4 9 0M6 18c3-4 6 4 9 0s6 4 9 0" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
    },
}


def get_sign_glyph_data(sign_id: str) -> Dict[str, str]:
    """Retrieve multi-mode rendering descriptors for a sign ID."""
    pad_id = f"{int(sign_id):02d}" if sign_id.isdigit() else sign_id
    if pad_id in GLYPH_REGISTRY:
        return GLYPH_REGISTRY[pad_id]
    return {
        "name": f"SIGN {pad_id}",
        "emoji": "𐇐",
        "short_name": f"Sign {pad_id}",
        "label": f"{pad_id} 𐇐",
        "unicode_char": "𐇐",
        "unicode_hex": "0x101D0",
        "vector_svg": '<circle cx="16" cy="16" r="12" fill="none" stroke="currentColor" stroke-width="2"/><text x="16" y="20" font-size="10" text-anchor="middle" fill="currentColor">?</text>',
    }


def get_sign_display(sign_id: str, mode: str = "emoji_utf8") -> str:
    """
    Format sign for UI or text display.
    Modes:
      - 'emoji_utf8' (default): Universal emoji + ID (e.g. '🪶 02')
      - 'emoji_only': Just the emoji (e.g. '🪶')
      - 'label': Extended mnemonic (e.g. '02 🪶 Plumed')
      - 'unicode': Raw SMP Unicode character (e.g. '𐇑')
    """
    data = get_sign_glyph_data(sign_id)
    pad_id = f"{int(sign_id):02d}" if sign_id.isdigit() else sign_id

    if mode == "emoji_only":
        return data["emoji"]
    elif mode == "label":
        return data["label"]
    elif mode == "unicode":
        return data["unicode_char"]
    else:  # default 'emoji_utf8'
        return f"{data['emoji']} {pad_id}"


def get_all_glyphs_catalog() -> Dict[str, Dict[str, str]]:
    """Return the entire 45-sign visual catalog."""
    return GLYPH_REGISTRY
