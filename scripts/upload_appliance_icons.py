#!/usr/bin/env python3
"""
Upload appliance icons to Ulanzi TC001 (AWTRIX NG) internal flash storage (/ICONS/).
"""

import os
import sys
import urllib.request

clock_ip = "192.168.10.110"
icon_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "icons", "appliances")

def upload_icon(clock_ip: str, filepath: str) -> bool:
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        file_bytes = f.read()

    boundary = "----WebKitFormBoundaryUlanziApplianceUpload7MA4YWxkTrZu0gW"
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
            "User-Agent": "UlanziApplianceUploader/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status in (200, 204):
                print(f"  [OK] Uploaded {filename} -> /ICONS/{filename}")
                return True
            else:
                print(f"  [WARN] Upload {filename} responded with HTTP {resp.status}")
                return False
    except Exception as e:
        print(f"  [ERROR] Failed to upload {filename}: {e}")
        return False

def main():
    icons = [f for f in os.listdir(icon_dir) if f.lower().endswith(".gif")]
    print(f"Uploading {len(icons)} appliance icons to clock at http://{clock_ip}/...")
    success = 0
    for name in sorted(icons):
        path = os.path.join(icon_dir, name)
        if upload_icon(clock_ip, path):
            success += 1
    print(f"\nUploaded {success}/{len(icons)} icons successfully!")

    # Verify clock storage
    verify_url = f"http://{clock_ip}/api/v1/files?dir=/ICONS"
    try:
        with urllib.request.urlopen(verify_url) as resp:
            print("\nCurrent /ICONS content on clock:")
            print(resp.read().decode())
    except Exception as e:
        print("Could not list /ICONS:", e)

if __name__ == "__main__":
    main()
