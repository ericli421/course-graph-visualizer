#!/bin/bash

VENV_DIR="venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Install required packages
pip install --upgrade pip
pip install matplotlib networkx

# Run your Python script (replace script.py with your filename)
python CourseGraphUI.py

# Deactivate the virtual environment
deactivate
echo "Virtual environment deactivated."
echo "Script execution completed."
echo "Thank you for using the Course Graph UI!"
# End of script