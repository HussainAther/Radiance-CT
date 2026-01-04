#!/bin/bash

# --- Radiance-CT (RBYRCT) Data Setup Script ---
# This script prepares the environment for Clinical Validation.

echo "🛡️  Initializing Radiance-CT Data Environment..."

# 1. Create Directory Structure
mkdir -p data/raw
mkdir -p data/processed
mkdir -p models/checkpoints
mkdir -p outputs/reconstructions
mkdir -p outputs/reports

echo "📂  Directory structure created."

# 2. Generate Mock Clinical Phantoms
# We run the mock generator to create the initial .pt files 
# validated against Grainger & Allison standards.
if [ -f "generate_mock_data.py" ]; then
    echo "🧪  Generating Huda-validated synthetic phantoms..."
    python3 generate_mock_data.py
else
    echo "❌  Error: generate_mock_data.py not found!"
    exit 1
fi

# 3. Verify Requirements
echo "📦  Verifying Python dependencies..."
pip install -r requirements.txt --quiet

echo "✅  Setup Complete."
echo "-------------------------------------------------------"
echo "To start the clinical training loop, run:"
echo "  python3 train.py"
echo ""
echo "To view the Dose Currency Dashboard, run:"
echo "  streamlit run dashboard.py"
echo "-------------------------------------------------------"
