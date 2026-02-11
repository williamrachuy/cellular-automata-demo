#!/bin/bash

# Cellular Automata Demo Launcher

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH"
    exit 1
fi

# Check if the automata module exists
if [ ! -d "$SCRIPT_DIR/automata" ]; then
    echo "Error: automata module not found in $SCRIPT_DIR"
    exit 1
fi

# Change to project directory and run the application
cd "$SCRIPT_DIR"
python3 -m automata
