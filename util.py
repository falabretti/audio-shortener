import os
import sys
import pyttsx3
import moviepy.editor as mp


def __get_audio_file_name(video_file_path):
    file_name = os.path.basename(video_file_path)
    file_name_without_ext = file_name.rsplit('.', 1)[0]

    audio_file_name = os.path.join('data', 'output', f'{file_name_without_ext}.mp3')

    return audio_file_name


def validate_file(file_path):
    '''Validates if a given file path points to a valid file or not'''

    if file_path is None:
        sys.exit('No audio or video file provided!')  

    if not os.path.isfile(file_path):
        sys.exit('Provided file does not exists!')


def extract_audio(video_file_path):
    '''Extract the audio portion from a video file and save it as an .mp3 file'''
    validate_file(video_file_path)
    audio_file_name = __get_audio_file_name(video_file_path)

    video = mp.VideoFileClip(video_file_path)
    video.audio.write_audiofile(audio_file_name)

    return os.path.abspath(audio_file_name)


def get_audio_file_path(args):
    '''Decide whether the program should use a video of audio file. If it's an video file, extract its audio as well'''
    audio_file_path = None

    if args.audio:
        audio_file_path = os.path.abspath(args.audio)
    elif args.video:
        audio_file_path = extract_audio(args.video)

    return audio_file_path


def save_transcript(transcript):
    '''Save the transcript object into a JSON file'''
    file_path = os.path.join('data', 'output', f'{transcript.id}.json')
    with open(file_path, 'w') as f:
        f.write(transcript.__str__())


def speak_text(text):
    '''Reproduce a given text in audio format'''
    out = pyttsx3.init()    
    out.say(text)
    out.runAndWait()
