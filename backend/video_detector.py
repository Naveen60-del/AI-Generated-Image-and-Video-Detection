import cv2
import tempfile
import os

from PIL import Image

from backend.model.detector import detect_image


def detect_video(video_bytes):

    # Create temporary video file
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    ) as temp_video:

        temp_video.write(video_bytes)

        video_path = temp_video.name


    # Open video
    cap = cv2.VideoCapture(video_path)

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    predictions = []

    # Check approximately 10 frames
    if total_frames > 0:

        frame_numbers = [
            int(total_frames * i / 10)
            for i in range(10)
        ]

    else:

        frame_numbers = []


    for frame_number in frame_numbers:

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_number
        )

        success, frame = cap.read()

        if not success:
            continue


        # Convert OpenCV BGR → RGB
        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Convert to PIL image
        image = Image.fromarray(frame_rgb)

        # Run existing AI detector
        result = detect_image(image)

        predictions.append(result)


    cap.release()

    # Delete temporary video
    os.remove(video_path)


    # No frames detected
    if not predictions:

        return {
            "human": 0,
            "artificial": 0
        }


    # Average all frame predictions
    human_average = sum(
        prediction["human"]
        for prediction in predictions
    ) / len(predictions)


    artificial_average = sum(
        prediction["artificial"]
        for prediction in predictions
    ) / len(predictions)


    return {
        "human": round(human_average, 2),
        "artificial": round(artificial_average, 2)
    }