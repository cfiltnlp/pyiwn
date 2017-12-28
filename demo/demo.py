# IndoWordNet API can be imported like this.
from pyiwn import pyiwn


# Download the IndoWordNet data (80 MB). It will download all the data in 'pyiwn_data' directory in the home directory.
# pyiwn.download()


# List of supported languages in IndoWordNet. Returns a list.
pyiwn.langs()


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


# Synset Properties
# syns = iwn.synsets('सज्जन', pos=pyiwn.NOUN)
# print(syns)
# syn = syns[0]
# # Synset ID. Returns an int.
# print(syn.synset_id())
# # Head Word. Returns a string.
# print(syn.head_word())
# # Lemmas. Returns a list of Lemma objects
# print(syn.lemma_names())
# print(syn.lemmas())
# # Part of Speech Tag. Returns a string.
# print(syn.pos())
# # Definition of the Synset. Returns a string.
# print(syn.gloss())
# # Examples of the Synset. Returns a list of example strings.
# print(syn.examples())
# # Ontology nodes. Returns a string denoting the name of the node.
# print(syn.ontology_nodes())


# Synset Relations
# syns = iwn.synsets('शिवालय', pos=pyiwn.NOUN)
# syn = syns[0]
# # Hypernymy relation
# print("HYPERNYMY: " + str(syn.hypernymy()))
# # print("HYPERNYMY: " + str(syn.hyponymy()))
# # Similarly, other relations can be accessed, for complete list of relations, please see: https://github.com/riteshpanjwani/pyiwn/blob/master/SYNSET-RELATIONS.md


# Lemmas
syn = iwn.synsets('सुबह', pos=pyiwn.NOUN)[1]
lemmas = syn.lemmas() # returns a list of objects of Lemma class
print(lemmas)
lemma = lemmas[0]
# Lemma Properties
# Returns raw string of the lemma.
print(lemma.name())
# Returns an object of the Synset class the lemma belongs to.
print(lemma.synset())
# Returns the language of the lemma.
print(lemma.lang())
# Returns low, medium and high gradation property of words
print(syn.lemmas()[0].gradation())
# Returns antonym of a given lemma
print(syn.lemmas()[0].antonym())


# # All Synsets
# syns = iwn.all_synsets()
# print(len(syns))


# # All Synsets filtered by a Part of Speech tag
# syns = iwn.all_synsets(pos=pyiwn.NOUN)
# print(len(syns))


# # List of all the unique words in the WordNet
# words = iwn.all_words()
# print(len(words))


# # List of all the unique words in the WordNet filtered by a Part of Speech tag
# words = iwn.all_words(pos=pyiwn.NOUN)
# print(len(words))