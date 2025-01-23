import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from yt_dlp import YoutubeDL
import os
from moviepy.config import change_settings
import time

change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})



# Function to download video from YouTube
def download_video(url, output_path="videos/input_video.mp4"):
    try:
        # Ensure the output folder exists
        output_folder = os.path.dirname(output_path)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # yt-dlp options for downloading
        ydl_opts = {
            "outtmpl": output_path  # Specify output file path
        }
        
        # Download the video
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        messagebox.showinfo("Success", f"Video downloaded successfully! Saved as: {output_path}")
        return output_path
    except Exception as e:
        messagebox.showerror("Error", f"Error downloading video: {e}")
        return None

# Function to create a short video
def create_short_video(input_path, output_dir="videos", clip_times=None, text_overlays=None, music_path=None, max_duration=15):
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate a unique output filename
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_path = os.path.join(output_dir, f"short_video_{timestamp}.mp4")

        # Load the input video
        video = VideoFileClip(input_path)
        video_duration = video.duration  # Get the total duration of the video

        # Validate and adjust clip times
        valid_clips = []
        total_duration = 0
        for start, end in clip_times:
            if start >= video_duration:
                print(f"Skipping clip: start time {start} exceeds video duration {video_duration}.")
                continue
            if end > video_duration:
                print(f"Adjusting end time for clip starting at {start} to {video_duration}.")
                end = video_duration

            clip_duration = end - start
            if total_duration + clip_duration > max_duration:
                # Trim the clip to fit within the 15-second limit
                end = start + (max_duration - total_duration)
                clip_duration = end - start

            valid_clips.append((start, end))
            total_duration += clip_duration

            if total_duration >= max_duration:
                break  # Stop adding clips once we reach the maximum duration

        if not valid_clips:
            raise ValueError("No valid clip times provided within the video's duration.")

        # Create and combine clips
        clips = [video.subclip(start, end) for start, end in valid_clips]
        combined = concatenate_videoclips(clips)

        # Add text overlays
        final_video = combined
        for text, start, duration in text_overlays:
            if start + duration > final_video.duration:
                print(f"Adjusting text overlay duration for '{text}'.")
                duration = final_video.duration - start
            overlay = TextClip(
                text, fontsize=50, color="white", size=combined.size, method="caption"
            )
            overlay = overlay.set_start(start).set_duration(duration).set_position(("center", "bottom"))
            final_video = CompositeVideoClip([final_video, overlay])

        # Add background music if provided
        if music_path:
            music = AudioFileClip(music_path).subclip(0, final_video.duration)
            final_video = final_video.set_audio(music)

        # Export the final short video
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        messagebox.showinfo("Success", f"Short video created successfully! Saved as: {output_path}")
    except FileNotFoundError as fnf_error:
        messagebox.showerror("Error", str(fnf_error))
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Error processing video: {e}")


# GUI Setup
def start_gui():
    def download():
        url = url_entry.get()
        if url:
            global downloaded_video_path
            downloaded_video_path = download_video(url)
        else:
            messagebox.showwarning("Input Error", "Please enter a YouTube URL.")

    def add_clip():
        try:
            start = float(start_time.get())
            end = float(end_time.get())
            if start >= end:
                messagebox.showwarning("Input Error", "Start time must be less than end time.")
                return
            clip_times.append((start, end))
            clips_list.insert(tk.END, f"Clip: {start}s - {end}s")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid start and end times.")

    def add_text_overlay():
        try:
            text = text_overlay.get()
            start = float(text_start_time.get())
            duration = float(text_duration.get())
            text_overlays.append((text, start, duration))
            text_list.insert(tk.END, f"Text: '{text}' at {start}s for {duration}s")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid text details.")

    def select_music():
        global selected_music_path
        selected_music_path = filedialog.askopenfilename(
            title="Select Background Music", filetypes=[("Audio Files", "*.mp3 *.wav *.aac *.mpeg")]
        )
        if selected_music_path:
            music_label.config(text=f"Music: {os.path.basename(selected_music_path)}")

    def create_video():
        if not downloaded_video_path:
            messagebox.showwarning("Error", "Please download a video first.")
            return
        if not clip_times:
            messagebox.showwarning("Error", "Please add at least one clip.")
            return

        # Generate a unique output filename based on the current timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")  # Unique timestamp for each video
        output_path = os.path.join("videos", f"short_video_{timestamp}.mp4")

        try:
            create_short_video(
                downloaded_video_path,  # Path to the downloaded video
                output_path,  # Dynamically generated output path
                clip_times,  # List of tuples (start_time, end_time)
                text_overlays,  # List of tuples (text, start_time, duration) for text overlays
                selected_music_path  # Path to the background music or None
            )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the video: {e}")

    # GUI Elements
    root = tk.Tk()
    root.title("Video Downloader & Short Video Creator")
    root.geometry("700x600")

    tk.Label(root, text="YouTube Video URL:").pack(pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    tk.Button(root, text="Download Video", command=download).pack(pady=10)

    tk.Label(root, text="Add Clips (Start and End Time in Seconds):").pack(pady=10)
    frame = tk.Frame(root)
    frame.pack(pady=5)

    tk.Label(frame, text="Start Time:").grid(row=0, column=0)
    start_time = tk.Entry(frame, width=10)
    start_time.grid(row=0, column=1)

    tk.Label(frame, text="End Time:").grid(row=0, column=2)
    end_time = tk.Entry(frame, width=10)
    end_time.grid(row=0, column=3)

    tk.Button(frame, text="Add Clip", command=add_clip).grid(row=0, column=4, padx=5)

    clips_list = tk.Listbox(root, width=60, height=5)
    clips_list.pack(pady=10)

    tk.Label(root, text="Add Text Overlays (Text, Start Time, Duration):").pack(pady=10)
    text_frame = tk.Frame(root)
    text_frame.pack(pady=5)

    tk.Label(text_frame, text="Text:").grid(row=0, column=0)
    text_overlay = tk.Entry(text_frame, width=20)
    text_overlay.grid(row=0, column=1)

    tk.Label(text_frame, text="Start Time:").grid(row=0, column=2)
    text_start_time = tk.Entry(text_frame, width=10)
    text_start_time.grid(row=0, column=3)

    tk.Label(text_frame, text="Duration:").grid(row=0, column=4)
    text_duration = tk.Entry(text_frame, width=10)
    text_duration.grid(row=0, column=5)

    tk.Button(text_frame, text="Add Text Overlay", command=add_text_overlay).grid(row=0, column=6, padx=5)

    text_list = tk.Listbox(root, width=60, height=5)
    text_list.pack(pady=10)

    tk.Button(root, text="Select Background Music", command=select_music).pack(pady=10)
    music_label = tk.Label(root, text="No music selected.")
    music_label.pack()

    tk.Button(root, text="Create Short Video", command=create_video).pack(pady=20)

    root.mainloop()

# Global variables
downloaded_video_path = None
clip_times = []  # List of tuples for (start, end) times
text_overlays = []  # List of tuples for (text, start, duration)
selected_music_path = None

# Start the GUI
start_gui()
