# FitnessForm - AI-Powered Weightlifting Form Analyzer

FitnessForm is an intelligent video analysis tool that helps weightlifters improve their technique by analyzing form and providing personalized recommendations and corrective exercises.

## Features

- **Video Analysis**: Upload videos of your squat or deadlift for instant AI-powered form analysis
- **Pose Detection**: Uses Google MediaPipe for accurate body landmark detection
- **Comprehensive Form Assessment**: Analyzes key aspects like:
  - Knee tracking and alignment
  - Squat depth
  - Back angle and posture
  - Bar path (deadlift)
  - Hip hinge mechanics
  - Balance and stability
- **Personalized Feedback**: Receive detailed recommendations tailored to your specific form issues
- **Corrective Exercises**: Get specific exercises with sets, reps, and focus areas to address weaknesses
- **Severity Ratings**: Issues are categorized as Critical, Warning, or Info to help prioritize improvements
- **Overall Score**: Get a numerical score (0-100) representing your overall form quality

## Supported Exercises

- **Squat**: Back squat analysis (side view recommended)
- **Deadlift**: Conventional deadlift analysis (side view recommended)

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework for building APIs
- **OpenCV**: Video processing and frame extraction
- **MediaPipe**: Google's ML solution for pose detection
- **NumPy**: Numerical computations for angle calculations and analysis

### Frontend
- **React**: Modern UI library
- **Vite**: Fast build tool and dev server
- **Axios**: HTTP client for API requests

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Start both servers**: Make sure both the backend (port 8000) and frontend (port 3000) are running

2. **Open the app**: Navigate to `http://localhost:3000` in your web browser

3. **Select exercise type**: Choose either "Squat" or "Deadlift"

4. **Upload video**:
   - Click the upload area or drag and drop your video
   - Supported formats: MP4, MOV, AVI (max 100MB)
   - Best results with side-view videos showing full body

5. **Analyze**: Click "Analyze My Form" and wait for processing

6. **Review results**:
   - Check your overall score
   - Read through detected form issues
   - Review recommendations
   - Note corrective exercises to incorporate into training

## API Endpoints

### `GET /`
Health check endpoint that returns API information.

### `GET /health`
Returns the health status of the API.

### `POST /analyze/squat`
Analyzes squat form from uploaded video.

**Request**: multipart/form-data with video file

**Response**:
```json
{
  "exercise": "Squat",
  "overall_score": 85.5,
  "issues": [...],
  "recommendations": [...],
  "corrective_exercises": [...],
  "summary": "Good squat form...",
  "frame_count": 120
}
```

### `POST /analyze/deadlift`
Analyzes deadlift form from uploaded video.

**Request**: multipart/form-data with video file

**Response**: Same structure as squat analysis

## Tips for Best Results

1. **Camera Position**: Film from the side (sagittal plane) with camera at waist height
2. **Full Body Visible**: Ensure your entire body is in frame throughout the movement
3. **Good Lighting**: Film in well-lit area without shadows
4. **Stable Camera**: Use a tripod or stable surface - avoid handheld filming
5. **Multiple Reps**: Include 1-3 repetitions for more comprehensive analysis
6. **Clear Background**: Avoid cluttered backgrounds that might interfere with pose detection

## Project Structure

```
fitnessform/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── analyzers/              # Exercise-specific analyzers
│   │   ├── squat_analyzer.py
│   │   └── deadlift_analyzer.py
│   ├── models/                 # Data models
│   │   └── analysis_result.py
│   └── utils/                  # Utility functions
│       └── pose_utils.py
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── VideoUpload.jsx
│   │   │   └── AnalysisResults.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Form Analysis Details

### Squat Analysis

The squat analyzer evaluates:

- **Knee Tracking**: Detects knee valgus (knees caving in) which can lead to injury
- **Depth**: Measures if you're reaching parallel or below
- **Back Angle**: Checks for excessive forward lean
- **Balance**: Monitors lateral sway and center of mass movement
- **Hip Hinge**: Evaluates hip and knee flexion patterns

### Deadlift Analysis

The deadlift analyzer evaluates:

- **Back Position**: Detects dangerous rounding of the lower back
- **Hip Height**: Ensures optimal starting position
- **Bar Path**: Checks if bar stays close to body in vertical path
- **Lockout**: Verifies complete hip and knee extension
- **Setup**: Evaluates shoulder position relative to the bar

## Corrective Exercise Database

The system includes a comprehensive database of corrective exercises for common form issues:

- Mobility exercises (ankle, hip, thoracic spine)
- Strength exercises (glutes, core, hip abductors)
- Technique drills (tempo work, paused reps, movement patterns)
- Balance and stability training

Each exercise includes:
- Clear description and instructions
- Recommended sets and reps
- Specific focus area and purpose

## Future Enhancements

Potential improvements for future versions:

- [ ] Support for more exercises (bench press, overhead press, etc.)
- [ ] Front-view analysis for additional angles
- [ ] Real-time analysis via webcam
- [ ] Progress tracking over time
- [ ] Comparison with ideal form demonstrations
- [ ] Mobile app version
- [ ] Export analysis reports as PDF
- [ ] Integration with fitness tracking apps

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is designed to assist with form analysis but should not replace professional coaching. Always consult with a qualified strength and conditioning coach or personal trainer, especially when learning new movements or recovering from injury.

## Support

For questions or issues, please open an issue on the GitHub repository.
