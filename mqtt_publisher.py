import time
import json
import paho.mqtt.client as mqtt
from nilmtk import DataSet

BROKER = "localhost"
TOPIC = "home/house1/aggregate"

print("Loading REFIT dataset...")
ds = DataSet("data/processed/refit.h5")

elec = ds.buildings[1].elec
aggregate = elec.mains()

client = mqtt.Client()
client.connect(BROKER, 1883, 60)
client.loop_start()

print("Streaming aggregate power via MQTT...")

# NILMTK-safe streaming
for chunk in aggregate.power_series():
    # chunk is a Pandas Series
    chunk = chunk.dropna()

    for ts, power in chunk.items():
        payload = {
            "timestamp": str(ts),
            "power": float(power)
        }
        client.publish(TOPIC, json.dumps(payload))
        time.sleep(1)  # 1 Hz real-time simulation

ds.store.close()

