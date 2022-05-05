# ox4n9ywtpc-10aa-430f-8602-7aa66c4fb4d1

import os
import sys
import dotenv
import requests
import json
import pyttsx3

dotenv.load_dotenv()

TRANSCRIPT_ENDPOINT = os.getenv('TRANSCRIPT_ENDPOINT')
API_KEY = os.getenv('API_KEY')

headers = {
    'authorization': API_KEY,
    'content-type': 'application/json'
}

if len(sys.argv) < 2:
    sys.exit('No transcript id provided!')

transcript_id = sys.argv[1]

url = TRANSCRIPT_ENDPOINT + '/' + transcript_id

print(url)

response = requests.get(url, headers=headers)
print(json.dumps(response.json(), indent=4))


def speak_text(text):
    out = pyttsx3.init()    
    out.say(text)
    out.runAndWait()

summary = response.json()['chapters'][0]['summary']
print(summary)

speak_text(summary)
