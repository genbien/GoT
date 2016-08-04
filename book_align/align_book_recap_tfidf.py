# -*- coding: utf-8 -*-
################################################################################
##
## align book chapters and scenes from episode recaps
##
################################################################################

from __future__ import print_function

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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


def parse_book(book_file):
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
                    line = preprocess(line)
                    chapter.append(line)
        # put the last chapter in the book
        i += 1
        chapter = ' '.join(chapter)
        book.append(chapter)
    return(book)


def parse_scenes(scenes_dir):
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
                    scene = preprocess(scene)
                    scenes.append(scene)
                nb += 1
            ep += 1
    return scenes


book_file  = '../../../0_corpus/books/AGameOfThrones.txt'
scenes_dir = '../../../0_corpus/recaps/recaps_txt/'

book   = parse_book(book_file)
scenes = parse_scenes(scenes_dir)

print('# of chapters: '+str(len(book)))
print('# of scenes: '+str(len(scenes)))
# pprint.pprint(book)
# pprint.pprint(scenes)

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
    ## only align if the tfidf score is higher than 0.25
    if max_value > 0.25:
        ## +1 because index in ground truth starts at 1 not 0
        distances.append((i + 1, max_index + 1))
    else:
        distances.append((i + 1, 'x'))

# pprint.pprint(distances)

plot_file = open("distance_plot_points.txt", 'w')
ep1 = open("scene_chapter_auto_align/tfidf/auto_align_ep01.txt", 'w')
ep2 = open("scene_chapter_auto_align/tfidf/auto_align_ep02.txt", 'w')
ep3 = open("scene_chapter_auto_align/tfidf/auto_align_ep03.txt", 'w')
ep4 = open("scene_chapter_auto_align/tfidf/auto_align_ep04.txt", 'w')
ep5 = open("scene_chapter_auto_align/tfidf/auto_align_ep05.txt", 'w')

x = []
y = []
scene_count = 1
print('scene\tchapter')
for d in distances:
    print(d[0], d[1])
    if 0 < d[0] and d[0] < 36:
        print(str(d[0])+'\t'+str(d[1]), file=ep1)
    if 35 < d[0] and d[0] < 67:
        print(str(d[0])+'\t'+str(d[1]), file=ep2)
    if 66 < d[0] and d[0] < 94:
        print(str(d[0])+'\t'+str(d[1]), file=ep3)
    if 93 < d[0] and d[0] < 120:
        print(str(d[0])+'\t'+str(d[1]), file=ep4)
    if 119 < d[0] and d[0] < 146:
        print(str(d[0])+'\t'+str(d[1]), file=ep5)
    print(str(d[0])+'\t'+str(d[1]), file=plot_file)
    if d[1] != 'x':
        x.append(d[0])
        y.append(d[1])
    scene_count += 1



plt.title('Game of Thrones book 1 and season 1 - chapter and scene alignment -- tfidf')
plt.xlabel('scenes')
plt.ylabel('chapters')
# [xmin, xmax, ymin, ymax]
plt.axis([0, len(scenes), 0, len(book)])
plt.scatter(x, y)
plt.savefig('GoT_chapter_scene_alignment_tfidf.eps', format='eps', dpi=1000)
# plt.show()