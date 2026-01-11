#!/bin/bash

# AI Chatbot - Quick Setup Script

echo "🚀 AI Chatbot - Production Setup"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env file exists in backend directory
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env file from template..."
    cp backend/.env.example backend/.env
    echo ""
    echo "⚠️  IMPORTANT: Please edit backend/.env and add your GEMINI_API_KEY"
    echo "   Get your free key from: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter after you've added your API key to backend/.env..."
fi

# Check if GEMINI_API_KEY is set
source backend/.env
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  WARNING: GEMINI_API_KEY is not set in backend/.env file"
    echo "   The chatbot will not work without an API key."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🐳 Starting Docker containers..."
echo ""

# Start Docker Compose
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Access your application:"
echo "   Frontend:  http://localhost:5173"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
