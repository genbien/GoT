# -*- coding: utf-8 -*-
from pprint import pprint

GREEN    = '\033[92m'
YELLOW   = '\033[33m'
RED      = '\033[31m'
ENDCOLOR = '\033[0m'

ep = '01'
# can be    :    '',      'lemma_',   'word2vec_', 'pos_', 'word2vec2_', 'pos2_','doc2vec_', 'word2vec3_', 'word2vec4_'
# distance #: (1, 2, 3)  (2.5, 3.5)       (4)       (4.5)      (5)        (5.5)     (6)          (7)          (8)
# align_t = 'word2vec4_'

# hypothesis: automatically aligned file
# reference : manually aligned file

# hypothesis_file = '../recap_aligned/'+align_t+'auto_align/tuples/auto_aligned_GameOfThrones.Season01.Episode'+ep+'.txt' ## scene + transcript
# reference_file  = '../recap_aligned/manual_align/manual_aligned_GameOfThrones.Season01.Episode'+ep+'.txt' ## scene + transcript

# tfidf_with_transcripts ... tfidf ... common_lemmas ... common_words
hypothesis_file = '../book_align/scene_chapter_auto_align/common_words/auto_align_ep'+ep+'.txt' ## scene + chapter
reference_file  = '../../../0_corpus/annotations/scene_chapter_manual_align/Xscene_chapter_manual_align_ep'+ep+'.txt' ## scene + chapter

hyp = set()
ref = set()

# add each line from a file to a set.
# file format:
# (number|'x')\t(number|'x')
def make_sets(filename, setname):
	with open(filename) as f:
		for line in f:
			line = line.rstrip()
			if line.startswith('%'):
				continue
			else:
				line = line.split('\t')
				setname.add((line[0], line[1]))

# make hypothesis and reference sets
make_sets(hypothesis_file, hyp)
make_sets(reference_file, ref)

# example :
#			- hypothesis-set((0,1), (1, 3), (2, 4))
#			- reference-set((0,1), (1, 4), (2, 4))
#
# - TP == elements that are in both the reference-set and the hypothesis-set (ie ((0,1), (2, 4)))
# - FN == all elements in the reference-set that are not also in the hypothesis-set (ie (1, 4))
# - FP == all elements in the hypothesis-set that are not also in the reference-set (ie (1, 3))

# calculate true positive, false positive, and false negative for precision and recall
tp = float(len(hyp & ref))
fp = float(len(hyp - ref))
fn = float(len(ref - hyp))

print GREEN+"true positives"+ENDCOLOR
for alignment in hyp & ref:
	print GREEN+str(alignment)+ENDCOLOR
print YELLOW+"false positives"+ENDCOLOR
for alignment in hyp - ref:
	print YELLOW+str(alignment)+ENDCOLOR
print RED+"false negatives"+ENDCOLOR
for alignment in ref - hyp:
	print RED+str(alignment)+ENDCOLOR

precision = tp / (tp + fp)
recall = tp / (tp + fn)

# The F-score is the harmonic mean of the precision and the recall.
# An F-score ranges between 0 (worst) and 1 (best).
fscore = (2 * ((precision * recall)/(precision + recall)))

print '=+=+=+=+=+=+=+=+=+=+=+=+=+=+='
print 'Calculations:'
print '- - - - - - -'
print 'Precision...:', precision
print 'Recall......:', recall
print 'F-score.....:', fscore
print '=+=+=+=+=+=+=+=+=+=+=+=+=+=+='
