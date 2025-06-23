import whisper
import os
import time
import string
import subprocess

# ---------- CONFIG ----------
MODEL_NAME = "turbo"  # or "base", "tiny" depending on your hardware
MFA_DICTIONARY = "english_us_mfa"
MFA_ACOUSTIC_MODEL = "english_us_mfa"

# ---------- FUNCTIONS ----------
def transcribe(audio_path):
    model = whisper.load_model(MODEL_NAME)
    result = model.transcribe(audio_path, language="English", task="transcribe")

    base = os.path.splitext(audio_path)[0]
    tsv_file = base + ".tsv"
    txt_file = base + ".txt"

    with open(tsv_file, "w", encoding="utf-8") as f:
        f.write("start\tend\ttext\n")
        for segment in result['segments']:
            f.write(f"{segment['start']}\t{segment['end']}\t{segment['text']}\n")

    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(result['text'])

    return txt_file

def clean_txt(txt_file):
    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    punctuation_to_remove = string.punctuation.replace("?", "")
    translator = str.maketrans('', '', punctuation_to_remove)
    cleaned_text = text.translate(translator).lower()
    cleaned_text = ' '.join(cleaned_text.split())

    processed_file = txt_file.replace(".txt", "_processed.txt")
    with open(processed_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    return processed_file

def batch_pipeline(folder):
    audio_files = [f for f in os.listdir(folder) if f.endswith(".wav")]
    
    for audio_file in audio_files:
        full_audio_path = os.path.join(folder, audio_file)
        print(f"Processing: {audio_file}")

        txt_file = transcribe(full_audio_path)
        processed_txt_file = clean_txt(txt_file)

        # Rename processed file to match audio name for MFA
        target_txt_file = full_audio_path.replace(".wav", ".txt")
        os.rename(processed_txt_file, target_txt_file)
        print(f"Prepared cleaned file for MFA: {target_txt_file}")

    print("All files transcribed and cleaned. Starting MFA alignment...")

    output_path = os.path.join(folder, "MFA_output")
    os.makedirs(output_path, exist_ok=True)

    subprocess.run([
        "mfa", "align",
        folder, MFA_DICTIONARY, MFA_ACOUSTIC_MODEL, output_path
    ], check=True)

    print(f"Alignment complete. Aligned TextGrids saved to: {output_path}")

# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    folder = r"C:\Users\jinfa\Desktop\CONYCE\SP19\YourInputFolderHere"  # <-- change this path
    batch_pipeline(folder)
