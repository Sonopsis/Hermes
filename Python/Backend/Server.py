from flask import Flask, render_template, request, jsonify
import os
import sounddevice as sd
import numpy as np
import wave
import threading
import sys
from analyzer import transcribe_audio, analyze_tone



app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

recording = False  # Flag to control recording

def record_audio(filename, duration=5, samplerate=44100):
    global recording
    recording = True
    print("Recording started...")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype=np.int16)
    sd.wait()
    recording = False
    print("Recording stopped.")
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    filename = os.path.join(app.config['UPLOAD_FOLDER'], "recorded_audio.wav")
    thread = threading.Thread(target=record_audio, args=(filename,))
    thread.start()
    return jsonify({"message": "Recording started..."})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recording
    if recording:
        sd.stop()
        return jsonify({"message": "Recording stopped."})
    else:
        return jsonify({"message": "No active recording."})

@app.route('/analyze', methods=['POST'])
def analyze():
    filename = os.path.join(app.config['UPLOAD_FOLDER'], "recorded_audio.wav")
    transcript = transcribe_audio(filename)
    mode = request.form.get('mode', 'formal')  # Default mode is formal
    feedback = analyze_tone(transcript, mode)
    
    return jsonify({"transcript": transcript, "feedback": feedback})

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5000)
