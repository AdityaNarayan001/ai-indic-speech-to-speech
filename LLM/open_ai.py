import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from blessed import Terminal
term = Terminal()
load_dotenv()
import socket

def llm_inference(PROMPT):
    client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OAI_BASE_URL"),
                api_version=os.getenv("AZURE_OAI_API_VERSION"),
                api_key=os.getenv("AZURE_OAI_API_KEY")
            )
    deployment_name=os.getenv("AZURE_GPT_DEPLOYMENT_NAME") 


    print(term.bold_black_on_white('🛠️ Fetching Result :'))

    PRE_SET_PROMPT = "Talk to me in Kannada. "

    response = client.chat.completions.create(
        model=deployment_name, 
        messages=[
            {
                "role": "user", 
            "content": PRE_SET_PROMPT + PROMPT
            }
            ], 
        max_tokens=100,
        stream=False
        )

    result = response.choices[0].message.content
    print(term.bold_blue(result))
    return result

def llm_server():
    host = 'localhost'
    port = 5002

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print('LLM Server is listening...')

    while True:
        conn, addr = server_socket.accept()
        print(f'Connected by {addr}') 

        text_data = conn.recv(65536).decode()
        print('Received text data from ASR:', text_data)

        response_text = llm_inference(text_data)
        print("Response Generated from LLM")
        
        # Send the generated response text to TTS server
        tts_host = 'localhost'
        tts_port = 5003
        tts_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tts_socket.connect((tts_host, tts_port))
        tts_socket.sendall(response_text.encode())
        tts_socket.close()
        
        conn.close()


if __name__ == "__main__":
    llm_server()