# ADR 0001: Deploy Home Assistant on Mini PC for Display Automation

## Status
Accepted

## Context
The Ulanzi desktop display requires a backend engine to schedule screens, aggregate sensor data, and push high-priority notifications. Kenneth maintains a local 24/7 server (`minipc` at `192.168.55.60`) running Docker containers alongside projects like `Sonos` and `Trading Assistant`.

Rather than using standalone ad-hoc scripts or relying on on-device cloud polling, the system needs an extensible, low-maintenance platform that makes it effortless to create and modify what is shown on the display.

## Decision
1. Deploy **Home Assistant Container** (`homeassistant/home-assistant:stable`) on the Mini PC using Docker Compose.
2. Maintain the deployment configuration (`docker-compose.yml`, environment files, and scripts) in this repository (`Ulanzi`) and sync/deploy to `minipc` via SSH/PowerShell, mirroring the operational pattern established in the `Sonos` project.
3. If an MQTT-based firmware (like AWTRIX NG) is selected, include an `eclipse-mosquitto` broker in the same Docker Compose stack.

## Consequences
- **Positive**: Provides a robust graphical UI, thousands of integrations (weather, calendars, media players like Sonos, system metrics), and no-code Blueprint support for screen management.
- **Positive**: Reuses existing Docker infrastructure on the Mini PC.
- **Trade-off**: Requires running and maintaining the Home Assistant Docker container and storage volumes on the Mini PC.
