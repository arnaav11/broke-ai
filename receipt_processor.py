import cv2
import pytesseract
import re
import os
from PIL import Image

# Connect Pyhton directly to your new Windows Tessearact installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """
    Applies Computer Vision (OpenCV) to clean the image before OCR.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Cannot find image file at: {image_path}")

    # Read image matrix via OpenCV
    img = cv2.imread(image_path)
    
    # NEW STEP: Scale the image up by 2x to make tiny decimal dots visible
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Step A: Convert to grayscale (removes color noise)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Step B: Apply Otsu Binarization (turns background pure white, text stark black)
    processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    return processed_img

def extract_prices(image_path):
    """
    Scans the processed image for text and parses out any line-item pricing patterns.
    """
    # Run OpenCV clean up pipeline
    cleaned_matrix = preprocess_image(image_path)

    # Convert OpenCV image matrix aray back to PIL format for pytesseract compatability
    pil_img = Image.fromarray(cleaned_matrix)

    # Run structural character recognition
    extracted_text = pytesseract.image_to_string(pil_img, config='--psm 6')

    print("\n--- [OCR RAW TEXT DATA EXTRACTION] ---")
    print(extracted_text)
    print("---------------------------------------\n")

    # Regex formula updated to accept BOTH dots and commas: \. or ,
    price_pattern = r'\b\d+[\.,]\d{2}\b'
    found_prices = re.findall(price_pattern, extracted_text)
    
    # Convert string matches safely into decimals
    final_prices = []
    for price in found_prices:
        # Swap any European-style commas for standard dots
        clean_price = price.replace(',', '.')
        final_prices.append(float(clean_price))
    
    return final_prices

if __name__ == "__main__":
    print("Receipt Engine Core Ready. Starting test scan...")
    
    # Updated to match your exact file name!
    test_image_name = "receipt.png" 
    
    try:
        extracted_prices = extract_prices(test_image_name)
        print("--- [TEST RESULT] ---")
        print(f"Prices found: {extracted_prices}")
        print("---------------------")
    except Exception as e:
        print(f"Oops, the test run crashed: {e}")
