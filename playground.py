import cv2
import numpy as np
import requests
import re
import time


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
        'ocrengine': 2  # Using OCR Engine 2
    }
    response = requests.post(endpoint, files=files, data=data)
    result = response.json()
    return result['ParsedResults'][0]['ParsedText']

pattern = re.compile(r'[^a-zA-Z0-9\\s]')
def remove_special_characters(text):
    return pattern.sub('', text)

if __name__ == "__main__":
    processed_image = preprocess_image('cropped.jpg')
    extracted_text = remove_special_characters(ocr_space_api(processed_image))
    print(extracted_text)
