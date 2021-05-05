#!/usr/bin/env python
# coding=utf-8
from config import Config
import argparse
from os import makedirs
from os.path import join, exists, split
from googleapiclient.discovery import build
from tqdm import tqdm
import sys

def get_videos(youtube, conv_id):
    '''
    Get all videos from youtube channel/playlist.

        Parameters:
        youtube (str): googleapiclient object.
        conv_id (str): google channel/playlist id.

        Returns:
        Videos (str): returns list of videos.
    '''

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

def search_videos(api_key, content_id, output_folderpath, output_result_file):
    '''
    Search all the videos from a channel

        Parameters:
        api_key (str): Google developer Key
        content_id (str): Playlist or Channel id
        output_folderpath (str): folder
        output_result_file (str): output file to save youtube videos list

        Returns:
        file_path: returns
    '''
    youtube_prefix = 'https://www.youtube.com/watch?v='

    api_service_name = 'youtube'
    api_version = 'v3'

    #print('Searching videos from {} - {}...'.format(Config.orig_base, content_id))
    path_dest = join(output_folderpath, Config.orig_base, content_id )

    if not(exists(path_dest)):
        makedirs(path_dest)

    output_filepath = join(path_dest, output_result_file)

    # Checks if it has already been downloaded
    if exists(output_filepath):
        return output_filepath

    try:
        # Open output file
        f = open(output_filepath, 'w+')

        youtube = build(api_service_name, api_version, developerKey = api_key)

        if Config.orig_base == 'playlist':
            conv_id = content_id
        elif Config.orig_base == 'channel':
            res = youtube.channels().list(id = content_id,
                        part = 'contentDetails').execute()
            conv_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        else:
            conv_id = None

        # Get all videos from youtube channel/playlist.
        videos = get_videos(youtube, conv_id)

        print('Writing video links to file...')
        for video in tqdm(videos):
            f.write( youtube_prefix + video['snippet']['resourceId']['videoId'] + '\n' )

        print("Total videos: {0}".format( len(videos) ))
        f.close()

    except KeyboardInterrupt:
        print("KeyboardInterrupt Detected!")
        exit()

    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        exc_file = split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, exc_file, exc_tb.tb_lineno)
        return False

    return output_filepath

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', default = '')
    parser.add_argument('--content_id', default = '')
    parser.add_argument('--base_dir', default = './')
    parser.add_argument('--dest_dir', default = 'output')
    parser.add_argument('--output_search_file', default='youtube_videos.txt')
    args = parser.parse_args()
    output_path = join(args.base_dir, args.dest_dir)
    search_videos(args.api_key, args.content_id, output_path, args.output_search_file)

if __name__ == '__main__':
    main()
