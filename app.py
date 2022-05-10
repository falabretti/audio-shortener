import argparse
import assemblyai
import util
import sys

args = None

def parse_args():
    '''Parse command line arguments'''
    global args

    parser = argparse.ArgumentParser('AudioShortener')

    parser.add_argument('-a', '--audio', type=str, help='Audio file for transcription')
    parser.add_argument('-v', '--video', type=str, help='Video file for transcription')
    parser.add_argument('-w', '--wait', action='store_true', help='Wait for transcription completion')
    parser.add_argument('-s', '--save', action='store_true', help='Save the transcription result in a JSON file')
    parser.add_argument('-p', '--play', action='store_true', help='Reproduce the summary text via audio')
    parser.add_argument('--id', type=str, help='Do not process a new file and use this transcription instead')

    args = parser.parse_args()

def send_file():
    '''Upload a file and submit it for transcription'''
    audio_file_path = util.get_audio_file_path(args)

    print('Uploading audio file...')
    file_url = assemblyai.upload_file(audio_file_path)

    print('Submitting transcript...')
    transcript = assemblyai.submit_transcript(file_url)

    return transcript


def process_transcript():
    '''Decide if the program should use a video, audio or an existing transcription'''
    if args.audio or args.video:
        transcript = send_file()
        return transcript.id
    elif args.id:
        return args.id
    else:
        sys.exit('No file or transcript id provided!') 


def get_transcript(transcript_id):
    '''Fetch the transcription result'''
    if args.wait:
        print('Waiting for transcript...')
        return assemblyai.wait_for_transcript(transcript_id)
    else:
        return assemblyai.get_transcript(transcript_id)

def main():
    '''Program main funcion'''

    parse_args()

    transcript_id = process_transcript()
    transcript = get_transcript(transcript_id)

    print(transcript)

    if args.play and transcript.summary is not None:
        print('Playing transcript text...')
        util.speak_text(transcript.summary)
    
    if args.save:
        util.save_transcript(transcript)

if __name__ == '__main__':
    main()
