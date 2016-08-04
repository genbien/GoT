# -*- coding: utf-8 -*-
################################################################################
##
## align book chapters and scenes from episode recaps
##
################################################################################

from __future__ import print_function
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
                        chapter = tokenize(chapter)
                        chapter = set(chapter)
                        book.append((chapter, i))
                    chapter = []
                else:
                    # preprocess line and put into chapter
                    line = preprocess(line)
                    chapter.append(line)
        # put the last chapter in the book
        i += 1
        chapter = ' '.join(chapter)
        chapter = tokenize(chapter)
        chapter = set(chapter)
        book.append((chapter, i))
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
                    scene = tokenize(scene)
                    scene = set(scene)
                    scenes.append((scene, ep, nb))
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

distances = collections.OrderedDict()
for chapter in book:
    for scene in scenes:
        this_scene = '('+str(scene[1])+', '+str(scene[2])+')'
        if this_scene in distances:
            distances[this_scene].append((chapter[1], len(scene[0]) - len(scene[0] & chapter[0])))
        else:
            distances[this_scene] = [(chapter[1], len(scene[0]) - len(scene[0] & chapter[0]))]
        print('Distance: scene ('+str(scene[1])+', '+str(scene[2])+') chapter: ('+str(chapter[1])+') = '+str(len(scene[0]) - len(scene[0] & chapter[0])))


plot_file = open("distance_plot_points.txt", 'w')
ep1 = open("scene_chapter_auto_align/common_words/auto_align_ep01.txt", 'w')
ep2 = open("scene_chapter_auto_align/common_words/auto_align_ep02.txt", 'w')
ep3 = open("scene_chapter_auto_align/common_words/auto_align_ep03.txt", 'w')
ep4 = open("scene_chapter_auto_align/common_words/auto_align_ep04.txt", 'w')
ep5 = open("scene_chapter_auto_align/common_words/auto_align_ep05.txt", 'w')

x = []
y = []
scene_count = 1
print('scene\tchapter')
for d in distances:
    if 0 < scene_count and scene_count < 36:
        print(str(scene_count)+'\t'+str(sorted(distances[d], key=operator.itemgetter(1))[0][0]), file=ep1)
    if 35 < scene_count and scene_count < 67:
        print(str(scene_count)+'\t'+str(sorted(distances[d], key=operator.itemgetter(1))[0][0]), file=ep2)
    if 66 < scene_count and scene_count < 94:
        print(str(scene_count)+'\t'+str(sorted(distances[d], key=operator.itemgetter(1))[0][0]), file=ep3)
    if 93 < scene_count and scene_count < 120:
        print(str(scene_count)+'\t'+str(sorted(distances[d], key=operator.itemgetter(1))[0][0]), file=ep4)
    if 119 < scene_count and scene_count < 146:
        print(str(scene_count)+'\t'+str(sorted(distances[d], key=operator.itemgetter(1))[0][0]), file=ep5)
    print(str(scene_count)+'\t'+str(sorted(distances[d], key=operator.itemgetter(1))[0][0]), file=plot_file)
    x.append(scene_count)
    y.append(sorted(distances[d], key=operator.itemgetter(1))[0][0])
    scene_count += 1



plt.title('Game of Thrones book 1 and season 1 - chapter and scene alignment')
plt.xlabel('scenes')
plt.ylabel('chapters')
# [xmin, xmax, ymin, ymax]
plt.axis([0, len(scenes), 0, len(book)])
plt.scatter(x, y)
plt.savefig('GoT_chapter_scene_alignment_words_in_common.eps', format='eps', dpi=1000)
# plt.show()