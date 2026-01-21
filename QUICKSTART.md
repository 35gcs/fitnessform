# Quick Start Guide

Get FitnessForm running in 2 minutes!

## Prerequisites

Make sure you have installed:
- **Python 3.8+** (`python3 --version`)
- **Node.js 16+** (`node --version`)
- **npm** (`npm --version`)

## Option 1: Automated Setup (Recommended)

Just run the startup script:

```bash
./start.sh
```

That's it! The script will:
- Set up the Python virtual environment if needed
- Install all dependencies automatically
- Start both backend and frontend servers
- Show you the URLs to access

Then open **http://localhost:3000** in your browser!

## Option 2: Manual Setup

### Terminal 1 - Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Terminal 2 - Frontend

```bash
cd frontend
npm install
npm run dev
```

Then open **http://localhost:3000** in your browser!

## Using the App

1. Select **Squat** or **Deadlift**
2. Upload a video (MP4, MOV, or AVI)
3. Click **"Analyze My Form"**
4. Review your results, recommendations, and corrective exercises!

## Tips for Best Video Quality

- Film from the **side view** (not front)
- Keep your **full body visible** in the frame
- Use **good lighting**
- Keep the camera **steady** (use a tripod if possible)
- Perform **1-3 reps** for best analysis

## Troubleshooting

### Backend won't start

```bash
# Make sure you're in the backend directory with venv activated
cd backend
source venv/bin/activate
python main.py
# Check for error messages
```

### Frontend won't start

```bash
# Delete node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### "No poses detected"

- Make sure your full body is visible in the video
- Try better lighting
- Use a side-view angle

### Port already in use

If port 8000 or 3000 is already in use:

```bash
# Find and kill the process
# For port 8000:
lsof -ti:8000 | xargs kill -9

# For port 3000:
lsof -ti:3000 | xargs kill -9
```

## Next Steps

- Read the full [README.md](README.md) for detailed features
- Check [SETUP.md](SETUP.md) for advanced configuration
- Review the [API documentation](http://localhost:8000/docs) when backend is running

Happy lifting!
