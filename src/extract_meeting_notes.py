import os
import subprocess
import whisper
import logging
import time
import math
from pydub import AudioSegment
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import shutil

# Download necessary NLTK data
import nltk
nltk.download('punkt')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Extract audio from video
video_file = 'data/meeting_video.mov'  # Path to the video file
audio_file = 'data/meeting_audio.mp3'  # Path to the audio file

temp_dir = 'data/temp'
os.makedirs(temp_dir, exist_ok=True)  # Create the temp directory if it doesn't exist

def split_audio(audio_file, chunk_length_ms=600000, overlap_ms=10000):  # Default 10-minute chunks with 10-second overlap
    audio = AudioSegment.from_file(audio_file)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms - overlap_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_file = f"{temp_dir}/chunk_{i // (chunk_length_ms - overlap_ms)}.mp3"
        chunk.export(chunk_file, format="mp3")
        chunks.append(chunk_file)
        logging.info(f"Created chunk: {chunk_file}")
    return chunks

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

# Split the audio file into smaller chunks if it's long
logging.info('Splitting audio into smaller chunks with overlap.')
audio_chunks = split_audio(audio_file)

# Step 2: Use Whisper to transcribe audio to text with streaming logs
logging.info('Loading Whisper model.')
try:
    start_time = time.time()
    model = whisper.load_model("base")  # You can choose larger models like 'medium', 'large' for higher accuracy
    logging.info('Model loaded successfully.')
    logging.debug(f'Model loading time: {time.time() - start_time:.2f} seconds')
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise

transcript_segments = []
for chunk_file in audio_chunks:
    logging.info(f'Transcribing chunk: {chunk_file}')
    start_time = time.time()

    # Transcribe each chunk with logging of each segment
    try:
        logging.debug(f"Starting transcription for audio file: {chunk_file}")
        result = model.transcribe(chunk_file, fp16=False, task="transcribe")
        logging.debug(f'Transcription time for {chunk_file}: {time.time() - start_time:.2f} seconds')
        # Append segments to transcript_segments for post-processing
        transcript_segments.extend(result['segments'])
        logging.info(f'Transcription completed successfully for {chunk_file}.')
    except Exception as e:
        logging.error(f"Error during transcription of {chunk_file}: {e}")
        raise

# Combine and clean up overlapping segments intelligently
combined_text = ""
last_end_time = 0
for segment in transcript_segments:
    if segment['start'] >= last_end_time:
        combined_text += segment['text'] + " "
    last_end_time = max(last_end_time, segment['end'])

# Save the full transcript to a separate file
logging.info('Saving full transcript to output file.')
try:
    with open('output/full_transcript.txt', 'w', encoding='utf-8') as file:
        file.write(combined_text)
    logging.info("Full transcript saved successfully to 'output/full_transcript.txt'")
except Exception as e:
    logging.error(f"Error saving full transcript: {e}")
    raise

# Step 3: Create effective meeting notes from the transcription
# (Uses text summarization to highlight key points)
def create_meeting_notes(text):
    logging.info('Creating meeting notes from transcribed text.')
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, 5)  # Adjust number of sentences as needed

        notes = "\n- " + "\n- ".join(str(sentence) for sentence in summary_sentences)
        logging.debug(f"Number of sentences in summary: {len(summary_sentences)}")
        logging.info('Meeting notes created successfully.')
        return notes
    except Exception as e:
        logging.error(f"Error creating meeting notes: {e}")
        raise

meeting_notes = create_meeting_notes(combined_text)

# Save the result to a file
logging.info('Saving meeting notes to output file.')
try:
    with open('output/meeting_notes.txt', 'w', encoding='utf-8') as file:
        file.write("Meeting Notes:\n" + meeting_notes)
    logging.info("Meeting notes saved successfully to 'output/meeting_notes.txt'")
except Exception as e:
    logging.error(f"Error saving meeting notes: {e}")
    raise

# Clean up temporary chunk files
logging.info('Cleaning up temporary files.')
try:
    shutil.rmtree(temp_dir)
    logging.info(f"Temporary directory '{temp_dir}' removed successfully.")
except Exception as e:
    logging.error(f"Error cleaning up temporary files: {e}")
    raise

print("Meeting notes created successfully and saved to 'output/meeting_notes.txt'")
