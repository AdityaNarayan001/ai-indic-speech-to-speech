import torch
import os
import nemo.collections.asr as nemo_asr
import socket
from pydub import AudioSegment
import json
from datetime import datetime
from utility.audio_to_mono import audio_to_mono


MODEL_PATH = "/Users/aditya.narayan/Desktop/s_To_s/indic-asr/asr_model/ai4b_indicConformer_kn.nemo"

RAW_AUDIO = "/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio/sample_audio.wav"
PROCESSED_AUDIO_0 = "/Users/aditya.narayan/Desktop/s_To_s/indic-asr/processed_audio/mono_left.wav"
PROCESSED_AUDIO_1 = "/Users/aditya.narayan/Desktop/s_To_s/indic-asr/processed_audio/mono_right.wav"

def audio_process():
    if len(os.listdir("/Users/aditya.narayan/Desktop/s_To_s/indic-asr/processed_audio")) == 1:
        print("🔴 No Mono file found !")
        audio_to_mono(RAW_AUDIO, PROCESSED_AUDIO_0, PROCESSED_AUDIO_1)
        print("🟢 Mono file created.")
    else:
        print("🟢 Mono files found.")

def infer():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = nemo_asr.models.EncDecCTCModel.restore_from(restore_path=MODEL_PATH, strict=False)
    model.freeze()
    model = model.to(device)

    model.cur_decoder = 'ctc'
    ctc_text = model.transcribe([PROCESSED_AUDIO_0], batch_size=1,logprobs=False, language_id='kn')[0]
    print('🟩 Text : ',ctc_text[0])
    return ctc_text

def file_rename(old_name):
    new_name = "/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio/sample_audio.wav"

    os.rename(old_name, new_name)
    print(f"File renamed from {old_name} to {new_name}")

def convert_webm_to_wav_and_delete(input_file, output_file):
    audio = AudioSegment.from_file(input_file, format='webm')
    audio.export(output_file, format='wav')
    os.remove(input_file)
    json_file = '/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio/metadata.json'
    print(f"Deleted the original file: {input_file}")
    if os.path.exists(json_file):
        os.remove(json_file)
        print(f"Deleted the JSON file: {json_file}")
    else:
        print(f"JSON file does not exist: {json_file}")

def make_metadata(): 
    current_time = datetime.now().isoformat()  # Format: YYYY-MM-DDTHH:MM:SS
    metadata = {
        "current_time": current_time,
        "re_iterate": True
    }
    filename = '/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio/metadata.json'
    with open(filename, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)
    print(f"Current time has been saved to {filename}")

def check_re_iterate(json_file):
    with open(json_file, 'r') as file:
        metadata = json.load(file)
    if metadata.get("re_iterate") is True:
        flag = True
    else:
        flag = False
    return flag

def update_re_iterate_to_False(json_file):
    with open(json_file, 'r') as file:
        metadata = json.load(file)
    metadata['re_iterate'] = False
    with open(json_file, 'w') as file:
        json.dump(metadata, file, indent=4)
    print(f"Updated 're_iterate' to False in {json_file}.")

def asr_server():
    host = 'localhost'
    port = 5001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print('ASR Server is Ready...')

    while True:

        for file in os.listdir('/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio'):

            if file.endswith('.webm'):
                full_file_path_webm = os.path.join('/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio', file)
                full_file_path_wav = os.path.join('/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio', 'new_audio_format.wav')
                convert_webm_to_wav_and_delete(full_file_path_webm,full_file_path_wav)

                for file in os.listdir('/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio'):
                    if file.endswith('.wav'):
                        make_metadata()
                        if check_re_iterate('/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio/metadata.json'):
                            full_file_path = os.path.join('/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio', file)
                            file_rename(full_file_path)
                            print('File Renamed')
                            audio_process()
                            print('Audio Processed')
                            text = infer()
                            print('Infer Ran.')
                            # Send the transcribed text to LLM server
                            llm_host = 'localhost'
                            llm_port = 5002
                            llm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            llm_socket.connect((llm_host, llm_port))
                            llm_socket.sendall(text[0].encode())
                            llm_socket.close()
                            update_re_iterate_to_False('/Users/aditya.narayan/Desktop/s_To_s/indic-asr/raw_audio/metadata.json')
        


if __name__ == "__main__":
    asr_server()

