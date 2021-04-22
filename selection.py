import argparse
import soundfile as sf
from os.path import isfile, join, dirname
import pandas as pd
import os
import csv
import tqdm

separator = '|'

def select(metadata, output_filepath, min_similarity, force):

    try:
        f = open(metadata)
        content_file = f.readlines()[1:]
    except IOError:
      print("Error: File {} does not appear to exist.".format(input_file1))
      return False
    else:
        f.close()

    output_file = open(output_filepath, 'w')
    header = separator.join(['filename', 'subtitle', 'transcript', 'similarity']) + '\n'
    output_file.write(header)

    for line in content_file:
        filepath, text1, text2, similarity = line.split(separator)
        if float(similarity) >= float(min_similarity):
            filename = os.path.basename(filepath)
            line = separator.join([filename.strip(), text1.strip(), text2.strip(), str(similarity).strip()])        
            output_file.write(line + '\n')            
        else:
            if force:
                os.remove(filepath)
            else:
                print('rm {}'.format(filepath))

    output_file.close()

    return True
       
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--csv_file', default='validation.csv', help='Name of csv file')
    parser.add_argument('--min_value', default=0.90, help='Minimal value of levenshtein distance') 
    parser.add_argument('--save_file', default='metadata.csv')
    parser.add_argument('--force', action='store_true', default=False)
    args = parser.parse_args()

    metadata = os.path.join(args.base_dir, args.csv_file)
    output_filepath = join(args.base_dir, args.save_file)

    select(metadata, output_filepath, args.min_value, args.force)

if __name__ == "__main__":
    main()
