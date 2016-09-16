# -*- coding:utf-8 -*-

import pprint
import collections
from contractions import *

def most_common(lst):
    data = collections.Counter(lst)
    return data.most_common(1)

def preprocess(text):
    text = text.lower()
    text = expandContractions(text)
    text = text.replace(".", "")
    text = text.replace(",", "")
    text = text.replace(";", "")
    text = text.replace(":", "")
    text = text.replace("?", "")
    text = text.replace("!", "")
    text = text.replace("- ", "")
    text = text.replace("\"", "")
    text = text.replace("\'", "")
    text = text.replace("-- ", "")
    text = text.replace(" --", "")
    text = text.replace("- ", "")
    text = text.replace("– ", "")
    text = text.replace("(", "")
    text = text.replace(")", "")
    return text



loc_file = "list_locations_got.txt"

location_list = []

with open(loc_file, 'r') as loc_f:
    for line in loc_f:
        line = line.rstrip()
        line = preprocess(line)
        location_list.append(line)


## text contains scene recaps and chapters as aligned by the scenerecap+chapter+transcript tfidf method
full_text_file = '../book_align/scene_chapter_auto_align/tfidf_with_transcripts/full_text/auto_align_ep01.txt'

scene_text = collections.OrderedDict()

with open(full_text_file, 'r') as f:
    for line in f:
        line = line.rstrip()
        line = line.split('\t')
        if line[0] in scene_text:
            line[1] = preprocess(line[1])
            scene_text[line[0]] += line[1]
        else:
            line[1] = preprocess(line[1])
            scene_text[line[0]] = line[1]


locations_dict = {}
nb = 0
for scene in scene_text.values():
    l_in_scene = [l for l in location_list if l in scene]
    locations_dict[nb] = []
    ## put all locations mentioned in a scene into
    ## a list of locations in the scene (as values in a dict (key == scene number))
    for l in l_in_scene:
        if l not in locations_dict.values():
            locations_dict[nb].append(l)
    nb += 1


for scene in locations_dict:
    print scene, most_common(locations_dict[scene])