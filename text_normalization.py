#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2021 Frederico Oliveira fred.santos.oliveira(at)gmail.com
#
#
import re
import argparse
import unicodedata
from utils.number_to_text import number_to_text

vocab="abcdefghijklmnopqrstuvwxyzçãàáâêéíóôõúû\-0123456789,.;:!?' "
chars_map = {'ï': 'i', 'ù': 'ú', 'ö': 'o', 'î':'i', 'ñ':' n', 'ë':'e', 'ì':'í', 'ò': 'ó', 'ũ': 'u','ẽ':'e', 'ü':'u', 'è':'é', 'æ':'a', 'å': 'a'}


def get_number_of_words(sentence):
    """
    Count number of words on sentence.
        Parameters:
        sentence (str). text sentence.

        Returns:
        int: returns sentence length
    """
    sentence_length = len(sentence.split(' '))
    return sentence_length


def get_text_from_subtitle(input_file):
    """
    Extracts the text from a subtitle file.
        Parameters:
        input_file (str): input subtitles file (.srt).

        Returns:
        text (str): returns text of subtitles files.
    """
    # Read all lines from file
    try:
        file = open(input_file, "r")
        lines = file.readlines()
        file.close()

    except IOError:
        print("Error: Reading subtitle file {}.".format(input_file))
        return False

    # Declare variable empty list
    line_list = []
    for line in lines:
        text = ''
        # Look for patterns and parse
        if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
            text += ' ' + line.strip('\n')
            line_list.append(text)

    # Finish with list.join() to bring everything together
    text = '\n'.join(line_list)
    return text


def merge_sentences(sentences, min_words):
    """
    Merge sentences that have a number of words less than min_words.
        Parameters:
        sentences (list): list of sentences.
        min_words (int): minimum quantity of words.

        Returns:
        sentences (list): returns sentences list with length bigger then min_words.
    """
    found_short_sentence = True
    while(found_short_sentence):
        found_short_sentence = False
        for index, sentence in enumerate(sentences):
            # Verify number of words on sentence
            if (len(sentence.split()) < min_words):
                found_short_sentence = True
                # Merge sentences
                sentences[index:index+2] = [' '.join(sentences[index:index+2])]
    # Removing blank itens from list
    nonempty_sentences = list(filter(None, sentences))
    return nonempty_sentences


def tokenize_sentences_on_blank_space(text):
    """
    Divide a text into words, that is, create tokens, breaking it into the blank spaces.
        Parameters:
        text (str): normalized text.

        Returns:
        words (list): returns list of words.
    """
    # Tokenize on blank spaces
    words = text.split(' ')
    return words


def tokenize_sentences_on_punctuation(text):
    """
    Creates sentences from a text, splitting it in the punctuation.
        Parameters:
        text (str): normalized text.

        Returns:
        sentences (list): returns list of sentences split on punctuation.
    """
    # Tokenize by punctuation
    # sentences = re.split(r'([.,!?:;])', text)# Result example: ['Esta é uma frase', '.', 'Esta é outra frase', ',']
    sentences = re.split(r'([.;!?])', text)
    for index, sentence in enumerate(sentences[:-1]):
        sentence = sentence.strip()
        sentences[index:index+2] = [''.join(sentences[index:index+2])] # Result example: ['Esta é uma frase.', 'Esta é outra frase,']
    # Removing blank itens from list
    nonempty_sentences = list(filter(None, sentences))
    sentences = nonempty_sentences
    return sentences


def tokenize_sentences_on_special_words(text):
    """
    Creates sentences from a text, splitting it in the special words of the Portuguese language.
        Parameters:
        text (str): normalized text.

        Returns:
        sentences (list): returns list of sentences split on special words.
    """
    special_words = [' mas ', ' porém ', ' todavia ', ' contudo ', ' entretanto ', ' no entanto ', ' pois ',' logo ', ' porque ', ' bem como ', ' por isso ', ' isto é ', ' visto que ', ' quando ', ' logo que ', ' desde que']
    # Tokenize by special words
    for word in special_words:
        sentences = re.split(r'({})'.format(word), text) 

    for index, sentence in enumerate(sentences[:-1]):
        sentences[index:index+2] = [''.join(sentences[index:index+2])]
    # Removing blank itens from list
    nonempty_sentences = list(filter(None, sentences))
    sentences = nonempty_sentences
    return sentences


def get_size_of_biggest_sentence(sentences):
    """
    Given a list of sentences, it returns the length of the largest sentence.
        Parameters:
        sentences (list): sentences list.

        Returns:
        int: returns length of largest sentence.
    """
    max_length_sentence = 0
    for sentence in sentences:
        length_sentence = get_number_of_words(sentence)
        if  length_sentence > max_length_sentence:
            max_length_sentence = length_sentence
    return max_length_sentence


