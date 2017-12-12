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
    pos = data[3]
    return (synset_id, head_word, lemma_names, pos, gloss, examples)

class Searcher:
    def __init__(self, filename):
        self.f = open(filename, 'rb')
        self.f.seek(0,2)
        self.length = self.f.tell()
        
    def find(self, string):
        low = 0
        high = self.length
        while low < high:
            mid = (low+high)//2
            p = mid
            while p >= 0:
                self.f.seek(p)
                if self.f.read(1) == '\n': break
                p -= 1
            if p < 0: self.f.seek(0)
            line = self.f.readline()
            if line < string:
                low = mid+1
            else:
                high = mid
        
        p = low
        while p >= 0:
            self.f.seek(p)
            if self.f.read(1) == '\n': break
            p -= 1
        if p < 0: self.f.seek(0)
        
        result = [ ]    
        while True:
            line = self.f.readline()
            if not line or not line.startswith(string): break
            if line[-1:] == '\n': line = line[:-1]
            result.append(line[len(string):])
        return result