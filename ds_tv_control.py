import asyncio
import subprocess
from wakeonlan import send_magic_packet
from bscpylgtv import WebOsClient

# --- CONFIGURATION ---
DUALSENSE_NAME = "DualSense"  # String to search for in bluetoothctl
TV_IP = "[IP_ADDRESS]"  # Your LG TV IP
TV_MAC = "XX:XX:XX:XX:XX:XX"  # Your LG TV MAC (for Power On)
TV_INPUT = "HDMI_1"  # The input your PC is on
CHECK_INTERVAL = 5  # Seconds between checks
# ---------------------

# Global state to prevent spamming the TV if the controller stays connected
controller_was_connected = False


def is_controller_connected():
    """Check if DualSense controller is connected via bluetoothctl."""
    try:
        # 'bluetoothctl devices Connected' is a quick way to list only active ones
        output = subprocess.check_output(
            ["bluetoothctl", "devices", "Connected"], text=True
        )
        return DUALSENSE_NAME.lower() in output.lower()
    except subprocess.CalledProcessError:
        return False


async def wake_and_switch():
    print("DualSense detected! Waking TV and switching input...")
    # 1. Send Magic Packet to wake the TV
    send_magic_packet(TV_MAC)

    # 2. Connect and Switch Input
    try:
        # Using bscpylgtv for modern webOS support
        client = await WebOsClient.create(TV_IP)
        await client.connect()

        # Give the TV a moment to initialize the UI/Input stack
        await asyncio.sleep(3)
        await client.set_input(TV_INPUT)

        print(f"Success: TV set to {TV_INPUT}")
        await client.disconnect()
    except Exception as e:
        print(f"Note: TV didn't respond to input command (might still be booting): {e}")


async def main():
    global controller_was_connected
    print(f"Monitoring for '{DUALSENSE_NAME}' connection...")

    while True:
        currently_connected = is_controller_connected()

        # Trigger only on the rising edge (Transition from Disconnected -> Connected)
        if currently_connected and not controller_was_connected:
            await wake_and_switch()
            controller_was_connected = True
        elif not currently_connected:
            controller_was_connected = False

        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
