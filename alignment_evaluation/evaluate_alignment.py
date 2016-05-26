################################################################################
##                                                                            ##
## program to evaluate the accuracy of automatically aligned                  ##
## subtitles and transcripts for Game of Thrones.                             ##
##                                                                            ##
################################################################################

import re
import collections
import pprint

transcripts_file  = 'GameOfThrones.Season01.Episode01.txt'
subtitle_file     = 'GameOfThrones.Season01.Episode01.en.srt'
manual_align_file = 'manual_alignment_subtitles_transcripts_ep01.txt'
## automatically aligned file we want to compare to the manually aligned file
auto_align_file   = 'aligned_GameOfThrones.Season01.Episode01.txt'


def auto_align_to_list(auto_align_file):
	auto_aligned_text = []
	with open(auto_align_file) as f:
		for line in f:
			line = line.rstrip()
			## put speaker and line information in the list, ignore time
			text = line.split(" ", 2)[2]
			auto_aligned_text.append(text)
	return auto_aligned_text


def manual_align_to_dict(manual_align_file):
	manual_align = collections.OrderedDict()
	with open(manual_align_file) as f:
		align = f.readlines()
	for line in align:
		line = line.rstrip()
		if line.startswith('%'):
			pass
		else:
			line_s = line.split('\t')
			manual_align[line_s[0]] = line_s[1]
	return manual_align


def transcripts_to_list(transcripts_file):
	names = []
	with open(transcripts_file) as f:
		for line in f:
			line = line.rstrip()
			## only keep speaker information
			name = line.split(" ", 1)[0]
			names.append(name)
	return names


def subtitles_to_list(subtitle_file):
	subtitles = []
	with open(subtitle_file) as f:
		lines = f.read().replace('\n', '')
	## split on timestamp
	lines = re.split(r'\d*:\d*:\d*,\d* --> \d*:\d*:\d*,\d*', lines)
	for line in lines:
		line_split = re.split(r'- ', line)
		for l in line_split:
			if l:
				subtitles.append(l)
	return subtitles


auto_aligned_text = auto_align_to_list(auto_align_file)
manual_align      = manual_align_to_dict(manual_align_file)
names             = transcripts_to_list(transcripts_file)
subtitles         = subtitles_to_list(subtitle_file)

# print "length auto aligned", len(auto_aligned_text)
# pprint.pprint(auto_aligned_text)
# print "length names", len(names)
# pprint.pprint(names)
# print "length subtitles", len(subtitles)
# print names[0], subtitles[0]


# i = 0
# j = 0
# while i <= len(subtitles) and j <= len(names):
# 	j += 1
# 	i += 1