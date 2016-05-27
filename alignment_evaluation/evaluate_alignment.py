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
	marks = [];
	mark = 0
	count = 1
	lines = re.split(r'\d*:\d*:\d*,\d* --> \d*:\d*:\d*,\d*', lines)
	for line in lines:
		marks.append([])
		line_split = re.split(r'- ', line)
		for l in line_split:
			if l:
				marks[mark].append(count)
				count += 1
				subtitles.append(l)
		mark += 1
	return subtitles, marks


auto_aligned_text = auto_align_to_list(auto_align_file)
manual_align      = manual_align_to_dict(manual_align_file)
names             = transcripts_to_list(transcripts_file)
subtitles, marks  = subtitles_to_list(subtitle_file)

#print "length auto aligned", len(auto_aligned_text)
#pprint.pprint(auto_aligned_text)
#print "length names", len(names)
# pprint.pprint(names)
#print "length subtitles", len(subtitles)
# print names[0], subtitles[0]

#####

# What line(s) does subtitle #640 in .srt correspond to in manual_align?
pprint.pprint(marks[640]) # [690, 691]
# What lines do these subtitles correspond to in transcript (from manual_align)?
pprint.pprint(manual_align['690']) # 325
pprint.pprint(manual_align['691']) # 326
# Whare are these names in transcript?
pprint.pprint(names[325]) # BRAN_STARK
pprint.pprint(names[326]) # JAIME_LANNISTER



# Where they in the automagic translation?
pprint.pprint(auto_aligned_text[ ??? ] )

# -----

# Now trying to do that in a program:


i = 0
for x in range(0, len(marks)):
	for y in marks[x]:
		z = manual_align[str(y)]
		if z != 'x':
			print " manual > [%s - %s]" % (z, names[int(z)])
			print " auto   > [%s - %s]" % (i, auto_aligned_text[i])
			print " "
			i += 1


#subtitles[690])

pprint.pprint(auto_aligned_text);
#(subtitles);
#pprint.pprint(manual_align)
