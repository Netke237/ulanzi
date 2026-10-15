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
