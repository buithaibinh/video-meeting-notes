import subprocess
import whisper
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Extract audio from video
video_file = 'data/meeting_video.mov'  # Path to the video file
audio_file = 'data/meeting_audio.mp3'  # Path to the audio file

logging.info('Starting audio extraction from video.')
# Use ffmpeg to extract audio from the video
subprocess.run(['ffmpeg', '-y', '-i', video_file, '-q:a', '0', '-map', 'a', audio_file], check=True)
logging.info('Audio extraction completed successfully.')

# Step 2: Use Whisper to transcribe audio to text with streaming logs
logging.info('Loading Whisper model.')
model = whisper.load_model("base")  # You can choose larger models like 'medium', 'large' for higher accuracy
logging.info('Model loaded successfully.')

logging.info('Transcribing audio to text with streaming logs.')

def log_transcription_progress(result_segments):
    for segment in result_segments:
        logging.info(f"Transcribing segment: [{segment['start']:.2f}s - {segment['end']:.2f}s]: {segment['text']}")

# Transcribe audio with logging of each segment
result = model.transcribe(audio_file, fp16=False, task="transcribe")

# Log each segment during transcription
log_transcription_progress(result['segments'])

transcript_text = result['text']
logging.info('Transcription completed successfully.')

# Step 3: Create simple meeting notes from the transcription
# (Assumes meeting notes are summarized into main points)
def create_meeting_notes(text):
    logging.info('Creating meeting notes from transcribed text.')
    sentences = text.split('. ')
    notes = "\n- " + "\n- ".join(sentences[:5])  # Select the first 5 sentences as an example (can be adjusted)
    logging.info('Meeting notes created successfully.')
    return notes

meeting_notes = create_meeting_notes(transcript_text)

# Save the result to a file
logging.info('Saving meeting notes to output file.')
with open('output/meeting_notes.txt', 'w', encoding='utf-8') as file:
    file.write("Meeting Notes:\n" + meeting_notes)
logging.info("Meeting notes saved successfully to 'output/meeting_notes.txt'")

print("Meeting notes created successfully and saved to 'output/meeting_notes.txt'")
