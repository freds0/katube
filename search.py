from config import Config
import argparse
import os
from os import makedirs
from os.path import join, exists
from pytube import YouTube
from googleapiclient import discovery
from googleapiclient.discovery import build
import tqdm
import sys

def search_videos(api_key, content_id, output_path, output_search_file):
    youtube_prefix = 'https://www.youtube.com/watch?v='

    api_service_name = 'youtube'
    api_version = 'v3'

    #print('Searching videos from {} - {}...'.format(Config.orig_base, content_id))
    path_dest = join(output_path, Config.orig_base, content_id )

    if not(exists(path_dest)):
        makedirs(path_dest)

    file_path = join(path_dest, output_search_file)

    # Checks if it has already been downloaded
    if os.path.exists(file_path):
        return file_path

    try:
        f = open(file_path, 'w+')

        youtube = build(api_service_name, api_version, developerKey = api_key)

        if Config.orig_base == 'playlist':
            conv_id = content_id
        elif Config.orig_base == 'channel':
            res = youtube.channels().list(id = content_id,
                        part = 'contentDetails').execute()
            conv_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        else:
            conv_id = None

        videos = get_videos(youtube, conv_id)

        print('Writing video links to file...')
        for video in tqdm.tqdm(videos):
            f.write( youtube_prefix + video['snippet']['resourceId']['videoId'] + '\n' )

        print("Total videos: {0}".format( len(videos) ))
        f.close()

    except KeyboardInterrupt:
        print("KeyboardInterrupt Detected!")
        exit()
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        exc_file = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, exc_file, exc_tb.tb_lineno)
        #sys.exit(1)
        return False

    return file_path

# Get all the videos from a channel
def get_videos(youtube, conv_id):
    videos = []
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(playlistId = conv_id,
                                            part = 'snippet',
                                            maxResults = 50,
                                            pageToken = next_page_token).execute()

        videos += res['items']
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    return videos

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', default = '')
    parser.add_argument('--content_id', default = '')
    parser.add_argument('--base_dir', default = './')
    parser.add_argument('--dest_dir', default = 'data')
    parser.add_argument('--output_search_file', default='youtube_videos.txt')
    args = parser.parse_args()
    output_path = join(args.base_dir, args.dest_dir)
    search_videos(args.api_key, args.content_id, output_path, args.output_search_file)

if __name__ == '__main__':
    main()
