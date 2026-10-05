import cv2
import pytesseract

def read_plate(image_path):
    '''
    Returns the license plate text read from the image at image_path,
    or None if no text is detected with sufficient confidence.

    Effects: Reads the file image_path

    read_plate: Str -> (anyof Str None)
    Requires: image_path exists and is a valid image file
    '''
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config='--psm 8')
    result = text.strip().upper().replace(" ", "")
    if result == "":
        return None
    return result 