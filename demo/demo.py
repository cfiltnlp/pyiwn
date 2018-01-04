# IndoWordNet API can be imported like this.
from pyiwn import pyiwn


# Download the IndoWordNet data (80 MB). It will download all the data in 'pyiwn_data' directory in the home directory.
pyiwn.download()


# List of supported languages in IndoWordNet. Returns a list.
print(pyiwn.langs())


# Choose a language and create an object of the IndoWordNet class.
iwn = pyiwn.IndoWordNet('hindi')


# Look up a word using synsets(). Returns a list of Synset objects.
iwn.synsets('सज्जन')


# synsets() function has an optional pos argument which lets you constrain the part of speech of the word.
iwn.synsets('सज्जन', pos=pyiwn.NOUN)


# You can access part of speech tags from pyiwn module as
pyiwn.NOUN
pyiwn.VERB
pyiwn.ADJECTIVE
pyiwn.ADVERB


print('\n\n****** Synset Properties ******\n')

# Synset Properties
syns = iwn.synsets('सज्जन', pos=pyiwn.NOUN)
print('Synsets: {}\n'.format(str(syns)))

# Select any one synset from the list (here we choose the first one, with index 0 in the list)
syn = syns[0]
# Synset ID. Returns an int.
print('Synset ID (unique identifier for the synset): {}\n'.format(str(syn.synset_id())))

# Head Word. Returns a string.
print('Head word (first word) of the synset: {}\n'.format(syn.head_word()))

# Lemmas. Returns a list of Lemma objects
lemmas = syn.lemmas() # returns a list of objects of Lemma class
print('Lemmas: {}\n'.format(str(lemmas)))

# Part of Speech Tag. Returns a string.
print('Part of Speech tag of the synset: {}\n'.format(syn.pos()))

# Definition of the Synset. Returns a string.
print('Definition (gloss) of the synset: {}\n'.format(syn.gloss()))

# Examples of the Synset. Returns a list of example strings.
print('Examples of the synset: {}\n'.format(str(syn.examples())))

# Ontology nodes. Returns a string denoting the name of the node.
print('Ontology nodes of the synset: {}\n'.format(str(syn.ontology_nodes())))

print('\n\n****** Synset Relations ******\n')

# Synset Relations
syns = iwn.synsets('शिवालय', pos=pyiwn.NOUN)
syn = syns[0]
# Hypernymy relation
print("Hypernymy synsets: {}\n".format(str(syn.hypernymy())))

print("Similarly, other relations can be accessed, for complete list of relations, please see: https://github.com/riteshpanjwani/pyiwn/blob/master/SYNSET-RELATIONS.md\n")

print('\n\n****** Lemmas ******\n')

# How to access Lemmas and various relations defined over Lemmas
syn = iwn.synsets('सुबह', pos=pyiwn.NOUN)[1]

lemmas = syn.lemmas() # returns a list of objects of Lemma class
print('Lemmas: {}\n'.format(str(lemmas)))

print('\n\n****** Lemma Properties ******\n')

# Select any one lemma from the list (here we choose the first one, with index 0 in the list)
lemma = lemmas[0]

# Lemma Properties
# Returns raw string of the lemma.
print('Lemma: {}\n'.format(lemma.name()))
# Returns an object of the Synset class the lemma belongs to.
print('Synset in which this lemma belongs: {}\n'.format(str(lemma.synset())))
# Returns the language of the lemma.
print('This lemma belongs to {} language.\n'.format(lemma.lang()))
# Returns low, medium and high gradation property of words
print('Gradation relation of the lemma: {}\n'.format(str(syn.lemmas()[0].gradation())))
# Returns antonym of a given lemma
print('Antonyms of the lemma are: {}\n'.format(str(syn.lemmas()[0].antonym())))

print('\n\n****** Access to all synsets ******\n')

# All Synsets
syns = iwn.all_synsets()
print('Total number of synsets in the Wordnet: {}\n'.format(str(len(syns))))

print('\n\n****** Access to all synsets filtered by POS tag ******\n')

# All Synsets filtered by a Part of Speech tag
syns = iwn.all_synsets(pos=pyiwn.NOUN)
print('Total number of synsets with {} as Part of Speech tag: {}\n'.format(pyiwn.NOUN, str(len(syns))))

print('\n\n****** Access to all unique words ******\n')

# List of all the unique words in the WordNet
words = iwn.all_words()
print('Total number of unique words in the Wordnet: {}\n'.format(str(len(words))))

print('\n\n****** Access to all unique words filtered by POS tag ******\n')

# List of all the unique words in the WordNet filtered by a Part of Speech tag
words = iwn.all_words(pos=pyiwn.NOUN)
print('Total number of unique words with {} as Part of Speech tag: {}\n'.format(pyiwn.NOUN, str(len(words))))

print('\n\n')