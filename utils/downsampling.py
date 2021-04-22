import argparse
import glob
import os
from os import makedirs
from os.path import join, exists
import tqdm

number_bits = 16
encoding = "signed-integer"
number_channels = 1

def downsampling(folder, wav_dir, new_wav_dir, sample_rate, force):
    for wav_path in glob.glob(join(folder, wav_dir) + "/*.wav"):           
        prev = '/'.join(wav_path.split('/')[0:5])            
        filename = wav_path.split('/')[-1]
        new_wav_path = join(prev, new_wav_dir, filename)
        dir_path = os.path.dirname(new_wav_path)  
        if not force:    
            print("sox %s -V0 -c %d -r %d -b %d -e %s %s"% (wav_path, int(number_channels), int(sample_rate), number_bits, encoding, new_wav_path))
        else:
            os.makedirs(dir_path, exist_ok=True)
            os.system("sox %s -V0 -c %d -r %d -b %d -e %s %s"% (wav_path, int(number_channels), int(sample_rate), number_bits, encoding, new_wav_path))
    return True

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', default='./output/channel/')  
  parser.add_argument('--wav_dir', default='wavs', help='Name of the origin directory of wav files')
  parser.add_argument('--new_wav_dir', default='wavs22', help='Name of the origin directory of wav files')
  parser.add_argument('--sample_rate', default=22050, help='Sample rate of destination wav files')
  parser.add_argument('--force', action='store_true', default=False)
  args = parser.parse_args()
  for folder in glob.glob(args.base_dir + "/**"): 
    downsampling(folder, args.wav_dir, args.new_wav_dir, args.sample_rate, args.force)

if __name__ == "__main__":
  main()
