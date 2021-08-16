from enum import Enum, unique
import re
import logging
import glob
import ntpath
import os

import pandas as pd

import pyiwn.constants as constants


logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO)
logger = logging.getLogger(__name__)


@unique
class Language(Enum):
    ASSAMESE = 'assamese'
    BENGALI = 'bengali'
    BODO = 'bodo'
    GUJARATI = 'gujarati'
    HINDI = 'hindi'
    KANNADA = 'kannada'
    KASHMIRI = 'kashmiri'
    KONKANI = 'konkani'
    MALAYALAM = 'malayalam'
    MARATHI = 'marathi'
    MEITEI = 'meitei'
    NEPALI = 'nepali'
    ORIYA = 'oriya'
    PUNJABI = 'punjabi'
    SANSKRIT = 'sanskrit'
    TAMIL = 'tamil'
    TELUGU = 'telugu'
    URDU = 'urdu'


class IndoWordNet:
    def __init__(self, lang=Language.HINDI):
        logger.info(f'Loading {lang.value} language synsets...')
        self._synset_idx_map = {}
        self._synset_df = self._load_synset_file(lang.value)
        self._synset_relations_dict = self._load_synset_relations()

    def _load_synset_file(self, lang):
        filename = os.path.join(*[constants.IWN_DATA_PATH, 'synsets', 'all.{}'.format(lang)])
        f = open(filename, encoding="utf-8")
        synsets = list(map(lambda line: self._load_synset(line), f.readlines()))
        synset_df = pd.DataFrame(synsets, columns=['synset_id', 'synsets', 'pos'])
        synset_df = synset_df.dropna()
        synset_df = synset_df.set_index('synset_id')
        return synset_df

    def _load_synset_relations(self):
        relations_dict = {}
        for file_path, relation_name in self._relation_list():
            relations_dict[relation_name] = []
            d = {}
            for line in open(file_path):
                line_parts = line.split('\t')
                synset_id, synset_ids = line_parts
                synset_id = int(synset_id)
                synset_ids = list(map(int, synset_ids.split(',')))
                synset_ids = list(filter(lambda x: True if x in self._synset_df.index else False, synset_ids))
                if synset_id in d:
                    d[synset_id].extend(synset_ids)
                else:
                    if synset_ids:
                        d[synset_id] = synset_ids
            relations_dict[relation_name] = d
        return relations_dict

    def _relation_list(self, type='synset_relations'):
        relations = []
        path_parts = '{},{},*'.format(constants.IWN_DATA_PATH, type).split(',')
        for file_path in glob.glob(os.path.join(*path_parts)):
            file_name = ntpath.basename(file_path)
            file_name_parts = file_name.split('.')
            if len(file_name_parts) != 2:
                continue
            relation_name, pos_tag = file_name_parts
            relations.append((file_path, relation_name))
        return relations

    def _update_synset_idx_map(self, synset):
        synset_id = synset.synset_id()
        for word in synset.lemma_names():
            if word in self._synset_idx_map:
                self._synset_idx_map[word].append(synset_id)
            else:
                self._synset_idx_map[word] = [synset_id]
        return True

    def _load_synset(self, synset_string):
        if 'null' in synset_string:
            return None, None, None

        synset_string = synset_string.replace('\n', '').strip()
        synset_pattern = '([0-9]+)\t(.+)\t(.+)\t([a-zA-Z]+)'
        try:
            matches = re.findall(synset_pattern, synset_string)
            synset_id, synset_words, gloss_examples, pos = matches[0]
        except Exception as e:
            return None, None, None

        synset_id = int(synset_id)
        synset_words = list(filter(lambda x: False if x == '' else True, synset_words.split(',')))
        if not synset_words:
            return None, None, None
        head_word = synset_words[0]
        if gloss_examples != '':
            if ':"' in gloss_examples:
                ge_list = gloss_examples.split(':')
                gloss = ge_list[0]
                if len(ge_list) > 1:
                    examples = ''.join(ge_list[1:])
                    examples = re.sub('["]', '', examples)
                    examples = examples.split('  /  ')
                else:
                    examples = []
            else:
                gloss = gloss_examples
                examples = []
        else:
            return None, None, None
        synset = Synset(synset_id, head_word, synset_words, pos, gloss, examples)

        self._update_synset_idx_map(synset)

        return synset_id, synset, pos

    def all_synsets(self, pos=None):
        if pos is None:
            result = self._synset_df
        else:
            mask = (self._synset_df.pos == pos.value)
            result = self._synset_df[mask]
        return list(result['synsets'].values)

    def synsets(self, word, pos=None):
        synset_id_list = self._synset_idx_map[word]

        synsets = []
        if pos is not None:
            for synset_id in synset_id_list:
                synset = self._synset_df.loc[[synset_id]]['synsets'].values[0]
                if synset.pos() == pos.value:
                    synsets.append(synset)
        else:
            for synset_id in synset_id_list:
                synset = self._synset_df.loc[[synset_id]]['synsets'].values[0]
                synsets.append(synset)

        return synsets

    def all_words(self, pos=None):
        if pos is None:
            return list(self._synset_idx_map.keys())

        words = set()
        mask = (self._synset_df.pos == pos.value)
        for synset in self._synset_df[mask]['synsets'].values:
            for word in synset.lemma_names():
                words.add(word)
        words = list(words)
        return words

    def synset_relation(self, synset, relation):
        return list(self._synset_df[self._synset_df.index.isin(self._synset_relations_dict[relation.value].get(synset.synset_id(), []))]['synsets'])


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
        return [Lemma(self, lemma) for lemma in self._lemma_names]

    def pos(self):
        return self._pos  

    def gloss(self):
        return self._gloss

    def examples(self):
        return self._examples

    def ontology_nodes(self):
        raise NotImplementedError("This method will be implemented soon.")


