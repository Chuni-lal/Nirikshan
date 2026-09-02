#!/usr/bin/env bash
# ==============================================================================
# Nirikshan — Environment Setup Script (Linux/macOS)
# ==============================================================================

set -e

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "========================================================"
echo "🔍 NIRIKSHAN — Packaged Commodity Compliance Auditor"
echo "🛠️  Setting up local development environment..."
echo "========================================================"

# Step 1: Initialize project directories and packages
echo ""
echo "▶ Step 1: Initializing directory structure..."
python3 scripts/init_project.py

# Step 2: Create Python Virtual Environment
echo ""
echo "▶ Step 2: Creating virtual environment (venv)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  ✅ Virtual environment created at ./venv"
else
    echo "  ℹ️  Virtual environment already exists at ./venv"
fi

# Step 3: Activate Virtual Environment
echo ""
echo "▶ Step 3: Activating virtual environment..."
# shellcheck source=/dev/null
source venv/bin/activate
echo "  ✅ Virtual environment activated ($(python3 --version))"

# Step 4: Upgrade pip, setuptools, wheel
echo ""
echo "▶ Step 4: Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

# Step 5: Install backend dependencies
echo ""
echo "▶ Step 5: Installing Python dependencies from backend/requirements.txt..."
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
    echo "  ✅ Dependencies installed successfully."
else
    echo "  ❌ backend/requirements.txt not found!"
    exit 1
fi

echo ""
echo "========================================================"
echo "🎉 Setup complete! Nirikshan is ready for use."
echo "========================================================"
echo ""
echo "To run the Nirikshan server:"
echo "  1. Activate virtual environment:"
echo "     $ source venv/bin/activate"
echo ""
echo "  2. Start the FastAPI application server:"
echo "     $ cd backend"
echo "     $ uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "  3. Open your browser:"
echo "     - Scanner UI:    http://localhost:8000"
echo "     - Dashboard:     http://localhost:8000/dashboard"
echo "     - API Docs:      http://localhost:8000/docs"
echo "========================================================"
