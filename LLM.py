
import base64
import json
import requests
import time

import os

import time


import nest_asyncio
from llama_parse import LlamaParse

def Research_paper():
    nest_asyncio.apply()
    #
    parser = LlamaParse(
        api_key="",  # can also be set in your env as LLAMA_CLOUD_API_KEY
        result_type="markdown"  # "markdown" and "text" are available
    )
    file_path_docs = r"D:\Akhil_Main_LLM_Code\Akhil_Main_LLM_Code\ASRAG\pages\RAG\paper.pdf"
    documents = parser.load_data(file_path_docs)

    sections_list = {}

    for para in documents[0].text.split('##'):
        section = para[:para.find('\n')].strip()
        if section.lower() != 'references':
            # print(section)
            # doc = Document(text=para, metadata={"file_name": title, "paper_name": title, "section": section})
            sections_list[section]=para


    values_list = list(sections_list.values())
    keys_list = list(sections_list.keys())

    paper_title = keys_list[1]

    paper_section_title_list = []
    paper_section_text_list = []

    for i in range(len(sections_list)):
        if i > 2:
            paper_section_title = keys_list[i]
            paper_section_title_list.append(paper_section_title)

            paper_section_text = values_list[i]
            paper_section_text_list.append(paper_section_text)

    def count_words(text):
        return len(text.split())

    text_list = [item for item in paper_section_text_list if count_words(item) >= 50]
    return text_list, paper_title
#-------------------------------------------------------------------------------------------------------

def check_start_text(file_path):
    retries = 0
    while True:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    if 'Start' in file.read():
                        print("The word 'Start' is found in the file.")
                        return True
                    else:
                        print("The word 'Start' is not found in the file.")
                        return False
            except FileNotFoundError:
                retries += 1
                print(f"File '{file_path}' not found. Retry {retries}. Waiting...")
                time.sleep(1)  # Wait for 10 seconds before checking again
        else:
            retries += 1
            print(f"File '{file_path}' not found. Retry {retries}. Waiting...")
            time.sleep(1)  # Wait for 10 seconds before checking again


# # Example usage:
# file_path = 'operate.txt'
# exists = check_start_text(file_path)
# print("Text 'Start' exists in the file:", exists)


def create_file(file_name, content=""):
    try:
        with open(file_name, "w") as file:
            file.write(content)
            print(file)
        print(f"File '{file_name}' created successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")




def create_text_file(message):
    file_path = r".\Communication\communication.txt"
    # Check if the file already exists
    #file_path_operate = r"C:\Users\akhil\Downloads\Communication\operate.txt"
    
    while os.path.exists(file_path):
        print(f"Waiting for file {file_path} to be deleted...")
        time.sleep(0.5)  # Wait for 1 second

    # Create a new text file
    with open(file_path, 'w') as file:
        file.write(message)

    print(f"Created new file: {file_path}")
    
    
# Function to write a message to the file
def write_message(message):
    with open(r".\Communication\communication.txt", "w") as file:
        file.write(message)

messages = []

def O_LLM_(query):
    #
    # tk_count = token_count(query)
    # print("Query Token Count: ",tk_count)
    data = {
    "model": "mistral",
    "prompt": query,
    "stream": False}
    response = requests.post("http://localhost:11434/api/generate", data=json.dumps(data))
    data = json.loads(response.text)
    answer = data['response']
    print(answer)
    return answer

message_history = []

from openai import OpenAI

def O_LLM(query):
    
    client = OpenAI(api_key='')
    messages = [{"role": "user","content": query}]
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",messages=messages, temperature = 1)
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

research_context = """
We study the effectiveness of a simple approach to develop a small base language model (LM) starting from an existing large base LM: first inherit a few transformer blocks from the larger LM, and then train this smaller model on a very small subset (0.1%) of the raw pretraining data of the larger model. We call our simple recipe Inheritune and first demonstrate it for building a small base LM with 1.5B parameters using 1B tokens (and a starting few layers of larger LM of 3B parameters); we do this using a single A6000 GPU for less than half a day. Across 9 diverse evaluation datasets as well as the MMLU benchmark, the resulting model compares favorably to publicly available base models of 1B-2B size, some of which have been trained using 50-1000 times more tokens. We investigate Inheritune in a slightly different setting where we train small LMs utilizing larger LMs and their full pre-training dataset. Here we show that smaller LMs trained utilizing some of the layers of GPT2- medium (355M) and GPT-2-large (770M) can effectively match the val loss of their bigger counterparts when trained from scratch for the same number of training steps on OpenWebText dataset with 9B tokens. We analyze Inheritune with extensive experiments and demonstrate it efficacy on diverse settings. Our code is available a
"""


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

# Main function
def main():
    summary_his = "No history, you just started the conversatation."
    research_context_list, paper_title = Research_paper()
    research_context = research_context_list[0]
    for i in range(15):
        
        
        Speaker = f"""
Consider yourself a podcaster (Mark) and guest (Leslie) and write a small conversation between them regarding the research paper Mark found. 
Give me the output as 'Guest:' and 'Host:' Make Host slightly critique and always ask questions to the Guest about whether this works.
Research Paper Title: {paper_title}.
Research Paper: {research_context}.

Always start with the host and end with the guest. You can add interruptions like sudden stop and next person talking, between host and guest like arguing. Dont write Interrupting at guet or host response.
Add filler words like, Ummm, Ahhhh, Yeeeah, I believe, I think, oh!, etc.
"""
        research_context_list, paper_title = Research_paper()
        research_context = research_context_list[1]
        exists = check_start_text(r'.\Communication\operate.txt')
        print("Exists FIle: ", exists)
        if exists:
            #
            print(f"*********ITERATION 0{i}**********")
            print("--------------------------------START------------------------------------------------------------------")
            print("LLM Send data")
            history = ' '.join(message_history)
            Prompt = f" {Speaker} \n\n History: {summary_his} \n\n continue this conversatation and Give me 3 dialouges between them."
            print("Full Prompt is ",Prompt)
            print("\n\n Model Answer:\n")
            message = O_LLM(Prompt)
            message = message.replace('*', '')
            print(message)
            message_history.append(message)
            messages.append(message)
            print("\n")
            create_text_file(message)
            print("History: ",history)
            summary_history = f"write a small and consize summary in paragraph, for this chat history with Host and Guest: {message}"
            summary_his = O_LLM(summary_history)
            print("*_*_*_*_*__*_*_*SUMMARY OF THE CHAT HISTORY_*_*_*_*_*_*_*_*_*_*_*_")
            print(summary_his)
            print("_+_+_+_+_+_+_+_+Summary Completed_+_+_+_+_+_+_+__+_")
            host, guest = conversation_list(message)
            last_host = host[-1]
            last_guest = guest[-1]
            summary_his = f" {summary_his}  last conversation between Host and Guest. \n Host: {last_host} \n Guest: {last_guest} \n Continue this conversation and add interruptions in between."
            print("Here is the chat summary: ", summary_his)
            print("Message sent.")
            print("_____________________________________________________________________________________")
            print("\n \n")
        else:
            break
        
        
if __name__ == "__main__":
    main()
#     create_text_file("HELLO")
        
