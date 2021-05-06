#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2021 Frederico Oliveira fred.santos.oliveira(at)gmail.com
#
#
import argparse
import sys
from os import remove
from os.path import basename, join, split


def select(input_csv_file, output_filepath, min_similarity, force):
    """
    Given a csv file, selects only files with similarity greater than min_similarity and deletes the others.

        Parameters:
        input_csv_file (str): Input csv filepath following the template: "filename| subtitle | transcript | similarity"
        output_filepath (str): Output csv filepath following the template: "filename| subtitle | transcript | similarity"
        min_similarity (float): Threshold that defines which files will be excluded.
        force (boolean):  if True, it will remove the files, otherwise only show what files wil be removed.

        Returns:
        Boolean: returns True or False.
    """

    try:
        f = open(input_csv_file)
        content_file = f.readlines()[1:]

    except IOError:
      print("Error: File {} does not appear to exist.".format(input_csv_file))
      return False

    else:
        f.close()

    try:
        separator = '|'
        output_file = open(output_filepath, 'w')
        header = separator.join(['filename', 'subtitle', 'transcript', 'similarity']) + '\n'
        output_file.write(header)

        for line in content_file:
            filepath, text1, text2, similarity = line.split(separator)

            # Selects only files with similarity greater than min_similarity
            if float(similarity) >= float(min_similarity):
                filename = basename(filepath)
                line = separator.join([filename.strip(), text1.strip(), text2.strip(), str(similarity).strip()])
                output_file.write(line + '\n')

            # otherwise, delete the file.
            else:
                if force:
                    remove(filepath)
                else:
                    print('rm {}'.format(filepath))

        output_file.close()

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
    parser.add_argument('--csv_file', default='validation.csv', help='Name of csv file')
    parser.add_argument('--min_value', default=0.90, help='Minimal value of levenshtein distance') 
    parser.add_argument('--save_file', default='metadata.csv')
    parser.add_argument('--force', action='store_true', default=False)
    args = parser.parse_args()

    input_csv_file = join(args.base_dir, args.csv_file)
    output_filepath = join(args.base_dir, args.save_file)

    select(input_csv_file, output_filepath, args.min_value, args.force)


if __name__ == "__main__":
    main()
