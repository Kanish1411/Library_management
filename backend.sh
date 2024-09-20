#!/bin/bash

# Navigate to Backend
echo "Setting up Backend..."
cd backend || { echo "Backend directory not found"; exit 1; }

# Install backend dependencies
if [ -f "./req.txt" ]; then
    pip install -r ./req.txt || { echo "Failed to install backend dependencies"; exit 1; }
else
    echo "Backend requirements file not found"
    exit 1
fi

# Run backend application
if [ -f "./app.py" ]; then
    python ./app.py || { echo "Failed to run backend application"; exit 1; }
else
    echo "Backend app.py not found"
    exit 1
fi