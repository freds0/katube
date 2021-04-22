import re
import argparse
import unicodedata
from utils.number_to_text import number_to_text

vocab="abcdefghijklmnopqrstuvwxyzçãàáâêéíóôõúû\-0123456789,.;:!?' "
chars_map = {'ï': 'i', 'ù': 'ú', 'ö': 'o', 'î':'i', 'ñ':' n', 'ë':'e', 'ì':'í', 'ò': 'ó', 'ũ': 'u','ẽ':'e', 'ü':'u', 'è':'é', 'æ':'a', 'å': 'a'}

def get_number_of_words(sentence):
        # counting number of words on sentence
    length_sentence = len(sentence.split(' '))
    return length_sentence


def get_text_from_subtitle(input_file):

    # read all lines from file
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
        # look for patterns and parse
        if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
            text += ' ' + line.strip('\n')
            line_list.append(text)
    # Finish with list.join() to bring everything together
    text = '\n'.join(line_list)
    return text

def merge_sentences(sentences, min_words):
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
     # tokenize on spaces
    sentences = text.split(' ')
    return sentences

def tokenize_sentences_on_punctuation(text):
    # Tokenize by punctuation
    #sentences = re.split(r'([.,!?:;])', text)# Result example: ['Esta é uma frase', '.', 'Esta é outra frase', ',']
    sentences = re.split(r'([.;!?])', text)
    for index, sentence in enumerate(sentences[:-1]):
        sentence = sentence.strip()
        sentences[index:index+2] = [''.join(sentences[index:index+2])] # Result example: ['Esta é uma frase.', 'Esta é outra frase,']
    # Removing blank itens from list
    nonempty_sentences = list(filter(None, sentences))
    sentences = nonempty_sentences
    return sentences

def tokenize_sentences_on_special_words(text):
    special_words = [' mas ', ' porém ', ' todavia ', ' contudo ', ' entretanto ', ' no entanto ', ' pois ',' logo ', ' porque ', ' bem como ', ' por isso ', ' isto é ', ' visto que ', ' quando ', ' logo que ', ' desde que']
    # Tokenize by special words
    for word in special_words:
        sentences = re.split(r'({})'.format(word), text) 

    for index, sentence in enumerate(sentences[:-1]):
        sentence = sentence.strip()
        sentences[index:index+2] = [''.join(sentences[index:index+2])]
    # Removing blank itens from list
    nonempty_sentences = list(filter(None, sentences))
    sentences = nonempty_sentences
    return sentences

def get_size_of_biggest_sentence(sentences):
    max_length_sentence = 0
    for sentence in sentences:
        length_sentence = get_number_of_words(sentence)
        if  length_sentence > max_length_sentence:
            max_length_sentence = length_sentence
    return max_length_sentence

def text_tokenization(text, min_words, max_words):
    # First: tokenize on punctuation
    sentences = tokenize_sentences_on_punctuation(text)

    # Verify lenght of sentences
    length_biggest_sentence = get_size_of_biggest_sentence(sentences)

    # Second: tokenize on special words
    if length_biggest_sentence > max_words: # very long sentence
        sentences = tokenize_sentences_on_special_words(text)

    # Verify lenght of sentences
    length_biggest_sentence = get_size_of_biggest_sentence(sentences)
    # Third: tokenize on blank space
    if length_biggest_sentence > max_words: # very long sentence
        sentences = tokenize_sentences_on_blank_space(text)

    # Concatenates small sentences
    sentences = iter(sentences)
    lines, current = [], next(sentences)
    for sentence in sentences:    
        if  get_number_of_words(current) > min_words:
            lines.append(current)
            current = sentence # next
        # Concatenates sentences
        else:
            current += " " + sentence # concatenate two sentences
    lines.append(current)
    nonempty_lines = list(filter(None, lines))
    return nonempty_lines

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def text_normalize(text):
    text = text.replace('\n', ' ')
    text = remove_html_tags(text)
    accents = ('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT') #portuguese
    chars = [c for c in unicodedata.normalize('NFD', text) if c not in accents]
    text = unicodedata.normalize('NFC', ''.join(chars))# Strip accent
    text = text.lower()
    #text = re.sub("[^{}]".format(vocab), " ", text) # Remove all not in vocab
    text = re.sub("[...]+", ".", text) # Substitute "..." for "."
    # remove ( and [
    text = re.sub("[(\[\])]+", "", text)
    # remove space before punctuation
    text = re.sub(r'\s([.,;:?!"](?:\s|$))', r'\1', text)
    # Removing double black spaces
    text = re.sub("[  ]+", " ", text)
    for word in text.split(' '):
        for c in word:
            if c in chars_map.keys():
                word = word.replace(c,chars_map[c])
                c = chars_map[c]

    return text


def create_normalized_text_from_subtitles_file(subtitle_file, output_file, min_words, max_words):

    #text = get_text_from_subtitle(subtitle_file)

    # read all lines from file
    try:
        file = open(subtitle_file, "r")
        text = '\n'.join(file.readlines())
        file.close()
    except IOError:
        print("Error: Reading subtitle file {}.".format(input_file))
        return False    

    if not text:
        return False

    text = text_normalize(text)
    sentences = text_tokenization(text, int(min_words), int(max_words))
    try:
        f = open(output_file, "w")
        for sentence in sentences:
            sentence = number_to_text(sentence)
            f.write(sentence.strip() + '\n')
        f.close()
    except IOError:
        print("Error: Writing audio file {}.".format(filepath))
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
