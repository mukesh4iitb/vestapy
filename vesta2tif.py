import pyautogui
import subprocess
import time

subprocess.Popen(["VESTA", "CONTCAR_Co_fix_new.vasp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)
subprocess.run(['wmctrl', '-a', 'VESTA'])
pyautogui.hotkey("alt", 'f')
pyautogui.press(['down'] * 8)
pyautogui.press('enter')
pyautogui.hotkey('ctrl', 'a')
pyautogui.press("backspace")
pyautogui.write("POSCAR.tif")
pyautogui.hotkey("shift", "tab")
pyautogui.hotkey("shift", "tab")
#for _ in range(2):
#    pyautogui.hotkey("shift", "tab")
pyautogui.press("enter")
pyautogui.press(['down'] * 5)
pyautogui.press("enter")
pyautogui.press(['tab']*4)
pyautogui.press("enter")


#pyautogui.press(['tab']*2)
#pyautogui.press('enter')

pyautogui.write('2')
time.sleep(1)
pyautogui.press(['tab']*2)
pyautogui.press('enter')
time.sleep(4)
pyautogui.press('enter')



# Close VESTA
time.sleep(1)
subprocess.run(["pkill", "VESTA"])


########## 2nd attempt #####

import pyautogui
import subprocess
import time

subprocess.Popen(["VESTA", "CONTCAR_Co_fix_new.vasp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)
subprocess.run(['wmctrl', '-a', 'VESTA'])
pyautogui.hotkey("alt", 'f')
pyautogui.press(['down'] * 8)
pyautogui.press('enter')
pyautogui.hotkey('ctrl', 'a')
pyautogui.press("backspace")
pyautogui.write("POSCAR.tif")
pyautogui.press(['tab']*2)
pyautogui.press('enter')
pyautogui.write('2')
pyautogui.press(['tab']*2)
pyautogui.press('enter')
time.sleep(4)
pyautogui.press('enter')



# Close VESTA gracefully
time.sleep(1)
subprocess.run(["pkill", "VESTA"])

