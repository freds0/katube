import argparse
import tarfile
import os
import tqdm

def create_brspech_file(input_file, output_file, min_value):
    root = 'BRSpeech-ASR'
    write_mode = 'w:bz2' # 'w' or 'w:gz' or 'w:bz2'
    internal_folder = 'wavs'

    tar_file = tarfile.open(output_file, mode=write_mode)

    num_lines = sum(1 for line in open(input_file,'r'))
    in_file = open(input_file, "r")
    folders_list = []
    for line in tqdm.tqdm(in_file, total=num_lines):

        file, subtitle, transcript, levenshtein = line.split('|')

        folder = file.split('/')[-3]
        folder_path = '/'.join(file.split('/')[:-2])
        filename = file.split('/')[-1]

        #if float(levenshtein) > float(min_value):

        tar_file.add(file, arcname=os.path.join(root, folder, internal_folder, filename))
        folders_list.append(folder_path)

    for folder in folders_list:
        tar_file.add(os.path.join(folder, 'validation.csv'), arcname=os.path.join(root, folder, internal_folder, filename))

    tar_file.add(input_file, arcname=os.path.join(root, 'metadata.csv'))
    tar_file.close()
    in_file.close()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--metadata_file', default='metadata_all.csv', help='Input filename')
    parser.add_argument('--output_file', default='BRSpeech.tar.bz', help='Tar.bz file')
    parser.add_argument('--min_value', default=0.95, help='Minimal value of levenshtein distance')

    args = parser.parse_args()

    input_file = os.path.join(args.base_dir, args.metadata_file)
    output_file = os.path.join(args.base_dir, args.output_file)

    create_brspech_file(input_file, output_file, args.min_value)

if __name__ == "__main__":
    main()
