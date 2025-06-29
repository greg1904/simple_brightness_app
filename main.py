import util.find_displays as find_displays
import gi, os
from util.Display import Display
from util.DisplayCapabilities import DisplayCapability
from typing import List
import sched, time

gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk, AppIndicator3 as appindicator

class BrightnessTrayApp:
  def __init__(self, displays : List[Display]):
    self.displays = displays
    self.on_scroll_scheduler = "NULL"
    for display in self.displays:
      display.get_capability_values(DisplayCapability.BRIGHTNESS)
    
  def main(self):
    image_path = os.path.abspath('./icon.png')
    indicator = appindicator.Indicator.new("Brightness Control", image_path, appindicator.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(self.menu())
    indicator.connect("scroll-event", self.on_scroll)
    gtk.main()

  def menu(self):
    menu = gtk.Menu()

    command_two = gtk.MenuItem(label='Max. Brightness')
    command_two.connect('activate', self.set_max_dp_brightness)
    menu.append(command_two)

    command_three = gtk.MenuItem(label='75% Brightness')
    command_three.connect('activate', self.set_75_dp_brightness)
    menu.append(command_three)

    command_three = gtk.MenuItem(label='50% Brightness')
    command_three.connect('activate', self.set_50_dp_brightness)
    menu.append(command_three)

    command_three = gtk.MenuItem(label='25% Brightness')
    command_three.connect('activate', self.set_25_dp_brightness)
    menu.append(command_three)

    command_four = gtk.MenuItem(label='Min. Brightness')
    command_four.connect('activate', self.set_0_dp_brightness)
    menu.append(command_four)

    exittray = gtk.MenuItem(label='Close')
    exittray.connect('activate', quit)
    menu.append(exittray)
    
    menu.show_all()
    return menu

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
    gtk.main_quit()

  def on_scroll(self, icon, amount, direction):
    if self.on_scroll_scheduler == "NULL":
      self.on_scroll_scheduler = sched.scheduler(time.time, time.sleep)
      self.on_scroll_scheduler.enter(750, 1, self.send_vals_to_displays)
      self.on_scroll_scheduler.run(blocking=False)

    for display in self.displays:
      brightness_vals = display.get_capability_values(DisplayCapability.BRIGHTNESS)

      if direction == 0: # scroll up
        brightness_vals["currentValue"] = int(brightness_vals["currentValue"]) + 2*amount
      else:
        brightness_vals["currentValue"] = int(brightness_vals["currentValue"]) - 2*amount
      
      if int(brightness_vals["currentValue"]) < int(brightness_vals["minValue"]):
        brightness_vals["currentValue"] = 0

      if int(brightness_vals["currentValue"]) > int(brightness_vals["maxValue"]):
        brightness_vals["currentValue"] = 100

      print("Setting Display {0} to {1}".format(display.display_id, brightness_vals["currentValue"]))

      

  def send_vals_to_displays(self, ignore_scheduler = False):
    if self.on_scroll_scheduler == "NULL" and ignore_scheduler == False:
      return
    
    for display in self.displays:
      display.apply_changes_in_capabilities()

    self.on_scroll_scheduler = "NULL"

if __name__ == "__main__":
  displays = find_displays.detect_display_devices()
  
  app = BrightnessTrayApp(displays)
  app.main()
