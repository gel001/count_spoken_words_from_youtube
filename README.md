Note: You may need to brew install ffmpeg. 

pip install -r requirements.txt

python count_words.py

Enter YouTube URL: https://www.youtube.com/watch?v=gdGgBKJiM2E
Enter S3 bucket name: YOUR_BUCKET_HERE
Downloading audio...
[youtube] Extracting URL: https://www.youtube.com/watch?v=gdGgBKJiM2E
[youtube] gdGgBKJiM2E: Downloading webpage
[youtube] gdGgBKJiM2E: Downloading ios player API JSON
[youtube] gdGgBKJiM2E: Downloading mweb player API JSON
[youtube] gdGgBKJiM2E: Downloading m3u8 information
[info] gdGgBKJiM2E: Downloading 1 format(s): 251
[download] Destination: audio.webm
[download] 100% of   38.43MiB in 00:00:05 at 7.63MiB/s
[ExtractAudio] Destination: audio.mp3
Deleting original file audio.webm (pass -k to keep)
Transcribing audio...
Counting words per speaker...

Word counts per speaker:
spk_0: 10682 words

