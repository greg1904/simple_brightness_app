from ui.TrayApp import TrayApp
import util.find_displays as find_displays


if __name__ == "__main__":
  displays = find_displays.detect_display_devices()
  
  app = TrayApp(displays)
  app.run()
