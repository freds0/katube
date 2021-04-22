import argparse
import soundfile as sf
import pandas as pd
from os.path import join, exists
import csv

        
def generate_metadata(args):

    metadata_file = join(args.base_dir, args.csv_file)
    if not exists(metadata_file):
        print('File {} not found.'.format(metadata_file))
        return

    df = pd.read_csv(metadata_file, sep = '|', header=None, quoting=csv.QUOTE_NONE)
    new_df = df[df[3] >= float(args.min_value)]
    new_df.to_csv(join(args.base_dir, args.save_file), sep = '|', header=False, index=False, quoting=csv.QUOTE_NONE)
    new_df = df[df[3] < float(args.min_value)]
    new_df.to_csv(join(args.base_dir, args.delete_file), sep = '|', header=False, index=False, quoting=csv.QUOTE_NONE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--csv_file', default='metadata_complete.csv', help='Name of csv file')
    parser.add_argument('--min_value', default=0.90, help='Minimal value of levenshtein distance')   
    parser.add_argument('--save_file', default='save.csv', help='Name of csv file')
    parser.add_argument('--delete_file', default='delete.csv', help='Name of csv file')
    args = parser.parse_args()
    generate_metadata(args)

if __name__ == "__main__":
    main()
