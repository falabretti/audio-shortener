import os
import argparse
import assemblyai
import util
import sys

parser = argparse.ArgumentParser('AudioShortener')

parser.add_argument('-a', '--audio', type=str)
parser.add_argument('-v', '--video', type=str)
parser.add_argument('-w', '--wait', action='store_true')
parser.add_argument('-s', '--save', action='store_true')
parser.add_argument('-p', '--play', action='store_true')
parser.add_argument('--id', type=str)

args = parser.parse_args()


def send_file():
    audio_file_path = util.get_audio_file_path(args)

    print('Uploading audio file...')
    file_url = assemblyai.upload_file(audio_file_path)

    print('Submitting transcript...')
    transcript = assemblyai.submit_transcript(file_url)

    return transcript


def process_transcript_id():
    if args.audio or args.video:
        transcript = send_file()
        return transcript.id
    elif args.id:
        return args.id
    else:
        sys.exit('No file or transcript id provided!') 


def process_transcript(transcript_id):
    if args.wait:
        print('Waiting for transcript...')
        return assemblyai.wait_for_transcript(transcript_id)
    else:
        return assemblyai.get_transcript(transcript_id)


if __name__ == '__main__':

    transcript_id = process_transcript_id()
    transcript = process_transcript(transcript_id)

    print(transcript)

    if args.play and transcript.summary is not None:
        print('Playing transcript text...')
        util.speak_text(transcript.summary)
    
    if args.save:
        util.save_transcript(transcript)
