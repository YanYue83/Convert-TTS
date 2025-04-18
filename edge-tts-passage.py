import os
import asyncio
import edge_tts
from docx import Document

""" This code reads input docx file and converts all to audio. 
Note: the voice will read the doc with title and paragraph by paragraph, instead of reading continuously without pause. 
"""

INPUT_DIR = "input"
BASE_OUTPUT_DIR = "final"
VOICE = "en-US-AriaNeural"

os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

def extract_bold_sections(doc):
    sections = []
    current_title = None
    current_text = []

    for para in doc.paragraphs:
        if not para.text.strip():
            continue

        has_bold = any(run.bold for run in para.runs if run.text.strip())

        if has_bold:
            if current_title and current_text:
                sections.append((current_title, " ".join(current_text)))
            current_title = para.text.strip()
            current_text = []
        else:
            current_text.append(para.text.strip())

    if current_title and current_text:
        sections.append((current_title, " ".join(current_text)))

    return sections

async def text_to_speech(text, output_file):
    communicate = edge_tts.Communicate(text=text, voice=VOICE)
    await communicate.save(output_file)
    print(f"🎧 Created: {output_file}")

async def main():
    for file_name in os.listdir(INPUT_DIR):
        if file_name.endswith(".docx"):
            file_path = os.path.join(INPUT_DIR, file_name)
            doc = Document(file_path)
            sections = extract_bold_sections(doc)

            base_name = os.path.splitext(file_name)[0]  

            for idx, (title, content) in enumerate(sections):
                merged_text = f"{title}. {content}"
                output_file_name = f"{base_name}_{idx}.mp3"
                output_path = os.path.join(BASE_OUTPUT_DIR, output_file_name)
                await text_to_speech(merged_text, output_path)

    print("🎉 Done all file!")

if __name__ == "__main__":
    asyncio.run(main())
