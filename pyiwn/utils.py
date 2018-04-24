import codecs
import re

def read_file(filename):
    return codecs.open(filename, 'r', encoding='utf-8')


def clean_line(line):
    line = re.sub('\n', '', line)
    line = line.strip().split('\t')
    return line


def synset_data(data, pos):
    synset_id = int(data[0])
    lemma_names = data[1].split(',')
    head_word = lemma_names[0]
    if ':' in ','.join(data):
        gloss_examples_sp = data[2].split(':')
        gloss = gloss_examples_sp[0]
        examples = re.sub('"', '', gloss_examples_sp[1]).split(' / ')
    else:
        gloss, examples = '', []
    return (synset_id, head_word, lemma_names, pos, gloss, examples)