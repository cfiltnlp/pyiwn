from pyiwn import utils
from pathlib import Path
import urllib.request
import shutil
import zipfile
import os


NOUN, VERB, ADVERB, ADJECTIVE = 'noun', 'verb', 'adverb', 'adjective'

languages = ['hindi', 'english', 'assamese', 'bengali', 'bodo', 'gujarati', 'kannada', 'kashmiri', 'konkani', 'malayalam', 'meitei', 'marathi', 'nepali', 'sanskrit', 'tamil', 'telugu', 'punjabi', 'urdu', 'oriya']

home = str(Path.home()) + '/pyiwn_data'

def langs():
    return 'pyiwn supports the WordNets of the following languages: {}'.format(str(languages))
                
def download():
    url = "https://www.dropbox.com/s/a3tlr5ll3y3pef6/pyiwn_data.zip?dl=1"
    pyiwn_data_path = '{}/pyiwn_data.zip'.format(str(Path.home()))
    print('Please wait. Downloading IndoWordnet synset data (80 MB) to {}'.format(str(Path.home())))
    with urllib.request.urlopen(url) as response, open(pyiwn_data_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    print('Extracting pyiwn data...')
    zip_ref = zipfile.ZipFile(pyiwn_data_path, 'r')
    zip_ref.extractall(str(Path.home()))
    zip_ref.close()
    os.remove(pyiwn_data_path)
    print('Download successful.')


class IndoWordNetError(Exception):
    '''An exception class for wordnet-related errors.'''


class IndoWordNet:
    def __init__(self, lang):
        if lang not in langs():
            raise IndoWordNetError('Language is not supported.')
        self._lang = lang

    def all_synsets(self, pos=None):
        synsets = []
        synset_file_name = 'all.{}'.format(self._lang) if pos == None else '{}.{}'.format(pos, self._lang)
        with utils.read_file('{}/synsets/{}'.format(home, synset_file_name)) as fo:
            for line in fo:
                sp = utils.clean_line(line)
                synset_data = utils.synset_data(sp, pos)
                synset_id, head_word, lemma_names, pos, gloss, examples = synset_data[0], synset_data[1], synset_data[2], synset_data[3], synset_data[4], synset_data[5]
                synsets.append(Synset(synset_id, head_word, lemma_names, pos, gloss, examples))
        return synsets

    def synsets(self, word, pos=None):
        synsets = []
        words_file_name = 'all.{}'.format(self._lang) if pos == None else '{}.{}'.format(pos, self._lang)
        with utils.read_file('{}/words/{}'.format(home, words_file_name)) as fo:
            for line in fo:
                sp = utils.clean_line(line)
                if word == sp[1]:
                    synset_id = sp[0]
                    pos = sp[2] if pos == None else pos
                    break
        synset_file_name = 'all.{}'.format(self._lang) if pos == None else '{}.{}'.format(pos, self._lang)
        with utils.read_file('{}/synsets/{}'.format(home, synset_file_name)) as fo:
            for line in fo:
                sp = utils.clean_line(line)
                synset_data = utils.synset_data(sp, pos)
                if word in synset_data[2]:
                    synset_id, head_word, lemma_names, pos, gloss, examples = synset_data[0], synset_data[1], synset_data[2], synset_data[3], synset_data[4], synset_data[5]
                    synsets.append(Synset(synset_id, head_word, lemma_names, pos, gloss, examples))
        return synsets

    def all_words(self, pos=None):
        words = []
        words_file_name = 'all.{}'.format(self._lang) if pos == None else '{}.{}'.format(pos, self._lang)
        with utils.read_file('{}/words/{}'.format(home, words_file_name)) as fo:
            for line in fo:
                sp = utils.clean_line(line)
                words.append(sp[1])
        return words


class Synset:
    def __init__(self, synset_id, head_word, lemma_names, pos, gloss, examples):
        self._synset_id = synset_id
        self._head_word = head_word
        self._lemma_names = lemma_names
        self._pos = pos
        self._gloss = gloss
        self._examples = examples

    def __repr__(self):
        return 'Synset(\'{}.{}.{}\')'.format(self._head_word, self._pos, self._synset_id)

    def synset_id(self):
        return self._synset_id

    def head_word(self):
        return self._head_word

    def lemma_names(self):
        return self._lemma_names

    def lemmas(self):
        return [Lemma(self, lemma)for lemma in self._lemma_names]

    def pos(self):
        return self._pos  

    def gloss(self):
        return self._gloss

    def examples(self):
        return self._examples

    def ontology_nodes(self):
        ontology_node_idx_list = []
        with utils.read_file('{}/ontology/map'.format(home)) as fo:
            for line in fo:
                sp = utils.clean_line(line)
                if self._synset_id == int(sp[0]):
                    ontology_node_idx_list = [int(idx) for idx in sp[1].split(',')]
                    break
        ontology_nodes_list = []
        with utils.read_file('{}/ontology/nodes'.format(home)) as fo:
            for line in fo:
                sp = utils.clean_line(line)
                if int(sp[0]) in ontology_node_idx_list:
                    ontology_nodes_list.append(' '.join(sp[1:]))
        return ontology_nodes_list

    def _relations(self, relation):
        synset_id_list = []
        with utils.read_file('{}/synset_relations/{}.{}'.format(home, relation, self._pos)) as fo:
            for line in fo:
                sp = utils.clean_line(line)
                sp[0] = int(sp[0])
                if self._synset_id == sp[0]:
                    synset_id_list = [int(idx) for idx in sp[1].split(',')]
                    break
        synsets = []
        with utils.read_file('{}/synsets/{}.hindi'.format(home, self._pos)) as fo:
            for line in fo:
                sp = utils.clean_line(line)
                if int(sp[0]) in synset_id_list:
                    synset_data = utils.synset_data(sp, self._pos)
                    synset_id, head_word, lemma_names, pos, gloss, examples = synset_data[0], synset_data[1], synset_data[2], synset_data[3], synset_data[4], synset_data[5]
                    synsets.append(Synset(synset_id, head_word, lemma_names, pos, gloss, examples))
        return synsets

    def hypernymy(self):
        if self._pos in [ADJECTIVE, ADVERB]:
            raise IndoWordNetError('This synset relation is not valid for adjectives and adverbs.')
        return self._relations('hypernymy')

    def ability_verb(self):
        return self._relations('ability_verb')

    def attributes(self):
        return self._relations('attributes')

    def capability_verb(self):
        return self._relations('capability_verb')

    def function_verb(self):
        return self._relations('function_verb')

    def holo_component_object(self):
        return self._relations('holo_component_object')

    def holo_member_collection(self):
        return self._relations('holo_member_collection')

    def holo_phase_state(self):
        return self._relations('holo_phase_state')

    def holo_place_area(self):
        return self._relations('holo_place_area')

    def holo_portion_mass(self):
        return self._relations('holo_portion_mass')

    def holo_position_area(self):
        return self._relations('holo_position_area')

    def holo_resource_process(self):
        return self._relations('holo_resource_process')

    def holo_stuff_object(self):
        return self._relations('holo_stuff_object')

    def mero_component_object(self):
        return self._relations('mero_component_object')

    def mero_feature_activity(self):
        return self._relations('mero_feature_activity')

    def mero_member_collection(self):
        return self._relations('mero_member_collection')

    def mero_phase_state(self):
        return self._relations('mero_phase_state')

    def mero_place_area(self):
        return self._relations('mero_place_area')

    def mero_portion_mass(self):
        return self._relations('mero_portion_mass')

    def mero_position_area(self):
        return self._relations('mero_position_area')

    def mero_resource_process(self):
        return self._relations('mero_resource_process')

    def mero_stuff_object(self):
        return self._relations('mero_stuff_object')

    def modifies_noun(self):
        if self._pos != ADJECTIVE:
            raise IndoWordNetError('This synset relation is valid only for adjectives.')
        return self._relations('modifies_noun')

    def similar(self):
        if self._pos != ADJECTIVE:
            raise IndoWordNetError('This synset relation is valid only for adjectives.')
        return self._relations('similar')

    def also_see(self):
        if self._pos == NOUN:
            raise IndoWordNetError('This synset relation is not valid for nouns.')
        return self._relations('also_see')

    def modifies_verb(self):
        if self._pos != ADVERB:
            raise IndoWordNetError('This synset relation is valid only for adverbs.')
        return self._relations('modifies_verb')

    def causative(self):
        return self._relations('causative')

    def compounding(self):
        return self._relations('compounding')

    def conjunction(self):
        return self._relations('conjunction')

    def entailment(self):
        return self._relations('entailment')

    def troponymy(self):
        return self._relations('troponymy')


class Lemma:
    def __init__(self, synset, name):
        self._synset = synset
        self._name = name
        self._lang = 'hindi'

    def __repr__(self):
        return 'Lemma(\'{}.{}.{}.{}\')'.format(self._synset.head_word(), self._synset.pos(), self._synset.synset_id(), self._name)

    def name(self):
        return self._name

    def synset(self):
        return self._synset

    def lang(self):
        return self._lang

    # def count(self):
    #     pass

    def gradation(self):
        with utils.read_file('{}/synset_relations/gradation'.format(home)) as fo:
            for line in fo:
                if str(self._synset.synset_id()) in line:
                    sp = line.split('\t')
                    synset_id_list = [int(sp[0]), int(sp[2]), int(sp[4])]
                    break
        synsets = []
        with utils.read_file('{}/synsets/{}.hindi'.format(home, self._synset.pos())) as fo:
            for line in fo:
                sp = utils.clean_line(line)
                if int(sp[0]) in synset_id_list:
                    synset_data = utils.synset_data(sp, self._synset.pos())
                    synset_id, head_word, lemma_names, pos, gloss, examples = synset_data[0], synset_data[1], synset_data[2], synset_data[3], synset_data[4], synset_data[5]
                    synsets.append(Synset(synset_id, head_word, lemma_names, pos, gloss, examples))
        return {'low': synsets[0], 'medium': synsets[1], 'high': synsets[2]}

    def antonym(self):
        antonym_synset_id = -1
        with utils.read_file('{}/synset_relations/antonyms'.format(home)) as fo:
            for line in fo:
                if self._name in line:
                    antonym_synset_id = int(line.split('\t')[2])
                    break
        synsets = []
        with utils.read_file('{}/synsets/{}.hindi'.format(home, self._synset.pos())) as fo:
            for line in fo:
                sp = utils.clean_line(line)
                if int(sp[0]) == antonym_synset_id:
                    synset_data = utils.synset_data(sp, self._synset.pos())
                    synset_id, head_word, lemma_names, pos, gloss, examples = synset_data[0], synset_data[1], synset_data[2], synset_data[3], synset_data[4], synset_data[5]
                    synsets.append(Synset(synset_id, head_word, lemma_names, pos, gloss, examples))
        return synsets