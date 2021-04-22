import argparse
import glob
import os
import shutil
import pandas as pd
import csv
import tqdm

def deletar(args):
    total = 0
    separator = '|'
    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*/*"))):
        if os.path.exists(folder) and os.path.isdir(folder):
            metadata_path = os.path.join(folder, args.csv_file)
            if not os.path.exists(metadata_path):
                continue
            f = open(metadata_path, 'r')
            content = f.readlines()[1:]
            for line in content:
                filename_metadata, _, _, _ = line.split(separator)
                filepath = os.path.join(folder, 'wavs', filename_metadata)
                print(filepath)
                if os.path.exists(filepath):
                    continue
                else:
                    total+=1
                    if not args.erase:
                        print('Excluir arquivo: ' + filename_metadata)
                    else:
                        os.remove(filename_metadata)

    if not args.erase:
        print('Total wavs to be erased: ', total)
    else:
        print('Total erased: ', total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--csv_file', default='metadata.csv')
    parser.add_argument('--erase', action='store_true', default=False)
    #parser.add_argument('--delete_file', default='delete.csv')

    args = parser.parse_args()
    deletar(args)

if __name__ == "__main__":
    main()
