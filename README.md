# VPS MQTT Monitor
A lightweight Python script to push VPS system metrics (CPU, RAM, Disk, Uptime) to an MQTT broker as JSON.

## Setup
1. Create a virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure: Edit `monitor.config.json` with your credentials.

## Deployment
Recommended to run as a systemd service pointing to the venv python interpreter.
