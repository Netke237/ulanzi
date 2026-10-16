# ADR 0006: Nuki Smart Lock Integration and Home Connect Interlocks

## Status
Accepted

## Context
Kenneth uses a **Nuki Smart Lock** with a **Nuki Bridge** (connected to home Wi-Fi and Bluetooth) and a **Nuki Door Sensor** (magnetic contact sensor) on the front entrance door. 

In addition, Home Assistant on the 24/7 Mini PC (`192.168.55.60`) manages BSH Home Connect appliances (washing machine, dryer) as defined in [ADR 0004](0004-home-connect-appliances-and-awtrix-notifications.md), and drives the Ulanzi TC001 desktop pixel clock (running AWTRIX NG).

The goal is to bridge entrance door physical events with appliance states and display notifications to solve common household friction:
1. Leaving the home while laundry is still sitting wet in the drum or without realizing an appliance is running.
2. Returning home unaware that an appliance finished while away.
3. Accidentally leaving the front door ajar or forgetting to lock the door before going to sleep.
4. Ensuring physical security by strictly restricting remote unlock permissions in automation rules.

## Decision

1. **Local LAN Connection via Nuki Bridge HTTP API**:
   - Integrate Nuki using Home Assistant Core's native Nuki integration configured for the **Local HTTP Bridge API** (Port 8080).
   - Authenticate with an API token generated via the Nuki Bridge Developer Mode in the Nuki mobile app.
   - The Bridge automatically registers a webhook callback (`/callback/add`) pointing to Home Assistant (`http://192.168.55.60:8123/api/nuki/webhook/...`), delivering sub-second, zero-cloud push updates for lock and contact state changes.

2. **Entity Exposure & Telemetry**:
   - **Lock Entity**: `lock.nuki_smart_lock` (states: `locked`, `unlocked`).
   - **Door Position Entity**: `binary_sensor.nuki_door_sensor` (states: `off` = closed, `on` = open).
   - **Battery Telemetry**: `sensor.nuki_smart_lock_battery_level` and `binary_sensor.nuki_smart_lock_battery_critical`.

3. **Departure Interlock (Leaving Home)**:
   - **Trigger**: Entrance door transition to `locked`.
   - **Condition**: Washing machine or dryer is currently running (`Run`, `DelayedStart`) OR has finished with laundry remaining inside.
   - **Display Action**:
     - Immediate **5-second** high-priority popup (`awtrix/cmd/notify`) on the Ulanzi TC001.
     - **Visual + Audio Chime**: If finished laundry is waiting in the drum (`WÄSCHE IN TROMMEL` / `TROCKNER FERTIG`).
     - **Visual Only (Silent)**: If an appliance cycle is actively running (`WÄSCHE LÄUFT` / `TROCKNET`).

4. **Arrival Task Digest (Coming Home)**:
   - **Trigger**: Entrance door transition from `locked` to `unlocked`.
   - **Condition**: Washing machine or dryer completed while away (`operation_state == 'finished'` or finished sensor present).
   - **Display Action**:
     - Immediate **10-second** welcome popup on Ulanzi with audible chime (`WÄSCHE FERTIG`).
     - Concurrently re-injects the persistent reminder app into the AWTRIX rotation loop until the appliance door is physically opened.

5. **Security Curfew (Night Lock Reminder)**:
   - **Trigger**: Daily at 22:00, or when the door unlocks between 22:00 and 06:00.
   - **Condition**: Door state is `unlocked`.
   - **Display Action**:
     - Injects a persistent reminder app (`awtrix/cmd/apps/pushed/nuki_night`) with red lock icon (`#FF3B30`) and text `BITTE ABSCHLIESSEN`.
     - Automatically dismisses as soon as `lock.nuki_smart_lock` transitions to `locked`.

6. **Door Left Open Alarm**:
   - **Trigger**: `binary_sensor.nuki_door_sensor` remains in state `on` (open) for longer than **5 minutes**.
   - **Display Action**:
     - 10-second urgent popup (`awtrix/cmd/notify`) displaying `TÜR OFFEN!` with warning icon.
     - Sounds warning chime during daytime (08:00–22:00); audio is automatically muted during night hours (22:00–08:00).

7. **Daily Low Battery Digest**:
   - **Trigger**: Daily at 09:00.
   - **Condition**: Nuki battery level below 20% or battery critical sensor is active.
   - **Display Action**: 10-second warning popup on Ulanzi (`NUKI BATTERIE LADEN`) with battery icon.

8. **Transient Door Events & Clean Rotation Loop**:
   - Keep normal AWTRIX cycling loop uncluttered by default.
   - Trigger brief 5-second transient popups on state changes (`TÜR VERRIEGELT` / `TÜR ENTSPERRT`).

9. **Physical Security Authority**:
   - Automations and scripts operate on a **read-only / telemetry-first** model.
   - Automated `unlock` or `unlatch` commands from Home Assistant or Ulanzi are strictly prohibited to prevent unauthorized or accidental physical entry.

10. **Local Asset Provisioning**:
    - Pixel-art 8×8 GIF icons (`nuki_locked.gif`, `nuki_unlocked.gif`, `door_open.gif`, `battery_low.gif`) are maintained in `assets/icons/nuki/` and uploaded directly to Ulanzi LittleFS `/ICONS/` via `scripts/upload_nuki_icons.py`.

## Consequences
- **Positive**: Eliminates forgotten wet laundry when leaving or returning home.
- **Positive**: Guarantees zero cloud latency and full local resilience via Nuki Bridge local HTTP callbacks.
- **Positive**: Enhances home security through door-left-open alerts and nighttime lock curfew verification.
- **Positive**: Preserves clean display rotation while giving instant visibility when action is required.
- **Trade-off**: Requires one-time activation of Developer Mode / HTTP API in the Nuki mobile app.
