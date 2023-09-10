import requests
import cv2
import csv
import re

def ocr_space_api(image, api_key='K89626776688957'):
    endpoint = "https://api.ocr.space/parse/image"
    files = {'file': ('image.jpg', cv2.imencode('.jpg', image)[1].tobytes())}
    data = {
        'apikey': api_key,
        'language' : 'eng',
        'ocrengine': 3  # Using OCR Engine 2
    }
    response = requests.post(endpoint, files=files, data=data)
    result = response.json()
    return result['ParsedResults'][0]['ParsedText']

pattern = re.compile(r'[^a-zA-Z0-9\s]')

def remove_special_characters(text):
    return pattern.sub('', text)

if __name__ == '__main__':
    with open('ocr_model3.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Extracted Text'])
        
        for x in range(56):
            image_path = r'c:\Users\Random\Documents\Ticket\OCR\processed_data\result' + str(x) + '.jpg'
            image_data = cv2.imread(image_path)
            extracted_text = remove_special_characters(ocr_space_api(image_data))
            csv_writer.writerow([extracted_text])
            print(str(x) + ' completed')