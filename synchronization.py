#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2021 Frederico Oliveira fred.santos.oliveira(at)gmail.com
#
#
import argparse
import sys
from os.path import split, join
from aeneas.executetask import ExecuteTask
from aeneas.task import Task


def create_aeneas_json_file(audio_path, text_path, output_path):
    """
    Use the api aeneas to synchronize audio and text.

        Parameters:
        audio_path (str): audio filepath.
        text_path (str): text filepath.
        output_path (str): output json filepath.

        Returns:
        Boolean: True or False.
    """
    try:
        # create Task object
        config_string = u"task_language=por|is_text_type=plain|os_task_file_format=json|task_adjust_boundary_percent_value=50|mfcc_mask_nonspeech_l2=True"
        task = Task(config_string=config_string)
        task.audio_file_path_absolute = u"{}".format(audio_path)
        task.text_file_path_absolute = u"{}".format(text_path)
        task.sync_map_file_path_absolute = u"{}".format(output_path)

        # process Task
        ExecuteTask(task).execute()

        # output sync map to file
        task.output_sync_map_file()

    except KeyboardInterrupt:
        print("KeyboardInterrupt Detected!")
        exit()

    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        exc_file = split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, exc_file, exc_tb.tb_lineno)
        return False

    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--audio_file', default='audio.mp3', help='Filename to input audio file')
    parser.add_argument('--text_file', default='input.txt', help='Filename of input text')
    parser.add_argument('--output_file', default='output.json', help='Output json file')
    args = parser.parse_args()

    audio_path = join(args.base_dir, args.audio_file)
    text_path = join(args.base_dir, args.text_file)
    output_path = join(args.base_dir, args.output_file)
    create_aeneas_json_file(audio_path, text_path, output_path)

if __name__ == "__main__":
    main()
