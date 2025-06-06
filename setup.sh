#!/bin/bash

# Exit on any error
set -e

# Function to create Python environment and start FastAPI backend
setup_backend() {
    echo "📦 Setting up Python backend..."

    cd backend

    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install requirements
    if [ -f requirements.txt ]; then
        echo "📥 Installing Python dependencies..."
        pip install -r requirements.txt
    else
        echo "❗ requirements.txt not found. Skipping pip install."
    fi

    # Create .env file
    echo "🔐 Creating .env file..."
    touch .env

    # Prompt for OpenAI key
    read -p "Enter your OpenAI API Key: " OPENAI_KEY
    echo "OPENAI_API_KEY=$OPENAI_KEY" >.env

    # Start Uvicorn server
    echo "🚀 Starting FastAPI with Uvicorn..."
    uvicorn app.main:app --reload &

    deactivate
    cd ..
}

# Function to set up and start React frontend
setup_frontend() {
    echo "🌐 Setting up React frontend..."

    cd frontend

    # Install npm dependencies
    if [ -f package.json ]; then
        echo "📥 Installing frontend dependencies..."
        npm install
    else
        echo "❗ package.json not found. Are you in the right frontend directory?"
        cd ..
        return
    fi

    # Start React dev server
    echo "🚀 Starting React app..."
    npm run dev &

    cd ..
}

# Main script
echo "🛠️ Full stack setup starting..."
setup_backend
setup_frontend
echo "✅ Setup complete. Backend and frontend are running."
