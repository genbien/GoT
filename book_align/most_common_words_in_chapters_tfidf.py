# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
import math
import re
from textblob import TextBlob as tb
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
                        book.append(tb(chapter))
                    chapter = []
                else:
                    # preprocess line and put into chapter
                    line = preprocess(line)
                    chapter.append(line)
        # put the last chapter in the book
        i += 1
        chapter = ' '.join(chapter)
        book.append(tb(chapter))
    return(book)


def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

book_file = '../../../0_corpus/books/AGameOfThrones.txt'
book = parse_book(book_file)

for i, blob in enumerate(book):
    print("Chapter {}".format(i + 1))
    print("\tNumber of words: {}".format(len(blob.words)))
    print("\tTop words:")
    scores = {word: tfidf(word, blob, book) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:5]:
        print("\t\tWord: {}\tTF-IDF: {}\tFreq: {}".format(word, round(score, 5), blob.word_counts[word]))