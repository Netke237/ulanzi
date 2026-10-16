import urllib.request
import json
import time

# Test deletion of pushed app via DELETE request
req_delete = urllib.request.Request(
    "http://192.168.10.110/api/v1/apps/pushed/washer",
    method="DELETE"
)
try:
    with urllib.request.urlopen(req_delete) as resp:
        print("DELETE APP SUCCESS:", resp.status, resp.read().decode())
except Exception as e:
    print("DELETE APP ERROR:", e)
