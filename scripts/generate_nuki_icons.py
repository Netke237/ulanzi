#!/usr/bin/env python3
"""
Generate curated 8x8 pixel-art GIF icons for Nuki Smart Lock and Door Security:
- nuki_locked.gif    (Closed green padlock)
- nuki_unlocked.gif  (Open amber/red padlock)
- door_open.gif      (Open doorway alert)
- battery_low.gif    (Animated blinking low battery)
"""

import os
from PIL import Image

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "icons", "nuki")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color constants (RGBA)
TRANS = (0, 0, 0, 0)
WHITE = (240, 240, 240, 255)
SILVER = (180, 190, 200, 255)
DARK_GRAY = (40, 45, 50, 255)
BLACK = (20, 20, 20, 255)

GREEN_BODY = (0, 215, 100, 255)
GREEN_HI = (80, 245, 150, 255)

AMBER_BODY = (255, 145, 0, 255)
AMBER_HI = (255, 190, 60, 255)

RED_ALERT = (255, 50, 50, 255)
RED_DIM = (160, 20, 20, 255)

WARM_DOOR = (255, 170, 50, 255)
DOOR_HANDLE = (255, 255, 255, 255)


def make_gif(frames, filename, duration=400):
    filepath = os.path.join(OUTPUT_DIR, filename)
    converted_frames = []
    for img in frames:
        # Convert RGBA to P mode with transparency
        p_img = Image.new("RGBA", (8, 8), TRANS)
        p_img.paste(img, (0, 0))
        converted = p_img.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=16)
        converted_frames.append(converted)

    converted_frames[0].save(
        filepath,
        save_all=True,
        append_images=converted_frames[1:],
        duration=duration,
        loop=0,
        optimize=False,
    )
    print(f"Generated: {filepath} ({os.path.getsize(filepath)} bytes)")


def generate_nuki_locked():
    # 8x8 Closed Green Padlock
    # Shackle closed, green body with keyhole
    grid = [
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [1, 2, 2, 2, 2, 2, 1, 0],
        [1, 2, 2, 3, 2, 2, 1, 0],
        [1, 2, 2, 3, 2, 2, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    color_map_f1 = {0: TRANS, 1: SILVER, 2: GREEN_BODY, 3: BLACK}
    color_map_f2 = {0: TRANS, 1: WHITE, 2: GREEN_HI, 3: DARK_GRAY}

    f1 = Image.new("RGBA", (8, 8))
    f2 = Image.new("RGBA", (8, 8))
    for y in range(8):
        for x in range(8):
            f1.putpixel((x, y), color_map_f1[grid[y][x]])
            f2.putpixel((x, y), color_map_f2[grid[y][x]])

    make_gif([f1, f2], "nuki_locked.gif", duration=800)


def generate_nuki_unlocked():
    # 8x8 Open Padlock (shackle raised and opened to the right)
    grid = [
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [1, 2, 2, 2, 2, 2, 1, 0],
        [1, 2, 2, 3, 2, 2, 1, 0],
        [1, 2, 2, 3, 2, 2, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    color_map_f1 = {0: TRANS, 1: SILVER, 2: AMBER_BODY, 3: BLACK}
    color_map_f2 = {0: TRANS, 1: WHITE, 2: AMBER_HI, 3: DARK_GRAY}

    f1 = Image.new("RGBA", (8, 8))
    f2 = Image.new("RGBA", (8, 8))
    for y in range(8):
        for x in range(8):
            f1.putpixel((x, y), color_map_f1[grid[y][x]])
            f2.putpixel((x, y), color_map_f2[grid[y][x]])

    make_gif([f1, f2], "nuki_unlocked.gif", duration=500)


def generate_door_open():
    # 8x8 Open Door / Frame with open portal
    grid = [
        [1, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 0, 2, 2, 0, 1, 0],
        [1, 0, 2, 2, 2, 0, 1, 0],
        [1, 0, 2, 3, 2, 0, 1, 0],
        [1, 0, 2, 2, 2, 0, 1, 0],
        [1, 0, 0, 2, 2, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    color_map_f1 = {0: TRANS, 1: WHITE, 2: WARM_DOOR, 3: RED_ALERT}
    color_map_f2 = {0: TRANS, 1: SILVER, 2: WARM_DOOR, 3: WHITE}

    f1 = Image.new("RGBA", (8, 8))
    f2 = Image.new("RGBA", (8, 8))
    for y in range(8):
        for x in range(8):
            f1.putpixel((x, y), color_map_f1[grid[y][x]])
            f2.putpixel((x, y), color_map_f2[grid[y][x]])

    make_gif([f1, f2], "door_open.gif", duration=400)


def generate_battery_low():
    # 8x8 Battery with blinking red segment
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 0],
        [1, 2, 0, 0, 0, 1, 1, 0],
        [1, 2, 0, 0, 0, 1, 1, 0],
        [1, 2, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    f1 = Image.new("RGBA", (8, 8))
    f2 = Image.new("RGBA", (8, 8))
    for y in range(8):
        for x in range(8):
            val = grid[y][x]
            f1.putpixel((x, y), TRANS if val == 0 else (WHITE if val == 1 else RED_ALERT))
            f2.putpixel((x, y), TRANS if val == 0 else (WHITE if val == 1 else RED_DIM))

    make_gif([f1, f2], "battery_low.gif", duration=500)


if __name__ == "__main__":
    generate_nuki_locked()
    generate_nuki_unlocked()
    generate_door_open()
    generate_battery_low()
