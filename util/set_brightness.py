
import subprocess
import re
import shlex

displayNames = []
displayNamesDDC = []
displayMaxBrightnesses = []


def query_xrandr():
    query = "xrandr --query"
    xrandr_output = subprocess.Popen(shlex.split(query), stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
    stdout, stderr = xrandr_output.communicate()
    return str(stdout, "utf-8")


def extract_displays(output):
    pattern = re.compile(r'\b({0})\b'.format("connected"), flags=re.IGNORECASE)
    lines = output.splitlines()
    connected = [line for line in lines if pattern.search(line)]
    connected_displays = list(
        map(lambda display: display.split()[0], connected))
    for name in connected_displays:
        displayNames.append(name)
    return connected_displays


def detect_display_devices():
    """
    Detects available displays.
    returns connected_displays
    This contains the available device names compatible with xrandr
    """
    displayNames = extract_displays(query_xrandr())
    return displayNames

def directly_set_brightness(brightness_int):
    percentage = brightness_int / 100

    for i in range(len(displayNames)):
       print("xrandr", "--output", displayNames[i], "--brightness", str(percentage))
       subprocess.run(["xrandr", "--output", displayNames[i], "--brightness", str(percentage)])


if __name__ == '__main__':
    print(detect_display_devices())



# below is the code for ddcutil - performance is very bad use xrandr instead

def findMonitors():
        try:
            getNames = str(subprocess.check_output(["ddcutil", "detect"]),
                           'utf-8').split("\n")

            for i in range(len(getNames)):
                if "Model:" in getNames[i]:

                    if not getNames[i].split(":")[1].strip() == "":
                        displayNamesDDC.append(
                            getNames[i].split(":")[1].strip())

                if "Invalid display" in getNames[i]:
                    displayNamesDDC.append(getNames[i].strip())

            for i in range(len(displayNamesDDC)):
                if not displayNames[i] == "Invalid display":
                    brightnessValue = str(subprocess.check_output(
                        ["ddcutil", "getvcp", "10", "-d", str(i + 1)]), 'utf-8')

                    displayMaxBrightnesses.append(int(
                        brightnessValue.split(",")[1].split("=")[1].strip()))

                    displayMaxBrightnesses.append(int(
                        brightnessValue.split(',')[0].split('=')[1].strip()))
                else:
                    displayMaxBrightnesses.append(1)
                    displayMaxBrightnesses.append(1)

        except Exception as e:
            print("error: " + str(e))
            print("Try running as sudo to allow monitor detection")

def directlySetMaxBrightness(percentage_int):

        percentage = round(percentage_int) / 100

        for i in range(len(displayNamesDDC)):
            print("ddcutil", "setvcp", "10", str(int(
            percentage_int)), "-d",
            str(i+1))

            subprocess.run(["ddcutil", "setvcp", "10", str(int(
            percentage_int)), "-d",
            str(i+1) ])
             
