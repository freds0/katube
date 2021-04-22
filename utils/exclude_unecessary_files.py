import argparse
import glob
import os
import tqdm

def exclude_files(args):

    total = 0
    for folder in tqdm.tqdm(sorted(glob.glob(args.base_dir + '/*/*'))):

        if not os.path.exists(folder) or not os.path.isdir(folder):
            continue

        old_metadata_file = os.path.join(folder, 'save.csv')
        metadata_file = os.path.join(folder, 'metadata.csv')

        if os.path.exists(metadata_file):
            continue

        if not os.path.exists(old_metadata_file):
            print('Verify the folder: ' + folder)
            continue
            #exit()

        folder_name = folder.split('/')[-1]
        json_file = os.path.join(folder, folder_name + '.json')
        if not os.path.isfile(json_file):
            print(json_file)
            continue      
        srt_file = os.path.join(folder, folder_name + '.srt')
        if not os.path.isfile(srt_file):
            print(srt_file)
            continue           
        txt_file = os.path.join(folder, folder_name + '.txt')
        if not os.path.isfile(txt_file):
            print(txt_file)
            continue  
        subtitles_file = os.path.join(folder, 'subtitles.csv')
        if not os.path.isfile(subtitles_file):
            print(subtitles_file)
            continue 
        transcript_file = os.path.join(folder, 'transcript.csv')
        if not os.path.isfile(transcript_file):
            print(transcript_file)
            continue 
        validation_file = os.path.join(folder, 'validation.csv')
        if not os.path.isfile(validation_file):
            print(validation_file)
            continue 
        delete_file = os.path.join(folder, 'delete.csv')
        if not os.path.isfile(delete_file):
            print(delete_file)
            continue 
   
        try:
            f = open(old_metadata_file)
            content_file = f.readlines()[1:]
        except IOError:
          print("Error: File {} does not appear to exist.".format(old_metadata_file))
          return False
        else:
            f.close()

        if (len(content_file) == len(os.listdir(os.path.join(folder, args.wav_folder)))):
            total +=1
            if not args.force:
                print('mv ' + old_metadata_file + ' ' + metadata_file)
            else:
                os.remove(json_file)
                os.remove(srt_file)
                os.remove(txt_file)
                os.remove(subtitles_file)
                os.remove(transcript_file)
                os.remove(validation_file)
                os.remove(delete_file)
                os.rename(old_metadata_file, metadata_file)

        else:
            print('Founded diferences between ' + folder + ' and wavs.')



def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./output/channel/')  
  parser.add_argument('--wav_folder', default='wavs', help='Name of old wavs folder, to erase')
  parser.add_argument('--force', action='store_true', default=False)
  args = parser.parse_args()
  exclude_files(args)

if __name__ == "__main__":
  main()