import os
import uuid  
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Path to save recorded audio
RECORDINGS_FOLDER = '/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio'
RESULT_AUDIO_FOLDER = '/Users/aditya.narayan/Desktop/s_To_s/indic-tts/output'

# Ensure the folders exist
# os.makedirs(RECORDINGS_FOLDER, exist_ok=True)
# os.makedirs(RESULT_AUDIO_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'webm'

def delete_all_files_in_folder(folder):
    # Delete all files in the folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if there is an audio file in the POST request
        if 'audio' not in request.files:
            return redirect(request.url)

        file = request.files['audio']

        # Delete all existing files in the rec_audio folder before saving the new one
        delete_all_files_in_folder(RECORDINGS_FOLDER)

        if file and allowed_file(file.filename):
            # Generate a unique filename using UUID
            unique_filename = f"{uuid.uuid4()}.webm"
            file.save(os.path.join(RECORDINGS_FOLDER, unique_filename))
            return redirect(url_for('index'))

    # Get list of recorded files and result audio files
    recorded_files = os.listdir(RECORDINGS_FOLDER)
    result_files = os.listdir(RESULT_AUDIO_FOLDER)

    return render_template('index.html', recorded_files=recorded_files, result_files=result_files)

@app.route('/recordings/<filename>')
def serve_recording(filename):
    return send_from_directory(RECORDINGS_FOLDER, filename)

@app.route('/results/<filename>')
def serve_result(filename):
    return send_from_directory(RESULT_AUDIO_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
