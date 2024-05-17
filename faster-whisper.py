import os
import pyaudio
import wave
import keyboard
from faster_whisper import WhisperModel

# Set environment variable to handle OpenMP error
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Configuration for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# Function to record audio
def record_audio(filename):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording... Press space again to stop.")

    frames = []

    # Recording loop
    while not keyboard.is_pressed('space'):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Recording stopped. Audio saved to", filename)

# Function to transcribe audio using faster-whisper
def transcribe_audio(input_filename, output_filename):
    model = WhisperModel("base")  # You can use "tiny", "base", "small", "medium", or "large"
    segments, info = model.transcribe(input_filename)
    transcription = " ".join(segment.text for segment in segments)
    
    with open(output_filename, "w") as f:
        f.write(transcription)
    
    print("Transcription saved to", output_filename)

# Function to get the next available filename
def get_next_filename(base, ext):
    counter = 1
    while True:
        filename = f"{base}{counter}.{ext}"
        if not os.path.exists(filename):
            return filename
        counter += 1

# Main function
def main():
    print("Press space to start recording.")
    while True:
        keyboard.wait('space')
        audio_filename = get_next_filename("audio", "wav")
        record_audio(audio_filename)
        transcript_filename = get_next_filename("transcript", "txt")
        transcribe_audio(audio_filename, transcript_filename)
        print("Press space to start a new recording or 'q' to quit.")
        keyboard.wait('space')
        if keyboard.is_pressed('q'):
            break

if __name__ == "__main__":
    main()
