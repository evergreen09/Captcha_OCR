import cv2
import numpy as np

dir_path = 'c:\\Users\\Random\\Documents\\Ticket\\OCR\\processed_data\\'

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
    result = 255 - opening
    cv2.imwrite(dir_path + 'result' + str(x) + '.jpg', result)

if __name__ == '__main__':
    for x in range(56):
        path = r'c:\Users\Random\Documents\Ticket\OCR\data\cropped' + str(x) + '.jpg'
        preprocess_image(path)