#!/bin/bash

# Personal Finance Assistant - Quick Start Script

echo "🚀 Personal Finance Assistant - Setup"
echo "======================================"
echo ""

# Check for .env
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Choose Provider
echo "Recommended: Google Gemini"
echo "--------------------------"
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY not found in .env"
    echo "   Using Ollama default if available..."
    python run.py --model ollama
else
    echo "✅ Gemini detected. Launching..."
    python run.py --model google
fi
