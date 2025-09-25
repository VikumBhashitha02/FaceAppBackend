from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import cv2
import numpy as np
from deepface import DeepFace

app = FastAPI()

# Allow requests from your Expo app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        # Read image bytes
        image_bytes = await file.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        # Convert to OpenCV format
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Analyze with DeepFace
        results = DeepFace.analyze(frame, actions=["emotion", "age", "gender"], enforce_detection=False)

        # Ensure results is a list
        if isinstance(results, dict):
            results = [results]

        response = []
        for res in results:
            response.append({
                "age": res.get("age", "N/A"),
                "gender": res.get("dominant_gender", "Unknown"),
                "emotion": res.get("dominant_emotion", "Unknown")
            })

        return {"faces": response}

    except Exception as e:
        return {"error": str(e)}
