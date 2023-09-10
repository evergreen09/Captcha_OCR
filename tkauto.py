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


def initialize_driver():
    options = uc.ChromeOptions()
    options.add_argument("--user-data-dir=C:\\Users\\Random\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument("--profile-directory=Profile 2")  # <-- substitute Profile 3 with your profile name
    options.add_argument('user-agent=Googlebot')  # Mimic Googlebot's user-agent
    driver = uc.Chrome(options=options)
    return driver


def open_webpage(driver, url):
    driver.get(url)
    time.sleep(1)  # wait for 1 second after loading the webpage


# Additional functions for popup handling, image processing etc. can be added here.

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 30:
            cv2.drawContours(opening, [c], -1, (0,0,0), -1)
    kernel2 = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    opening = cv2.filter2D(opening, -1, kernel2)
    return 255 - opening

def ocr_space_api(image, api_key='K89626776688957'):
    endpoint = "https://api.ocr.space/parse/image"
    files = {'file': ('image.jpg', cv2.imencode('.jpg', image)[1].tobytes())}
    data = {
        'apikey': api_key,
        'language' : 'eng',
        'ocrengine': 5  # Using OCR Engine 2
    }
    response = requests.post(endpoint, files=files, data=data)
    result = response.json()
    return result['ParsedResults'][0]['ParsedText']

pattern = re.compile(r'[^a-zA-Z0-9\\s]')

def remove_special_characters(text):
    return pattern.sub('', text)

def main():
    global driver
    driver = initialize_driver()
    open_webpage(driver, "https://tickets.interpark.com/goods/23011026")
    

    '''processed_image = preprocess_image('cropped.jpg')
    extracted_text = remove_special_characters(ocr_space_api(processed_image))
    x, y = pyautogui.locateCenterOnScreen('input.jpg', confidence=0.8)
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.leftClick()
    time.sleep(0.3)
    pyautogui.write(extracted_text)
    time.sleep(5)'''

def ticket_click():
    x, y = pyautogui.locateCenterOnScreen('button.jpg', confidence=0.8)
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.leftClick()

    time.sleep(1)  # wait for 1 second after loading the webpage
    driver.switch_to.window(driver.window_handles[1])

def crop_img():
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
    cropped_img.save('cropped' + str(x) + '.jpg')

if __name__ == '__main__':
    main()
    for x in range(100):
        ticket_click()
        crop_img()
        driver.close()
    

    
