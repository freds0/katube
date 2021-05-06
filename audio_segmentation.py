#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2021 Frederico Oliveira fred.santos.oliveira(at)gmail.com
#
# Adapted from https://gist.github.com/keithito/771cfc1a1ab69d1957914e377e65b6bd from Keith Ito: kito@kito.us
#
import argparse
import os
import json
from pydub import AudioSegment


class Segment:
    """
    Linked segments lists
    """
    def __init__(self, begin, end, text):
        self.begin = begin
        self.end = end
        self.text = text
        self.next = None
        self.filename = None
        self.gap = 0 # gap between segments (current and next)

    def set_next(self, next):
        self.next = next
        self.gap = next.begin - self.end

    def set_filename_and_id(self, filename, id):
        self.filename = filename
        self.id = id

    def merge_from(self, next):
        # merge two segments (current and next)
        self.next = next.next
        self.gap = next.gap
        self.end = next.end

    def duration(self, sample_rate):
        return (self.end - self.start - 1) / sample_rate


def create_segments_list_from_aeneas_json(json_path):
    """
    Creates a list of segments from the json file resulting from aeneas processing.
    """

    head = None
    with  open(json_path) as jfile :
        data = json.load(jfile)
        for i, fragment in enumerate(data['fragments']):
            text = fragment['lines']
            begin = float(fragment['begin'])*1000
            end = float(fragment['end'])*1000

            # Build a segment list
            segment = Segment(begin, end, text)
            if head is None:
                head = segment
            else:
                prev.set_next(segment)
            prev = segment

    return head


def create_audio_files_from_segments_list(audio_file, filenames_base, head_list, output_dir):
    """
    Segments an audio file from a segment list, saving the files in a folder.
        Parameters:
        audio_file (str): filepath of source audio file.
        filenames_base (str): Filename prefix of audio segmented files.
        head_list (str): Reference of the linked list of segments.
        output_dir (str): Folder to save segmented audio files.

        Returns:
        String: returns True or False
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sound = AudioSegment.from_file(audio_file)
    curr = head_list
    i = 1
    while curr is not None:
        begin = curr.begin
        end = curr.end
        text = curr.text
        audio_segment = sound[begin:end]
        filename = '{}-{:04d}.wav'.format(filenames_base, i)
        curr.set_filename_and_id(filename, i)
        filepath = os.path.join(output_dir, filename)
        try:
            audio_segment.export(filepath, 'wav')
        except IOError:
          print("Error: Writing audio file {} problem.".format(filepath))
          return False
        else:
            curr = curr.next
            i += 1
    return True


def create_metadata_from_segments_list(head_list, output_file):
    """
    Creates a csv file following the template: "filename | text"
        Parameters:
        head_list (str): Reference of the linked list of segments.
        output_file (str): csv output filename.

        Returns:
        String: returns True or False
    """
    separator = '|'
    curr = head_list
    try:
        f = open(output_file, "w")
        while curr is not None:
            text = curr.text
            filename = curr.filename.replace('.mp3', '')
            f.write(filename + separator + text[0] + '\n')
            curr = curr.next
        f.close()
    except IOError:
        print("Error: creating File {} problem.".format(output_file))
        return False
    return True


def segment_audio(audio_path, json_path, output_path, metadata_output_file, filename_base):
    """
    Performs the segmentation of the audio files and the creation of the csv file.
        Parameters:
        audio_path (str): filepath of source audio file.
        json_path (str): json file resulting from aeneas processing.
        output_path (str): Folder to save segmented audio files.
        metadata_output_file (str): csv output filename.
        filename_base (str): Filename prefix of audio segmented files.

        Returns:
        String: returns True or False
    """
    segments_list = create_segments_list_from_aeneas_json(json_path)
    if not create_audio_files_from_segments_list(audio_path, filename_base, segments_list, output_path):
        return False
    if not create_metadata_from_segments_list(segments_list, metadata_output_file):
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--audio_file', default='audio.mp3', help='Filename to input audio file')
    parser.add_argument('--filename_base', default='audio', help='Filename base of splited audios file. Ex. audio-0001.wav')
    parser.add_argument('--json_file', default='output.json', help='Filename of input json file')
    parser.add_argument('--output_dir', default='output', help='Output dir')
    parser.add_argument('--metadata_file', default='metadata.csv', help='Filename to metadata output file')
    args = parser.parse_args()

    audio_path = os.path.join(args.base_dir, args.audio_file)
    json_path = os.path.join(args.base_dir, args.json_file)
    output_dir = os.path.join(args.base_dir, args.output_dir)
    metadata_output_file = os.path.join(args.base_dir, args.output_dir, args.metadata_file)

    segment_audio(audio_path, json_path, output_dir, metadata_output_file, args.filename_base)

if __name__ == "__main__":
    main()