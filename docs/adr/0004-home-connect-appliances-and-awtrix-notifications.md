# ADR 0004: Home Connect Appliance Integration and AWTRIX Notifications

## Status
Accepted

## Context
Kenneth uses Home Connect-enabled appliances (a washing machine and a dryer) on the local Wi-Fi network and wants real-time status notifications and operational messages pushed to the Ulanzi TC001 desktop pixel clock (running AWTRIX NG).

Home Connect appliances do not provide a local LAN API; they report telemetry through the BSH cloud platform. Home Assistant is deployed as a container on the local Mini PC without Nabu Casa Cloud subscription.

## Decision
1. **Home Connect Integration**:
   - Utilize the official built-in **Home Assistant Core Home Connect** integration.
   - Authenticate using a free **Home Connect Developer Account** (`developer.home-connect.com`) with OAuth credentials (`Client ID` and `Client Secret`) registered with the `https://my.home-assistant.io/redirect/oauth` redirect URI.
2. **Alert Scope & Messaging**:
   - Track program completion (`BSH.Common.Status.OperationState` transitioning to `Finished` or progress reaching 100%).
   - Track active washing cycle phases and display dynamic phase-specific icons:
     - Washing phase: `waschmaschine_waschen` (Text: `WASCHEN` or remaining time)
     - Rinsing phase: `waschmaschine_spuehlen` (Text: `SPÜLEN`)
     - Spinning phase: `waschmaschine_schleudern` (Text: `SCHLEUDERN`)
     - Finished phase: `waschmaschine_fertig` (Text: `WÄSCHE FERTIG`, persistent reminder)
   - Track dryer cycle completion: `TROCKNER FERTIG` (Icon `trockner_fertig` or `#2062`).
   - Track critical warnings/errors: `FEHLER` (Icon `#638`).
3. **Display & Notification Architecture**:
   - **Immediate Pop-up Notification**: When a cycle finishes or an error triggers, publish an immediate high-priority notification to Mosquitto (`awtrix/notify`) with the machine-specific icon, German text, and audible chime.
   - **Persistent Rotation Reminder**: Concurrently register a custom app screen in AWTRIX (`awtrix/custom/washer` or `awtrix/custom/dryer`) showing completion status in the regular rotation cycle.
   - **Dismissal Mechanism**: Clear the persistent reminder automatically when:
     - The appliance door sensor changes to `open` (`door` binary sensor), OR
     - The Ulanzi TC001 middle/Select button is pressed, OR
     - A 6-hour safety timeout elapses.
4. **Quiet Hours**:
   - Suppress audio buzzer chimes during night hours (22:00–08:00) while keeping visual notifications active.

## Consequences
- **Positive**: Eliminates forgotten laundry or clean dishes without requiring constant phone checking.
- **Positive**: Low overhead using native Home Assistant automations and MQTT payloads directly to AWTRIX NG.
- **Trade-off**: Requires one-time registration of an application on the Home Connect Developer Portal to generate OAuth credentials.
