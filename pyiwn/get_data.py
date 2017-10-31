from utils2 import *
import codecs
from operator import itemgetter

pos_tags = ['noun', 'verb', 'adjective', 'adverb']


'''
words - all.lang (19), pos.lang (19 * 4 = 76) => (76 + 19 = 95) - done
synsets - all.lang (19), pos.lang (19 * 4 = 76) => (76 + 19 = 95) - done
synset relations - relation.pos (34) - done
statistics - statistics (1) - todo
ontology - map, nodes (2) - done
----------------------------------------------------
Total: 227
'''

# words - hindi - pos
for pos_tag in pos_tags:
	query = 'SELECT synset_id, word from tbl_all_words where pos=%s'
	rows = execute_query(query, [HWN_DB], FETCH_ALL_ROWS, (pos_tag,))
	rows = [(int(item[0]), item[1]) for item in rows]
	sorted(rows, key=itemgetter(0))
	with codecs.open('data/words/{}.hindi'.format(pos_tag), 'w', encoding='utf-8') as fw:
		for row in rows:
			fw.write('{}\t{}\n'.format(row[1], row[0].decode('utf-8')))

# words - hindi - all pos
query = 'SELECT synset_id, word, pos from tbl_all_words'
rows = execute_query(query, [HWN_DB], FETCH_ALL_ROWS, None)
rows = [(int(item[0]), item[1], item[2]) for item in rows]
sorted(rows, key=itemgetter(0))
with codecs.open('data/words/all.hindi', 'w', encoding='utf-8') as fw:
	for row in rows:
		fw.write('{}\t{}\t{}\n'.format(row[0], row[1].decode('utf-8'), row[2].decode('utf-8')))

# words - non-hindi - pos
query = 'show tables'
langs = execute_query(query, [IWN_DB], FETCH_ALL_ROWS, None)
tables = []
for lang_table in langs:
	table = lang_table[0]
	if table.endswith('synset_data') and 'english' not in table:
		lang = table.split("_")[2]
		if lang in ['hindi', 'english', 'synset']:
			continue
		for pos_tag in pos_tags:
			s = set()
			with codecs.open('data/words/all.{}'.format(lang), 'r', encoding='utf-8') as fo:
				for line in fo:
					line = clean_line(line)
					sp = line.split('\t')
					try:
						if sp[2] == pos_tag:
							s.add((sp[0], sp[1]))
					except Exception as e:
						continue
			with codecs.open('data/words/{}.{}'.format(pos_tag, lang), 'w', encoding='utf-8') as fw:
				for item in s:
					fw.write('{}\t{}\n'.format(item[0], item[1]))

# words - non-hindi - all pos
query = 'show tables'
langs = execute_query(query, [IWN_DB], FETCH_ALL_ROWS, None)
for lang_table in langs:
	table = lang_table[0]
	if table.endswith('synset_data') and 'english' not in table:
		lang = table.split("_")[2]
		if lang in ['hindi', 'english']:
			continue
		s = set()
		query = 'SELECT synset_id, synset, category from {}'.format(table)
		rows = execute_query(query, [IWN_DB], FETCH_ALL_ROWS, None)
		for row in rows:
			for word in row[1].split(','):
				if row[2] is None:
					continue
				s.add((row[0], word, row[2].lower()))
		with codecs.open('data/words/all.{}'.format(lang), 'w', encoding='utf-8') as fw:
			for item in s:
				# fw.write('{}\t{}\t{}\n'.format(item[0], item[1], item[2]))
				fw.write('{}\t{}\n'.format(item[0], item[1]))

# non-hindi - synsets - pos
query = 'show tables'
langs = execute_query(query, [IWN_DB], FETCH_ALL_ROWS, None)
for lang_table in langs:
	table = lang_table[0]
	if table.endswith('synset_data') and 'english' not in table:
		lang = table.split("_")[2]
		if lang in ['hindi', 'english', 'synset']:
			continue
		for pos_tag in pos_tags:
			query = 'SELECT synset_id, synset, gloss from {} where category=%s'.format(table)
			rows = execute_query(query, [IWN_DB], FETCH_ALL_ROWS, (pos_tag,))
			rows = [(int(item[0]), item[1], item[2]) for item in rows]
			sorted(rows, key=itemgetter(0))
			with codecs.open('data/synsets/{}.{}'.format(pos_tag, lang), 'w', encoding='utf-8') as fw:
				for row in rows:
					row = [str(item).strip() for item in row]
					row[1] = ','.join(row[1].split(', '))
					row[2] = ':'.join(row[2].split('; '))
					fw.write("\t".join(row))
					fw.write("\n")

