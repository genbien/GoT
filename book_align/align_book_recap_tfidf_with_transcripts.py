# -*- coding: utf-8 -*-
################################################################################
##
## align book chapters (with added aligned transcripts) and scenes from episode recaps
##
################################################################################

from __future__ import print_function

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from tvd import GameOfThrones
from pyannote.parser import SRTParser
from pyannote.algorithms.alignment.dtw import DynamicTimeWarping

import re
import os
import pprint
import operator
import collections
import matplotlib.pyplot as plt
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


def parse_book(book_file, flag):
    # chapter titles are all caps and only one word
    title_pattern = re.compile("^[A-Z]+$")

    book    = []
    chapter = []
    i = 0
    with open(book_file, 'r') as f:
        for line in f:
            line = line.rstrip()
            if line:
                if title_pattern.match(line):
                    # if there's something in the chapter, put it in the book
                    if chapter:
                        i += 1
                        chapter = ' '.join(chapter)
                        book.append(chapter)
                    chapter = []
                else:
                    # preprocess line and put into chapter
                    if flag == 1:
                        line = preprocess(line)
                    chapter.append(line)
        # put the last chapter in the book
        i += 1
        chapter = ' '.join(chapter)
        book.append(chapter)
    return(book)


def parse_scenes(scenes_dir, flag):
    scenes = []
    ep = 1
    for filename in os.listdir(scenes_dir):
        if filename.endswith('ascii.txt'):
            with open(scenes_dir+filename, 'r') as f:
                recap = f.read().replace('\n', '')
            recap = re.split(r'=== SCENE \d+ ===', recap)
            nb = 1
            recap.pop(0)
            for scene in recap:
                if scene:
                    # preprocess
                    if flag == 1:
                        scene = preprocess(scene)
                    scenes.append(scene)
                nb += 1
            ep += 1
    return scenes


# This function generates a sequence of scene formatted in such a way it
# can be used with DTW
def dtwScenes(dataset, episode):
    sequence  = []
    with open(scenes_dir+'/'+str(episode)+'.txt') as f:
        recap = f.read().replace('\n', '')
    recap = re.split(r'=== SCENE \d+ ===', recap)
    nb = 1
    for scene in recap:
        if scene:
            # preprocess
            scene = preprocess(scene)
            sequence.append((scene, nb))
            nb += 1
    # ("Walking through the Red Keep, Eddard is intercepted ...", 19),
    return sequence


# This function generates a sequence of transcripts formatted in such a way it
# can be used with DTW
def dtwTranscript(dataset, episode):
    sequence   = []
    transcript = dataset.get_resource('transcript', episode)
    for start, end, data in transcript.ordered_edges_iter(data=True):
        if 'speaker' not in data:
            continue
        # UTF8 encoding + strip
        speech  = data['speech'].encode('utf8').strip()
        # preprocess
        speech = preprocess(speech)
        speaker = data['speaker']
        sequence.append((speech, speaker))
    ## ('A crown for a King.', u'KHAL_DROGO'),
    return sequence


# This function takes one element of each sequence and returns a distance based
# on the number of common words
def dtwDistance(scene, transcript):
    scene = scene[0]
    transcript = transcript[0]
    scene_words = set(scene.split())
    transcript_words = set(transcript.split())
    # number of unique words in transcripts - number of unique words in common
    return len(transcript_words) - len(transcript_words & scene_words)


dataset = GameOfThrones('../../../0_corpus/tvd')
book_file  = '../../../0_corpus/books/AGameOfThrones.txt'
scenes_dir = '../../../0_corpus/recaps/recaps_txt/'

book   = parse_book(book_file, 1)
scenes = parse_scenes(scenes_dir, 1)

# don't preprocess for NER text
book_for_text   = parse_book(book_file, 0)
scenes_for_text = parse_scenes(scenes_dir, 0)

print('# of chapters: '+str(len(book)))
print('# of scenes: '+str(len(scenes)))
# pprint.pprint(book)
# pprint.pprint(scenes)

# scene are vertical and transcripts are horizontal
# make sure that DTW doesn't align a transcript to multiple scenes by adding no_vertical=True
dtw = DynamicTimeWarping(distance_func=dtwDistance, no_vertical=True)

for episode in dataset.episodes[:5]:
    # extract scene and transcript sequences
    scene      = dtwScenes(dataset, episode)
    transcript = dtwTranscript(dataset, episode)

    # dynamic time warping
    alignment = set(dtw(scene, transcript))

    for s, t in alignment:
        e = str(episode)
        scene_idx = scene[s][1]
        if e.endswith('02'):
            scene_idx += 35
        if e.endswith('03'):
            scene_idx += (35 + 31)
        if e.endswith('04'):
            scene_idx += (35 + 31 + 27)
        if e.endswith('05'):
            scene_idx += (35 + 31 + 27 + 26)

        if 0 < scene_idx and scene_idx < 36:
            scenes[scene_idx - 1] += ' '+transcript[t][0]
        if 35 < scene_idx and scene_idx < 67:
            scenes[scene_idx - 1] += ' '+transcript[t][0]
        if 66 < scene_idx and scene_idx < 94:
            scenes[scene_idx - 1] += ' '+transcript[t][0]
        if 93 < scene_idx and scene_idx < 120:
            scenes[scene_idx - 1] += ' '+transcript[t][0]
        if 119 < scene_idx and scene_idx < 146:
            scenes[scene_idx - 1] += ' '+transcript[t][0]


