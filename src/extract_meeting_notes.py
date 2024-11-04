import os
import subprocess
import whisper
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Extract audio from video
video_file = 'data/meeting_video.mov'  # Path to the video file
audio_file = 'data/meeting_audio.mp3'  # Path to the audio file

if not os.path.exists(audio_file):
    logging.info('Starting audio extraction from video.')
    # Use ffmpeg to extract audio from the video
    try:
        logging.debug(f"Running ffmpeg command: ['ffmpeg', '-y', '-i', {video_file}, '-q:a', '0', '-map', 'a', {audio_file}]")
        start_time = time.time()
        subprocess.run(['ffmpeg', '-y', '-i', video_file, '-q:a', '0', '-map', 'a', audio_file], check=True)
        logging.info(f'Audio extraction completed successfully in {time.time() - start_time:.2f} seconds.')
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during audio extraction: {e}")
        raise
else:
    logging.info('Audio file already exists, skipping extraction.')

# Step 2: Use Whisper to transcribe audio to text with streaming logs
logging.info('Loading Whisper model.')
try:
    start_time = time.time()
    # tiny, small, base, medium, large
    model = whisper.load_model("tiny")  # You can choose larger models like 'medium', 'large' for higher accuracy
    logging.info('Model loaded successfully.')
    logging.debug(f'Model loading time: {time.time() - start_time:.2f} seconds')
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise

logging.info('Transcribing audio to text with streaming logs.')
start_time = time.time()

def log_transcription_progress(result_segments):
    for i, segment in enumerate(result_segments):
        logging.debug(f"Segment {i+1}: Start={segment['start']:.2f}s, End={segment['end']:.2f}s, Text={segment['text']}")
        logging.info(f"Transcribing segment: [{segment['start']:.2f}s - {segment['end']:.2f}s]: {segment['text']}")

# Transcribe audio with logging of each segment
try:
    logging.debug(f"Starting transcription for audio file: {audio_file}")
    result = model.transcribe(audio_file, fp16=False, task="transcribe")
    logging.debug("Transcription result obtained.")
    logging.debug(f'Transcription time: {time.time() - start_time:.2f} seconds')
    # Log each segment during transcription
    log_transcription_progress(result['segments'])
    logging.info('Transcription completed successfully.')
except Exception as e:
    logging.error(f"Error during transcription: {e}")
    raise

transcript_text = result['text']

# Step 3: Create simple meeting notes from the transcription
# (Assumes meeting notes are summarized into main points)
def create_meeting_notes(text):
    logging.info('Creating meeting notes from transcribed text.')
    try:
        sentences = text.split('. ')
        logging.debug(f"Number of sentences in transcript: {len(sentences)}")
        notes = "\n- " + "\n- ".join(sentences[:5])  # Select the first 5 sentences as an example (can be adjusted)
        logging.info('Meeting notes created successfully.')
        return notes
    except Exception as e:
        logging.error(f"Error creating meeting notes: {e}")
        raise

meeting_notes = create_meeting_notes(transcript_text)

# Save the result to a file
logging.info('Saving meeting notes to output file.')
try:
    with open('output/meeting_notes.txt', 'w', encoding='utf-8') as file:
        file.write("Meeting Notes:\n" + meeting_notes)
    logging.info("Meeting notes saved successfully to 'output/meeting_notes.txt'")
except Exception as e:
    logging.error(f"Error saving meeting notes: {e}")
    raise

print("Meeting notes created successfully and saved to 'output/meeting_notes.txt'")
