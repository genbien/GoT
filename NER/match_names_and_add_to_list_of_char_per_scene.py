# -*- coding: UTF-8 -*-

################################################################################
##
## mactch chatacter names from a list to the scene recaps to find missing
## characters in a scene (those with no speaking role)
##
################################################################################

import json
import pprint
from character_dictionary import characters
from contractions import *

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


def tokenize(text):
    text = text.split(' ')
    return text

## too much ambiguity if we search by first or last name, too many characters share a last name
## most characters are refered to by their first names
list_char   = 'season1_got_list_characters_first_names.txt'
recaps_file = '../../../0_corpus/recaps/recaps_txt/GameOfThrones.Season01.Episode01.ascii.txt'

characters_list = []

with open(list_char, 'r') as char_f:
    for line in char_f:
        line = line.rstrip()
        line = preprocess(line)
        characters_list.append(line)



def parse_recaps(recaps_file):
    character_dict = {}
    with open(recaps_file, 'r') as f:
        recap = f.read().replace('\n', '')
    recap = re.split(r'=== SCENE \d+ ===', recap)
    nb = 0
    recap.pop(0)
    for scene in recap:
        if scene:
            # preprocess
            scene = preprocess(scene)
            c_in_scene = [c for c in characters_list if c in scene]
            character_dict[nb] = []
            ## put all characters mentioned in a scene by their first name into
            ## a list of characters in the scene (as values in a dict (key == scene numebr))
            for c in c_in_scene:
                if c not in character_dict.values():
                    character_dict[nb].append(c)

        nb += 1
    return character_dict



character_dict = parse_recaps(recaps_file)

character_dict_ids = {}
for seg in character_dict:
    character_dict_ids[seg] = []
    for c in character_dict[seg]:
        tmp = []
        for p in characters:
            if c.upper() in p:
                tmp.append(p)
        if len(tmp) == 1:
            character_dict_ids[seg].append(characters[tmp[0]])


with open('data_to_append.json') as data_file:
    data = json.load(data_file)

char_list_final = {}
for i, s in enumerate(data["scenes"]):
    char_list_final[i] = []
    for c_id in s:
        char_list_final[i].append(c_id)
    for ids in character_dict_ids[i]:
        if ids not in s:
            char_list_final[i].append(ids)


pprint.pprint(data["scenes"])
pprint.pprint(char_list_final)
