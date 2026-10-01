from pathlib import Path
from PIL import Image

from backend.model.detector import detect_image


def test_folder(folder_path, actual_type):
    folder = Path(folder_path)

    print("\nTesting:", actual_type.upper())

    for image_path in folder.rglob("*"):

        if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            continue

        image = Image.open(image_path)

        result = detect_image(image)

        print("\nImage:", image_path.name)
        print("Actual:", actual_type)
        print("Prediction:", result)


test_folder("test_images/real", "human")
test_folder("test_images/ai", "artificial")