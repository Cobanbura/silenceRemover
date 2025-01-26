from moviepy import VideoFileClip, concatenate_videoclips
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os

data_folder = '../data'
video_files = [file for file in os.listdir(data_folder) if file.endswith(".mp4")]

print("Available video files:")
for idx, file_name in enumerate(video_files, start=1):
    print(f"{idx}: {file_name}")

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

video = VideoFileClip(selected_file)
audio = AudioSegment.from_file(selected_file, format="mp4")

min_silence_len = 500
silence_thresh = -35
padding = 350

nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
padded_ranges = [
    (max(start - padding, 0), min(end + padding, len(audio)))
    for start, end in nonsilent_ranges
]

clips = []
for start, end in padded_ranges:
    start_seconds = start / 1000
    end_seconds = end / 1000
    clip = video.subclipped(start_seconds, end_seconds)
    clips.append(clip)

if clips:
    final_video = concatenate_videoclips(clips)
    output_path = os.path.join(data_folder, "processed_video.mp4")
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Processed video saved to: {output_path}")
else:
    print("No nonsilent sections detected. Check your silence detection parameters.")
