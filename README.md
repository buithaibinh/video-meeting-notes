# Project: Video Meeting Notes Extraction

## Overview

This project provides a script to extract, transcribe, summarize, and translate meeting notes from a video file. The workflow includes the following steps:

1. Extract audio from a video file
2. Transcribe the audio into text using Whisper
3. Summarize the transcribed text into meeting notes
4. Translate the meeting notes into Vietnamese


## Prerequisites

Ensure you have the following software installed on your system:

* Python 3.9 or higher
* ffmpeg for audio processing

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd video-meeting-notes
   ```
2. Create a virtual environment

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate # for Linux or macOS
   .venv\Scripts\activate # for Windows
   ```
3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```
4. Install `ffmpeg` (if not already installed)

   ```bash
      # For Ubuntu/Debian systems
   sudo apt-get update && sudo apt-get install -y ffmpeg

   # For macOS (using Homebrew)
   brew install ffmpeg
   ```
5. **Download NLTK data** (This is handled in the script, but you can run it manually if needed)

   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```
## Running the Script Locally

1. Ensure you have the video file in the data/ directory with the name `meeting_video.mov`.
2. Run the script using:
   ```bash
   python src/extract_meeting_notes.py
   ```

## Outputs

1. The full transcription will be saved in `output/full_transcript.txt`
2. The summarized meeting notes will be saved in o`utput/meeting_notes.txt`
3. The translated meeting notes (in Vietnamese) will be saved in `output/meeting_notes_vi.txt`

There is a `sh` script that can be used to run the script in one go. You can run it using:

```bash
sh ./run_local_setup.sh
```

## Running in a Docker Container

1. Build the Docker image:

   ```bash
   docker build -t meeting-notes-extractor .
   ```
2. Run the Docker container:

   ```bash
   docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output meeting-notes-extractor
   ```

## Libraries Used

* Python Packages:
  * whisper for transcription
  * pydub for audio processing
  * sumy for text summarization
  * transformers for translation using MarianMT
  * nltk for tokenization

## Troubleshooting

* **Error: ffmpeg not found:** Ensure ffmpeg is installed and accessible from your system path.
* **Error: sentencepiece not found:** Install sentencepiece using:
   ```bash
   pip install sentencepiece
   ```

## License

This project is licensed under the MIT License.