#!/bin/bash

# Determine the script directory
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Path to the virtual environment (relative to SCRIPT_DIR)
VENV_DIR="$SCRIPT_DIR/venv"

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Execute the Python script
python "$SCRIPT_DIR/my_script.py" --option value