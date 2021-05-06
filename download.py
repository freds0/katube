# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2021 Frederico Oliveira fred.santos.oliveira(at)gmail.com
#
#
import argparse
import sys
from os import makedirs
from os.path import join, exists, split
import time
import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from random import randint

def my_progress(d):
    '''
    Show download progress.
    '''
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_audio_and_subtitles_from_youtube(yt_url, output_path): # function for ingesting when given a url
    '''
    Download audio and subtitle from a youtube video given a url.
        Parameters:
        yt_url (str): Youtube URL format https://www.youtube.com/watch?v=XXXXXXXXXXX
        output_path (str): folder to save youtube audio.

        Returns:
        String: returns True or False

    '''
    # Use vid as the diretory name for download and processing
    vids = parse_qs(urlparse(yt_url).query, keep_blank_values=True).get('v')
    vid = None if vids == None else vids[0]

    video_dir = join(output_path, vid)

    # Filename for audio stream (.mp4) and subtitle (.srt) files
    audio = join(video_dir, vid + '.webm')
    subtitle = join(video_dir, vid + '.srt')

    if Path(audio).exists() and Path(subtitle).exists():
        return False

    if exists(audio.replace('.webm', '.mp3')) and exists(subtitle):
        return False

    # Get information on the YouTube content
    try:
        # Random time do waiting to avoid youtube access blocking
        t = randint(30,60) 
        print('Waiting %d seconds ...'%(t))
        time.sleep(t) # Overcome YouTube blocking

        if not (exists(video_dir)):
            makedirs(video_dir)

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
            ydl.download([yt_url])

        # get video_id from youtube_uri
        video_id = yt_url.replace('https://www.youtube.com/watch?v=','')
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
        exc_file = split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, exc_file, exc_tb.tb_lineno)
        return False

    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--youtube_url', help="URL of the youtube video.")
    parser.add_argument('--output_dir', default='data', help='Directory to save downloaded audio and transcript files.')

    args = parser.parse_args()

    if args.youtube_url.startswith('https://'):
        download_audio_and_subtitles_from_youtube(args.youtube_url, args.output_dir)

    else:
        print("URL of the video file should start with https://")
        sys.exit(1)

if __name__ == '__main__':
    main()

