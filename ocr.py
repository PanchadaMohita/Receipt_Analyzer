import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    img = cv2.imread(image_path)

    # Resize
    img = cv2.resize(img, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

    # Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #  Increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    #  Sharpen (FIXED)
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    gray = cv2.filter2D(gray, -1, kernel)

    #  Threshold
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # OCR
    text = pytesseract.image_to_string(
        thresh,
        config='--oem 3 --psm 6'
    )

    return text
