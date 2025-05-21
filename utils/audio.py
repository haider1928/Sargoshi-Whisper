import sounddevice as sd
import scipy.io.wavfile as wav
import io

def record_audio(duration, sample_rate=44100):
    """Record audio and return it as an in-memory BytesIO WAV file."""
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    buffer = io.BytesIO()
    wav.write(buffer, sample_rate, audio_data)
    buffer.seek(0)
    return buffer
