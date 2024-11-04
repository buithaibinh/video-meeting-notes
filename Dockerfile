# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt ./

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . .

# Download necessary NLTK data
RUN python -c "import nltk; nltk.download('punkt')"

# Expose port if needed (optional)
# EXPOSE 8080

# Command to run the script
CMD ["python", "src/extract_meeting_notes.py"]
