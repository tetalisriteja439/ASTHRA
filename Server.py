from flask import Flask, Response
import os
import time

app = Flask(__name__)

# Directory where your dynamically generated audio files are stored
AUDIO_DIRECTORY = r'.\AudioTemp'

def generate_audio_files():
    counter = 1
    while True:
        audio_file = f"{counter}.mp3"
        file_path = os.path.join(AUDIO_DIRECTORY, audio_file)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                yield file.read()
            counter += 1
        else:
            # File not found, wait and retry
            time.sleep(1)  # Adjust the wait time as needed

@app.route('/stream')
def stream():
    return Response(generate_audio_files(), mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)