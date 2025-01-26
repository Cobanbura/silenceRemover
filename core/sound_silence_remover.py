from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os

data_folder = '../data'
wav_files = [file for file in os.listdir(data_folder) if file.endswith(".wav")]

print("Available WAV files:")
for idx, file_name in enumerate(wav_files, start=1):
    print(f"{idx}: {file_name}")

selected_file = None
while selected_file is None:
    try:
        user_input = input("Enter the number of the WAV file you want to process: ")
        file_index = int(user_input) - 1
        if 0 <= file_index < len(wav_files):
            selected_file = os.path.join(data_folder, wav_files[file_index])
        else:
            print(f"Invalid number. Please select a number between 1 and {len(wav_files)}.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

audio = AudioSegment.from_file(selected_file, format="wav")

min_silence_len = 500
silence_thresh = -35
padding = 350

nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

padded_ranges = [
    (max(start - padding, 0), min(end + padding, len(audio)))
    for start, end in nonsilent_ranges
]

print(f"Original nonsilent sections: {nonsilent_ranges}")
print(f"Padded nonsilent sections: {padded_ranges}")

# Extract and concatenate the nonsilent audio
if padded_ranges:
    nonsilent_audio = [audio[start:end] for start, end in padded_ranges]
    processed_audio = sum(nonsilent_audio)

    processed_path = os.path.join(data_folder, "processed_audio.wav")
    processed_audio.export(processed_path, format="wav")
    print(f"Processed audio saved to: {processed_path}")
else:
    print("No nonsilent sections detected. Check your silence detection parameters.")
