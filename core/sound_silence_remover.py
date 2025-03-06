from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os

# Define the data folder
data_folder = '../data'

# Check if the folder exists; if not, create it and inform the user
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    print(f"The folder '{data_folder}' did not exist and has been created.")
    print("The folder is currently empty. Please add some WAV files to process.")
    exit()

# Check if there are available files in the data folder
wav_files = [file for file in os.listdir(data_folder) if file.endswith(".wav")]

# If there is no file available, inform the user and exit
if not wav_files:
    print("No WAV files found in the folder. Please add some WAV files to process.")
    exit()

# List WAV files for the user
print("Available WAV files:")
for idx, file_name in enumerate(wav_files, start=1):
    print(f"{idx}: {file_name}")

# Allow the user to select a WAV file
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

# Load the selected audio file
audio = AudioSegment.from_file(selected_file, format="wav")

# Parameters for silence detection
min_silence_len = 500
silence_thresh = -35
padding = 350

# Detect nonsilent sections
nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

# Add padding to the detected ranges
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
