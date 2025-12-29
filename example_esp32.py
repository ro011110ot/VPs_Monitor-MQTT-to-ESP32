import network
import ujson
from umqtt.simple import MQTTClient
import time

# --- Konfiguration ---
WIFI_SSID = "DEIN_WLAN"
WIFI_PASS = "DEIN_PASSWORT"

MQTT_BROKER = "DEINE_VPS_IP_ODER_DOMAIN"
MQTT_USER = "ro011110ot"
MQTT_PASS = "DEIN_MQTT_PASSWORT"
MQTT_TOPIC = b"vps/monitor"

# --- WLAN Verbindung ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            pass
    print('WiFi connected:', wlan.ifconfig()[0])

# --- MQTT Callback (Hier passiert die Magie) ---
def on_message(topic, msg):
    print(f"Received from {topic.decode()}: {msg.decode()}")
    try:
        data = ujson.loads(msg)
        
        # Zugriff auf die Werte vom VPS
        cpu = data.get("cpu")
        ram = data.get("ram")
        uptime = data.get("uptime")
        
        print(f"--- VPS Status ---")
        print(f"CPU Usage: {cpu}%")
        print(f"RAM Usage: {ram}%")
        print(f"Uptime:    {uptime}s")
        
        # Hier würdest du deine LVGL-Labels aktualisieren:
        # my_label.set_text(f"CPU: {cpu}%")
        
    except Exception as e:
        print("Error parsing JSON:", e)

# --- Main Flow ---
connect_wifi()

client = MQTTClient("esp32_monitor", MQTT_BROKER, user=MQTT_USER, password=MQTT_PASS, port=1883)
client.set_callback(on_message)
client.connect()
client.subscribe(MQTT_TOPIC)

print("ESP32 Monitor is running...")

while True:
    # Auf neue Nachrichten vom VPS warten
    client.check_msg()
    time.sleep(1)
