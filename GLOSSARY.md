# Glossary

Domain vocabulary and architectural concepts for the Ulanzi desktop project.

## Hardware & Deployment

- **`Ulanzi TC001`**: Smart Pixel Clock featuring an 8×32 WS2812B RGB LED matrix (256 pixels), ESP32 microcontroller, ambient light sensor, buzzer, microphone, 3 navigation buttons, and a 4,400 mAh rechargeable battery.
- **`Mini PC (minipc)`**: Kenneth's local 24/7 Windows server at `192.168.55.60` running Docker containers for local infrastructure (`sonos-network`, `trading-assistant`, and now `home-assistant`).
- **`Home Assistant (HA)`**: Open-source local automation platform running as a Docker container on the Mini PC, serving as the central coordinator for sensors, screen rotation, and push notifications to the display.
- **`Mosquitto`**: Lightweight MQTT broker running in Docker on the Mini PC to handle pub/sub messaging between Home Assistant and the display clock.

## Firmware & Display Concepts

- **`AWTRIX NG`**: The next-generation open-source firmware for ESP32 matrix displays (successor to Awtrix Light / Awtrix 3) created by Blueforcer. Provides local Web UI, MQTT auto-discovery, Berry scripting, and animation engines.
- **`AWTRIX Blueprints`**: Pre-built Home Assistant automation templates allowing zero-code creation, configuration, and scheduling of custom apps and notification popups on the TC001 matrix directly from the Home Assistant web UI.
- **`App Rotation`**: The continuous cyclic loop of active information screens displayed on the AWTRIX matrix (e.g., clock, weather, room temp, Sonos now-playing).
- **`Push Notifications`**: High-priority transient messages that preempt the normal App Rotation cycle (e.g., doorbell ring, laundry done, trading alerts) with custom icons, text, and optional buzzer tones.
- **`Web Serial Flasher`**: Browser-based flashing tool (utilizing Google Chrome or Microsoft Edge Web Serial API) that writes the AWTRIX NG firmware directly to the ESP32 over USB-C without requiring command-line toolchains.

## Home Connect & Appliance Integration

- **`Home Connect`**: Cloud IoT platform developed by BSH Hausgeräte (Bosch, Siemens, Neff, Gaggenau) providing status telemetry and remote control for household appliances via SingleKey ID.
- **`Operation State`**: Standardized Home Connect state variable (`BSH.Common.Status.OperationState` e.g., `Inactive`, `Ready`, `DelayedStart`, `Run`, `Pause`, `ActionRequired`, `Finished`, `Error`).
- **`Persistent Reminder Screen`**: A temporary custom app injected into the AWTRIX display rotation that continually reminds the user of an unaddressed task (e.g., clean dishes waiting, damp laundry in drum) until cleared by an event such as the appliance door opening.
- **`Phase-Aware Appliance App`**: A dynamic AWTRIX screen that changes its animated icon and caption as the cycle progresses through physical stages (e.g. `waschmaschine_waschen` -> `waschmaschine_spuehlen` -> `waschmaschine_schleudern` -> `waschmaschine_fertig`).

## Weather & Environmental Telemetry

- **`DWD (Deutscher Wetterdienst)`**: Official German meteorological service integrated into Home Assistant via the DWD Weather & DWD Warnings integrations, supplying local radar forecasts, temperature predictions, and tiered severe weather/storm warnings.
- **`AWTRIX Icon Flash Storage (/ICONS/)`**: The on-device SPIFFS/LittleFS storage on the TC001 ESP32 where 8×8 pixel-art GIF icons (`sun.gif`, `storm.gif`, `wind.gif`, `rain.gif`, etc.) are cached and referenced locally by filename without internet CDN dependencies.
- **`Weather Rotation Apps`**: Custom AWTRIX apps (`weather_now`, `weather_today`, and `weather_tomorrow`) injected into the continuous matrix cycle displaying current temperature, today's high/low (or active wind speed), and tomorrow's forecast alongside matching animated pixel-art icons.
- **`Severe Weather Push Alert`**: High-priority transient alert (`awtrix/cmd/notify`) that preempts the normal rotation with a flashing storm/wind icon, alert description, and audible chime when DWD warning levels exceed threshold.

## Nuki Smart Lock & Door Security

- **`Nuki Smart Lock`**: Motorized smart lock mounted onto the internal euro-profile cylinder of the entrance door, exposing lock/unlock state and motor actuation.
- **`Nuki Bridge (HTTP API)`**: Local Wi-Fi hardware bridge connecting to Nuki via Bluetooth Low Energy and exposing an authenticated local REST API on port 8080 (`/list`, `/lockAction`, `/callback/add`) for sub-second push callbacks to Home Assistant without cloud dependencies.
- **`Nuki Door Sensor`**: Magnetic contact sensor installed on the door frame reporting physical position (`open` or `closed`), distinguishing physical door status from motor lock position.

## Cross-Device Interlocks & Security Curfew

- **`Departure Interlock`**: A 5-second transient check executed the moment the entrance door is locked, querying Home Connect telemetry and warning the user via Ulanzi popup (and audio chime if laundry is waiting in the drum) before they leave the premises.
- **`Arrival Task Digest`**: An automated welcome sequence triggered when the entrance door is unlocked upon returning home, alerting to completed appliance cycles and reviving persistent reminders on the desktop display.
- **`Night Lock Curfew`**: A safety automation active from 22:00 displaying a persistent red lock warning on the Ulanzi TC001 matrix until the entrance door is locked.
- **`Door Left Open Alarm`**: A safety alert triggered if the Nuki magnetic contact sensor remains open for more than 5 minutes, popping up an alert on Ulanzi with audible alarm during daytime (muted at night).


