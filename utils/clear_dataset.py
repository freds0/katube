import argparse
import glob
import os
import shutil
def clear_dataset(args):
    total = 0
    for folder in sorted(glob.glob(args.base_dir + "/*/*")):
        if os.path.isdir(folder) and not os.path.exists(os.path.join(folder, 'metatada.csv')):
            total+=1
            if not args.force:
                print(folder)
            else:
                shutil.rmtree(folder)
        if os.path.isdir(folder) and not os.listdir(folder):
            total+=1
            if not args.force:
                print(folder)
            else:
                shutil.rmtree(folder)
        wavs_folder = os.path.join(folder, args.wavs_folder)
        if os.path.exists(wavs_folder) and os.path.isdir(wavs_folder):            
            if not os.listdir(wavs_folder): #if len (os.listdir(wavs_folder)) == 0:
                total+=1
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
    parser.add_argument('--wavs_folder', default='wavs', help='Input wavs folder')
    parser.add_argument('--force', action='store_true', default=False)

    args = parser.parse_args()
    clear_dataset(args)

if __name__ == "__main__":
    main()





