import os
import time
import asyncio
import edge_tts
from docx import Document

"""This code reads each input docx file, separates the sentences and converts each sentence into audio. 
    The audio sentences in the same input docx file will be placed into the same corresponding output folder.
    Note: Input_dir is folder containing many docx files.
"""
INPUT_DIR = "input"
BASE_OUTPUT_DIR = "output"
VOICE = "en-US-GuyNeural"  # Choose your voice en-US-GuyNeural (male-US), en-US-JennyNeural (female US)


# Create a base folder that contains all your voice output
os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

def read_docx(file_path):
    doc = Document(file_path)
    return [para.text.strip() for para in doc.paragraphs if para.text.strip()]

async def text_to_speech(text, output_file):
    communicate = edge_tts.Communicate(text=text, voice=VOICE)
    await communicate.save(output_file)
    print(f"✅ Created: {output_file}")


# read each line in .docx in folder input, convert them to audio and export under separating audio files.
async def main():
    for file_name in os.listdir(INPUT_DIR):
        if file_name.endswith(".docx"):
            file_path = os.path.join(INPUT_DIR, file_name)
            lines = read_docx(file_path)

            base_name = os.path.splitext(file_name)[0]
            output_folder = os.path.join(BASE_OUTPUT_DIR, f"output_{base_name}")
            os.makedirs(output_folder, exist_ok=True)

            for i, line in enumerate(lines):
                output_path = os.path.join(output_folder, f"audio_{i}.mp3")
                await text_to_speech(line, output_path)
                # time.sleep(1)  

    print("🎉 All audio created!")

if __name__ == "__main__":
    asyncio.run(main())
