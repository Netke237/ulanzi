#!/usr/bin/env python3
"""
Generate and upload pixel-art 8x8 animated GIFs for Washing Machine and Dryer to Ulanzi TC001.
"""

import os
from PIL import Image

output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "icons", "appliances")
os.makedirs(output_dir, exist_ok=True)

# Colors
T = (0, 0, 0, 0)          # Transparent
W = (230, 235, 240, 255)  # White body
D = (50, 60, 70, 255)     # Display / control
G = (100, 110, 120, 255)  # Door rim
K = (80, 80, 80, 255)     # Feet

# 1. waschmaschine_waschen (Washing - rotating blue water)
water_frames = [
    # Frame 1
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (0,180,255,255), (200,240,255,255), G, W, T],
        [T, W, G, (0,120,240,255), (0,150,255,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
    # Frame 2
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (0,120,240,255), (0,180,255,255), G, W, T],
        [T, W, G, (0,150,255,255), (200,240,255,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
    # Frame 3
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (0,150,255,255), (0,120,240,255), G, W, T],
        [T, W, G, (200,240,255,255), (0,180,255,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
    # Frame 4
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (200,240,255,255), (0,150,255,255), G, W, T],
        [T, W, G, (0,180,255,255), (0,120,240,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
]

def make_gif(grid_frames, duration_ms=250):
    images = []
    for grid in grid_frames:
        im = Image.new("RGBA", (8, 8))
        for y in range(8):
            for x in range(8):
                im.putpixel((x, y), grid[y][x])
        images.append(im.convert("P", palette=Image.ADAPTIVE))
    return images

# Save waschmaschine_waschen
imgs_waschen = make_gif(water_frames, duration_ms=250)
imgs_waschen[0].save(
    os.path.join(output_dir, "waschmaschine_waschen.gif"),
    save_all=True,
    append_images=imgs_waschen[1:],
    duration=250,
    loop=0,
    disposal=2
)

# 2. waschmaschine_spuehlen (Rinsing - rising bubbles)
rinse_frames = [
    # Frame 1
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (255,255,255,255), (0,120,220,255), G, W, T],
        [T, W, G, (0,150,255,255), (255,255,255,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
    # Frame 2
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (0,150,255,255), (255,255,255,255), G, W, T],
        [T, W, G, (255,255,255,255), (0,120,220,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
]
imgs_spuehlen = make_gif(rinse_frames, duration_ms=300)
imgs_spuehlen[0].save(
    os.path.join(output_dir, "waschmaschine_spuehlen.gif"),
    save_all=True,
    append_images=imgs_spuehlen[1:],
    duration=300,
    loop=0,
    disposal=2
)

# 3. waschmaschine_schleudern (Spinning - fast streak animation)
spin_frames = [
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (255,255,255,255), (0,200,255,255), G, W, T],
        [T, W, G, (0,200,255,255), (255,255,255,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (0,200,255,255), (255,255,255,255), G, W, T],
        [T, W, G, (255,255,255,255), (0,200,255,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
]
imgs_schleudern = make_gif(spin_frames, duration_ms=120)
imgs_schleudern[0].save(
    os.path.join(output_dir, "waschmaschine_schleudern.gif"),
    save_all=True,
    append_images=imgs_schleudern[1:],
    duration=120,
    loop=0,
    disposal=2
)

# 4. waschmaschine_fertig (Finished - glowing green checkmark / pulse)
fertig_frames = [
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, (0,255,100,255), (0,255,100,255), G, W, T],
        [T, W, (0,255,100,255), (200,255,200,255), (0,255,100,255), (0,255,100,255), W, T],
        [T, W, (0,255,100,255), (0,255,100,255), (200,255,200,255), (0,255,100,255), W, T],
        [T, W, G, (0,255,100,255), (0,255,100,255), G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, (0,200,80,255), (0,200,80,255), G, W, T],
        [T, W, (0,200,80,255), (255,255,255,255), (0,200,80,255), (0,200,80,255), W, T],
        [T, W, (0,200,80,255), (0,200,80,255), (255,255,255,255), (0,200,80,255), W, T],
        [T, W, G, (0,200,80,255), (0,200,80,255), G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
]
imgs_fertig = make_gif(fertig_frames, duration_ms=400)
imgs_fertig[0].save(
    os.path.join(output_dir, "waschmaschine_fertig.gif"),
    save_all=True,
    append_images=imgs_fertig[1:],
    duration=400,
    loop=0,
    disposal=2
)

# 5. trockner_trocknen (Dryer - rotating warm orange/yellow heat drum)
dryer_heat_frames = [
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (255,120,0,255), (255,200,0,255), G, W, T],
        [T, W, G, (255,60,0,255), (255,140,0,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (255,60,0,255), (255,120,0,255), G, W, T],
        [T, W, G, (255,140,0,255), (255,200,0,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (255,140,0,255), (255,60,0,255), G, W, T],
        [T, W, G, (255,200,0,255), (255,120,0,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, G, (255,200,0,255), (255,140,0,255), G, W, T],
        [T, W, G, (255,120,0,255), (255,60,0,255), G, W, T],
        [T, W, G, G, G, G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
]
imgs_dryer = make_gif(dryer_heat_frames, duration_ms=250)
imgs_dryer[0].save(
    os.path.join(output_dir, "trockner_trocknen.gif"),
    save_all=True,
    append_images=imgs_dryer[1:],
    duration=250,
    loop=0,
    disposal=2
)

# 6. trockner_fertig (Dryer finished - green clean pulse)
dryer_fertig_frames = [
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, (0,255,120,255), (0,255,120,255), G, W, T],
        [T, W, (0,255,120,255), (255,255,255,255), (0,255,120,255), (0,255,120,255), W, T],
        [T, W, (0,255,120,255), (0,255,120,255), (255,255,255,255), (0,255,120,255), W, T],
        [T, W, G, (0,255,120,255), (0,255,120,255), G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
    [
        [T, W, D, D, W, D, W, T],
        [T, W, W, W, W, W, W, T],
        [T, W, G, (0,200,90,255), (0,200,90,255), G, W, T],
        [T, W, (0,200,90,255), (200,255,200,255), (0,200,90,255), (0,200,90,255), W, T],
        [T, W, (0,200,90,255), (0,200,90,255), (200,255,200,255), (0,200,90,255), W, T],
        [T, W, G, (0,200,90,255), (0,200,90,255), G, W, T],
        [T, W, W, W, W, W, W, T],
        [T, K, T, T, T, T, K, T],
    ],
]
imgs_dryer_fertig = make_gif(dryer_fertig_frames, duration_ms=400)
imgs_dryer_fertig[0].save(
    os.path.join(output_dir, "trockner_fertig.gif"),
    save_all=True,
    append_images=imgs_dryer_fertig[1:],
    duration=400,
    loop=0,
    disposal=2
)

# 7. idos_warnung (Warning triangle with exclamation)
R = (255, 40, 0, 255)
Y = (255, 200, 0, 255)
B = (255, 255, 255, 255)
warn_frames = [
    [
        [T, T, T, Y, Y, T, T, T],
        [T, T, Y, B, B, Y, T, T],
        [T, T, Y, B, B, Y, T, T],
        [T, Y, Y, B, B, Y, Y, T],
        [T, Y, Y, T, T, Y, Y, T],
        [Y, Y, Y, B, B, Y, Y, Y],
        [Y, Y, Y, Y, Y, Y, Y, Y],
        [T, T, T, T, T, T, T, T],
    ],
    [
        [T, T, T, R, R, T, T, T],
        [T, T, R, B, B, R, T, T],
        [T, T, R, B, B, R, T, T],
        [T, R, R, B, B, R, R, T],
        [T, R, R, T, T, R, R, T],
        [R, R, R, B, B, R, R, R],
        [R, R, R, R, R, R, R, R],
        [T, T, T, T, T, T, T, T],
    ],
]
imgs_warn = make_gif(warn_frames, duration_ms=350)
imgs_warn[0].save(
    os.path.join(output_dir, "idos_warnung.gif"),
    save_all=True,
    append_images=imgs_warn[1:],
    duration=350,
    loop=0,
    disposal=2
)

print("Created 7 appliance icons in:", output_dir)
for f in os.listdir(output_dir):
    print(" -", f, os.path.getsize(os.path.join(output_dir, f)), "bytes")
