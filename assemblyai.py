import os
import dotenv
import requests
import time
import random
import json

dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY')
UPLOAD_ENDPOINT = os.getenv('UPLOAD_ENDPOINT')
TRANSCRIPT_ENDPOINT = os.getenv('TRANSCRIPT_ENDPOINT')

headers = {
    'authorization': API_KEY,
    'content-type': 'application/json'
}


class Transcript:
    def __init__(self, id, status, summary = None):
        self.id = id
        self.status = status
        self.summary = summary

    def __str__(self) -> str:
        return json.dumps(self.__dict__, indent=4)


def __read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def __convert(response) -> Transcript:
    id = response['id']
    status = response['status']
    summary = None

    chapters = response['chapters']
    if chapters is not None:
        summary = '. '.join([chapter['summary'] for chapter in chapters])
    
    return Transcript(id, status, summary)


def upload_file(audio_file_path):
    response = requests.post(UPLOAD_ENDPOINT, headers=headers, data=__read_file(audio_file_path))
    file_url = response.json().get('upload_url')
    return file_url


def submit_transcript(file_url):
    data = {
        'audio_url': file_url,
        'auto_chapters': True
    }

    response = requests.post(TRANSCRIPT_ENDPOINT, json=data, headers=headers)
    return __convert(response.json())


def get_transcript(transcript_id):
    endpoint = TRANSCRIPT_ENDPOINT + '/' + transcript_id
    response = requests.get(endpoint, headers=headers)
    return __convert(response.json())


def wait_for_transcript(transcript_id):
    max_retries = 10
    retry_count = 0
    max_backoff = 32

    while True:
        transcript = get_transcript(transcript_id)
        print(transcript)

        if transcript.status == 'completed':
            print('Transcript ready.')
            return transcript

        if transcript.status == 'error':
            print('There was an error while processing the transcript.')
            break

        if transcript.status in ['processing', 'queued']:
            if retry_count == max_retries:
                print('Max retries reached.')
                break

            print('Transcript not ready yet.')

            sleep_time = min(2 ** retry_count, max_backoff) + random.uniform(0, 1)
            print(f'Sleeping for {sleep_time} seconds.')
            time.sleep(sleep_time)

            retry_count += 1

            continue

