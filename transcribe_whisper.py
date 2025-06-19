import subprocess
import whisper
import os
import time

def transcribe_to_tsv(audio_path):
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
    print(f"Finished transcription in {transcription_end - transcription_start:.2f} seconds. Writing to tsv...")

    # Write to TSV
    writing_start = time.time()

    tsv_file = os.path.splitext(audio_path)[0] + ".tsv"
    with open(tsv_file, "w", encoding="utf-8") as f:
        f.write("start\tend\ttext\n")
        for segment in result['segments']:
            f.write(f"{segment['start']}\t{segment['end']}\t{segment['text']}\n")
    
    writing_end = time.time()

    print(f"TSV saved to: {tsv_file} after {writing_end - writing_start:.2f} seconds.")
    return tsv_file

# def transcribe_to_tsv(audio_path):
#     # Ensure the file exists
#     if not os.path.isfile(audio_path):
#         raise FileNotFoundError(f"No such file: {audio_path}")

#     # Get the directory and filename (no extension)
#     dir_path = os.path.dirname(audio_path)
#     base_name = os.path.splitext(os.path.basename(audio_path))[0]
#     tsv_file = os.path.join(dir_path, f"{base_name}.tsv")

#     # Run Whisper with only TSV output
#     subprocess.run([
#         "python", "-m", "whisper",
#         audio_path,
#         "--model", "turbo",
#         "--language", "English",
#         "--output_format", "tsv"
#     ], check=True)

#     # Clean up other output formats
#     extensions_to_delete = [".txt", ".json", ".srt", ".vtt"]
#     for ext in extensions_to_delete:
#         file_to_remove = os.path.join(dir_path, f"{base_name}{ext}")
#         if os.path.exists(file_to_remove):
#             os.remove(file_to_remove)

#     print(f"TSV file saved at: {tsv_file}")
#     return tsv_file

# Example usage
if __name__ == "__main__":
    audio_files = [r"C:\Users\jinfa\Desktop\CONYCE\SP19\conyce_bh_sp19_FrancescaCimieri_all_interview_mod_061925.wav",
                   r"C:\Users\jinfa\Desktop\CONYCE\SP19\conyce_bh_sp19_JennieCastillo_all_interview_mod_061925.wav",
                   r"C:\Users\jinfa\Desktop\CONYCE\SP19\conyce_bh_sp19_JimmyCandy_all_interview_mod_061925.wav",
                   r"C:\Users\jinfa\Desktop\CONYCE\SP19\conyce_bh_sp19_MickeyGarplume_all_interview_mod_061925.wav",
                   r"C:\Users\jinfa\Desktop\CONYCE\SP19\conyce_bh_sp19_PandaBear_all_interview_mod_061925.wav",
                   r"C:\Users\jinfa\Desktop\CONYCE\SP19\conyce_bh_sp19_VivianSmith_all_interview_mod_061925.wav",]
    for audio_file in audio_files:
        transcribe_to_tsv(audio_file)