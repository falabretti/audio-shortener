# Audio Shortener

Through an audio or video file, this application is able to generate a text summary of the contents of the file, and also reproduce the summarized text as audio for the user. It leverages [AssemblyAI](https://www.assemblyai.com/) to do so.

---
## Installation

The application was tested only with Python 3.10.4.

### Install required dependencies
```
python -m pip intall -r requirements.txt
```

### Environment variables

Duplicate the `.env.example` file to a `.env` file:
```
cp .env.example .env
```

Set your `API_KEY` in the `.env` file. You can get an API key by creating an account on [AssemblyAI](https://www.assemblyai.com/).

---
## Usage

Example of usage with all functionalities:
```
python .\app.py --video .\path\to\audio\file.mp4 --wait --save --play
```

### Possible options
* `-h, --help`: show this help message and exit
* `-a <AUDIO>, --audio <AUDIO>`: Audio file for transcription
* `-v <VIDEO>, --video <VIDEO>`: Video file for transcription
* `-w, --wait`: Wait for transcription completion
* `-s, --save`: Save the transcription result in a JSON file     
* `-p, --play`: Reproduce the summary text via audio
* `--id <ID>`: Do not process a new file and use this transcription instead

> **_Note:_** Use only one of `--video`, `--audio` or `--id` to specify which file or transcription to use. Do not use multiple of them at the same time.
