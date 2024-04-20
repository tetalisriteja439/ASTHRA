import streamlit as st
import pygame
from pygame import mixer
import os
import time
import shutil

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been successfully deleted.")
    except OSError as e:
        print(f"Error: {folder_path} : {e.strerror}")

# Example usage:

delete_folder("D:/Akhil_Main_LLM_Code/Akhil_Main_LLM_Code/AudioTemp")
delete_folder("D:/Akhil_Main_LLM_Code/Akhil_Main_LLM_Code/Communication")


# Initialize Pygame mixer
pygame.init()
pygame.mixer.init()

# Global variables to keep track of the currently playing audio and index
current_sound = None

# Define podcast data
podcasts = [
    {
    "title": "The Societal and Transformational Impacts of Data Science",
    "description": "Companies have understood the wonders that can be done with data, and with the Harvard Business Review describing Data Scientist as the Sexiest Job of the 21st Century, Data science is now more than a buzzword. This paper discusses the various stages by which data science is implemented and describes some interesting business case studies on how large organizations like Apple, Facebook, Google, Tesla, Virgin Hyperloop, Netflix, and many more have benefited from Data Science. ",
    "audio_file": "1.mp3",
    "image_url": "image2.jpg"
},
{
    "title": "A Comparative Study of Various Data Visualization Techniques using COVID-19 Data",
    "description": "To apply various data visualization techniques on COVID-19 datasets that help to get insights, make accurate decisions, find trends and patterns, and present valuable information. Methods: The following data visualization techniques, i.e., Bar graph, Box plot, Bubble chart, Choropleth map, Density plot, Heat map, Histogram, Line graph, Network analysis, Parallel coordinates, Pie chart, Scatter plot, Scatter plot matrices, Timeline chart, Time series plot, Tree map, Violin plot, Word cloud are used on various Covid-19 datasets taken from Kaggle. Findings: Analyzing vast volumes of data is a tedious task and practically impossible, and hence data visualization is needed to make those datasets meaningful.",
    "audio_file": "2.mp3",
    "image_url": "image3.jpg"
},
{
    "title": "MoAI: Mixture of All Intelligence for Large Language and Vision Models",
    "description": "The rise of large language models (LLMs) and instruction tuning has led to the current trend of instruction-tuned large language and vision models (LLVMs). This trend involves either meticulously curating numerous instruction tuning datasets tailored to specific objectives or enlarging LLVMs to manage vast amounts of vision language (VL) data. However, current LLVMs have disregarded the detailed and comprehensive real-world scene understanding available from specialized computer vision (CV) models in visual perception tasks such as segmentation, detection, scene graph generation (SGG), and optical character recognition (OCR). Instead, the existing LLVMs rely mainly on the large capacity and emergent capabilities of their LLM backbones.",
    "audio_file": "3.mp3",
    "image_url": "image4.jpg"
},
{
    "title": "Large Language Models: A Survey",
    "description": "Large Language Models (LLMs) have drawn a lot of attention due to their strong performance on a wide range of natural language tasks, since the release of ChatGPT in November 2022. LLMs' ability of general-purpose language understanding and generation is acquired by training billions of model's parameters on massive amounts of text data, as predicted by scaling laws \cite{kaplan2020scaling,hoffmann2022training}. The research area of LLMs, while very recent, is evolving rapidly in many different ways.",
    "audio_file": "4.mp3",
    "image_url": "image5.jpg"
}
]

# Function to play or stop audio based on podcast index
def audio_start(index):
    global current_sound
    if current_sound is not None:
        current_sound.stop()  # Stop currently playing sound if any

    audio_file = podcasts[index]["audio_file"]
    current_sound = pygame.mixer.Sound(audio_file)
    current_sound.play()

# Function to stop currently playing audio
def audio_stop():
    global current_sound
    if current_sound is not None:
        current_sound.stop()
        current_sound = None    

def create_text_file(message):
    file_path = "D:/Akhil_Main_LLM_Code/Akhil_Main_LLM_Code/Communication/operate.txt"
    while os.path.exists(file_path):
        print(f"Waiting for file {file_path} to be deleted...")
        time.sleep(0.5)  # Wait for 1 second

    # Create a new text file
    with open(file_path, 'w') as file:
        file.write(message)

    print(f"Created new file: {file_path}")

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")


# Main Streamlit app
def upload():
    import sys
    sys.path.append(r"D:/Akhil_Main_LLM_Code/Akhil_Main_LLM_Code/ASRAG/pages/RAG")
    create_folder_if_not_exists("D:/Akhil_Main_LLM_Code/Akhil_Main_LLM_Code/AudioTemp")
    from RAG import RAG
    with st.status("Uploading the Research Paper...",expanded=False) as status:
        st.write("Uploading the Research Paper")
        time.sleep(1)
        st.write("Creating chunks...")
        status.update(label="Creating Chunks!")
        RAG()
        create_folder_if_not_exists("D:/Akhil_Main_LLM_Code/Akhil_Main_LLM_Code/Communication")
        create_text_file("Start")
        st.write("Redirecting to the Chat Window...")
        status.update(label="Redirecting to the Chat Window...")
        time.sleep(1)
    print("Done")
    app4_path = os.path.join(os.path.dirname(__file__), "pages/Chat.py")
    st.switch_page(app4_path)

def layout():
    st.set_page_config(
    page_title="ASHTRA Podcast",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    )

    st.title("Podcast Player")
    st.sidebar.markdown("# Upload your Research Paper")
    file=st.sidebar.file_uploader("")
    if file:
        # print(str(file.name))
        # with open("./db/file_location.txt", "w") as f:
        #     f.write(str(file))
        with open('./pages/RAG/paper.pdf', 'wb') as f:
            f.write(file.getvalue())
        upload()
    # Display podcasts in rows with 2 cards per row
    for i in range(0, len(podcasts), 2):
        row_podcasts = podcasts[i:i+2]

        # Create a row for each set of 2 podcasts
        col1, col3, col2 = st.columns([6, 1, 6])#st.columns(3)

        for col, podcast in zip([col1, col2], row_podcasts):
            with col:
                st.image(podcast['image_url'], use_column_width=True)
                #st.image(podcast['image_url'], use_column_width=True, output_format='JPG', width=500, style={'border-radius': '10px'})
                #st.markdown(f'<img src="{podcast["image_url"]}" style="border-radius: 10px;" />',unsafe_allow_html=True)
                #st.markdown(f'<img src="{podcast["image_url"]}" style="border-radius: 10px; max-width: 100%;" />', unsafe_allow_html=True)   
                st.write(f"**{podcast['title']}**")
                st.write(podcast['description'])
                # Play button
                if st.button("Play", key=f"play_{podcast['title']}"):
                    index = podcasts.index(podcast)
                    audio_start(index)
                # Stop button (only show if audio is playing)
                if st.button("Stop", key=f"stop_{podcast['title']}"):
                    audio_stop()
        st.write("---")
if __name__ == "__main__":
    print(current_sound)
    layout()