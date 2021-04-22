import argparse
import glob
import os
import pandas as pd
import csv
import tqdm

def deletar(args):
    total = 0
    for metadata_file in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*/*/" + args.input_file))):
        if os.path.isfile(metadata_file):         
            df = pd.read_csv(metadata_file, sep = '|', quoting=csv.QUOTE_NONE)
            folder_path = os.path.join(*metadata_file.split('/')[0:-1])
            for index, row in df.iterrows():                 
                path_file = os.path.join(folder_path, args.wavs_folder, row[0])
                if os.path.exists(path_file):
                    total += 1
                    if not(args.force):
                        print(path_file)
                    else:
                        os.remove(path_file)

    if args.force:    
        print('Total wav files erased: ', total)
    else:
        print('Total wav files read to be erased: ', total)  

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./output/channel/')
    parser.add_argument('--input_file', default='delete.csv')
    parser.add_argument('--wavs_folder', default='wavs', help='Input wavs folder')
    parser.add_argument('--force', action='store_true', default=False)
    args = parser.parse_args()
    deletar(args)

if __name__ == "__main__":
    main()
