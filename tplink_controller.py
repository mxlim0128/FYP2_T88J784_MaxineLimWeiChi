# src/control/tplink_controller.py
# TP-Link Kasa Smart Plug Controller
# Used for appliance ON/OFF control (Objective O3)

import asyncio
import sys
from kasa import SmartPlug
import time


async def control_plug(ip_address: str, command: str):
    """
    Control a TP-Link Kasa smart plug.

    Args:
        ip_address (str): IP address of the smart plug
        command (str): 'on' or 'off'
    """

    plug = SmartPlug(ip_address)

    try:
        # Measure control response latency
        start_time = time.perf_counter()

        await plug.update()

        if command.lower() == "on":
            await plug.turn_on()
            action = "ON"

        elif command.lower() == "off":
            await plug.turn_off()
            action = "OFF"

        else:
            print("Invalid command. Use 'on' or 'off'.")
            return

        end_time = time.perf_counter()
        control_latency_ms = (end_time - start_time) * 1000

        print(
            f"Plug {action} at {ip_address} | "
            f"Control latency: {control_latency_ms:.2f} ms"
        )

    except Exception as e:
        print(f"Failed to control plug at {ip_address}: {e}")


def main():
    """
    Command-line interface:
    python tplink_controller.py <IP_ADDRESS> <on/off>
    """

    if len(sys.argv) != 3:
        print("Usage: python tplink_controller.py <IP_ADDRESS> <on/off>")
        sys.exit(1)

    ip_address = sys.argv[1]
    command = sys.argv[2]

    asyncio.run(control_plug(ip_address, command))


if __name__ == "__main__":
    main()

