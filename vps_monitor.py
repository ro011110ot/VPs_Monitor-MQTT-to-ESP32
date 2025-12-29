import psutil
import paho.mqtt.client as mqtt
import json
import time
import os

# Load config
config_path = os.path.join(os.path.dirname(__file__), 'monitor.config.json')
with open(config_path) as f:
    config = json.load(f)

client = mqtt.Client()
client.username_pw_set(config['user'], config['pass'])

def get_stats():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "uptime": int(time.time() - psutil.boot_time())
    }

try:
    client.connect(config['broker'], config['port'])
    while True:
        payload = json.dumps(get_stats())
        client.publish(config['topic'], payload, retain=True)
        time.sleep(30)
except Exception as e:
    print(f"Error: {e}")
