from selenium import webdriver
import requests
import sys
import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Start the Chrome browser
driver = webdriver.Chrome()  # No need to provide path if chromedriver.exe is in the working directory

# Step 1: Navigate to the login page
wait = WebDriverWait(driver, 1)

userID = "ltk0906"
userPW = "password"
userNum = "생년월일"

def log_in():
    try:
        login_url = "https://ticket.interpark.com/Gate/TPLogin.asp?CPage=B&MN=Y&tid1=main_gnb&tid2=right_top&tid3=login&tid4=login"
        driver.get(login_url)
        driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
        time.sleep(0.5)
        driver.find_element_by_id('userId').send_keys(userID)  # ID 입력
        driver.find_element_by_id('userPwd').send_keys(userPW)  # PW 입력
        driver.find_element_by_id('btn_login').click()
        wait.until(EC.presence_of_element_located((By.ID, "logstatus")))
    except:
        print("got exception(log_in)")

if __name__ == '__main__':
    log_in()

# Step 4: Navigate to the desired URL
url_target = "https://tickets.interpark.com/goods/23011026"
driver.get(url_target)

# Step 5: Check the box to close the popup
driver.find_element_by_class_name("popupCheckLabel").click()

# Step 6: Click on the link
driver.find_element_by_class_name("sideBtn is-primary").click()

# Switch to the new window that pops up
driver.switch_to.window(driver.window_handles[1])

# Step 7: Get the image src
img_src = driver.find_element_by_id("imgCaptcha").get_attribute("src")

# Step 8: Download and save the image
response = requests.get(img_src, stream=True)
response.raise_for_status()
with open(os.path.join(os.getcwd(), "downloaded_image.jpg"), 'wb') as file:
    for chunk in response.iter_content(8192):
        file.write(chunk)

driver.quit()
