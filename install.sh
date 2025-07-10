#!/bin/bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
sed "s|{{WORKING_DIR}}|${SCRIPT_DIR}|g" ${SCRIPT_DIR}/install/simple_brightness_app.desktop.template > ${SCRIPT_DIR}/install/simple_brightness_app.desktop

cp -f ${SCRIPT_DIR}/install/simple_brightness_app.desktop ~/.config/autostart/simple_brightness_app.desktop

python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install pystray

# sudo cp -f ${SCRIPT_DIR}/install/simple_brightness_app.service /etc/systemd/system/simple_brightness_app.service
# rm ${SCRIPT_DIR}/install/simple_brightness_app.service

# sudo systemctl enable simple_brightness_app
# sudo systemctl start simple_brightness_app