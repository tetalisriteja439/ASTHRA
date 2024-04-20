import time
import pyttsx3

import os



def check_start_text(file_path, max_retries=3, retry_delay=1):
    retries = 0
    while retries < max_retries:
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if 'Start' in line:
                        return True
            return False
        except FileNotFoundError:
            print("File not found. Retrying...")
            retries += 1
            time.sleep(retry_delay)
    
    print(f"File '{file_path}' not found after {max_retries} retries.")
    return False

        
    
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")



counter = 0
import requests

def Deegram_voice(content, voice_inp):
    #
    global counter 
    
    counter = counter + 1
    i = counter
    voice_inp = int(voice_inp)
    if  voice_inp == 1:
        voice = "arcas"
    else:
        voice = "stella"

    url = f"https://api.deepgram.com/v1/speak?model=aura-{voice}-en"

    # Set your Deepgram API key
    api_key = ""

    # Define the headers
    headers = {
      "Authorization": f"Token {api_key}",
      "Content-Type": "application/json"
    }

    # Define the payload
    payload = {
      "text": content
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        #
        path = ".\AudioTemp\\"
        file_name = str(i)
        extension = ".mp3"
        full_file_path = path + file_name + extension
        
        with open(full_file_path, "wb") as f:
            f.write(response.content)
            print("File saved successfully.")
    else:
      print(f"Error: {response.status_code} - {response.text}")
    
    
    
import pygame
import time
import os


def delete_file(file_path):
    file_path = r".\Communication\communication.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
        return True
    else:
        print(f"File '{file_path}' does not exist.")
        return False

def wait_for_file(timeout=None, polling_interval=1):
    file_path = r".\Communication\communication.txt"
    start_time = time.time()

    while True:
        if os.path.exists(file_path):
            print(f"File '{file_path}' found!")
            return True

        if timeout is not None and time.time() - start_time > timeout:
            print("Timeout reached. File not found.")
            return False

        time.sleep(polling_interval)
        
    
import re

def conversation_list(conversation_text):
    pattern = r'(?P<speaker>Host|Guest): (?P<text>.*)'

    host = []
    guest = []

    matches = re.findall(pattern, conversation_text)
    for speaker, text in matches:
        if speaker == 'Host':
            host.append(text.strip())
        elif speaker == 'Guest':
            guest.append(text.strip())

    return host, guest


def voice_conversation(text):
    host, guest = conversation_list(text)
    try:
        hos_len = len(host)
        gue_len = len(guest)

        max_hg = max(hos_len, gue_len)
        
        for i in range(max_hg):
            print(i)
            print(f"*********************CONVERSATION {i}********************************")
            Host_message = host[i]
            Guest_message = guest[i]
            
            Deegram_voice(Host_message,1)
            Deegram_voice(Guest_message,2)

    except Exception as e:
        print(e)
#-------------------------------------------------------------------------------------------------------

def read_message():
    with open(r".\Communication\communication.txt", "r") as file:
        message = file.read()
    return message

if __name__ == "__main__":
    folder_path = r".\AudioTemp"
    create_folder_if_not_exists(folder_path)
    folder_path_communication = r".\Communication"
    create_folder_if_not_exists(folder_path_communication)
    
    delete_file(folder_path_communication)
    try:
        #
        while True:
            wait_for_file()
            # Read message from the file
            message = read_message()
            file_path_operate = r".\Communication\operate.txt"
            check_start_text(file_path_operate)

            # Check if there's a message
            if message:
                print("Received message:", message)
                voice_conversation(message)

                open("communication.txt", "w").close()
                delete_file(folder_path_communication)
            else:
                print("Waiting for message...")
            
    except Exception as e:
        #
        print(e)
            
            
            
            