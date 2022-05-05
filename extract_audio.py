import sys
import os
import moviepy.editor as mp

if len(sys.argv) < 2:
    sys.exit('No video file provided!')

video_file_path = os.path.abspath(sys.argv[1])

if not os.path.isfile(video_file_path):
    sys.exit('File does not exists!')

video = mp.VideoFileClip(video_file_path)

video.audio.write_audiofile('output.mp3')
