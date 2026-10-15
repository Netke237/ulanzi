# ADR 0002: Select AWTRIX NG Firmware with Home Assistant Blueprints

## Status
Accepted

## Context
The Ulanzi TC001 requires firmware to drive its 8×32 WS2812B RGB LED matrix, onboard sensors (ambient light, battery voltage, temperature), buttons, buzzer, and Wi-Fi interface. Kenneth wanted a solution similar to AWTRIX that makes it as easy and user-friendly as possible to modify what is shown on screen, without incurring heavy development or maintenance overhead.

We evaluated three alternatives:
1. **AWTRIX NG (Next Generation)**: Dedicated, actively maintained matrix clock firmware featuring on-device Berry scripting, web UI, MQTT auto-discovery, and deep Home Assistant Blueprint integration.
2. **EspHoMaTriXv3 (Native ESPHome)**: ESPHome component for TC001 integrating directly via the ESPHome native API (no MQTT). Updating display layouts or features requires compiling YAML configurations.
3. **PixelIt / Custom Microservice**: Generic matrix display client driven by a custom rendering host.

## Decision
1. Flash the **Ulanzi TC001** with **AWTRIX NG** via the browser-based Web Serial installer.
2. Manage display screens, rotations, and notifications inside **Home Assistant** using community **Blueprints** (e.g. `10der` or `vasqued2` Awtrix blueprints).
3. Connect AWTRIX NG to the local **Mosquitto MQTT broker** hosted on the Mini PC.

## Consequences
- **Positive**: Changing what is displayed requires zero programming; users configure sensors, icons, colors, and durations via visual dropdowns in the Home Assistant web interface.
- **Positive**: 10,000+ community pixel icons and animations are accessible directly.
- **Positive**: Firmware updates and diagnostics can be performed over Wi-Fi via the clock's local web UI.
- **Trade-off**: Requires running an MQTT broker (Mosquitto) on the Mini PC in addition to Home Assistant.
