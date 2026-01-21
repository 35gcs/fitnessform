# FitnessForm Setup Guide

This guide will walk you through setting up FitnessForm on your local machine.

## Quick Start

For the impatient, here's the TL;DR:

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

Then open `http://localhost:3000` in your browser!

## Detailed Setup Instructions

### Step 1: Check Prerequisites

Make sure you have the following installed:

**Python 3.8+**
```bash
python --version
# Should output: Python 3.8.x or higher
```

**Node.js 16+**
```bash
node --version
# Should output: v16.x.x or higher
```

**npm**
```bash
npm --version
# Should output: 8.x.x or higher
```

If you don't have these installed:
- Python: Download from [python.org](https://www.python.org/downloads/)
- Node.js: Download from [nodejs.org](https://nodejs.org/)

### Step 2: Clone/Download the Project

If you haven't already, get the project code:

```bash
git clone <repository-url>
cd fitnessform
```

### Step 3: Backend Setup

#### 3.1 Navigate to Backend Directory
```bash
cd backend
```

#### 3.2 Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

#### 3.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- uvicorn (ASGI server)
- OpenCV (video processing)
- MediaPipe (pose detection)
- NumPy (numerical computations)
- And other dependencies

**Note**: Installing OpenCV and MediaPipe may take a few minutes.

#### 3.4 Verify Installation

```bash
python -c "import cv2; import mediapipe; print('All dependencies installed!')"
```

If you see "All dependencies installed!" - you're good to go!

#### 3.5 Start the Backend Server

```bash
python main.py
```

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal window open!** The backend needs to stay running.

To test the backend is working, open a browser and go to:
- `http://localhost:8000` - Should show API info
- `http://localhost:8000/health` - Should show `{"status": "healthy"}`

### Step 4: Frontend Setup

Open a **new terminal window** (keep the backend running in the first one).

#### 4.1 Navigate to Frontend Directory
```bash
cd frontend  # If you're in the project root
# OR
cd ../frontend  # If you're in the backend directory
```

#### 4.2 Install Node Dependencies

```bash
npm install
```

This will install:
- React (UI library)
- Vite (build tool)
- Axios (HTTP client)
- And other dependencies

This may take a few minutes the first time.

#### 4.3 Start the Development Server

```bash
npm run dev
```

You should see output like:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

#### 4.4 Open the Application

Open your browser and go to `http://localhost:3000`

You should see the FitnessForm application!

### Step 5: Test the Application

1. **Select Exercise**: Choose "Squat" or "Deadlift"
2. **Upload Video**: Use a test video of your lifting form
3. **Analyze**: Click "Analyze My Form"
4. **View Results**: Check the analysis, recommendations, and corrective exercises

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Make sure your virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Problem**: `Port 8000 already in use`
**Solution**: Either kill the process using port 8000, or modify `main.py` to use a different port:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed to 8001
```

**Problem**: OpenCV or MediaPipe installation fails
**Solution**: Try installing them separately:
```bash
pip install opencv-python==4.9.0.80
pip install mediapipe==0.10.9
```

### Frontend Issues

**Problem**: `npm: command not found`
**Solution**: Install Node.js from [nodejs.org](https://nodejs.org/)

**Problem**: `Port 3000 already in use`
**Solution**: Either kill the process using port 3000, or modify `vite.config.js`:
```javascript
export default defineConfig({
  server: {
    port: 3001,  // Changed to 3001
  }
})
```

**Problem**: Cannot connect to backend
**Solution**:
1. Verify backend is running on port 8000
2. Check `vite.config.js` proxy configuration
3. Try accessing `http://localhost:8000/health` directly

### Video Upload Issues

**Problem**: Video upload fails or gets stuck
**Solution**:
1. Check video file size (must be < 100MB)
2. Try converting video to MP4 format
3. Ensure backend is running and accessible

**Problem**: No poses detected
**Solution**:
1. Ensure full body is visible in video
2. Check lighting conditions
3. Try a different camera angle (side view works best)

## Development Tips

### Backend Development

To enable auto-reload during development, modify `main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### Frontend Development

Vite automatically hot-reloads when you save changes. Just edit files in `frontend/src/` and see changes instantly!

### API Documentation

FastAPI provides automatic interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Production Deployment

For production deployment:

1. **Backend**: Use a production ASGI server and set proper environment variables
2. **Frontend**: Build the production bundle with `npm run build`
3. **Hosting**: Deploy to services like Heroku, AWS, or DigitalOcean

See the main README for more deployment details.

## Next Steps

- Read through the main `README.md` for feature details
- Try analyzing your own lifting videos
- Review the corrective exercises and incorporate them into training
- Check out the codebase to understand how it works

## Getting Help

If you encounter issues:
1. Check this troubleshooting section
2. Review error messages carefully
3. Check terminal logs for both backend and frontend
4. Open an issue on GitHub with details about your problem

Happy lifting!
