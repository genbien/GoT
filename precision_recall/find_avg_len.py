# -*- coding: utf-8 -*-

################################################################################
##
## Find average length of scenes and recaps for each episode
##
################################################################################

import re
import pprint
import numpy as np
from tvd import GameOfThrones
from pyannote.parser import SRTParser
from contractions import *

dataset = GameOfThrones('../../../0_corpus/tvd')
recaps_txt_dir = '../../../0_corpus/recaps/recaps_txt'

def cleanText(text):
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


def getScenes(dataset, episode):
    sequence  = []
    with open(recaps_txt_dir+'/'+str(episode)+'.txt') as f:
        recap = f.read().replace('\n', '')
    recap = re.split(r'=== SCENE \d+ ===', recap)
    nb = 1
    for scene in recap:
        if scene:
            # preprocess
            scene = cleanText(scene)
            sequence.append(scene)
            nb += 1
    # ('walking through the red keep eddard is intercepted')
    return sequence


def getTranscripts(dataset, episode):
    sequence   = []
    transcript = dataset.get_resource('transcript', episode)
    for start, end, data in transcript.ordered_edges_iter(data=True):
        if 'speaker' not in data:
            continue
        # UTF8 encoding + strip
        speech  = data['speech'].encode('utf8').strip()
        # preprocess
        speech = cleanText(speech)
        speaker = data['speaker']
        sequence.append(speech)
    ## ('a crown for a king')
    return sequence


print '------------------------------------------------------------------------'
for episode in dataset.episodes[:5]:
    scene      = getScenes(dataset, episode)
    transcript = getTranscripts(dataset, episode)

    len_scenes = []
    for s in scene:
        words = s.split(' ')
        len_scenes.append(len(words))

    len_transcripts = []
    for t in transcript:
        words = t.split(' ')
        len_transcripts.append(len(words))


    print '['+str(episode)+']'
    print '\t- scene average length..........:  '+str(round(np.mean(len_scenes), 3))+' words'
    print '\t- transcript average length.....:   '+str(round(np.mean(len_transcripts), 3))+' words'
    print '\t- total words in scene recaps...: '+str(np.sum(len_scenes))+' words'
    print '\t- total words in transcripts....: '+str(np.sum(len_transcripts))+' words'
    print '\t- number of scenes..............:   '+str(len(len_scenes))+' scenes'
    print '\t- number of transcripts.........:  '+str(len(len_transcripts))+' transcripts'
    print '\t- avg # of transcripts per scene:   '+str(round(len(len_transcripts)/float(len(len_scenes)), 3))+' transcripts'

print '------------------------------------------------------------------------'