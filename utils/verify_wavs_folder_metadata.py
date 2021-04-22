import argparse
import glob
import os
from os import makedirs
from os.path import join, exists
import tqdm

separator = '|'

def verify_folder(args):

    i = 0
    for wav_file in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*/wavs/*.wav"))): 

            filename = wav_file.split('/')[-1]
            folder = '/'.join(wav_file.split('/')[0:-2])

            metadata_path = join(folder, args.csv_file)
            if not exists(metadata_path):
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
                i+=1
                if not args.erase:    
                    print('Excluir arquivo: ' + wav_file)
                else:
                    os.remove(wav_file)


    print('Total: ' + str(i) + ' arquivos')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./')  
  parser.add_argument('--folder', default='', help='Name of the origin directory of wav files')
  parser.add_argument('--csv_file', default='metadata.csv')
  parser.add_argument('--erase', action='store_true', default=False)
  args = parser.parse_args()
  verify_folder(args)

if __name__ == "__main__":
  main()
