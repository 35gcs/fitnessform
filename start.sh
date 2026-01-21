#!/bin/bash

# FitnessForm Startup Script

echo "🏋️  Starting FitnessForm..."
echo ""

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Setting up backend virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    cd ..
    echo "✅ Backend setup complete"
    echo ""
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
    echo "✅ Frontend setup complete"
    echo ""
fi

# Start backend
echo "🚀 Starting backend server..."
cd backend
source venv/bin/activate
python main.py > /tmp/fitnessform-backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend running on http://localhost:8000"
else
    echo "❌ Backend failed to start. Check /tmp/fitnessform-backend.log"
    exit 1
fi

# Start frontend
echo "🚀 Starting frontend server..."
cd frontend
npm run dev > /tmp/fitnessform-frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

sleep 2

echo ""
echo "✨ FitnessForm is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📋 API Docs: http://localhost:8000/docs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "📊 Logs:"
echo "  Backend:  /tmp/fitnessform-backend.log"
echo "  Frontend: /tmp/fitnessform-frontend.log"
echo ""
echo "To stop the servers:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to view frontend output..."
tail -f /tmp/fitnessform-frontend.log
