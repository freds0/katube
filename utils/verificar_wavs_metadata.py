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
            for wav_file in sorted(glob.glob(folder + "/wavs/*.wav")): 
                filename = wav_file.split('/')[-1]
                folder = '/'.join(wav_file.split('/')[0:-2])
                metadata_path = os.path.join(folder, args.csv_file)
                if not os.path.exists(metadata_path):
                    continue
                f = open(metadata_path, 'r')
                content = f.readlines()
                found = False
                for line in content:
                    filename_metadata, _, _, _ = line.split(separator)
                    if filename_metadata == filename:
                        found = True
                        break
                if not found:
                    total+=1
                    if not args.erase:    
                        print('Excluir arquivo: ' + wav_file)
                    else:
                        os.remove(wav_file)

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
