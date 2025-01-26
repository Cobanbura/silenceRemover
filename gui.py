import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from moviepy import VideoFileClip, concatenate_videoclips
from threading import Thread

class SilenceRemoverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Silence Remover")
        
        # Main frame with padding
        main_frame = ttk.Frame(root, padding=10)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File type selection
        type_frame = ttk.LabelFrame(main_frame, text="File Type", padding=5)
        type_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        self.file_type = tk.StringVar(value="audio")
        ttk.Radiobutton(type_frame, text="Audio", variable=self.file_type, value="audio").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(type_frame, text="Video", variable=self.file_type, value="video").grid(row=0, column=1, padx=5)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding=5)
        file_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).grid(row=0, column=0, padx=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=1, padx=5)
        
        # Parameters
        params_frame = ttk.LabelFrame(main_frame, text="Parameters", padding=5)
        params_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        # Silence threshold
        ttk.Label(params_frame, text="Silence Threshold (dB):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.silence_thresh = tk.StringVar(value="-35")
        ttk.Entry(params_frame, textvariable=self.silence_thresh, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Minimum silence length
        ttk.Label(params_frame, text="Min Silence Length (ms):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.min_silence_len = tk.StringVar(value="500")
        ttk.Entry(params_frame, textvariable=self.min_silence_len, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Padding
        ttk.Label(params_frame, text="Padding (ms):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.padding = tk.StringVar(value="350")
        ttk.Entry(params_frame, textvariable=self.padding, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Progress
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding=5)
        progress_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate', variable=self.progress_var)
        self.progress.grid(row=0, column=0, columnspan=2, pady=2)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, columnspan=2)
        
        # Process button
        self.process_btn = ttk.Button(main_frame, text="Process", command=self.process_file)
        self.process_btn.grid(row=4, column=0, columnspan=4, pady=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        
        # Make window size adapt to contents
        self.root.update_idletasks()
        self.root.geometry('')

    def browse_file(self):
        filetypes = [("Audio Files", "*.wav")] if self.file_type.get() == "audio" else [("Video Files", "*.mp4")]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_path.set(filename)

    def update_status(self, message, progress=None):
        self.status_var.set(message)
        if progress is not None:
            self.progress_var.set(progress)
        self.root.update_idletasks()

    def process_file(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a file first")
            return

        try:
            self.process_btn.state(['disabled'])
            Thread(target=self._process_file_thread).start()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.process_btn.state(['!disabled'])

    def _process_file_thread(self):
        try:
            input_file = self.file_path.get()
            min_silence_len = int(self.min_silence_len.get())
            silence_thresh = int(self.silence_thresh.get())
            padding = int(self.padding.get())

            self.update_status("Loading file...", 0)

            if self.file_type.get() == "audio":
                self._process_audio(input_file, min_silence_len, silence_thresh, padding)
            else:
                self._process_video(input_file, min_silence_len, silence_thresh, padding)

            self.update_status("Processing complete!", 100)
            messagebox.showinfo("Success", "File processed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.process_btn.state(['!disabled'])

    def _process_audio(self, input_file, min_silence_len, silence_thresh, padding):
        self.update_status("Loading audio...", 10)
        audio = AudioSegment.from_file(input_file, format="wav")

        self.update_status("Detecting non-silent ranges...", 30)
        nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
        
        self.update_status("Processing audio...", 50)
        padded_ranges = [
            (max(start - padding, 0), min(end + padding, len(audio)))
            for start, end in nonsilent_ranges
        ]

        if padded_ranges:
            self.update_status("Concatenating audio segments...", 70)
            nonsilent_audio = [audio[start:end] for start, end in padded_ranges]
            processed_audio = sum(nonsilent_audio)

            output_path = os.path.splitext(input_file)[0] + "_processed.wav"
            self.update_status("Exporting audio...", 90)
            processed_audio.export(output_path, format="wav")
        else:
            raise Exception("No non-silent sections detected. Try adjusting the parameters.")

    def _process_video(self, input_file, min_silence_len, silence_thresh, padding):
        self.update_status("Loading video...", 10)
        video = VideoFileClip(input_file)
        audio = AudioSegment.from_file(input_file, format="mp4")

        self.update_status("Detecting non-silent ranges...", 30)
        nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
        
        self.update_status("Processing video...", 50)
        padded_ranges = [
            (max(start - padding, 0), min(end + padding, len(audio)))
            for start, end in nonsilent_ranges
        ]

        if padded_ranges:
            self.update_status("Creating video clips...", 70)
            clips = []
            for start, end in padded_ranges:
                start_seconds = start / 1000
                end_seconds = end / 1000
                clip = video.subclip(start_seconds, end_seconds)
                clips.append(clip)

            self.update_status("Concatenating video clips...", 80)
            final_video = concatenate_videoclips(clips)
            
            output_path = os.path.splitext(input_file)[0] + "_processed.mp4"
            self.update_status("Exporting video...", 90)
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
            video.close()
        else:
            video.close()
            raise Exception("No non-silent sections detected. Try adjusting the parameters.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SilenceRemoverGUI(root)
    root.mainloop()
