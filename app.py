import os
import argparse
import assemblyai
import util

parser = argparse.ArgumentParser('AudioShortener')

parser.add_argument('-a', '--audio', type=str)
parser.add_argument('-v', '--video', type=str)

args = parser.parse_args()


def get_audio_file_path():
    audio_file_path = None

    if args.audio:
        audio_file_path = os.path.abspath(args.audio)
    elif args.video:
        audio_file_path = util.extract_audio(args.video)

    util.validate_file(audio_file_path)    
    return audio_file_path


if __name__ == '__main__':
    audio_file_path = get_audio_file_path()

    print('Uploading audio file...')
    file_url = assemblyai.upload_file(audio_file_path)

    print('Submitting transcript...')
    transcript = assemblyai.submit_transcript(file_url)

    print('Waiting for transcript...')
    transcript = assemblyai.wait_for_transcript(transcript.id)

    print('Playing transcript text...')
    util.speak_text(transcript.summary)
