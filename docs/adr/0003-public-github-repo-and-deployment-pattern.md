# ADR 0003: Public GitHub Repository and Mini PC Deployment Pipeline

## Status
Accepted

## Context
The project needs a version-controlled repository to store Docker Compose files, Mosquitto configurations, Home Assistant automations/blueprints, and deployment automation scripts. Kenneth requested that this project be hosted as a public GitHub repository under his account (`Netke237/ulanzi`).

In addition, deployment to the local 24/7 Mini PC (`minipc` at `192.168.55.60`) needs to follow the proven, isolated operational model established in the `Sonos` platform.

## Decision
1. Initialize a standalone git repository at `f:\Git\GitHub\Ulanzi` and publish it to GitHub as `Netke237/ulanzi` (public).
2. Create a self-contained deployment pipeline via `scripts/deploy.ps1` that:
   - Connects to `minipc` via SSH (`ssh minipc`).
   - Syncs the Docker Compose and service configuration to `C:\Users\KENNETH\ulanzi\`.
   - Executes `docker compose up -d` on `minipc`.
   - Validates that Home Assistant (`:8123`) and Mosquitto (`:1883`) become healthy.

## Consequences
- **Positive**: Clean separation from other projects on the Mini PC; safe, idempotent deployments.
- **Positive**: Open-source, shareable repo structure on GitHub.
- **Trade-off**: Public repo requires strict discipline regarding credentials (using `.env.example` and `.gitignore` to avoid exposing Wi-Fi, MQTT passwords, or Home Assistant tokens).
