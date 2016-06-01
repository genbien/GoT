# -*- coding: utf-8 -*-
from pprint import pprint

# hypothesis: automatically aligned file
# reference : manually aligned file
hypothesis_file = 'auto_subtitles_transcripts/auto_aligned_GameOfThrones.Season01.Episode03.txt'
reference_file  = 'manual_subtitles_transcripts/manual_alignment_subtitles_transcripts_ep03.txt'

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
