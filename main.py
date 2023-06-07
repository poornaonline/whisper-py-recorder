import pyaudio
import wave
import subprocess
import whisper

# https://github.com/openai/whisper

# pip install git+https://github.com/openai/whisper.git
# brew install ffmpeg

# Set parameters for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
MP3_OUTPUT_FILENAME = "output.mp3"

# Initialize PyAudio object
p = pyaudio.PyAudio()

# Open audio stream for recording
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording...")

# Record audio data
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop audio stream
stream.stop_stream()
stream.close()
p.terminate()

# Save audio data to WAV file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Convert WAV file to MP3 format using ffmpeg
subprocess.call(['ffmpeg', '-i', WAVE_OUTPUT_FILENAME, MP3_OUTPUT_FILENAME])

print("File converted to MP3 format.")

# Wisper impl

model = whisper.load_model("base")
result = model.transcribe("output.mp3")
print(result["text"])