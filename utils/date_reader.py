# utils/date_reader.py
# This file handles reading expiry dates from food package images using EasyOCR

# easyocr is the OCR library we installed in Lesson 2
import easyocr

# re is Python's BUILT-IN "regular expressions" library
# Regular expressions let us search for PATTERNS in text
# (like "find something that looks like a date") instead of exact words
import re

# Create the OCR "reader" object
# ['en'] means we want to read English text
# gpu=False tells it to use your CPU (most laptops don't have a 
# compatible GPU for this, so CPU mode is the safe default)
#
# IMPORTANT: The FIRST time this line runs, EasyOCR will DOWNLOAD 
# its language recognition model files (a few hundred MB) - this 
# can take a few minutes depending on your internet speed
reader = easyocr.Reader(['en'], gpu=False)


def extract_text_from_image(image_path):
    """
    Runs EasyOCR on an image and returns ALL text it finds,
    as a list of strings.
    """
    # readtext() runs the OCR model on our image
    # It returns a list of results, where each result contains:
    # [bounding_box_coordinates, detected_text, confidence_score]
    results = reader.readtext(image_path)

    # We only care about the actual TEXT (not coordinates or confidence)
    # so we extract just that part from each result
    all_text = []
    for detection in results:
        text = detection[1]  # index 1 = the actual text string
        all_text.append(text)

    return all_text


def find_expiry_date(text_list):
    """
    Searches through a list of text strings to find something 
    that LOOKS LIKE a date, using pattern matching.
    Returns the first date-like text found, or None if nothing matches.
    """
    # This is a REGULAR EXPRESSION PATTERN that matches common date formats:
    # \d{1,2}   -> 1 or 2 digits (like "5" or "25")
    # [/-]      -> a slash or dash character
    # \d{1,2}   -> 1 or 2 digits again
    # [/-]      -> another slash or dash
    # \d{2,4}   -> 2 to 4 digits (like "26" or "2026")
    # This matches formats like: 25/07/2026, 25-07-26, 5/7/2026
    date_pattern = r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"

    for text in text_list:
        # re.search() checks if our pattern appears ANYWHERE in this text
        match = re.search(date_pattern, text)
        if match:
            # .group() returns just the matching part of the text
            return match.group()

    # If we looped through everything and found no date-like pattern
    return None


def read_expiry_date(image_path):
    """
    Main function: takes an image path, runs OCR, and tries to find 
    an expiry date. Returns the date as text, or "Not Found".
    """
    print("Reading text from image... (this may take a few seconds)")
    all_text = extract_text_from_image(image_path)

    print(f"All text found in image: {all_text}")

    expiry_date = find_expiry_date(all_text)

    if expiry_date is None:
        return "Not Found"

    return expiry_date


# This test code only runs when we execute this file directly
if __name__ == "__main__":
    # CHANGE THIS to match your actual uploaded image filename
    test_image_path = "static/uploads/images.jpg"

    result = read_expiry_date(test_image_path)
    print(f"\nExtracted Expiry Date: {result}")
    