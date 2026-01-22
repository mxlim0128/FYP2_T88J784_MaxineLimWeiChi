# src/control/control_service.py
# Appliance Control Service with Response Time Measurement
# Objective O3.2

import time
import random

print("control_service.py loaded")

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------

POWER_THRESHOLD = 50.0  # Watts

SIMULATED_CONTROL_DELAY_MS = (80, 150)

USE_REAL_PLUG = False  # Set True only if hardware exists

SMART_PLUG_IP = "192.168.1.100"

# -------------------------------------------------
# CONTROL FUNCTIONS
# -------------------------------------------------

def simulated_control(command: str):
    """
    Simulate appliance ON/OFF control and measure latency.
    """
    start_time = time.perf_counter()

    delay_ms = random.uniform(*SIMULATED_CONTROL_DELAY_MS)
    time.sleep(delay_ms / 1000)

    end_time = time.perf_counter()
    control_latency_ms = (end_time - start_time) * 1000

    print(
        f"[SIM CONTROL] Command: {command.upper()} | "
        f"Latency: {control_latency_ms:.2f} ms"
    )

    return control_latency_ms


def real_control(command: str):
    """
    Control a real TP-Link smart plug.
    """
    from src.control.tplink_controller import control_plug
    import asyncio

    start_time = time.perf_counter()
    asyncio.run(control_plug(SMART_PLUG_IP, command))
    end_time = time.perf_counter()

    control_latency_ms = (end_time - start_time) * 1000

    print(
        f"[REAL CONTROL] Command: {command.upper()} | "
        f"Latency: {control_latency_ms:.2f} ms"
    )

    return control_latency_ms

# -------------------------------------------------
# CONTROL DECISION LOGIC
# -------------------------------------------------

def control_decision(predicted_power: float):
    """
    Decide whether to turn appliance ON or OFF based on NILM output.
    """
    if predicted_power >= POWER_THRESHOLD:
        command = "on"
    else:
        command = "off"

    print(
        f"Predicted Power: {predicted_power:.2f} W | "
        f"Decision: {command.upper()}"
    )

    if USE_REAL_PLUG:
        return real_control(command)
    else:
        return simulated_control(command)

# -------------------------------------------------
# MAIN ENTRY POINT
# -------------------------------------------------

if __name__ == "__main__":
    print("Starting Control Service (O3.2)")

    test_predictions = [10, 30, 65, 120, 45, 80]

    for power in test_predictions:
        control_decision(power)
