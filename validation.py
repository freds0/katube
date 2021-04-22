import argparse
import glob
from os import makedirs
from os.path import join, exists, isdir
import string
import csv
import textdistance
import tqdm


def remove_punctuations(sentence):
    punctuations = '''—!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in sentence:
       if char not in punctuations:
           no_punct = no_punct + char
    return no_punct.strip()

def clear_sentences(sentence1, sentence2):
    sentence1 = sentence1.lower()
    sentence2 = sentence2.lower()
    clean_sentence1 = remove_punctuations(sentence1)
    clean_sentence2 = remove_punctuations(sentence2)
    return clean_sentence1, clean_sentence2

def create_validation_file(input_file1, input_file2, basename, output_file):

    try:
        with open(input_file1) as f:
            content_file1 = f.readlines()
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected!")
        exit()
    except IOError:
      print("Error: File {} does not appear to exist.".format(input_file1))
      return False

    try:
        with open(input_file2) as g:
            content_file2 = g.readlines()
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected!")
        exit()
    except IOError:
      print("Error: File {} does not appear to exist.".format(input_file2))
      return False

    if not (len(content_file1) == len(content_file2)):
        print("Error: length File {} not igual to File {}.".format(content_file1, content_file2))
        return False

    try:
        o_file = open(output_file, 'w')
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected!")
        exit()
    except IOError:
        print("Error: creating File {} problem.".format(output_file))
        return False
    else:
        separator = '|'
        header = separator.join(['filename', 'subtitle', 'transcript', 'similarity'])
        o_file.write(header + '\n')
        for line1, line2 in tqdm.tqdm(zip(content_file1, content_file2), total=len(content_file1)):
            file1, text1 = line1.split('|')
            file2, text2 = line2.split('|')
            clean_text1, clean_text2 = clear_sentences(text1, text2)
            filepath = join(basename, file1)
            l = textdistance.levenshtein.normalized_similarity(clean_text1, clean_text2)
            line = separator.join([filepath, text1.strip(), text2.strip(), str(l)])           
            o_file.write(line + '\n')
    finally:
        o_file.close()

    return True

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--metadata_text', default='metadata_text.csv', help='Input filename')
    parser.add_argument('--metadata_transcript', default='metadata_transcript.csv', help='Input filename')
    parser.add_argument('--prefix', default='', help='Prefix to filename on metadata output file.')
    parser.add_argument('--output_dir', default='output', help='Directory to save distances')
    parser.add_argument('--output_file', default='validation.csv', help='Metadata file with sentences with minimal similarity')

    args = parser.parse_args()

    input_path_file1 = join(args.base_dir, args.metadata_text)
    input_path_file2 = join(args.base_dir, args.metadata_transcript)
    output_path_file = join(args.base_dir, args.output_dir, args.output_file)

    create_validation_file(input_path_file1, input_path_file2, args.prefix, output_path_file)

if __name__ == "__main__":
    main()
