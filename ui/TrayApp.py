import gi, os

from util.DisplayCapability import DisplayCapability
from util.Display import Display
from typing import List

gi.require_versions({"Gtk" : "3.0", "XApp" : "1.0"})

from gi.repository import Gtk, XApp

class TrayApp:
    def __init__(self, displays : List[Display]):
        self.display_toggles = {}
        self.is_dummy_selection = False
        self.displays = displays
        self.on_scroll_scheduler = "NULL"
        for display in self.displays:
            display.get_capability_values(DisplayCapability.BRIGHTNESS)

        self.status_icon = XApp.StatusIcon()

        image_path = os.path.abspath('./ui/icon.png')
        self.status_icon.set_icon_name(image_path)
        self.status_icon.set_tooltip_text("Simple Brightness App")
        menu = self.menu()
        self.status_icon.set_secondary_menu(menu)
        self.status_icon.set_primary_menu(menu)

    def menu(self):
        menu = Gtk.Menu()

        if len(self.displays) > 1:
            # multiple monitors exist - allow toggling on and off
            select_all = Gtk.CheckMenuItem(label="all Displays")
            select_all.set_draw_as_radio(draw_as_radio=True)
            select_all.set_active(True)
            select_all.connect("toggled", self.display_selection_clicked)
            menu.append(select_all)
            self.display_toggles.update({select_all : "BOTH"})

            for display in self.displays:
                display_label = "Display {0}: {1}".format(display.display_id, display.display_name)
                entry = Gtk.CheckMenuItem(label=display_label)
                entry.set_draw_as_radio(draw_as_radio=True)
                entry.connect("toggled", self.display_selection_clicked)
                self.display_toggles.update({entry : display})
                menu.append(entry)


            separator = Gtk.SeparatorMenuItem()
            menu.append(separator)
                    
        max_br = Gtk.MenuItem(label='Max. Brightness')
        max_br.connect('activate', self.set_max_dp_brightness)
        menu.append(max_br)

        br_75 = Gtk.MenuItem(label='75% Brightness')
        br_75.connect('activate', self.set_75_dp_brightness)
        menu.append(br_75)

        br_50 = Gtk.MenuItem(label='50% Brightness')
        br_50.connect('activate', self.set_50_dp_brightness)
        menu.append(br_50)

        br25 = Gtk.MenuItem(label='25% Brightness')
        br25.connect('activate', self.set_25_dp_brightness)
        menu.append(br25)

        min_br = Gtk.MenuItem(label='Min. Brightness')
        min_br.connect('activate', self.set_0_dp_brightness)
        menu.append(min_br)

        exittray = Gtk.ImageMenuItem(label='Close', image=Gtk.Image.new_from_icon_name("application-exit", 16))
        exittray.connect('activate', quit)
        menu.append(exittray)
        
        menu.show_all()
        return menu
  
    def open_app(self, item):
        window = Gtk.ApplicationWindow()
        window.present()

    def display_selection_clicked(self, item):
        if self.is_dummy_selection == True:
            return
        
        toggle_display = self.display_toggles[item]
        
        self.is_dummy_selection = True
        for ditem in self.display_toggles:
            if ditem == item:
                ditem.set_active(True)
            else:
                ditem.set_active(False)
        self.is_dummy_selection = False

        if toggle_display == "BOTH":
            for display in self.displays:
                display.set_is_active(True)

            
        else:
            for display in self.displays:
                if display == toggle_display:
                    display.set_is_active(True)
                else:
                    display.set_is_active(False)    


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
    
    def quit(*_):
        Gtk.main_quit()

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
