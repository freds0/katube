import glob
import os
import shutil
import tqdm
import argparse

def remove_folder(args):
    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*/*"))):
        if os.path.exists(folder) and os.path.isdir(folder):
            old_file = os.path.join(folder, 'metadata.csv')
            new_file = os.path.join(folder, 'metadata_new.csv')
            if not os.path.exists(old_file):
                print(folder)
                continue
            if not os.path.exists(new_file):
                print(folder)
                continue

            os.remove(old_file)
            os.rename(new_file, old_file)
            #print(old_file)
            #print(new_file)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./BRSpeech-ASR-beta3/')  
  args = parser.parse_args()
  remove_folder(args)

if __name__ == "__main__":
  main()
