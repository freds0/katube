import argparse
import glob
from os import makedirs
from os.path import join, exists
import librosa
import requests
import soundfile as sf
import json
import tqdm
import sys, os

new_sample_rate = 16000

def convert_audios_samplerate(input_path, output_path):

    if not(exists(output_path)):
        makedirs(output_path)

    for wavfile_path in tqdm.tqdm(sorted(glob.glob(input_path + "/*.wav"))):
        try:
            filename = wavfile_path.split('/')[-1]
            #print(filename)
            data, sample_rate = librosa.load(wavfile_path)
            data = data.T
            data_16k = librosa.resample(data, sample_rate, new_sample_rate)
            output_file = join(output_path, filename)
            sf.write(output_file, data_16k, new_sample_rate)
        except:
            print('erro converting ' + wavfile_path)
            return False

    return True

def get_transcript(wavefile_path):
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
            res = requests.post(url='https://your_asr_service.com',
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
    with open(output_file, 'w') as out:
        for wavfile_path in tqdm.tqdm(sorted(glob.glob(input_path + "/*.wav"))):
            filename = wavfile_path.split('/')[-1]

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
                        #print(transcript_json[0]['alternatives'][0]['text'])
                        text = transcript_json[0]['alternatives'][0]['text']
                        break
                    else:
                        #print("Erro")
                        text = ''
                        break
                except:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    exc_file = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("Transcribing error: ")
                    print(exc_type, exc_file, exc_tb.tb_lineno)

            else:
                text = ''

            out.write("{}|{}\n".format(str(filename),str(text)))

    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--transcription_file', default='transcript.txt', help='Filename to save the transcripts')
    parser.add_argument('--input_dir', default='wavs', help='Directory of wav files')
    parser.add_argument('--temp_dir', default='wavs_16k', help='Directory to save wav files with sample rate (16k)')
    args = parser.parse_args()

    input_path = join(args.base_dir, args.input_dir)
    converted_wavs_temp_path = join(args.base_dir,args.temp_dir)
    output_file = join(args.base_dir,args.transcription_file)
    # Convert audio sample rate
    print('Converting wav files...')
    convert_audios_samplerate(input_path, converted_wavs_temp_path)
    # Transcript
    print('Transcribing...')
    transcribe_audios(input_path, output_file)

if __name__ == "__main__":
  main()
