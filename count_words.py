# This was generated with Amazon Q with this prompt:
# "Using Python and boto3 and any AWS services that are required write a script that takes a YouTube url and determines how many words each speaker says in it."

import boto3
import yt_dlp
import os
import uuid
from urllib.parse import urlparse

def download_audio(youtube_url):
    """Downloads audio from YouTube video"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    return 'audio.mp3'

def transcribe_audio(audio_file, bucket_name):
    """Transcribes audio using Amazon Transcribe"""
    transcribe = boto3.client('transcribe')
    
    # Upload audio file to S3
    s3 = boto3.client('s3')
    s3_path = f'uploads/{os.path.basename(audio_file)}'
    s3.upload_file(audio_file, bucket_name, s3_path)
    
    # Start transcription job
    job_name = f"transcription_{urlparse(s3_path).path.split('/')[-1]}" + str(uuid.uuid4()).replace('-', '')
    job_uri = f's3://{bucket_name}/{s3_path}'
    
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US',
        Settings={'ShowSpeakerLabels': True,
                 'MaxSpeakerLabels': 10}
    )
    
    # Wait for completion
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
            
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        return status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    return None

def count_words_per_speaker(transcript_uri):
    """Counts words spoken by each speaker"""
    import json
    import requests
    
    # Get transcript JSON
    response = requests.get(transcript_uri)
    transcript = json.loads(response.text)
    
    # Initialize word counts
    speaker_word_counts = {}
    
    # Count words for each speaker
    for segment in transcript['results']['speaker_labels']['segments']:
        speaker_label = segment['speaker_label']
        if speaker_label not in speaker_word_counts:
            speaker_word_counts[speaker_label] = 0
            
        start_time = segment['start_time']
        end_time = segment['end_time']
        
        # Find items that fall within this time segment
        for item in transcript['results']['items']:
            if 'start_time' in item and 'end_time' in item:
                if float(item['start_time']) >= float(start_time) and float(item['end_time']) <= float(end_time):
                    if item['type'] == 'pronunciation':
                        speaker_word_counts[speaker_label] += 1
                        
    return speaker_word_counts

def main():
    youtube_url = input("Enter YouTube URL: ")
    bucket = input("Enter S3 bucket name: ")
    
    # Download audio
    print("Downloading audio...")
    audio_file = download_audio(youtube_url)
    
    # Transcribe audio
    print("Transcribing audio...")
    transcript_uri = transcribe_audio(audio_file, bucket)
    
    if transcript_uri:
        # Count words per speaker
        print("Counting words per speaker...")
        word_counts = count_words_per_speaker(transcript_uri)
        
        # Print results
        print("\nWord counts per speaker:")
        for speaker, count in word_counts.items():
            print(f"{speaker}: {count} words")
    else:
        print("Transcription failed")
        
    # Cleanup
    os.remove(audio_file)

if __name__ == "__main__":
    main()
