import argparse
import sys, os
import time
from pytube import YouTube
from pytube.helpers import safe_filename
import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
#import pysubs2
#from pydub.playback import play
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from random import randint

def my_progress(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def ingest_dataset(yt_uri, output_path): # function for ingesting when given a url
    # Use vid as the diretory name for download and processing
    vids = parse_qs(urlparse(yt_uri).query, keep_blank_values=True).get('v')
    vid = None if vids == None else vids[0]

    v_dir = os.path.join(output_path, vid)

    # Filename for audio stream (.mp4) and subtitle (.srt) files
    audio = os.path.join(v_dir, vid + '.webm')
    subtitle = os.path.join(v_dir, vid + '.srt')

    if Path(audio).exists() and Path(subtitle).exists():
        return False

    if os.path.exists(audio.replace('.webm', '.mp3')) and os.path.exists(subtitle):
        return False

    # Get information on the YouTube content
    try:
        # Random time do waiting
        t = randint(30,60) 
        print('Waiting %d seconds ...'%(t))
        time.sleep(t) # Overcome YouTube blocking

        os.makedirs(v_dir, exist_ok=True)
        # yt = YouTube(yt_uri) // Not working

        ydl_opts = {
            'format': 'bestaudio/best',  
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],     
            'outtmpl': audio,        
            'noplaylist' : True,        
            'progress_hooks': [my_progress],  
        }
        # Download audio stream and convert to mp3
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_uri])     

        # get video_id from youtube_uri
        video_id = yt_uri.replace('https://www.youtube.com/watch?v=','')
        # Download subtitle and write to an .srt file
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # filter first for manually created transcripts and second for automatically generated ones
        transcript = transcript_list.find_transcript(['pt'])
        # get only text from transcript
        text_transcript_list = []
        for line in transcript.fetch():
            text_transcript_list.append(line['text'])
        text_transcript = ' '.join(text_transcript_list)

        # Write transcript to file
        output_file = open(subtitle, 'w')
        output_file.write(text_transcript)
        output_file.close()

    except KeyboardInterrupt:
        print("KeyboardInterrupt Detected!")
        exit()
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        exc_file = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, exc_file, exc_tb.tb_lineno)
        #sys.exit(1)
        return False

    return True

# Executing the function
if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('path', help="URL of the video file to make speech recognition corpus from")
	parser.add_argument('--output_dir', default='data', help='Directory to download audio and transcript.')

	args = parser.parse_args()

	if args.path.startswith('https://'):
		ingest_dataset(args.path, args.output_dir)
	else:
		print("URL of the video file should start with https://")
		sys.exit(1)
