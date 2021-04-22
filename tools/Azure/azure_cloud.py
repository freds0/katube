import azure.cognitiveservices.speech as speechsdk
from config import Config as config
import os
from pathlib import Path
import tqdm
import glob

import pandas as pd

def pass_through_files(speech_config=None):
    '''
    Realiza a análise de todos os arquivos no diretório desejado 
    para a transcrição.
    '''

    transcribed_texts = []
    file_names = []

    for filepath in tqdm.tqdm(sorted(glob.glob(config.base_dir + '/**/*.wav', recursive=True))):
        transcription = run_transcription(filepath, speech_config)

        transcribed_texts.append(transcription)
        file_names.append(filepath.split('/')[-1])


    return transcribed_texts, file_names


def run_transcription(filepath='./', speech_config=None):
    '''
    Realiza a transcrição de um único áudio de forma assíncrona.
    '''
    
    audio_input = speechsdk.AudioConfig(filename=filepath)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, 
                                                    audio_config=audio_input, 
                                                    language="pt-BR")

    result_future = speech_recognizer.recognize_once_async()

    # Retrieve the recognition result. This blocks until recognition is complete.
    result = result_future.get()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # print(result.text)
        return result.text
    else:
        return ''
    # elif result.reason == speechsdk.ResultReason.NoMatch:
    #     print("No speech could be recognized: {}".format(result.no_match_details))
    # elif result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = result.cancellation_details
    #     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         print("Error details: {}".format(cancellation_details.error_details))

def make_matadata(file_names, transcribed_texts):
    """
    Cria um arquivo csv com os textos transcritos.
    """

    os.makedirs(config.output_path, exist_ok=True)

    df = pd.DataFrame()

    for file_name, text in zip(file_names, transcribed_texts):
        df = df.append({'A': file_name, 'B' : text}, ignore_index=True)

    df.to_csv(os.path.join(config.output_path, config.output_name.lower() + '_transcribed_azure' + '.csv'), sep='|', index=False, header=False, quotechar="'")

def main():

    speech_config = speechsdk.SpeechConfig(subscription=config.speech_key, region=config.service_region)
    transcribed_texts, file_names = pass_through_files(speech_config)
    make_matadata(file_names, transcribed_texts)


if __name__ == '__main__':
    main()