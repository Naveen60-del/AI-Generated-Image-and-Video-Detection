from transformers import pipeline

MODEL_NAME = "umm-maybe/AI-image-detector"

classifier = pipeline(
    "image-classification",
    model=MODEL_NAME
)


def detect_image(image):
    results = classifier(image)

    probabilities = {}

    for result in results:
        label = result["label"]
        confidence = result["score"] * 100
        probabilities[label] = round(confidence, 2)

    return probabilities