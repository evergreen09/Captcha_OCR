from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service


options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\Random\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("profile-directory=Profile 2")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage") # <-- substitute Profile 3 with your profile name

driver = webdriver.Chrome(options=options, service=Service())
driver.get("https://tickets.interpark.com/goods/23011026")
time.sleep(10)  # wait for 1 second after loading the webpage


'''# Step 5: Check the box to close the popup
checkbox = driver.find_element(By.CLASS_NAME, "popupCheckLabel")
checkbox.click()
time.sleep(1)  # wait for 1 second after clicking

# Step 6: Click the link with the specified class
link_to_click = driver.find_element(By.CLASS_NAME, "sideBtn is-primary")
link_to_click.click()
time.sleep(1)  # wait for 1 second after clicking

# Switch to the new window (popup)
driver.switch_to.window(driver.window_handles[1])

# Step 7: Get the image src
image_src = driver.find_element(By.ID, "imgCaptcha").get_attribute("src")

# Step 8: Download and save the image
response = requests.get(image_src, stream=True)
with open("captcha_image.jpg", "wb") as file:
    for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)'''

# Close the browser windows
driver.quit()
