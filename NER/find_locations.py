import collections

ner_file = 'GoT_ep01_chapter_scene_NER_from_tfidf_with_transcripts.txt'

def most_common(lst):
    data = collections.Counter(lst)
    return data.most_common(1)

with open(ner_file, 'r') as f:
	lines = f.read().splitlines()

i = 0
scenes = collections.OrderedDict()

while i < len(lines):
	if lines[i][0].isdigit():
		scenes[lines[i]] = []
		nb = lines[i]
		i += 1
		while lines[i][0].isalpha():
			tag, loc = lines[i].split(' ', 1)
			# if tag == 'LOC' or tag == 'ORG':
			if tag == 'LOC':
				scenes[nb].append(loc)
			i += 1
	i += 1


for scene in scenes:
	print scene, most_common(scenes[scene])


