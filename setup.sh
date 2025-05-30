#!/bin/bash

# Setup script for Attendance Tracker

echo "Setting up Attendance Tracker environment..."

# Install pipenv if not already installed
pip install pipenv

# Install dependencies
echo "Installing dependencies with Pipenv..."
pipenv install

echo "Setup complete!"
echo "To activate the virtual environment, run: pipenv shell"
echo "Then run the application with: python run.py"
echo "To migrate existing data, run: python migrate.py"