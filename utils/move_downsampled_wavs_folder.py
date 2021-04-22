import glob
import os
import shutil
import tqdm
import argparse

def remove_old_folder_wavs(args):
    total_erased = 0
    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + "/*/*"))):
        if os.path.exists(folder) and os.path.isdir(folder):
            old_folder = os.path.join(folder, args.old_folder)
            new_folder = os.path.join(folder, args.new_folder)
            if not os.path.exists(old_folder):
                print('Verify folder: ' + old_folder)
                continue
                #exit()
            if not os.path.exists(new_folder):
                print('Verify folder: ' + new_folder)
                continue
                #exit()
            total_erased+=1
            if not args.force:
                print('rm ' + old_folder)
                print('mv ' + new_folder + ' ' + old_folder)
            else:
                shutil.rmtree(old_folder) 
                os.rename(new_folder, old_folder)                

    if args.force:
        print('Total modified folders ', total_erased)
    else:
        print('Total to be modified folders ', total_erased)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./output/channel/')  
  parser.add_argument('--old_folder', default='wavs', help='Name of old wavs folder, to erase')
  parser.add_argument('--new_folder', default='wavs22', help='Name of new wavs folder')
  parser.add_argument('--force', action='store_true', default=False)
  args = parser.parse_args()
  remove_old_folder_wavs(args)

if __name__ == "__main__":
  main()
