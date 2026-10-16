#!/usr/bin/env python3
"""
Upload weather icons to Ulanzi TC001 (AWTRIX NG) internal flash storage (/ICONS/).

Usage:
    python scripts/upload_weather_icons.py [--ip <clock_ip>] [--dir <icon_dir>]

Reads default IP from .env (AWTRIX_IP) if not specified on the command line.
"""

import argparse
import os
import sys
import urllib.parse
import urllib.request


def load_env_ip():
    """Attempt to load AWTRIX_IP from .env file in repository root."""
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.isfile(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("AWTRIX_IP=") and not line.startswith("#"):
                    ip = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if ip and not ip.endswith("xxx"):
                        return ip
    return None


def upload_icon(clock_ip: str, filepath: str) -> bool:
    """
    Upload a single icon file to AWTRIX NG via the /api/v1/files multipart upload endpoint.
    AWTRIX NG LittleFS stores icons in the /ICONS/ directory.
    """
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        file_bytes = f.read()

    boundary = "----WebKitFormBoundaryUlanziWeatherUpload7MA4YWxkTrZu0gW"

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: image/gif\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    url = f"http://{clock_ip}/api/v1/files?dir=%2FICONS"
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "UlanziWeatherUploader/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status in (200, 204):
                print(f"  [OK] Uploaded {filename} -> /ICONS/{filename}")
                return True
            else:
                print(f"  [WARNING] Upload {filename} responded with HTTP {resp.status}")
                return False
    except Exception as e:
        print(f"  [ERROR] Failed to upload {filename} to {url}: {e}")
        return False


def test_connection(clock_ip: str) -> bool:
    """Verify that the AWTRIX NG clock is reachable on the network."""
    url = f"http://{clock_ip}/api/v1/system"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"Could not reach AWTRIX clock at http://{clock_ip}/ ({e})")
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload weather icons to Ulanzi TC001 AWTRIX display.")
    parser.add_argument("--ip", help="IP address of the Ulanzi TC001 clock (e.g. 192.168.10.110)")
    parser.add_argument(
        "--dir",
        default=os.path.join(os.path.dirname(__file__), "..", "assets", "icons", "weather"),
        help="Directory containing weather icon GIF files (default: assets/icons/weather)",
    )
    args = parser.parse_args()

    clock_ip = args.ip or load_env_ip() or "192.168.10.110"

    if not clock_ip:
        print("\nERROR: No clock IP provided.")
        print("Please specify --ip <clock_ip> or set AWTRIX_IP in your .env file.\n")
        sys.exit(1)

    icon_dir = os.path.abspath(args.dir)
    if not os.path.isdir(icon_dir):
        print(f"ERROR: Icon directory not found at {icon_dir}")
        sys.exit(1)

    icons = [f for f in os.listdir(icon_dir) if f.lower().endswith(".gif")]
    if not icons:
        print(f"ERROR: No .gif files found in {icon_dir}")
        sys.exit(1)

    print(f"\nTarget Ulanzi TC001 Clock: http://{clock_ip}/")
    print(f"Icon Source Directory:    {icon_dir}")
    print(f"Found {len(icons)} weather icons: {', '.join(icons)}\n")

    print("Checking clock connectivity...")
    if not test_connection(clock_ip):
        print("\nWARNING: Clock did not respond to ping at http://{clock_ip}/.")
        print("Ensure the device is powered on, connected to Wi-Fi, and your IP is correct.\n")

    print("Uploading icons to clock LittleFS /ICONS/...")
    success_count = 0
    for icon_name in sorted(icons):
        filepath = os.path.join(icon_dir, icon_name)
        if upload_icon(clock_ip, filepath):
            success_count += 1

    print(f"\nUpload complete: {success_count}/{len(icons)} icons successfully uploaded.\n")


if __name__ == "__main__":
    main()
