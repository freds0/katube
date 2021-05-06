#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2021 Frederico Oliveira fred.santos.oliveira(at)gmail.com
#
#
import argparse
from os import makedirs
from os.path import join, exists, dirname
from textdistance import levenshtein
from tqdm import tqdm


def remove_punctuations(sentence):
    """
    Removes punctuations and unwanted characters from a sentence.
    """
    punctuations = '''—!()-[]{};:'"\,<>./?@#$%^&*_~'''
    sentence_with_no_punct = ""
    for char in sentence:
       if char not in punctuations:
           sentence_with_no_punct = sentence_with_no_punct + char
    return sentence_with_no_punct.strip()


def clear_sentences(sentence):
    """
    Converts the sentence to lowercase and removes unwanted characters.
    """
    sentence = sentence.lower()
    clean_sentence = remove_punctuations(sentence)
    return clean_sentence


def create_validation_file(input_file1, input_file2, prefix_filepath, output_file):
    """
    Given two files containing different transcriptions of audio files, this function calculates the similarity (levenshtein distance) between the sentences,
    saving the result in a third file.

        Parameters:
        input_file1 (str): First filepath. The contents of the file must follow the template: "filename | text"
        input_file2 (str): Second filepath. The contents of the file must follow the template: "filename | text"
        prefix_filepath: Prefix to be added to the file path within the output file.

        Returns:
        output_file (str): Returns output filepath. The content of the file follows the template: prefix_filepath/filename | text1 | text2 | similarity
    """

    # Loads the contents of the first input file
    try:
        with open(input_file1) as f:
            content_file1 = f.readlines()

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected!")
        exit()

    except IOError:
      print("Error: File {} does not appear to exist.".format(input_file1))
      return False

    # Loads the contents of the second input file
    try:
        with open(input_file2) as g:
            content_file2 = g.readlines()

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected!")
        exit()

    except IOError:
      print("Error: File {} does not appear to exist.".format(input_file2))
      return False

    # Both files must be the same length, otherwise there is an error.
    if not (len(content_file1) == len(content_file2)):
        print("Error: length File {} not igual to File {}.".format(content_file1, content_file2))
        return False

    # Checks if the output folder exists
    output_folderpath = dirname(output_file)

    if not(exists(output_folderpath)):
        makedirs(output_folderpath)

    # Saves the result to the output file.
    try:
        o_file = open(output_file, 'w')

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected!")
        exit()

    except IOError:
        print("Error: creating File {} problem.".format(output_file))
        return False

    # Iterate over the two files content simultaneously to calculate the similarity between the sentences.
    else:
        separator = '|'
        header = separator.join(['filename', 'subtitle', 'transcript', 'similarity'])
        o_file.write(header + '\n')

        # Input files must be csv files with the character "|" as a separator: filename | text
        for line1, line2 in tqdm(zip(content_file1, content_file2), total=len(content_file1)):

            file1, text1 = line1.split('|')
            file2, text2 = line2.split('|')

            # Clears sentences by removing unwanted characters.
            clean_text1 = clear_sentences(text1)
            clean_text2 = clear_sentences(text2)
            filepath = join(prefix_filepath, file1)

            # Calculates the levenshtein distance to define the normalized similarity (0-1) between two sentences.
            l = levenshtein.normalized_similarity(clean_text1, clean_text2)

            # Defines the output content and writes to a file.
            line = separator.join([filepath, text1.strip(), text2.strip(), str(l)])           
            o_file.write(line + '\n')

    finally:
        o_file.close()

    return True


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--input_file1', default='metadata1.csv', help='Input first filename')
    parser.add_argument('--input_file2', default='metadata2.csv', help='Input second filename')
    parser.add_argument('--prefix', default='', help='Prefix to filename on metadata output file.')
    parser.add_argument('--output_dir', default='output', help='Directory to save distances')
    parser.add_argument('--output_file', default='validation.csv', help='Output file with the template: "filename, text1, text2, similarity"')

    args = parser.parse_args()

    input_path_file1 = join(args.base_dir, args.input_file1)
    input_path_file2 = join(args.base_dir, args.input_file2)
    output_path_file = join(args.base_dir, args.output_dir, args.output_file)

    create_validation_file(input_path_file1, input_path_file2, args.prefix, output_path_file)


if __name__ == "__main__":
    main()