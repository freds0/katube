import argparse
import glob
import os
import shutil
import pandas as pd
import csv
import tqdm

def deletar(args):
    total = 0
    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*/*"))):
        if os.path.exists(folder) and os.path.isdir(folder):
            metadata = os.path.join(folder, args.input_file)
            if not os.path.exists(metadata):
                continue            
            df = pd.read_csv(metadata, sep = '|', quoting=csv.QUOTE_NONE)
            # Creating save files
            save_df = df[df['similarity'] >= float(args.min_value)].copy()
            filenames = save_df['filename'].apply(lambda x: x.split('/')[-1])
            save_df['filename'] = filenames
            save_df.to_csv(os.path.join(folder, args.save_file), sep = '|', index=False, quoting=csv.QUOTE_NONE)
            # Creating delete files
            delete_df = df[df['similarity'] < float(args.min_value)].copy()
            filenames = delete_df['filename'].apply(lambda x: x.split('/')[-1])
            delete_df['filename'] = filenames
            delete_df.to_csv(os.path.join(folder, args.delete_file), sep = '|', index=False, quoting=csv.QUOTE_NONE)

            total += 1

    print('Total save/delete files metadata created: ', total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./output/channel/')
    parser.add_argument('--input_file', default='validation.csv')
    parser.add_argument('--save_file', default='save.csv')
    parser.add_argument('--delete_file', default='delete.csv')
    parser.add_argument('--min_value', default=0.90, help='Minimal value of levenshtein distance') 
    args = parser.parse_args()
    deletar(args)

if __name__ == "__main__":
    main()