# non-hindi - synsets - pos all
query = 'show tables'
langs = execute_query(query, [IWN_DB], FETCH_ALL_ROWS, None)
for lang_table in langs:
	table = lang_table[0]
	if table.endswith('synset_data') and 'english' not in table:
		lang = table.split("_")[2]
		if lang in ['hindi', 'english', 'synset']:
			continue
		query = 'SELECT synset_id, synset, gloss, category from {}'.format(table)
		rows = execute_query(query, [IWN_DB], FETCH_ALL_ROWS, None)
		sorted(rows, key=itemgetter(0))
		with codecs.open('data/synsets/all.{}'.format(lang), 'w', encoding='utf-8') as fw:
			for row in rows:
				row = [str(item).strip() for item in row]
				row[1] = ','.join(row[1].split(', '))
				row[2] = ':'.join(row[2].split('; '))
				row[3] = row[3].lower()
				fw.write("\t".join(row))
				fw.write("\n")

# hindi - synsets - pos
for pos_tag in pos_tags:
	query = 'SELECT synset_id, synset, gloss from tbl_all_synset where category=%s'
	rows = execute_query(query, [HWN_DB], FETCH_ALL_ROWS, (pos_tag,))
	sorted(rows, key=itemgetter(0))
	with codecs.open('data/synsets/{}.hindi'.format(pos_tag), 'w', encoding='utf-8') as fw:
		for row in rows:
			row = [str(item).strip() for item in row]
			fw.write("\t".join(row))
			fw.write("\n")

# hindi - synsets - pos all
query = 'SELECT synset_id, synset, gloss, category from tbl_all_synset'
rows = execute_query(query, [HWN_DB], FETCH_ALL_ROWS, None)
sorted(rows, key=itemgetter(0))
with codecs.open('data/synsets/all.hindi', 'w', encoding='utf-8') as fw:
	for row in rows:
		row = [str(item).strip() for item in row]
		fw.write("\t".join(row))
		fw.write("\n")


# Fetch synset relations
query = 'show tables'
tables = execute_query(query, [HWN_DB], FETCH_ALL_ROWS, None)

for table_list in tables:
	table = table_list[0]
	if 'grad' in table or 'anto' in table or 'relations' in table or 'sense_num' in table or 'derived_from' in table:
		print(table, 'skipped')
		continue
	if table.split("_")[1] in pos_tags:
		relation = "_".join(table.split("_")[2:])
		pos_tag = table.split("_")[1]
		query = 'SHOW COLUMNS FROM {}'.format(table)
		cols = execute_query(query, [HWN_DB], FETCH_ALL_ROWS, None)
		query = 'SELECT * FROM  {}'.format(table)
		rows = execute_query(query, [HWN_DB], FETCH_ALL_ROWS, None)
		sorted(rows, key=itemgetter(0))
		d = {}
		for row in rows:
			if row[0] in d:
				d[row[0]].append(row[1])
			else:
				d[row[0]] = [row[1]]
		with codecs.open('data/synset_relations/{}.{}'.format(relation, pos_tag), 'w', encoding='utf-8') as fw:
			for k, v in d.items():
				fw.write(str(k) + '\t' +','.join([str(item) for item in v]))
				fw.write("\n")


# ontology synset-ontology node map
query = 'SELECT * FROM  tbl_onto_nodes'
rows = execute_query(query, [HWN_DB], FETCH_ALL_ROWS, None)
sorted(rows, key=itemgetter(0))
d = {}
for row in rows:
	if row[0] in d:
		d[row[0]].append(row[1])
	else:
		d[row[0]] = [row[1]]
with codecs.open('data/ontology/map', 'w', encoding='utf-8') as fw:
	for k, v in d.items():
		fw.write(str(k) + '\t' +','.join([str(item) for item in v]))
		fw.write("\n")

ontology-node to description map
query = 'SELECT * FROM  tbl_onto_data'
rows = execute_query(query, [HWN_DB], FETCH_ALL_ROWS, None)
sorted(rows, key=itemgetter(0))
with codecs.open('data/ontology/nodes', 'w', encoding='utf-8') as fw:
	for row in rows:
		row = [str(item).strip() for item in row]
		fw.write("\t".join(row))
		fw.write("\n")