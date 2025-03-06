from moviepy import VideoFileClip, concatenate_videoclips
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os
from datetime import datetime

# Define the data folder
data_folder = '../data'

# Check if the folder exists; if not, create it and inform the user
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    print(f"The folder '{data_folder}' was not found and has been created. Please add video files to this folder.")
    exit()

# Check for available video files in supported formats (.mp4, .mov, .mkv)
supported_formats = (".mp4", ".mov", ".mkv")
video_files = [file for file in os.listdir(data_folder) if file.endswith(supported_formats)]

# If there is no file available, inform the user and exit
if not video_files:
    print(f"The folder '{data_folder}' contains no supported video files. Please add files in .mp4, .mov, or .mkv formats.")
    exit()

# List available video files for the user
print("Available video files:")
for idx, file_name in enumerate(video_files, start=1):
    print(f"{idx}: {file_name}")

# Allow the user to select a video file
selected_file = None
while selected_file is None:
    try:
        user_input = input("Enter the number of the video file you want to process: ")
        file_index = int(user_input) - 1
        if 0 <= file_index < len(video_files):
            selected_file = os.path.join(data_folder, video_files[file_index])
        else:
            print(f"Invalid number. Please select a number between 1 and {len(video_files)}.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Load the selected video and extract its audio
video = VideoFileClip(selected_file)
audio = AudioSegment.from_file(selected_file)

# Silence detection parameters
min_silence_len = 500
silence_thresh = -35
padding = 350

# Detect nonsilent sections
nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

# Add padding to nonsilent sections
padded_ranges = [
    (max(start - padding, 0), min(end + padding, len(audio)))
    for start, end in nonsilent_ranges
]

# Extract and concatenate nonsilent sections
clips = []
for start, end in padded_ranges:
    start_seconds = start / 1000
    end_seconds = end / 1000
    clip = video.subclipped(start_seconds, end_seconds)
    clips.append(clip)

# Save the processed video
if clips:
    final_video = concatenate_videoclips(clips)
    file_extension = os.path.splitext(selected_file)[1]  # Get the extension of the selected video
    current_date = datetime.now().strftime("%Y-%m-%d")  # Get current date in YYYY-MM-DD format
    output_path = os.path.join(data_folder, f"processed_video_{current_date}{file_extension}")  # Add date to output name
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Processed video saved to: {output_path}")
else:
    print("No nonsilent sections detected. Check your silence detection parameters.")