def create_sentences_from_text(text, min_words, max_words):
    """
    Creates sentences from a text, taking into account the minimum and maximum number of words.
    Initially, it divides the text according to the punctuation, then it divides the larger sentences according to special words,
    and, finally, it divides the larger sentences into tokens.
    After the division, the tokens are concatenated until they are within the min and max limits.
        Parameters:
        text (str): normalized text.
        min_words (int): number minimum of words of each sentence.
        max_words (int): number maximum of words of each sentence.

        Returns:
        sentences (list): returns sentences list.
    """
    # First: tokenize on punctuation
    sentences = tokenize_sentences_on_punctuation(text)

    # Verify length of sentences
    length_biggest_sentence = get_size_of_biggest_sentence(sentences)

    # Second: tokenize on special words
    if length_biggest_sentence > max_words: # very long sentence
        sentences = tokenize_sentences_on_special_words(text)

    # Verify length of sentences
    length_biggest_sentence = get_size_of_biggest_sentence(sentences)

    # Third: tokenize on blank space
    if length_biggest_sentence > max_words: # very long sentence
        sentences = tokenize_sentences_on_blank_space(text)

    # Concatenates small sentences
    sentences = iter(sentences)
    lines, current = [], next(sentences)
    for sentence in sentences:    
        if get_number_of_words(current) > min_words:
            lines.append(current)
            current = sentence # next
        # Concatenates sentences
        else:
            current += " " + sentence # concatenate two sentences

    lines.append(current)
    nonempty_lines = list(filter(None, lines))
    return nonempty_lines


def remove_html_tags(text):
    """
    Remove html tags from a string using regular expressions.
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def text_cleaning(text):
    """
    Performs a series of operations to clear the text in order to normalize it.
    """
    # Removing line break.
    text = text.replace('\n', ' ')

    # Removing html tags.
    text = remove_html_tags(text)

    # Normalizing accents to unidecode.
    accents = ('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT') #portuguese
    chars = [c for c in unicodedata.normalize('NFD', text) if c not in accents]
    text = unicodedata.normalize('NFC', ''.join(chars))# Strip accent

    # Converting to lower case
    text = text.lower()

    # Remove all not in vocab
    #text = re.sub("[^{}]".format(vocab), " ", text)

    # Replacing ... for .
    text = re.sub("[...]+", ".", text) # Substitute "..." for "."

    # Remove (, [
    text = re.sub("[(\[\])]+", "", text)

    # Remove space before punctuation
    text = re.sub(r'\s([.,;:?!"](?:\s|$))', r'\1', text)

    # Removing double blank spaces
    text = re.sub("[  ]+", " ", text)
    for word in text.split(' '):
        for c in word:
            if c in chars_map.keys():
                word = word.replace(c,chars_map[c])
                c = chars_map[c]

    return text


def create_normalized_text_from_subtitles_file(subtitle_file, output_file, min_words, max_words):
    """
    Given a subtitle file (.srt) it cleans and normalizes the text, dividing it into sentences,
    according to the number of words (min_words and max_words),
    saving the result in output_file.
        Parameters:
        subtitle_file (str): subtitles .srt file.
        output_file (str): file path to save the normalized text.
        min_words (int): number minimum of words of each sentence.
        max_words (int): number maximum of words of each sentence.

        Returns:
        Boolean: returns True or False.
    """

    # If the file comes with the time for each subtitle, uncomment this line as only the subtitles text will be extracted.
    #text = get_text_from_subtitle(subtitle_file)

    # Read all lines from file
    try:
        file = open(subtitle_file, "r")
        text = '\n'.join(file.readlines())
        file.close()
    except IOError:
        print("Error: Reading subtitle file {}.".format(subtitle_file))
        return False    

    # If it was unable to extract the text.
    if not text:
        return False

    # Clear and normalize the text.
    text = text_cleaning(text)

    # Creates a list of sentences.
    sentences = create_sentences_from_text(text, int(min_words), int(max_words))

    # Save the sentences to the output file.
    try:
        f = open(output_file, "w")
        for sentence in sentences:
            #  Converting numbers by its full version.
            sentence = number_to_text(sentence)
            f.write(sentence.strip() + '\n')
        f.close()

    except IOError:
        print("Error: Writing audio file {}.".format(output_file))
        return False

    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--input_file', default='subtitles.txt', help='Subtitles filename (only text)')
    parser.add_argument('--output_file', default='output.txt', help='Filename to save the normalize text')
    parser.add_argument('--min_words', default=10, help='Minimal number of words on sentence')
    parser.add_argument('--max_words', default=30, help='Maximal number of words on sentence')
    args = parser.parse_args()

    min_words = int(args.min_words)
    max_words = int(args.max_words)

    create_normalized_text_from_subtitles_file(args.input_file, args.output_file, min_words, max_words)

if __name__ == "__main__":
    main()
