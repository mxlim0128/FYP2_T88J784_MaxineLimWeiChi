import time
import random
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "home/aggregate/power"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("✅ MQTT power simulator started (High = OFF, Low = ON)")

while True:
    # Simulated aggregate power values (W)
    power = random.choice([
        90,     # ON
        120,    # ON
        150,    # ON
        300,    # ON
        600,    # ON
        800,    # ON
        1100,   # OFF
        1800,   # OFF
        2500    # OFF
    ])

    client.publish(TOPIC, power)
    print(f"📤 Published: {power} W")

    time.sleep(1)

