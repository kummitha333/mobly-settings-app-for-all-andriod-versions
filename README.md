# mobly-settings-app-for-all-andriod-versions
Mobly Settings Toggle Automation (applicable for All Android Versions)
This project uses Mobly and uiautomator2 to automate Android Settings toggles (Wi-Fi, Bluetooth, Location, Mobile Data,Dark Theame etc....) across Android versions 10 to 15+. It ensures compatibility across stock and OEM-specific UIs.

📁 Project Structure

mobly-settings-app/
├── andriod.py       
├── andriod.sh          
├── andriod.yml               
├── README.md                  
└── requirements.txt             
✅ Features
Works across Android 10–15+

Dynamically detects Android version for UI compatibility

Handles system confirmation popups (Yes/OK/Allow)

Scrolls to toggles even if deeply nested in custom UIs

Automates:

Wi-Fi toggle

Bluetooth pairing

Location services

Mobile data toggle.......

 **Requirements**
Python Packages
List these in requirements.txt:

mobly
uiautomator2

-------------

Install via:

bash

pip install -r requirements.txt
**Android Device Setup
Enable USB Debugging**

Connect device and authorize ADB

Optional: adb tcpip 5555 && adb connect <ip> (for wireless)

🚀** How to Run**
Step 1: Connect a device
bash
adb devices
Get the device serial.

Step 2: Run with device serial
bash
bash andriod.sh <device_serial>
This:
Creates a temp_config.yml

Launches Mobly with andriod.py

📜 Example andriod.sh
bash
#!/bin/bash

DEVICE_SERIAL="$1"

if [ -z "$DEVICE_SERIAL" ]; then
  echo "Usage: $0 <device_serial>"
  exit 1
fi

cat > temp_config.yml <<EOF
TestBeds:
  - Name: ToggleTest
    Controllers:
      AndroidDevice:
        - serial: $DEVICE_SERIAL
EOF

python3 android_toggle_test.py -c temp_config.yml
🔍 Sample Log Output

[INFO] Test 01: Wi-Fi toggle
[INFO] Switch set to ON
[INFO] Switch set to OFF
...
[INFO] Returned to Home screen
🧪 Extend Tests
You can add other toggles by copying the pattern used in:

test_01_wifi_toggle

test_02_bluetooth_toggle

etc.

Use adb shell am start -a to launch specific settings.

📞 Need Help?
Raise an Issue or contribute via Pull Request. 
