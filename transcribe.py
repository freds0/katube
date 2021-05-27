#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2021 Frederico Oliveira fred.santos.oliveira(at)gmail.com
#
#
import argparse
import sys
from os import makedirs
from os.path import join, exists, basename, split
from glob import glob
from tqdm import tqdm
import librosa
import requests
import soundfile as sf
import json


def convert_audios_samplerate(input_path, output_path, new_sample_rate):
    """
    Converts all audio files within a folder to a new sample rate.
        parameters:
            input_path: input folder path with wav files.
            output_path: output folder path to save converted wav files.

        Returns:
            Boolean: True of False.
    """

    if not(exists(output_path)):
        makedirs(output_path)

    for wavfile_path in tqdm(sorted(glob(input_path + "/*.wav"))):
        try:
            filename = basename(wavfile_path)
            data, sample_rate = librosa.load(wavfile_path)
            data = data.T
            new_data = librosa.resample(data, sample_rate, new_sample_rate)
            output_file = join(output_path, filename)
            sf.write(output_file, new_data, new_sample_rate)
        except:
            print('Error converting ' + wavfile_path)
            return False

    return True


def get_transcript(wavefile_path):
    """
    Custom function to access a service STT. You must adapt it to use your contracted STT service.
        parameters:
            wavefile_path: wav filepath which will be transcribed.

        Returns:
            Text (str): Transcription of wav file.
    """
    with open(wavefile_path,'rb') as file_data:
        headers_raw = {
                'Content-Type': "application/x-www-form-urlencoded",
            	'endpointer.enabled': "true",
            	'endpointer.waitEnd': "5000",
            	'endpointer.levelThreshold': "5",
            	'decoder.confidenceThreshold': "10",
            	'decoder.maxSentences': "1",
            	'decoder.wordDetails': "0",
        }
        try:
            res = requests.post(url='https://your_url_here',
                                data=file_data,
                                headers=headers_raw)

            res.encoding='utf-8'
        except KeyboardInterrupt:
            print("KeyboardInterrupt Detected!")
            exit()
        except:
            #json_data=[{"message": "ERROR NO SPEECH"}]
            #return json_data
            return False
    return res.text


def transcribe_audios(input_path, output_file):
    """
    Iterate over the wav files inside a folder and transcribe them all.
        parameters:
            input_path: input wavs folder.
            output_file: output file to save the transcriptions following the template: "filename| transcription"

        Returns:
            Boolean: True or False.
    """

    out = open(output_file, 'w')

    for wavfile_path in tqdm(sorted(glob(input_path + "/*.wav"))):
        filename = basename(wavfile_path)
        # Four attempts if connection error occurs.
        for attempts in range(4):

            if attempts != 0:
                print('Attempt - {}...'.format(attempts))

            transcript = get_transcript(wavfile_path)
            if not transcript:
                text = ''
                break

            try:
                transcript_json = json.loads(str(transcript).replace("'", '"'))
                if transcript_json[0]['result_status'] == 'RECOGNIZED':
                    text = transcript_json[0]['alternatives'][0]['text']
                    break
                else:
                    #print("Erro")
                    text = ''
                    break
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                exc_file = split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Transcribing error: ")
                print(exc_type, exc_file, exc_tb.tb_lineno)

        else:
            text = ''

        out.write("{}|{}\n".format(str(filename),str(text)))

    out.close()
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--transcription_file', default='transcript.txt', help='Filename to save the transcripts')
    parser.add_argument('--input_dir', default='wavs', help='Directory of wav files')
    parser.add_argument('--temp_dir', default='wavs_16k', help='Directory to save wav files with sample rate (16k)')
    parser.add_argument('--new_sample_rate', default=16000, help='Sample rate used by the transcription api.')

    args = parser.parse_args()

    input_path = join(args.base_dir, args.input_dir)
    converted_wavs_temp_path = join(args.base_dir,args.temp_dir)
    output_file = join(args.base_dir,args.transcription_file)

    # Convert audio sample rate
    print('Converting wav files...')
    convert_audios_samplerate(input_path, converted_wavs_temp_path, args.new_sample_rate)

    # Transcribe all wavs files
    print('Transcribing...')
    transcribe_audios(converted_wavs_temp_path, output_file)


if __name__ == "__main__":
  main()
