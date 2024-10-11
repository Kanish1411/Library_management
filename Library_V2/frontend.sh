#!/bin/bash

echo "Setting up Frontend..."
cd ../frontend || { echo "Frontend directory not found"; exit 1; }

# Install frontend dependencies
if [ -f "./package.json" ]; then
    npm install || { echo "Failed to install frontend dependencies"; exit 1; }
else
    echo "package.json not found"
    exit 1
fi

# Run frontend development server
npm run dev || { echo "Failed to run frontend server"; exit 1; }