import argparse
import soundfile as sf
from os.path import isfile, join, dirname, exists
import pandas as pd
import os
import csv
import tqdm

def delete_wavs(args):
    metadata_file = os.path.join(args.base_dir, args.csv_file)
    if not exists(metadata_file):
        print('File {} not found.'.format(metadata_file))
        return

    df = pd.read_csv(metadata_file, sep = '|', quoting=csv.QUOTE_NONE)
    total = 0
    total_deleted = 0

    for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
        path_file = os.path.join(row[0])
        if os.path.exists(path_file):
            total_deleted += 1
            if not(args.force):
                print(path_file)
            else:
                os.remove(path_file)

    if not(args.force):
        print('Total wavs to be deleted: ', total_deleted)
    else:
        print('Total wavs deleted: ', total_deleted)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--csv_file', default='delete.csv', help='Name of csv file')
    parser.add_argument('--force', action='store_true', default=False)
    args = parser.parse_args()
    delete_wavs(args)

if __name__ == "__main__":
    main()
