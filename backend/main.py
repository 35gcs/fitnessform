from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
from pathlib import Path
from typing import List, Dict, Any
from analyzers.squat_analyzer import SquatAnalyzer
from analyzers.deadlift_analyzer import DeadliftAnalyzer
from models.analysis_result import AnalysisResult

app = FastAPI(title="Weightlifting Form Analyzer API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Initialize analyzers
squat_analyzer = SquatAnalyzer()
deadlift_analyzer = DeadliftAnalyzer()


def extract_poses_from_video(video_path: str) -> List[Dict[str, Any]]:
    """Extract pose landmarks from video frames."""
    poses = []
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert BGR to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Process pose detection
            results = pose.process(image)

            if results.pose_landmarks:
                landmarks = []
                for landmark in results.pose_landmarks.landmark:
                    landmarks.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z,
                        'visibility': landmark.visibility
                    })

                poses.append({
                    'frame': frame_count,
                    'timestamp': frame_count / fps,
                    'landmarks': landmarks
                })

            frame_count += 1

    cap.release()
    return poses


@app.get("/")
async def root():
    return {"message": "Weightlifting Form Analyzer API", "version": "1.0.0"}


@app.post("/analyze/squat")
async def analyze_squat(file: UploadFile = File(...)):
    """Analyze squat form from uploaded video."""
    if not file.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        # Extract poses from video
        poses = extract_poses_from_video(tmp_path)

        if not poses:
            raise HTTPException(status_code=400, detail="No poses detected in video")

        # Analyze squat form
        analysis_result = squat_analyzer.analyze(poses)

        # Clean up
        os.unlink(tmp_path)

        return JSONResponse(content=analysis_result.dict())

    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/deadlift")
async def analyze_deadlift(file: UploadFile = File(...)):
    """Analyze deadlift form from uploaded video."""
    if not file.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        # Extract poses from video
        poses = extract_poses_from_video(tmp_path)

        if not poses:
            raise HTTPException(status_code=400, detail="No poses detected in video")

        # Analyze deadlift form
        analysis_result = deadlift_analyzer.analyze(poses)

        # Clean up
        os.unlink(tmp_path)

        return JSONResponse(content=analysis_result.dict())

    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
