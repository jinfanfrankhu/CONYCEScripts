import whisper
import os
import time

def transcribe(audio_path):
    # Ensure the file exists
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"No such file: {audio_path}")
    
    print(f"Transcribing {audio_path}...")

    # Load model (this will download once and cache locally)
    model = whisper.load_model("turbo")  # or "base", "tiny", whatever you want

    print("Loaded turbo model.")

    # Transcribe
    transcription_start = time.time()
    result = model.transcribe(audio_path, language="English", task="transcribe")
    transcription_end = time.time()
    print(f"Finished transcription in {transcription_end - transcription_start:.2f} seconds. Writing outputs...")

    # Write TSV file
    tsv_file = os.path.splitext(audio_path)[0] + ".tsv"
    with open(tsv_file, "w", encoding="utf-8") as f:
        f.write("start\tend\ttext\n")
        for segment in result['segments']:
            f.write(f"{segment['start']}\t{segment['end']}\t{segment['text']}\n")

    # Write plain TXT file for MFA
    txt_file = os.path.splitext(audio_path)[0] + ".txt"
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(result['text'])

    print(f"TSV saved to: {tsv_file}")
    print(f"TXT saved to: {txt_file}")
    
    return tsv_file, txt_file

# Example usage
if __name__ == "__main__":
    audio_files = [r"C:\Users\jinfa\Desktop\CONYCE\TestAaravDengla\conyce_bh_sp19_AaravDengla_all_interview_mod_050825.wav"]
    for audio_file in audio_files:
        transcribe(audio_file)
