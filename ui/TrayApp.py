import os

from util.DisplayCapability import DisplayCapability
from util.Display import Display
from typing import List
import pystray
from PIL import Image



class TrayApp:
    def __init__(self, displays : List[Display]):
        self.display_toggles = {}
        self.display_storage = {}
        self.displays = displays
        self.on_scroll_scheduler = "NULL"
        for display in self.displays:
            display.get_capability_values(DisplayCapability.BRIGHTNESS)

        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.png')
        self.image = Image.open(image_path)
        
        menu = self.menu()
        self.icon = pystray.Icon("gregssimplbrightapp", self.image, "Simple Brightness App", menu)

    def run(self):
        self.icon.run()

    def menu(self):
        menu = []

        if len(self.displays) > 1:
            # multiple monitors exist - allow toggling on and off
            select_all = pystray.MenuItem("all Displays", self.display_selection_clicked, checked=lambda item: self.display_toggles["ALL"], radio=True )
            menu.append(select_all)
            self.display_toggles.update({"ALL" : True})
            self.display_storage.update({select_all : "ALL"})

            for display in self.displays:
                display_label = "Display {0}: {1}".format(display.display_id, display.display_name)
                entry = pystray.MenuItem(display_label, self.display_selection_clicked, checked=lambda item: self.display_toggles[str(display.display_id)], radio=True)
                self.display_toggles.update({str(display.display_id) : False})
                self.display_storage.update({entry : display})
                menu.append(entry)


            separator = pystray.Menu.SEPARATOR
            menu.append(separator)
                    
        max_br = pystray.MenuItem('Max. Brightness', self.set_max_dp_brightness)
        menu.append(max_br)

        br_75 = pystray.MenuItem('75% Brightness', self.set_75_dp_brightness)
        menu.append(br_75)

        br_50 = pystray.MenuItem('50% Brightness', self.set_50_dp_brightness)
        menu.append(br_50)

        br25 = pystray.MenuItem('25% Brightness', self.set_25_dp_brightness)
        menu.append(br25)

        min_br = pystray.MenuItem('Min. Brightness', self.set_0_dp_brightness)
        menu.append(min_br)

        exittray = pystray.MenuItem('Exit', self.quit)
        menu.append(exittray)
        
        return pystray.Menu(*menu)

    def display_selection_clicked(self, icon, item):        
        toggle_display = self.display_storage[item]

        if toggle_display == "ALL":
            for display in self.displays:
                display.set_is_active(True)
            for toggle in self.display_toggles:
                if toggle == "ALL":
                    self.display_toggles[toggle] = True
                else:
                    self.display_toggles[toggle] = False
        else:
            for display in self.displays:
                if display == toggle_display:
                    display.set_is_active(True)
                else:
                    display.set_is_active(False)
                
            for toggle in self.display_toggles:
                if toggle == "ALL":
                    self.display_toggles[toggle] = False
                elif toggle == toggle_display.display_id:
                    self.display_toggles[toggle] = True
                else:
                    self.display_toggles[toggle] = False


    def set_max_dp_brightness(self, item):
        self.set_dp_brightness(100)

    def set_dp_brightness(self, percentage):
        for display in self.displays:
            brightness_vals = display.get_capability_values(DisplayCapability.BRIGHTNESS)
            brightness_vals["currentValue"] = percentage
        self.send_vals_to_displays(ignore_scheduler=True)

    def set_75_dp_brightness(self, item):
        self.set_dp_brightness(75)

    def set_50_dp_brightness(self, item):
        self.set_dp_brightness(50) 
    
    def set_25_dp_brightness(self, item):
        self.set_dp_brightness(25)
    
    def set_0_dp_brightness(self, item):
        self.set_dp_brightness(0)
    
    def quit(self, icon, item):
        self.icon.stop()
        

    def send_vals_to_displays(self, ignore_scheduler = False):
        if self.on_scroll_scheduler == "NULL" and ignore_scheduler == False:
            return
    
        for display in self.displays:
            display.apply_changes_in_capabilities()

        self.on_scroll_scheduler = "NULL"

  # def on_scroll(self, icon, amount, direction):
  #   if self.on_scroll_scheduler == "NULL":
  #     self.on_scroll_scheduler = sched.scheduler(time.time, time.sleep)
  #     self.on_scroll_scheduler.enter(750, 1, self.send_vals_to_displays)
  #     self.on_scroll_scheduler.run(blocking=False)

  #   for display in self.displays:
  #     brightness_vals = display.get_capability_values(DisplayCapability.BRIGHTNESS)

  #     if direction == 0: # scroll up
  #       brightness_vals["currentValue"] = int(brightness_vals["currentValue"]) + 2*amount
  #     else:
  #       brightness_vals["currentValue"] = int(brightness_vals["currentValue"]) - 2*amount
      
  #     if int(brightness_vals["currentValue"]) < int(brightness_vals["minValue"]):
  #       brightness_vals["currentValue"] = 0

  #     if int(brightness_vals["currentValue"]) > int(brightness_vals["maxValue"]):
  #       brightness_vals["currentValue"] = 100

  #     print("Setting Display {0} to {1}".format(display.display_id, brightness_vals["currentValue"]))
