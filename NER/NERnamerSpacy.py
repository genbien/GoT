import spacy.en
import pprint
import collections


parser = spacy.en.English()

full_text_file = '../book_align/scene_chapter_auto_align/tfidf_with_transcripts/full_text/auto_align_ep01.txt'

scene_text = collections.OrderedDict()

with open(full_text_file, 'r') as f:
    for line in f:
        line = line.rstrip()
        line = line.split('\t')
        if line[0] in scene_text:
            scene_text[line[0]] += line[1]
        else:
            scene_text[line[0]] = line[1]


for scene in scene_text:
    parsed = parser(unicode(scene_text[scene]))
    print scene
    for ent in parsed.ents:
        print ent.label_,' '.join(t.orth_ for t in ent)
    print '--------------------------------------------------------------------'
