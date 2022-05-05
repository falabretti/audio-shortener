import os
from typing import Dict
import dotenv
import requests
from classes import *

dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY')
UPLOAD_ENDPOINT = os.getenv('UPLOAD_ENDPOINT')
TRANSCRIPT_ENDPOINT = os.getenv('TRANSCRIPT_ENDPOINT')

headers = {
    'authorization': API_KEY,
    'content-type': 'application/json'
}


def __read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def __convert(response: Dict) -> Transcript:
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

