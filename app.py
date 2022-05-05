import sys
import os
import assemblyai
import text_player


def get_audio_file_name():
    if len(sys.argv) < 2:
        sys.exit('No audio file provided!')

    audio_file_path = os.path.abspath(sys.argv[1])

    if not os.path.isfile(audio_file_path):
        sys.exit('File does not exists!')

    return audio_file_path


if __name__ == '__main__':
    audio_file_path = get_audio_file_name()

    print('Uploading audio file...')
    file_url = assemblyai.upload_file(audio_file_path)

    print('Submitting transcript...')
    transcript = assemblyai.submit_transcript(file_url)

    print('Waiting for transcript...')
    transcript = assemblyai.wait_for_transcript(transcript.id)

    print('Playing transcript text...')
    text_player.speak_text(transcript.summary)
