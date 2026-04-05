🛠️ Installation
1. Prerequisites

Ensure your LG TV has the following enabled:

    Connection > Mobile TV On (Turn on via Wi-Fi/Bluetooth)

    General > Additional Settings > Quick Start+

    Connection > HDMI-CEC (Simplink)

2. Setup Environment
```Bash
# Clone the repo
git clone https://github.com/zachstultz/dualsense-lg-tv-bridge.git
cd dualsense-lg-tv-bridge

# Create a virtual environment with system access (for DBus/Bluez)
python3 -m venv venv --system-site-packages
source venv/bin/activate

# Install dependencies
pip install bscpylgtv wakeonlan
```

3. Configuration

Edit ```dualsense-lg-tv-bridge.py``` and update the following variables:

    TV_IP: The static IP of your LG TV.

    TV_MAC: The physical MAC address of your TV (for Wake-on-LAN).

    TV_INPUT: The HDMI port your PC is connected to (e.g., HDMI_1).
