import argparse
import soundfile as sf
import pandas as pd
import csv
import glob
import os
import tqdm

def generate_metadata(args):
    separator = '|'
    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*/*"))):        
        if os.path.isdir(folder) and os.path.exists(os.path.join(folder, args.csv_file)):
            output_file = open(os.path.join(folder, args.output_file), 'w')        
            line = separator.join(['filename', 'subtitle', 'transcript', 'levenshtein'])
            output_file.write(line + '\n')
            df = pd.read_csv(os.path.join(folder, args.csv_file), sep = '|', quoting=csv.QUOTE_NONE)
            for index, row in df.iterrows():
                filename = row[0].split('/')[-1]                
                line = separator.join([filename, row[1], row[2], str(row[3])])
                output_file.write(line + '\n')           
            output_file.close()                       


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--csv_file', default='metadata.csv', help='Name of csv file')  
    parser.add_argument('--output_file', default='metadata_new.csv', help='Name of csv file')
    args = parser.parse_args()
    generate_metadata(args)

if __name__ == "__main__":
    main()
