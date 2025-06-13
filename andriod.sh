#!/bin/bash

DEVICE_SERIAL="$1"

if [ -z "$DEVICE_SERIAL" ]; then
  echo "Usage: $0 <device_serial>"
  exit 1
fi

# Generate the Mobly config file
cat > temp_config.yml <<EOF
TestBeds:
  - Name: ToggleTest
    Controllers:
      AndroidDevice:
        - serial: $DEVICE_SERIAL
EOF

# Run the test using Python
python andriod.py -c temp_config.yml
