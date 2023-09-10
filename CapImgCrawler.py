import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
import requests
import pyautogui
import pygetwindow
from PIL import Image
import cv2
import re
import numpy as np



options = uc.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Users\\Random\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("--profile-directory=Profile 2") # <-- substitute Profile 3 with your profile name
options.add_argument('user-agent=Googlebot')  # Mimic Googlebot's user-agent


driver = uc.Chrome(options=options)
driver.get("https://tickets.interpark.com/goods/23011026")
time.sleep(1)  # wait for 1 second after loading the webpage

'''try:
    # Step 5: Check the box to close the popup
    checkbox = driver.find_element(By.CLASS_NAME, "popupCheckLabel")
    checkbox.click()
    time.sleep(1)  # wait for 1 second after clicking
except:
    print("Pop Up Alreaddy Closed")'''

x, y = pyautogui.locateCenterOnScreen('button.jpg', confidence=0.8)
pyautogui.moveTo(x, y, duration=0.1)
pyautogui.leftClick()

time.sleep(1)  # wait for 1 second after loading the webpage
driver.switch_to.window(driver.window_handles[1])


path = 'ticketing.jpg'

window = pygetwindow.getWindowsWithTitle('인터파크 티켓')[0]
left, top = window.topleft
right, bottom = window.bottomright
pyautogui.screenshot(path)
im = Image.open(path)
im = im.crop((left, top, right, bottom))
im.save(path)

left, upper, right, lower = 397, 405, 740, 546

img = Image.open(path)
cropped_img = img.crop((left, upper, right, lower))
cropped_img.save('cropped.jpg')



x, y = pyautogui.locateCenterOnScreen('input.jpg', confidence=0.8)
pyautogui.moveTo(x, y, duration=0.1)
pyautogui.leftClick()
pyautogui.write('AAAAA')
time.sleep(5)



# Close the browser windows
driver.quit()
