from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO

from backend.model.detector import detect_image
from backend.video_detector import detect_video


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Detection System Backend is Working!"
    }


# IMAGE DETECTION
@app.post("/detect")
async def detect_file(file: UploadFile = File(...)):

    contents = await file.read()

    image = Image.open(
        BytesIO(contents)
    )

    result = detect_image(image)

    return {
        "filename": file.filename,
        "probabilities": result
    }


# VIDEO DETECTION
@app.post("/detect-video")
async def detect_video_file(file: UploadFile = File(...)):

    contents = await file.read()

    result = detect_video(contents)

    return {
        "filename": file.filename,
        "probabilities": result
    }