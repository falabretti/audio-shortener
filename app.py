import sys
import os
import assemblyai
import time
import json


def get_audio_file_name():
    if len(sys.argv) < 2:
        sys.exit('No audio file provided!')

    audio_file_path = os.path.abspath(sys.argv[1])

    if not os.path.isfile(audio_file_path):
        sys.exit('File does not exists!')

    return audio_file_path

def wait_for_transcript(transcript_id):
    transcript = assemblyai.get_transcript(transcript_id)

    while True:
        if transcript.status == 'completed':
            print('Transcript ready.')
            return transcript

        if transcript.status == 'error':
            print('There was an error while processing the transcript.')
            break

        if transcript.status == 'processing':
            print('Transcript not ready yet.')
            time.sleep(10)
            continue

if __name__ == '__main__':
    audio_file_path = get_audio_file_name()
    file_url = assemblyai.upload_file(audio_file_path)
    transcript = assemblyai.submit_transcript(file_url)

    print(transcript)
    transcript = wait_for_transcript(transcript.id)
    print(transcript)
