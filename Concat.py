import os
import subprocess

""" This code merges mp3 files in each folder into one file,
     with a duration gap between the separating files.
     The output audio then is placed in the folder corresponding to it.
     Note: the base input folder has many child folders containing separating .mp3 files.
"""

# FFMPEG_PATH = r"C:\Program Files\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"
BASE_OUTPUT_DIR = "output"
SILENT_FILE = "silent.mp3"
GAP_DURATION = 7  # Silence between each audio

"""if not os.path.exists(FFMPEG_PATH):
    print(f"❌ FFmpeg not found in {FFMPEG_PATH}!")
    exit()
"""

if not os.path.exists(BASE_OUTPUT_DIR):
    print(f"❌ Folder '{BASE_OUTPUT_DIR}' does not exist!")
    exit()

# Create silence audio
print(f"🛠️ Creating silence audio ({GAP_DURATION} sec)...")
try:
    subprocess.run([
        FFMPEG_PATH, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
        "-t", str(GAP_DURATION), SILENT_FILE, "-y"
    ], check=True)
except subprocess.CalledProcessError as e:
    print(f"❌ Error when making silence audio : {e}")
    exit()

# Traverse folder
for folder_name in os.listdir(BASE_OUTPUT_DIR):
    folder_path = os.path.join(BASE_OUTPUT_DIR, folder_name)
    if not os.path.isdir(folder_path):
        continue

    audio_files = sorted(
    [f for f in os.listdir(folder_path) if f.endswith(".mp3") and f.startswith("audio_")],
    key=lambda x: int(x.split("_")[1].split(".")[0])
)

    
    if not audio_files:
        print(f"⚠️ Ignore {folder_name}, no file .mp3")
        continue

    concat_file = os.path.join(folder_path, "concat_list.txt")
    output_file = os.path.join(folder_path, f"{folder_name}_full.mp3")

    print(f"📋 Solving: {folder_name} ({len(audio_files)} )...")

    # write file to concat_list.txt
    with open(concat_file, "w", encoding="utf-8") as f:
        for file in audio_files:
            file_path = os.path.abspath(os.path.join(folder_path, file)).replace("\\", "/")
            silent_path = os.path.abspath(SILENT_FILE).replace("\\", "/")
            f.write(f"file '{file_path}'\n")
            f.write(f"file '{silent_path}'\n")

    try:
        subprocess.run([
            FFMPEG_PATH, "-f", "concat", "-safe", "0",
            "-i", concat_file, "-c", "copy", output_file, "-y"
        ], check=True)
        print(f"✅ Created: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error {folder_name}: {e}")

    if os.path.exists(concat_file):
        os.remove(concat_file)

if os.path.exists(SILENT_FILE):
    os.remove(SILENT_FILE)

print("🎉 Done all folders !")
