import re
import collections
import pprint

transcripts_file  = 'GameOfThrones.Season01.Episode01.txt'
subtitle_file     = 'GameOfThrones.Season01.Episode01.en.srt'
manual_align_file = 'mod_manual_alignment_subtitles_transcripts_ep01.txt'

def transcripts_to_list(transcripts_file):
	names = []
	with open(transcripts_file) as f:
		for line in f:
			line = line.rstrip()
			name = line.split(" ", 1)[0]
			names.append(name)
	return names


def subtitles_to_list(subtitle_file):
	subtitles = []
	with open(subtitle_file) as f:
		lines = f.read().replace('\n', '')
	lines = re.split(r'\d*:\d*:\d*,\d* --> \d*:\d*:\d*,\d*', lines)
	for line in lines:
		line_split = re.split(r'- ', line)
		for l in line_split:
			if l:
				subtitles.append(l)
	return subtitles


names = transcripts_to_list(transcripts_file)
subtitles = subtitles_to_list(subtitle_file)

# print "length", len(subtitles)
print names[0], subtitles[0]

## indexes all start at 0 (with modify_subtitle_numbers.py)
with open(manual_align_file) as f:
	for line in f:
		line = line.rstrip()
		if line.startswith('%'):
			pass
		else:
			# print line
			index = line.split('\t')