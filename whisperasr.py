import subprocess
import os

def transcribe_to_tsv(audio_path):
    # Ensure the file exists
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"No such file: {audio_path}")

    # Get the directory and filename (no extension)
    dir_path = os.path.dirname(audio_path)
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    tsv_file = os.path.join(dir_path, f"{base_name}.tsv")

    # Run Whisper with only TSV output
    subprocess.run([
        "python", "-m", "whisper",
        audio_path,
        "--model", "turbo",
        "--language", "zh",
        "--output_format", "tsv"
    ], check=True)

    # Clean up other output formats
    extensions_to_delete = [".txt", ".json", ".srt", ".vtt"]
    for ext in extensions_to_delete:
        file_to_remove = os.path.join(dir_path, f"{base_name}{ext}")
        if os.path.exists(file_to_remove):
            os.remove(file_to_remove)

    print(f"TSV file saved at: {tsv_file}")
    return tsv_file

# Example usage
if __name__ == "__main__":
    audio_file = r"C:\Users\jinfa\Desktop\CONYCE\Wuhanese\嫁嫁.wav"
    transcribe_to_tsv(audio_file)
