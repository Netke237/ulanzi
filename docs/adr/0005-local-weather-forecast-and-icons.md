# ADR 0005: DWD Local Weather Forecast, Dual Matrix Screens, and Local Icon Provisioning

## Status
Accepted

## Context
Kenneth wants local weather forecasts displayed on the Ulanzi TC001 desktop pixel clock (running AWTRIX NG), integrated via Home Assistant on the Mini PC (`192.168.55.60`). The display needs appropriate pixel-art icons for conditions including sun, rain, storm, and wind.

The Ulanzi TC001 8×32 WS2812B LED matrix has limited horizontal resolution (24 text pixels when an 8×8 icon is shown). The system needs glanceable daily forecasting without slow marquee text, reliable offline icon storage on the clock's flash filesystem, and proactive warnings when severe storm or gale conditions approach.

## Decision
1. **Weather Data Provider**:
   - Integrate **Deutscher Wetterdienst (DWD)** via Home Assistant (`dwd_weather` and `dwd_weather_warnings`).
   - Automatically resolves local station data and warning cell identifier using Home Assistant's configured `zone.home` GPS coordinates.
   - Supplies local weather observations, hourly/daily forecasts, and official warning levels (Gelb, Orange, Rot, Violett) for storm and wind events without API keys.

2. **Display Architecture (3-Screen Weather Rotation)**:
   - Implement three complementary custom apps in the AWTRIX rotation:
     - **App 1 (`weather_now`)**: Current condition icon + current temperature (e.g., `[☀️] 19°C`).
     - **App 2 (`weather_today`)**: Dynamic secondary display showing today's High/Low (`[⛅] 23° 14°`) by default, automatically switching to live Wind Speed (`[💨] 35 km/h`) whenever local wind speeds exceed 30 km/h.
     - **App 3 (`weather_tomorrow`)**: Tomorrow's forecast with weekday abbreviation and condition icon (e.g., `[🌧️] SA 17° 9°`).
   - Screen duration: 5 seconds per app in the rotation cycle.

3. **Icon Management & Provisioning**:
   - Maintain a curated suite of 8×8 animated pixel-art GIF icons in this repository under `assets/icons/weather/`:
     - `sun.gif` (clear / sunny)
     - `cloud.gif` (partly cloudy / overcast)
     - `rain.gif` (rain / showers)
     - `storm.gif` (thunderstorm / lightning)
     - `wind.gif` (high winds / gale)
     - `snow.gif` (snow / sleet)
     - `fog.gif` (fog / mist)
   - Provision icons directly to the TC001 internal flash storage (`/ICONS/`) via `scripts/upload_weather_icons.py` utilizing the AWTRIX HTTP API (`POST /api/download` or `/api/upload`).
   - Clock IP configured via `AWTRIX_IP` in `.env` with CLI argument override.
   - Ensures zero runtime latency, zero reliance on external icon cloud services, and full offline survivability.

4. **Severe Weather & High Wind Push Alerts**:
   - Standard conditions rotate calmly in the normal cycle.
   - When DWD issues an active warning of **Level 2 (Orange / Markante Wetterwarnung)** or higher, or wind gusts exceed 60 km/h:
     - Trigger an immediate high-priority push notification (`awtrix/notify`).
     - Display flashing `storm.gif` or `wind.gif`, warning title, and buzzer chime.
     - Quiet hours policy (22:00–08:00) mutes acoustic chimes while preserving visual alerts as established in ADR 0004.

5. **Implementation & Deployment**:
   - Managed as a version-controlled Home Assistant package (`homeassistant/packages/weather_awtrix.yaml`).
   - Deployed along with icon assets to the Mini PC and TC001 via `scripts/deploy.ps1`.

## Consequences
- **Positive**: High glanceability at desk distance without unreadable marquee scrolling.
- **Positive**: 100% local operation with icons stored directly on the clock's ESP32 flash.
- **Positive**: Dynamic transition highlights wind velocity when windy without adding extra permanent rotation slots.
- **Positive**: Timely safety alerts for storms and high wind with quiet hours protection.
- **Trade-off**: Requires one-time icon upload to the Ulanzi TC001 over the local Wi-Fi network.
