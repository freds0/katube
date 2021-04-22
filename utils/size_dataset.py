import argparse
import soundfile as sf
from os.path import isfile, join, dirname
import pandas as pd
import os
import csv
import tqdm

def get_seconds(x):
    f = sf.SoundFile(x)
    t = len(f) / f.samplerate
    return t


def calcular_horas(args):
    metadata = os.path.join(args.base_dir, args.csv_file)
    df = pd.read_csv(metadata, sep = '|', quoting=csv.QUOTE_NONE)
    total = 0
    for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
        path_file = os.path.join(row[0])
        temp = get_seconds(path_file)
        total += temp

    print('Total em Segundos: {}'.format(total))
    print('horas: {}'.format(total/3600))
    print('Minutos: {}'.format(total%3600/60))
    print('Segundos: {}'.format( (total%3600)%60))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--csv_file', default='metadata.csv', help='Name of csv file')
    args = parser.parse_args()
    calcular_horas(args)

if __name__ == "__main__":
    main()
