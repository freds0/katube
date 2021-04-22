import argparse
import glob
import os
import csv

        
def generate_file(args):
    try:
        f = open(os.path.join(args.base_dir, args.output_file), 'w')
        for folder in sorted(glob.glob(os.path.join(args.base_dir, args.input_folder) + '/*/*')):
            if os.path.exists(folder) and os.path.isdir(folder):
                youtube_link = 'https://www.youtube.com/watch?v=' + folder.split('/')[-1]
                f.write(youtube_link + '\n')
        f.close()
    except IOError:
      print("Error: Create file {}.".format(args.output_file))
      return False
    
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--input_folder', default='./output/playlist')
    parser.add_argument('--output_file', default='youtube_ignored_videos.txt', help='Name of csv file')
    args = parser.parse_args()
    generate_file(args)

if __name__ == "__main__":
    main()

