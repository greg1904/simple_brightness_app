from ui.TrayApp import TrayApp
import util.find_displays as find_displays
import gi

gi.require_versions({"Gtk" : "3.0"})

from gi.repository import Gtk

if __name__ == "__main__":
  displays = find_displays.detect_display_devices()
  
  app = TrayApp(displays)
  Gtk.main()
