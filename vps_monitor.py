import psutil
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import json
import time
import os

# Load config
config_path = os.path.join(os.path.dirname(__file__), "monitor.config.json")
with open(config_path) as f:
    config = json.load(f)

# Use CallbackAPIVersion.VERSION2 to fix DeprecationWarning
client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.username_pw_set(config["user"], config["pass"])


def get_stats():
    # Improved uptime detection for Debian 12 VPS
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = int(float(f.readline().split()[0]))
    except FileNotFoundError:
        uptime_seconds = int(time.time() - psutil.boot_time())

    return {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "uptime": uptime_seconds,
    }


try:
    # Check if broker is reachable
    client.connect(config["broker"], config["port"], keepalive=60)

    # Start the loop in a non-blocking way or use a simple loop
    while True:
        payload = json.dumps(get_stats())
        client.publish(config["topic"], payload, retain=True)
        time.sleep(30)
except Exception as e:
    print(f"Error: {e}")
