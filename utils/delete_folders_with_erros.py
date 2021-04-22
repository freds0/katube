import argparse
import glob
import os
import shutil

def erase_folders_with_error(args):
    total = 0
    for folder in sorted(glob.glob(args.base_dir + "/*/*")):
        if os.path.exists(folder) and os.path.isdir(folder):
            if os.path.isfile(os.path.join(folder, args.metada_file1)):
                try:
                    with open(os.path.join(folder, args.metada_file1)) as f:
                        content_file1 = f.readlines()
                except IOError:
                  print("Error: File {} does not appear to exist.".format(metada_file1))
                 # return False
            else:
                total += 1
                if not args.force:
                    print(folder)
                else:                 
                    shutil.rmtree(folder)
                continue
            if os.path.isfile(os.path.join(folder, args.metada_file2)):
                try:
                    with open(os.path.join(folder, args.metada_file2)) as f:
                        content_file2 = f.readlines()
                except IOError:
                  print("Error: File {} does not appear to exist.".format(filename2))
                  #return False
            else:
                total += 1
                if not args.force:
                    print(folder)
                else:
                    shutil.rmtree(folder)
                continue

            if not (len(content_file1) == len(content_file2)):
                total += 1
                if not args.force:
                    print(folder)
                else:
                    shutil.rmtree(folder)
    if args.force:
        print('Total folders erased: ', total)
    else:
        print('Total folders with problems: ', total)  
  
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./output/channel')
    parser.add_argument('--metada_file1', default='subtitles.csv')
    parser.add_argument('--metada_file2', default='transcript.csv')
    parser.add_argument('--force', action='store_true', default=False)
    args = parser.parse_args()
    erase_folders_with_error(args)

if __name__ == "__main__":
    main()
