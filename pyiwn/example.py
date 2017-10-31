import pyiwn

'''
TODO 
clean up files
'''

iwn = pyiwn.IndoWordNet('hindi')
# all_synsets = iwn.all_synsets(pos=pyiwn.NOUN)
# print(len(all_synsets))
# print(iwn.synsets('आगत'))
syns = iwn.synsets('दुश्चरित्रता', pos=pyiwn.NOUN)
# print(syns[0].pos())
print(syns[0].synset_id())
# print(syns[0].head_word())
# print(syns[0].lemma_names())
# print(syns[0].lemmas())
# print(syns[0].gloss())
# print(syns[0].examples())
# print(syns[0].ontology_nodes())
print(syns[0].hypernymy())
# iwn.all_words(pos='verb')