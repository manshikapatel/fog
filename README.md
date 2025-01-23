YouTube Video Downloader & Short Video Creator

This project allows you to download a video from YouTube and create a short video by selecting specific clips, adding text overlays, and including background music. The output video is saved with a unique filename based on the timestamp to avoid overwriting.

Features


Download videos from YouTube.

Select specific clips from the downloaded video (by defining start and end times).

Add text overlays at specified times with customizable duration.

Add background music to the video.

Save the resulting video with a unique filename.


Technologies Used
Programming Language: Python

Libraries:
yt-dlp: For downloading videos from YouTube.

moviepy: For video processing (trimming, combining clips, and adding text/audio).

os: For file handling and directory creation.

Additional Tools:
ImageMagick: Required for rendering text overlays with moviepy.

FFmpeg: Used internally by moviepy for efficient video encoding.

Installation
Prerequisites

Install Python (>= 3.7).
Install FFmpeg:
On Windows: Download FFmpeg and add it to your system PATH.

Install ImageMagick (for text rendering):
Download and install from the official website.
Ensure the path to the magick.exe binary is correctly configured in the script.



High-Level Approach
1.Download Video:

Open the application and input the YouTube video URL in the provided field.
Click on Download Video to download the video to your local machine.

2.Add Clips:

Enter the start and end times for the clips you want to extract from the video.
Click on Add Clip to add the selected clip to the list.

3.Add Text Overlays:

Enter the text, start time, and duration for the overlay.
Click on Add Text Overlay to add the text overlay to the video.

4.Select Background Music:

Click on Select Background Music to choose an audio file from your local machine (e.g., MP3, WAV).

5.Create Short Video:

Once all clips and text overlays have been added, and the music is selected, click on Create Short Video.
The video will be processed and saved with a unique filename based on the current timestamp (e.g., short_video_20250123-123456.mp4)




