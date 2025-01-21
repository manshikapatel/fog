import os
from yt_dlp import YoutubeDL
from moviepy.editor import *
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})


def download_video(url, output_path="videos/input_video.mp4"):
    """
    Downloads a video from the provided URL using yt-dlp.

    Parameters:
        url (str): The URL of the video to download.
        output_path (str): The file name or path where the downloaded video will be saved.
    """
    try:
        # Ensure the "videos" folder exists
        output_folder = "videos"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)  # Create the "videos" folder if it doesn't exist
        
        # yt-dlp options
        ydl_opts = {
            "outtmpl": output_path  # Define the output file name and path
        }
        
        # Initialize downloader and download the video
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print(f"Video downloaded successfully! Saved as: {output_path}")
        return output_path  # Return the downloaded video path
    
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None


def create_short_video(input_path, output_path="videos/short_video.mp4"):
    """
    Creates a 30-second short video from a longer input video.
    
    Parameters:
        input_path (str): Path to the input video.
        output_path (str): Path to save the processed short video.
    """
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Load the input video
        video = VideoFileClip(input_path)

        # Step 1: Extract interesting clips (adjust the timestamps as needed)
        clip1 = video.subclip(5, 10)  # From 5 to 10 seconds
        clip2 = video.subclip(15, 20)  # From 15 to 20 seconds
        clip3 = video.subclip(35, 40)  # From 35 to 40 seconds

        # Step 2: Combine the clips into one video
        combined = concatenate_videoclips([clip1, clip2, clip3])

        # Step 3: Add text overlay (optional)
        text = TextClip("My Short Video", fontsize=50, color="white", size=combined.size, method="caption")
        text = text.set_duration(3).set_position(("center", "bottom"))  # Display for 3 seconds

        # # Combine video and text
        final_video = CompositeVideoClip([combined, text])

        # Step 4: Add background music (optional)
        music = AudioFileClip("audio.mpeg").subclip(0, final_video.duration)
        final_video = final_video.set_audio(music)

        # Step 5: Export the final short video
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        print(f"Short video created successfully! Saved as: {output_path}")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except Exception as e:
        print(f"Error processing video: {e}")


# ===========================
# Instructions to Use:
# ===========================

# Step 1: Provide the video URL here
video_url = "https://youtu.be/y3RIHnK0_NE?si=1vRLvB6cdhOGP7rg"  # Example: "https://www.youtube.com/watch?v=EXAMPLE"

# Step 2: Download the video
input_video_path = download_video(video_url)

# Step 3: Process the downloaded video to create a short video
if input_video_path:  # Ensure the video was downloaded successfully
    create_short_video(input_video_path, "videos/short_video.mp4")

# ===========================
# Notes:
# ===========================
# 1. Replace "YOUR_VIDEO_URL" with the link to the video you want to download.
# 2. The video will be saved in the "videos" folder.
# 3. Adjust clip timestamps and text as needed.
# 4. Uncomment the music section to add background music.
