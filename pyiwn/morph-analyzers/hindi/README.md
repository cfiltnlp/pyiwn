# Hindi Morphological Analyzer


The goal of this library is to provide Morphological Analysis for Hindi language. Morphology is the part of linguistics that deals with the study of words, their internal structure and partially their meanings. It refers to identification of a root word from a full word form. A morpheme in morphology is the smallest units that carry meaning and fulfill some grammatical function. 

Morphological Analysis is the process of providing grammatical information of a word given its suffix.

A morphological analyzer is a program for analyzing the morphology of an input word, it detects its root word & its constituent morphemes.

The library provides the following:

* Root word / Lemma
* Paradigm of the word
* POS tag
* Suffix List

## Pre-requisites

* [Java SE 7](http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html)

## Running

You can see the demo file (src/HindiMADemo.java) to see how to use the library.

## Accuracy

These scores are calculated on 37291 words:

* Precision: 92.64 %
* Recall: 90.3 %
* F1-Score: 90.77 %

## Paradigms and Categories

| Paradigm | Category | Description | Examples |
| -------- | -------- | ----------- | -------- |
| pronoun_pn | pn | Pronoun | maĩ (I), həm (we), tū (you), vəh (he/she/it), ve (they) |
| adjective | adjective | Adjective | |
| post_posi | pp | Post-position | mẽ (in), pər (on), kā (of), ne (ergative marker), |
| foreign | foreign | Foreign word | |
| particle | particle | Particle | hī (only), bhī (also, additive/scalar) |
| oblique_demonstrative | demonstrative | Oblique Demonstrative | |
| demonstrative | demonstrative | Demonstrative | |
| pronoun_reciprocal | pn_rec | Reciprocal Pronoun | ek-dūsre (ek-dūsre) |
| proper_noun | pnoun | Proper Noun | ətəl bihārī vājpeyī (Atal Bihari Vajpeyi), lāl kilā (Red Fort) |
| oblique_sg_pn | pn | Oblique Singular Pronoun | |
| oblique_pl_pn | pn | Oblique Plural Pronoun | |
| oblique_pn | pn | Oblique Pronoun | |
| direct_pn | pn | Direct Pronoun | |
| p_wh | P_wh | Question Pronoun | kaun (who), kis (which) |
| wh | wh | Any 'wh' question word, which is not pronoun | kidhar (where), kahan (where) |
| quantifier | quantifier | Quantifier | səb/səbhī (all), hər (every/each), prətyek (every one) |
| neg | neg | Negation Markers | |
| verb | verb | Verb | |
| adverb | adverb | Adverb | |
| noun | noun | Noun | |
| intensifier | intensifier | Intensifier | bəhut (very), zyādā (many) |
| pronoun_gen | png | Pronoun Genitive | |
| interjection | inj | Interjection | |
| vaux | verb_aux | Auxiliary Verb | |
| nst | nst | Noun that represents space or time | ab (now), tab (then), yahan (here), wahan (there) |
| case | cm | Case Marker | ko |
| ordinal | ordinal | Ordinal numbers | pehlā (first), tīsrā (second), sātvã (seventh), bāīsvã (twenty-second) |
| direct_pl_pn | pn | Direct Plural Pronoun | |
| oblique_sg_demonstrative | demonstrative | Oblique Singular Demonstrative | |
| conjunction | conj | Conjunction | |
| pronoun_reflexive | pn_ref | Reflexive Pronoun | əpne-āp (myself), khud/svəyəm(himself) |
| direct_demonstrative | demonstrative | Direct Demonstrative | |
| ex_noun | noun | Noun | |
| cardinal | cardinal | Cardinal numbers | ek (one), do (two), tīn (three) |
| SYM | SYM | Symbol, not a hindi character | ., ,, /, ?, !, etc. |


## Author

Ritesh Panjwani (riteshppanjwani@gmail.com)