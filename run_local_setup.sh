#!/bin/bash

# Filename: run_local_setup.sh

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Please install Python 3.9 or higher."
    exit
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 could not be found. Please install pip."
    exit
fi

# Install required Python libraries from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found. Please make sure it is in the current directory."
    exit
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg could not be found. Installing ffmpeg..."
    # Install ffmpeg (for Ubuntu/Debian systems)
    sudo apt-get update && sudo apt-get install -y ffmpeg
fi

# Download NLTK data if needed
python3 -c "import nltk; nltk.download('punkt')"

# Run the Python script
echo "Running the Python script..."
python3 src/extract_meeting_notes.py

echo "Script execution completed."
