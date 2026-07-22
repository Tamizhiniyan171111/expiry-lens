# utils/food_detector.py
# This file handles AI-based food detection using YOLOv8

from ultralytics import YOLO

# UPGRADED: switched to "yolov8m.pt" (medium)
# Model sizes from fastest/least accurate to slowest/most accurate:
# nano (n) -> small (s) -> medium (m) -> large (l) -> extra-large (x)
# "m" gives noticeably better accuracy than nano/small, while still 
# running in a reasonable time on a normal laptop CPU
#
# IMPORTANT: The first time this runs, it will DOWNLOAD this model 
# file (~50MB) from the internet - this may take a few minutes.
# After that, it's saved locally and reused instantly.
model = YOLO("yolov8m.pt")

# If YOLOv8 isn't at least this confident, we don't fully trust the result
# Lowered slightly from 0.40 to 0.30 to allow reasonable (but not perfect)
# guesses through, now that we have a more accurate model backing it up
CONFIDENCE_THRESHOLD = 0.30


def detect_food_item(image_path):
    """
    Takes the file path of an image, runs YOLOv8 on it,
    and returns the name of the most confidently detected object,
    along with its confidence score (0 to 1).
    If confidence is too low, returns "Unknown Item" instead of a bad guess.
    """
    # This actually runs the AI model on our image
    results = model(image_path)

    best_detection_name = None
    best_confidence = 0.0

    # Loop through every object YOLOv8 found in the image
    for result in results:
        for box in result.boxes:
            class_index = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[class_index]

            print(f"Detected: {class_name} (confidence: {confidence:.2f})")

            # Keep track of whichever detection has the highest confidence so far
            if confidence > best_confidence:
                best_confidence = confidence
                best_detection_name = class_name

    # Safety check: if nothing was detected, OR our best guess wasn't
    # confident enough, honestly report "Unknown Item" instead of guessing wrong
    if best_detection_name is None or best_confidence < CONFIDENCE_THRESHOLD:
        print(f"Confidence too low ({best_confidence:.2f}) - reporting as Unknown Item")
        return "Unknown Item", best_confidence

    return best_detection_name, best_confidence


# This test code only runs when we execute this file directly
if __name__ == "__main__":
    # CHANGE THIS to match your actual uploaded image filename
    test_image_path = "static/uploads/images.jpg"

    food_name, confidence = detect_food_item(test_image_path)
    print(f"\nFinal Result: {food_name} (confidence: {confidence:.2f})")
    