tfidf_vectorizer = TfidfVectorizer(stop_words='english')

## tfidf of chapters
chapter_matrix = tfidf_vectorizer.fit_transform(book)

## tfidf of recaps
scene_matrix = tfidf_vectorizer.transform(scenes)

# cosine similarities for chapters and recaps
distances = []
for i, s in enumerate(scene_matrix):
    sim = cosine_similarity(scene_matrix[i], chapter_matrix)
    max_index, max_value = max(enumerate(sim[0]), key=operator.itemgetter(1))
    ## +1 because index in ground truth starts at 1 not 0
    ## append (scene#, chapter#) to distances
    if max_value > 0.25:
        distances.append((i + 1, max_index + 1))
    else:
        distances.append((i + 1, 'x'))


plot_file = open("distance_plot_points.txt", 'w')
ep1 = open("scene_chapter_auto_align/tfidf_with_transcripts/auto_align_ep01.txt", 'w')
ep2 = open("scene_chapter_auto_align/tfidf_with_transcripts/auto_align_ep02.txt", 'w')
ep3 = open("scene_chapter_auto_align/tfidf_with_transcripts/auto_align_ep03.txt", 'w')
ep4 = open("scene_chapter_auto_align/tfidf_with_transcripts/auto_align_ep04.txt", 'w')
ep5 = open("scene_chapter_auto_align/tfidf_with_transcripts/auto_align_ep05.txt", 'w')

ep1_full_text = open("scene_chapter_auto_align/tfidf_with_transcripts/full_text/auto_align_ep01.txt", 'w')
ep2_full_text = open("scene_chapter_auto_align/tfidf_with_transcripts/full_text/auto_align_ep02.txt", 'w')
ep3_full_text = open("scene_chapter_auto_align/tfidf_with_transcripts/full_text/auto_align_ep03.txt", 'w')
ep4_full_text = open("scene_chapter_auto_align/tfidf_with_transcripts/full_text/auto_align_ep04.txt", 'w')
ep5_full_text = open("scene_chapter_auto_align/tfidf_with_transcripts/full_text/auto_align_ep05.txt", 'w')


x = []
y = []

for d in distances:
    print(d[0], d[1])
    if 0 < d[0] and d[0] < 36:
        print(str(d[0])+'\t'+str(d[1]), file=ep1)
        if d[0] != 'x' and d[1] != 'x':
            print(str(d[0])+'\t'+scenes_for_text[d[0] - 1], file=ep1_full_text)
            print(str(d[0])+'\t'+book_for_text[d[1] - 1], file=ep1_full_text)
        elif d[0] != 'x':
            print(str(d[0])+'\t'+scenes_for_text[d[0] - 1], file=ep1_full_text)
    if 35 < d[0] and d[0] < 67:
        print(str(d[0])+'\t'+str(d[1]), file=ep2)
        if d[0] != 'x' and d[1] != 'x':
            print(str(d[0])+'\t'+scenes_for_text[d[0] - 1], file=ep2_full_text)
            print(str(d[0])+'\t'+book_for_text[d[1] - 1], file=ep2_full_text)
        elif d[0] != 'x':
            print(str(d[0])+'\t'+scenes_for_text[d[0] - 1], file=ep2_full_text)
    if 66 < d[0] and d[0] < 94:
        print(str(d[0])+'\t'+str(d[1]), file=ep3)
        if d[0] != 'x' and d[1] != 'x':
            print(str(d[0])+'\t'+scenes_for_text[d[0] - 1], file=ep3_full_text)
            print(str(d[0])+'\t'+book_for_text[d[1] - 1], file=ep3_full_text)
        elif d[0] != 'x':
            print(str(d[0])+'\t'+scenes_for_text[d[0] - 1], file=ep3_full_text)
    if 93 < d[0] and d[0] < 120:
        print(str(d[0])+'\t'+str(d[1]), file=ep4)
        if d[0] != 'x' and d[1] != 'x':
            print(str(d[0])+'\t'+scenes_for_text[d[0] - 1], file=ep4_full_text)
            print(str(d[0])+'\t'+book_for_text[d[1] - 1], file=ep4_full_text)
        elif d[0] != 'x':
            print(str(d[0])+'\t'+scenes_for_text[d[0] - 1], file=ep4_full_text)
    if 119 < d[0] and d[0] < 146:
        print(str(d[0])+'\t'+str(d[1]), file=ep5)
        if d[0] != 'x' and d[1] != 'x':
            print(str(d[0])+'\t'+scenes_for_text[d[0] - 1], file=ep5_full_text)
            print(str(d[0])+'\t'+book_for_text[d[1] - 1], file=ep5_full_text)
        elif d[0] != 'x':
            print(str(d[0])+'\t'+scenes_for_text[d[0] - 1], file=ep5_full_text)
    print(str(d[0])+'\t'+str(d[1]), file=plot_file)
    if d[1] != 'x':
        x.append(d[0])
        y.append(d[1])




plt.title('Game of Thrones book 1 and season 1 - chapter and scene alignment -- tfidf')
plt.xlabel('scenes')
plt.ylabel('chapters')
# [xmin, xmax, ymin, ymax]
plt.axis([0, len(scenes), 0, len(book)])
plt.scatter(x, y)
plt.savefig('GoT_chapter_scene_alignment_tfidf_with_transcripts.eps', format='eps', dpi=1000)
# plt.show()