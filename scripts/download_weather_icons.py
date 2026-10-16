"""
Download curated 8x8 animated pixel-art weather icons from the LaMetric icon database
into the repository's assets/icons/weather/ directory.
"""

import os
import urllib.request

ICON_DEFINITIONS = {
    "sun.gif": {
        "id": 2282,
        "url": "https://developer.lametric.com/content/apps/icon_thumbs/2282.gif",
        "description": "Animated shining sun (clear/sunny)",
    },
    "cloud.gif": {
        "id": 2283,
        "url": "https://developer.lametric.com/content/apps/icon_thumbs/2283.gif",
        "description": "Animated drifting cloud (partly cloudy/overcast)",
    },
    "rain.gif": {
        "id": 2284,
        "url": "https://developer.lametric.com/content/apps/icon_thumbs/2284.gif",
        "description": "Animated falling raindrops (rain/showers)",
    },
    "storm.gif": {
        "id": 49299,
        "url": "https://developer.lametric.com/content/apps/icon_thumbs/49299.gif",
        "description": "Animated thunderstorm with lightning flash (storm/unwetter)",
    },
    "wind.gif": {
        "id": 15618,
        "url": "https://developer.lametric.com/content/apps/icon_thumbs/15618.gif",
        "description": "Animated wind gust swirl (high wind/gale)",
    },
    "snow.gif": {
        "id": 2285,
        "url": "https://developer.lametric.com/content/apps/icon_thumbs/2285.gif",
        "description": "Animated falling snowflakes (snow/sleet)",
    },
    "fog.gif": {
        "id": 2286,
        "url": "https://developer.lametric.com/content/apps/icon_thumbs/2286.gif",
        "description": "Animated mist / fog drifting (fog/foggy)",
    },
}

def download_icons(output_dir="assets/icons/weather"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Downloading weather icons to: {os.path.abspath(output_dir)}")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for filename, info in ICON_DEFINITIONS.items():
        filepath = os.path.join(output_dir, filename)
        url = info["url"]
        print(f"Fetching {filename} (ID #{info['id']} - {info['description']})...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                with open(filepath, "wb") as f:
                    f.write(data)
            print(f"  [OK] Saved {filename} ({len(data)} bytes)")
        except Exception as e:
            print(f"  [ERROR] Failed to download {filename}: {e}")

if __name__ == "__main__":
    download_icons()
