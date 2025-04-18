# 🎙️ TTS - Audio Generator

This toolkit helps you:
- 📄 Read `.docx` files and convert their contents to speech using Microsoft Edge TTS.
- 🔊 Export audio either **sentence-by-sentence** or **by full paragraph sections**.
- 🔗 Concatenate multiple audio files into a single track with configurable silence between parts.

---

## 🗂 Overview

### 1. `edge-tts-sentence.py` – Convert each sentence in `.docx` to a separate audio file
- 📥 **Input folder:** `input/` (contains your `.docx` files).
- 📤 **Output folder:** `output/`, where each sentence in one .docx will be converted into an individual `.mp3` file and put into the corresponding folder.
- 📌 Ideal for situations where you want to rearrange or reuse sentences flexibly.

---

### 2. `edge-tts-passage.py` – Convert each bolded section and paragraph into one audio
- 📥 **Input folder:** `input`, containing `.docx` files.
- 🧾 The script identifies bolded titles and groups the text beneath them as one section.
- 📤 **Output folder:** `final/`, where each `.docx` will produce a single audio file named after the document.
- 🎧 Each output file reads the title followed by its corresponding paragraph.

---

### 3. `concat.py` – Merge multiple `.mp3` files into one, with silence between
- 🔍 Searches through each subfolder of `output/` and looks for files named `audio_*.mp3`.
- 🕐 Adds a silent gap (configurable via `GAP_DURATION`) between audio files using `silent.mp3`.
- ⚙️ Requires **FFmpeg** installed and configured in the `FFMPEG_PATH`.

---

## 🧪 Installation

```bash
pip install edge-tts python-docx
