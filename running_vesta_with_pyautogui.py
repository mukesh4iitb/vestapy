import pyautogui
import time
import subprocess

# Open VESTA
subprocess.run(["VESTA", "legend.vasp"])
time.sleep(1)  # Wait for VESTA to open


# Move to "File" menu and click
pyautogui.hotkey("alt", "f")  # Open File menu
time.sleep(1)

pyautogui.press("enter")

## Press down arrow 8 times to reach "Export"
#for _ in range(8):
#    pyautogui.press("down")
#    time.sleep(0.2)  # Small delay to ensure the UI registers the keypress
#
## Press Enter to select "Export"
#time.sleep(1)


########## 2nd attempt ########
import pyautogui
import time
import subprocess
#import pygetwindow as gw

# Open VESTA

subprocess.run(["VESTA", "legend.vasp"])
time.sleep(1)
# Opening and focusing on the VESTA window
# Use wmctrl to focus the VESTA window by its title
subprocess.run(['wmctrl', '-a', 'legend.vasp - VESTA'])

pyautogui.hotkey('alt', 'f')  # For file menu
time.sleep(1)

for _ in range(8):
    pyautogui.press("down")
    time.sleep(0.1)
pyautogui.press('enter')
# You can continue with the rest of your actions here

##########3rd attempt ########

import pyautogui
import time
import subprocess
import os

# Open VESTA
subprocess.run(["VESTA", "legend.vasp"])
#subprocess.run(["VESTA", "CONTCAR_pri_S8.vasp"])


# Focus on the VESTA window using wmctrl
#subprocess.run(['wmctrl', '-a', 'legend.vasp - VESTA'])
#pyautogui.moveTo(85, 75)
# Navigate through the File menu
pyautogui.hotkey('alt', 'f')  # Open File menu

time.sleep(1)
pyautogui.press('enter')  # Select the desired option

time.sleep(2)
pyautogui.hotkey('alt', 'f')  # Open File menu


## Press 'down' to navigate through the menu options
#for _ in range(8):
#    pyautogui.press("down")
#    time.sleep(0.1)

