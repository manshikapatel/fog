YouTube Video Downloader & Short Video Creator
This project allows you to download a video from YouTube and create a short video by selecting specific clips, adding text overlays, and including background music. The output video is saved with a unique filename based on the timestamp to avoid overwriting.

Features
Download videos from YouTube.
Select specific clips from the downloaded video (by defining start and end times).
Add text overlays at specified times with customizable duration.
Add background music to the video.
Save the resulting video with a unique filename.
Requirements
Make sure you have the following installed before running the project:

Python 3.x: You can download it from python.org.
MoviePy: For video editing. Install it via pip:
Copy
Edit
pip install moviepy
yt-dlp: For downloading YouTube videos. Install it via pip:
Copy
Edit
pip install yt-dlp
ImageMagick: Required for MoviePy to handle text rendering.
Download ImageMagick from here.
Ensure that the magick.exe file is available and the path is correctly set in the code. (The default path used in the code is C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe).
Setup Instructions
Clone or download the repository to your local machine.
Install the required dependencies:
Copy
Edit
pip install moviepy yt-dlp
Install ImageMagick (if not already installed).
Ensure that the IMAGEMAGICK_BINARY path in the code matches the location of magick.exe on your system.
How to Use
Download Video:

Open the application and input the YouTube video URL in the provided field.
Click on Download Video to download the video to your local machine.
Add Clips:

Enter the start and end times for the clips you want to extract from the video.
Click on Add Clip to add the selected clip to the list.
Add Text Overlays:

Enter the text, start time, and duration for the overlay.
Click on Add Text Overlay to add the text overlay to the video.
Select Background Music (Optional):

Click on Select Background Music to choose an audio file from your local machine (e.g., MP3, WAV).
Create Short Video:

Once all clips and text overlays have been added, and the music is selected (if applicable), click on Create Short Video.
The video will be processed and saved with a unique filename based on the current timestamp (e.g., short_video_20250123-123456.mp4).
Code Structure
download_video(url, output_path): Downloads a video from YouTube using yt-dlp.
create_short_video(input_path, output_path, clip_times, text_overlays, music_path): Creates the short video by selecting clips, adding text overlays, and including background music.
start_gui(): Sets up the Tkinter-based graphical user interface (GUI) for user interaction.
Example Usage
After running the GUI, the following steps can be followed:

Enter the YouTube video URL (e.g., https://www.youtube.com/watch?v=example).
Download the video by clicking Download Video.
Add clips by specifying start and end times (e.g., 0s - 10s).
Add text overlays with the desired text, start time, and duration.
Select background music (optional).
Click Create Short Video to generate the final video, saved in the videos/ folder with a unique filename.
