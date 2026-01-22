# src/inference_service.py
# FINAL IoT NILM Inference Service with Latency Measurement

import paho.mqtt.client as mqtt
import numpy as np
import tensorflow as tf
from collections import deque
import os
import time
import random

# ============================================================
# CONFIGURATION (from configs/seq2point_fridge.yaml)
# ============================================================

WINDOW_SIZE = 599

MAINS_MAX = 24000.0
MAINS_MIN = 0.0
APPLIANCE_MAX = 1466.0

MQTT_BROKER = "localhost"
AGGREGATE_TOPIC = "home/aggregate/power"
OUTPUT_TOPIC = "home/appliance/fridge/power"

MODEL_PATH = "results/checkpoints/seq2point_fridge/model.best.h5"

# IMPORTANT: Set False for REAL MQTT mode
USE_SIMULATION = False

# ============================================================
# LOAD NILM MODEL (outside callbacks for performance)
# ============================================================

try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

    from src.models.seq2point import build_seq2point_model

    model = build_seq2point_model(input_shape=(WINDOW_SIZE, 1))
    model.load_weights(MODEL_PATH)

    print("NILM model loaded and weights set successfully.")

except Exception as e:
    print(f"FATAL ERROR: Could not load model or weights. Error: {e}")
    exit(1)

# ============================================================
# SLIDING WINDOW BUFFER
# ============================================================

power_buffer = deque(maxlen=WINDOW_SIZE)

# ============================================================
# MQTT CALLBACKS
# ============================================================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(AGGREGATE_TOPIC)
        print(f"Connected to MQTT Broker and subscribed to {AGGREGATE_TOPIC}")
    else:
        print(f"Failed to connect to MQTT, return code {rc}")

def on_message(client, userdata, msg):
    try:
        # 1. Read incoming aggregate power
        power_val = float(msg.payload.decode())
        power_buffer.append(power_val)

        # 2. Run inference only when buffer is full
        if len(power_buffer) == WINDOW_SIZE:

            # Normalization
            normalized_buffer = (
                (np.array(power_buffer) - MAINS_MIN)
                / (MAINS_MAX - MAINS_MIN)
            )

            # Reshape for Seq2Point: (1, window_size, 1)
            input_tensor = normalized_buffer.reshape(
                1, WINDOW_SIZE, 1
            ).astype(np.float32)

            # Inference latency measurement
            start_time = time.perf_counter()
            normalized_prediction = model.predict(
                input_tensor, verbose=0
            )[0][0]
            end_time = time.perf_counter()

            inference_latency_ms = (end_time - start_time) * 1000

            # De-normalize appliance power
            appliance_power = max(
                0.0, normalized_prediction * APPLIANCE_MAX
            )

            # Publish result
            client.publish(
                OUTPUT_TOPIC, f"{appliance_power:.2f}"
            )

            print(
                f"Disaggregated: {appliance_power:.2f} W | "
                f"Inference latency: {inference_latency_ms:.2f} ms"
            )

    except Exception as e:
        print(f"Error during NILM processing: {e}")

# ============================================================
# MAIN EXECUTION
# ============================================================

if not USE_SIMULATION:
    # -------- REAL MQTT MODE --------
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, 1883, 60)
        print("NILM Inference Service starting (MQTT MODE)...")
        client.loop_forever()
    except Exception as e:
        print(f"FATAL: MQTT connection failed. Error: {e}")

else:
    # -------- SIMULATION MODE --------
    print("Running in SIMULATION MODE (no MQTT broker)...")

    for _ in range(800):
        simulated_power = random.uniform(100, 800)
        power_buffer.append(simulated_power)

        if len(power_buffer) == WINDOW_SIZE:

            normalized_buffer = (
                (np.array(power_buffer) - MAINS_MIN)
                / (MAINS_MAX - MAINS_MIN)
            )

            input_tensor = normalized_buffer.reshape(
                1, WINDOW_SIZE, 1
            ).astype(np.float32)

            start_time = time.perf_counter()
            normalized_prediction = model.predict(
                input_tensor, verbose=0
            )[0][0]
            end_time = time.perf_counter()

            inference_latency_ms = (end_time - start_time) * 1000
            appliance_power = max(
                0.0, normalized_prediction * APPLIANCE_MAX
            )

            print(
                f"[SIM] Disaggregated: {appliance_power:.2f} W | "
                f"Latency: {inference_latency_ms:.2f} ms"
            )

