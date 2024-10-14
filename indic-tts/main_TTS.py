import subprocess
import socket
import uuid
import os

def unique_name():
    return str(uuid.uuid4())


def dir_deleter():
    for i in os.listdir('/Users/aditya.narayan/Desktop/s_To_s/indic-tts/output'):
        file_path = os.path.join('/Users/aditya.narayan/Desktop/s_To_s/indic-tts/output', i)
        if i.endswith('.wav'):
            os.remove(file_path)

def synthesize_text(text, speaker_idx):
    # Define the paths for configuration and model files
    config_path = "/Users/aditya.narayan/Desktop/speechToSpeech/indic-tts/models/v1/kn/fastpitch/config.json"
    model_path = "/Users/aditya.narayan/Desktop/speechToSpeech/indic-tts/models/v1/kn/fastpitch/best_model.pth"
    out_path = "/Users/aditya.narayan/Desktop/s_To_s/indic-tts/output/"+unique_name()+".wav"
    vocoder_path = "/Users/aditya.narayan/Desktop/speechToSpeech/indic-tts/models/v1/kn/hifigan/best_model.pth"
    vocoder_config_path = "/Users/aditya.narayan/Desktop/speechToSpeech/indic-tts/models/v1/kn/hifigan/config.json"

    # Create the command
    command = [
        "tts",
        "--text", text,
        "--config_path", config_path,
        "--model_path", model_path,
        "--out_path", out_path,
        "--vocoder_path", vocoder_path,
        "--vocoder_config_path", vocoder_config_path,
        "--speaker_idx", str(speaker_idx)  # Convert speaker_idx to string if necessary
    ]

    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)
    print("🟢 Speech Generated")
    

def tts_server():
    host = 'localhost'
    port = 5003

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print('TTS Server is listening...')

    while True:
        conn, addr = server_socket.accept()
        print(f'Connected by {addr}')

        text_data = conn.recv(65536).decode()
        print('Received text data from LLM:', text_data)

        dir_deleter()

        synthesize_text(text_data, "female")



if __name__ == "__main__":
    tts_server()