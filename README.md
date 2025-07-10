## Simple Brightness Adjustment App

requires DDCUTIL installed!
- try running "ddcutil detect" in your terminal to verify installation - the script installs which ddcutil to output /usr/bin/ddcutil - in case this needs to be adjusted change this in util/constants.py
- uses pystray for system icon - configure backend in start.sh!

first install using install.sh
- creates a .desktop file in ./install
- creates a venv and installs dependencies

run with:
start.sh

### Features
clicking on the icon brings up options for changing the monitors brightness through DDCUTIL in 25% steps (also on a per MonitorBasis)