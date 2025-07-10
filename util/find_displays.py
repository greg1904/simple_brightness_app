#!/usr/bin/env python3

import subprocess
from util.DisplayCapabilities import DisplayCapabilities
from util.DisplayCapability import DisplayCapability
from util.Display import Display
from util.constants import DDCUTIL_PATH

def __detect():
    query_output = subprocess.run([DDCUTIL_PATH, "detect"], capture_output=True, text=True, check=True)
    return query_output.stdout

def __display_capabilities_read(display_id : str):
    query_output = subprocess.run([DDCUTIL_PATH, "capabilities", "--display", str(display_id)], capture_output=True, text=True, check=True)
    return query_output.stdout


def __extract_displays(detect : str):
    displays = []

    for line_w_space in detect.splitlines():
        line = line_w_space.strip()
        
        if line.startswith("Display"):
            display_id = line.split()[1]
            displays.append(__get_display(display_id))
        else:
            continue

    return displays


def __get_display(display_id : str):
    output = __display_capabilities_read(display_id)
    capabilities = DisplayCapabilities()
    in_vcp_features = False

    props_found = {
        "brightness" : False
    }

    for line_w_space in output.splitlines():
        line = line_w_space.strip() 

        if line.startswith("Model: ") and in_vcp_features == False:
            name = line[len("Model: "):]

        if line.startswith("VCP Features:") and in_vcp_features == False:
            in_vcp_features = True

        if in_vcp_features == True and props_found["brightness"] == False and line.find("Brightness") != -1:
            capabilities.add_capability(capability=DisplayCapability.BRIGHTNESS, code=line.split()[1])
            props_found["brightness"] = True

        if all(props_found.values()) == True:
            break
            
    return Display(display_id=display_id, display_name=name, display_capabilities=capabilities)

def detect_display_devices():
    """
    Detects available displays.
    returns connected_displays
    also contains feature number for brightness
    """
    return __extract_displays(__detect())