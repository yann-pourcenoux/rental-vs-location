#!/bin/bash
# Script to run the Swedish Housing Calculator

echo "🏠 Starting Swedish Housing Calculator..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Installing dependencies..."
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo "🚀 Launching Streamlit application..."
echo "📱 Open your browser to: http://localhost:3156"
echo "🛑 Press Ctrl+C to stop the application"

streamlit run app.py --server.port 3156 --server.address 0.0.0.0
