import urllib.request
import json

payload = {
    "text": "WÄSCHE FERTIG",
    "icon": "waschmaschine_fertig",
    "textColor": "#00FF80",
    "durationMs": 10000,
    "sound": {
        "rtttl": "bell:d=4,o=5,b=100:e,c"
    }
}

req = urllib.request.Request(
    "http://192.168.10.110/api/v1/notifications",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        print("NOTIFICATION SUCCESS:", resp.status, resp.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code, e.read().decode())
except Exception as e:
    print("ERROR:", e)

# Also test pushed app
app_payload = {
    "text": "WÄSCHT 45%",
    "icon": "waschmaschine_waschen",
    "textColor": "#64C8FF"
}

app_req = urllib.request.Request(
    "http://192.168.10.110/api/v1/apps/pushed/washer",
    data=json.dumps(app_payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="PUT"
)

try:
    with urllib.request.urlopen(app_req) as resp:
        print("PUSHED APP SUCCESS:", resp.status, resp.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR PUSHED APP:", e.code, e.read().decode())
except Exception as e:
    print("ERROR PUSHED APP:", e)