class Lemma:
    def __init__(self, synset, name):
        self._synset = synset
        self._name = name

    def __repr__(self):
        return 'Lemma(\'{}.{}.{}.{}\')'.format(self._synset.head_word(), self._synset.pos(), self._synset.synset_id(), self._name)

    def name(self):
        return self._name

    def synset(self):
        return self._synset

    def gradation(self):
        raise NotImplementedError("This method will be implemented soon.")

    def antonym(self):
        raise NotImplementedError("This method will be implemented soon.")


@unique
class PosTag(Enum):
    NOUN = 'noun'
    VERB = 'verb'
    ADVERB = 'adverb'
    ADJECTIVE = 'adjective'


class IndoWordNetError(Exception):
    """ An exception class for IndoWordNet-related errors. """


@unique
class SynsetRelations(Enum):
    MERO_MEMBER_COLLECTION = 'mero_member_collection'
    ABILITY_VERB = 'ability_verb'
    CAUSATIVE = 'causative'
    CAPABILITY_VERB = 'capability_verb'
    MERO_COMPONENT_OBJECT = 'mero_component_object'
    HOLO_PORTION_MASS = 'holo_portion_mass'
    FUNCTION_VERB = 'function_verb'
    HOLO_COMPONENT_OBJECT = 'holo_component_object'
    HYPERNYMY = 'hypernymy'
    ENTAILMENT = 'entailment'
    ALSO_SEE = 'also_see'
    MERO_FEATURE_ACTIVITY = 'mero_feature_activity'
    HOLO_PLACE_AREA = 'holo_place_area'
    MODIFIES_VERB = 'modifies_verb'
    ATTRIBUTES = 'attributes'
    MERO_PORTION_MASS = 'mero_portion_mass'
    MODIFIES_NOUN = 'modifies_noun'
    HOLO_FEATURE_ACTIVITY = 'holo_feature_activity'
    MERO_STUFF_OBJECT = 'mero_stuff_object'
    TROPONYMY = 'troponymy'
    MERO_PLACE_AREA = 'mero_place_area'
    HOLO_MEMBER_COLLECTION = 'holo_member_collection'
    HYPONYMY = 'hyponymy'
    SIMILAR = 'similar'
    MERO_POSITION_AREA = 'mero_position_area'
    HOLO_POSITION_AREA = 'holo_position_area'
    HOLO_STUFF_OBJECT = 'holo_stuff_object'
