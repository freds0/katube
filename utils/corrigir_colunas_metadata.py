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
            #new_df = df[df['levenshtein'] >= float(args.min_value)].copy()
            if set(['levenshtein']).issubset(df.columns):
                continue
            print(metadata)
            df.rename(columns={"text": "subtitle", "similarity" : "levenshtein"}, inplace=True)
            df.to_csv(os.path.join(folder, args.input_file), sep = '|', index=False, quoting=csv.QUOTE_NONE)
            total += 1
    print('Total created metadata: ', total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--input_file', default='validation.csv')
    #parser.add_argument('--delete_file', default='delete.csv')
    args = parser.parse_args()
    deletar(args)

if __name__ == "__main__":
    main()
