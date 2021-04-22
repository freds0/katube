import os
from urllib.parse import parse_qs, urlparse
import argparse
import tqdm

def check_line(youtube_link, output_path):
    with open(output_path, 'r') as read_obj:
        for line in read_obj:
            if youtube_link in line:
                return True
    return False

def get_id(input_path, output_path):
    input_file = open(input_path, "r")
    output_file = open(output_path, "a")

    for youtube_link in tqdm.tqdm(input_file):
        if youtube_link.startswith('#'):
            if check_line(youtube_link, output_path):
                print("Ignoring... {}".format(youtube_link))
                continue
            output_file.write(youtube_link)
        else:
            if check_line(youtube_link.split('/')[-1], output_path):
                continue
            output_file.write(youtube_link.split('/')[-1])

    input_file.close()
    output_file.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default = './')
    parser.add_argument('--orig_file', default = 'youtube_channels.txt')
    parser.add_argument('--output_file', default = 'channels_id.txt')
    args = parser.parse_args()
    input_path = os.path.join(args.base_dir, args.orig_file)
    output_path = os.path.join(args.base_dir, args.output_file)
    get_id(input_path, output_path)

if __name__ == '__main__':
    main()