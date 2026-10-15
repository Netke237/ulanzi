# Ulanzi TC001 Smart Desktop Matrix & Automation Hub

Open-source automation platform for the **Ulanzi TC001 Smart Pixel Clock** (8×32 RGB LED matrix, ESP32), powered by **AWTRIX NG** firmware and orchestrated by **Home Assistant** and **Mosquitto MQTT** running on Kenneth's 24/7 Mini PC (`192.168.55.60`).

---

## Architecture Overview

```
                      +---------------------------------------+
                      |       Mini PC (192.168.55.60)         |
                      |                                       |
                      |  +---------------------------------+  |
                      |  |     Home Assistant Container    |  |
                      |  |           (Port 8123)           |  |
                      |  |   - AWTRIX Blueprints           |  |
                      |  |   - Sonos Integration           |  |
                      |  |   - Weather & NTP Clock         |  |
                      |  +----------------+----------------+  |
                      |                   |                   |
                      |  +----------------v----------------+  |
                      |  |       Mosquitto Broker          |  |
                      |  |           (Port 1883)           |  |
                      |  +----------------+----------------+  |
                      +-------------------|-------------------+
                                          |
                                    MQTT over Wi-Fi
                                          |
                      +-------------------v-------------------+
                      |      Ulanzi TC001 Pixel Clock         |
                      |         (AWTRIX NG Firmware)          |
                      |   - 8x32 RGB LED Matrix Display       |
                      |   - Onboard Sensors & Buttons         |
                      +---------------------------------------+
```

---

## 1. Flashing the Ulanzi TC001 with AWTRIX NG

AWTRIX NG features a zero-install browser flasher using the Web Serial API.

1. **Connect the Clock**: Plug your Ulanzi TC001 into your computer using a USB-C data cable. Turn the device on using the side switch.
2. **Open the Web Flasher**: In Google Chrome or Microsoft Edge, navigate to:
   👉 **[https://blueforcer.github.io/awtrix-ng/](https://blueforcer.github.io/awtrix-ng/)**
3. **Select Port & Flash**:
   - Click **Connect** and select the ESP32 serial port (e.g. `CP210x` or `CH340`).
   - Select **Install AWTRIX NG** and choose **Erase device** for a clean install.
   - The flashing process takes approximately 60 seconds.
4. **Initial Wi-Fi Configuration**:
   - Once flashed, the clock reboots and creates a Wi-Fi Access Point named `AWTRIX-XXXXXX`.
   - Connect your phone or PC to that AP (password: `awtrixxx` or open captive portal).
   - In the captive portal, select your home Wi-Fi network and enter the password.
   - The clock will reboot and display its assigned local IP address (e.g. `192.168.55.xxx`).

---

## 2. Connecting AWTRIX NG to MQTT

1. Open your browser and go to `http://<clock-ip>/` to access the AWTRIX NG Web UI.
2. Navigate to **Settings** -> **MQTT**:
   - **Broker IP**: `192.168.55.60`
   - **Port**: `1883`
   - **User / Password**: Leave blank (anonymous enabled on local LAN) or enter credentials if configured.
   - **Topic Prefix**: `awtrix` (default).
3. Click **Save & Restart**. The clock will connect to Mosquitto on the Mini PC.

---

## 3. Deploying Home Assistant & Mosquitto on Mini PC

The Docker Compose stack runs on the 24/7 Mini PC (`minipc` at `192.168.55.60`).

### Quick Deploy from Dev Machine
Run the deployment script:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/deploy.ps1
```

The script automatically:
1. Pushes the latest commits to GitHub (`origin/main`).
2. SSHs into `minipc` and syncs the repository into `C:\GitHub\ulanzi`.
3. Executes `docker compose up -d`.
4. Verifies TCP connectivity on port `1883` (Mosquitto) and HTTP `8123` (Home Assistant).

---

## 4. Configuring Display Screens via Blueprints (No Coding)

Once Home Assistant is running:
1. Open Home Assistant at **`http://192.168.55.60:8123`** and complete the one-time owner account setup.
2. In Home Assistant, add the **MQTT** integration (**Settings** -> **Devices & Services** -> **Add Integration** -> **MQTT** -> enter broker `localhost` or `mosquitto`, port `1883`).
3. Import the official AWTRIX Light/NG Blueprints:
   - Navigate to **Settings** -> **Automations & Scenes** -> **Blueprints** -> **Import Blueprint**.
   - Paste the blueprint URL from GitHub (e.g. [Awtrix Light Core Blueprint](https://github.com/10der/homeassistant-custom_components-awtrix)).
4. Create an Automation from the Blueprint:
   - Pick your sensor (e.g. Weather, Sonos currently playing title, Room Temperature).
   - Select an icon ID from the [Awtrix Icon Library](https://developer.lametric.com/icons).
   - Set duration and color.
   - Click **Save**.

The screen immediately enters the rotation cycle on your Ulanzi TC001!

---

## Repository Structure

```
├── CLAUDE.md                   # Agent workflow guidelines
├── AGENTS.md                   # Shared agent rules
├── GLOSSARY.md                 # Project vocabulary & hardware terms
├── docker-compose.yml          # Production Docker Compose for Mini PC
├── mosquitto/
│   └── config/
│       └── mosquitto.conf      # Local MQTT broker configuration
├── docs/
│   ├── adr/                    # Architecture Decision Records (ADRs)
│   └── agents/                 # Agent specifications (issue tracker, domain rules)
└── scripts/
    └── deploy.ps1              # Deployment and verification script for Mini PC
```
