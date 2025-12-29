import network
import ujson
import time
from umqtt.simple import MQTTClient
try:
    import secrets
except ImportError:
    print("Error: secrets.py not found on device!")
    # Fallback or dummy data for compilation check
    class secrets:
        WIFI_SSID = "NA"; WIFI_PASS = "NA"; MQTT_BROKER = "0.0.0.0"
        MQTT_USER = "NA"; MQTT_PASS = "NA"; MQTT_TOPIC = b"vps/monitor"

def connect_wifi():
    """Connects to the local WiFi network using credentials from secrets.py"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f'Connecting to WiFi: {secrets.WIFI_SSID}...')
        wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(1)
            print(".", end="")
    print('\nWiFi connected! IP:', wlan.ifconfig()[0])

def on_message(topic, msg):
    """Callback function triggered when a new MQTT message is received"""
    print(f"\nNew message on topic: {topic.decode()}")
    try:
        # Parse the JSON payload from the VPS
        data = ujson.loads(msg)
        
        cpu = data.get("cpu", 0)
        ram = data.get("ram", 0)
        disk = data.get("disk", 0)
        uptime = data.get("uptime", 0)
        
        # Displaying the data (you can route this to LVGL labels later)
        print("--- VPS Status Report ---")
        print(f"CPU Usage: {cpu}%")
        print(f"RAM Usage: {ram}%")
        print(f"Disk:      {disk}%")
        print(f"Uptime:    {uptime} seconds")
        print("-------------------------")
        
    except Exception as e:
        print("Failed to parse JSON:", e)

def main():
    connect_wifi()
    
    # Initialize MQTT Client
    client = MQTTClient(
        client_id="esp32_vps_monitor",
        server=secrets.MQTT_BROKER,
        user=secrets.MQTT_USER,
        password=secrets.MQTT_PASS,
        port=1883
    )
    
    client.set_callback(on_message)
    
    try:
        client.connect()
        client.subscribe(secrets.MQTT_TOPIC)
        print(f"Subscribed to {secrets.MQTT_TOPIC.decode()}. Waiting for data...")
        
        while True:
            # Check for new messages non-blocking
            client.check_msg()
            time.sleep(1)
            
    except Exception as e:
        print("MQTT Connection Error:", e)
        time.sleep(10)
        import machine
        machine.reset() # Auto-reboot on persistent connection loss

if __name__ == "__main__":
    main()
