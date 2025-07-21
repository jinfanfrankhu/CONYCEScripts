import whisper
import os
import time
import string
import subprocess
import shutil

# ---------- CONFIG ----------
MODEL_NAME = "turbo"  # or "base", "tiny" depending on your hardware
MFA_DICTIONARY = "english_us_mfa"
MFA_ACOUSTIC_MODEL = "english_mfa"

# ---------- TRANSCRIPTION ----------
def transcribe_audio(audio_path, verbosity=0):
    if verbosity == 1:
        print(f"Transcribing {audio_path} with model {MODEL_NAME}...")
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
    if verbosity == 1:
        print(f"Transcription complete. Output saved to {txt_file}")
    return txt_file

# ---------- CLEANING ----------
def clean_transcript(txt_file, verbosity=0):
    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    punctuation_to_remove = string.punctuation.replace("?", "").replace("'", "")
    translator = str.maketrans('', '', punctuation_to_remove)
    cleaned_text = text.translate(translator).lower()
    cleaned_text = ' '.join(cleaned_text.split())

    processed_file = txt_file.replace(".txt", "_processed.txt")
    with open(processed_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    if verbosity == 1:
        print(f"Cleaned transcript saved to {processed_file}")
    return processed_file

# ---------- MFA PREPARATION ----------
def prepare_for_mfa(audio_path, processed_txt_file, verbosity=0):
    target_txt_file = audio_path.replace(".wav", ".txt")
    if os.path.abspath(processed_txt_file) != os.path.abspath(target_txt_file):
        if os.path.exists(target_txt_file):
            os.remove(target_txt_file)
        shutil.move(processed_txt_file, target_txt_file)
    if verbosity == 1:
        print(f"Prepared {target_txt_file} for MFA")

# ---------- MFA ALIGNMENT ----------
def run_mfa(folder, verbosity=0):
    output_path = os.path.join(folder, "MFA_output")
    os.makedirs(output_path, exist_ok=True)

    if verbosity == 1:
        subprocess.run([
            "C:\\Users\\jinfa\\Desktop\\CONYCE\\Python Code\\verbosemfa.bat",
            folder, MFA_DICTIONARY, MFA_ACOUSTIC_MODEL, output_path
        ], check=True)
        print(f"Alignment complete. TextGrids saved to: {output_path}")

    else:
        subprocess.run([
            "C:\\Users\\jinfa\\Desktop\\CONYCE\\Python Code\\quietmfa.bat",
            folder, MFA_DICTIONARY, MFA_ACOUSTIC_MODEL, output_path
        ], check=True)
        print(f"Alignment complete. TextGrids saved to: {output_path}")

# ---------- PIPELINE ORCHESTRATOR ----------
def batch_pipeline(folder, verbosity=0):
    audio_files = [f for f in os.listdir(folder) if f.endswith(".wav")]
    
    for audio_file in audio_files:
        full_audio_path = os.path.join(folder, audio_file)

        txt_file = transcribe_audio(full_audio_path, verbosity)
        processed_txt_file = clean_transcript(txt_file, verbosity)
        prepare_for_mfa(full_audio_path, processed_txt_file, verbosity)

    print("All files transcribed and cleaned. Starting MFA alignment...")
    run_mfa(folder, verbosity)

# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    folder = r"C:\Users\jinfa\Desktop\CONYCE\Wuhanese"  
    #batch_pipeline(folder, verbosity=1)

    run_mfa(folder, verbosity=1)


