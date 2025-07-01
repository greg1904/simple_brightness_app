from util.DisplayCapability import DisplayCapability
from util.DisplayCapabilities import DisplayCapabilities
import subprocess


class Display:
    def __init__(self, display_id : int, display_name : str, display_capabilities : DisplayCapabilities):
        self.display_id = display_id
        self.display_name = display_name
        self.display_capabilities = display_capabilities
        self.is_active = True

    def __set_capability(self, capability : DisplayCapability, new_value):
        capability_id = self.display_capabilities.dictionary[capability.value]["code"]
        query_output = subprocess.run(["/usr/bin/ddcutil", "setvcp", str(capability_id), str(new_value), "--display", str(self.display_id)], capture_output=True, text=True, check=True)
        return query_output.stdout
    
    def __read_capability(self, capability : DisplayCapability):
        capability_id = self.display_capabilities.dictionary[capability.value]["code"]
        query_output = subprocess.run(["/usr/bin/ddcutil", "getvcp", str(capability_id), "--display", str(self.display_id)], capture_output=True, text=True, check=True)
        return query_output.stdout
    
    def get_capability_values(self, capability : DisplayCapability):
        monitor_capability = self.display_capabilities.dictionary[capability.value]
        if DisplayCapabilities.INITIAL_VAL in monitor_capability.values():
            capability_val_read = self.__read_capability(capability)
            if capability_val_read.find("current value =") == -1:
                monitor_capability["minValue"] = 0
                monitor_capability["maxValue"] = 100
                monitor_capability["currentValue"] = 50
                monitor_capability["actualValue"] = 50
            else:
                value_section = capability_val_read[capability_val_read.find("):") + len("):"):]
                values = value_section.split(',')

                for value_w_space in values:
                    value = value_w_space.strip()

                    if value.startswith("current value ="):
                        monitor_capability["currentValue"] = value[len("current value ="):].strip()
                        monitor_capability["actualValue"] = monitor_capability["currentValue"]

                    if value.startswith("max value ="):
                        monitor_capability["maxValue"] = value[len("max value ="):].strip()

                    if value.startswith("min value ="):
                        monitor_capability["minValue"] = value[len("min value ="):].strip()

                monitor_capability["minValue"] = monitor_capability["minValue"] if monitor_capability["minValue"] != DisplayCapabilities.INITIAL_VAL else 0
                monitor_capability["maxValue"] = monitor_capability["maxValue"] if monitor_capability["maxValue"] != DisplayCapabilities.INITIAL_VAL else 100
                monitor_capability["currentValue"] = monitor_capability["currentValue"] if monitor_capability["currentValue"] != DisplayCapabilities.INITIAL_VAL else 50

        return monitor_capability
    
    def apply_changes_in_capabilities(self):
        if self.is_active == False:
            return
        
        for capability_key in self.display_capabilities.dictionary:
            capability = self.display_capabilities.dictionary[capability_key]
            if capability["currentValue"] != capability["actualValue"]:
                self.__set_capability(DisplayCapability(capability_key), capability["currentValue"])
                capability["actualValue"] = capability["currentValue"]

    def set_is_active(self, is_active):
        self.is_active = is_active

                    