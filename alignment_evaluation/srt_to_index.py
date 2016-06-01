################################################################################
##                                                                            ##
## program to evaluate the accuracy of automatically aligned                  ##
## subtitles and transcripts for Game of Thrones.                             ##
##                                                                            ##
################################################################################

import re
import sys
import collections
from pprint import pprint

# define episode number on the command line or in run_eval.sh
episode = sys.argv[1]

subtitle_file     = 'subtitles/GameOfThrones.Season01.Episode'+episode+'.en.srt'
manual_align_file = 'manual_aligned/manual_alignment_subtitles_transcripts_ep'+episode+'.txt'
transcripts_file  = 'transcripts/GameOfThrones.Season01.Episode'+episode+'.txt'

# Turns subtitle file with format
#  642
#  00:57:55,599 --> 00:57:57,829
#  - The things I do for love.
#  - (Gash)
# Into an array of format
#   [ ('642', '00:57:55,599 --> 00:57:57,829', 692, 'The things I do for love. '),
#     ('642', '00:57:55,599 --> 00:57:57,829', 693, '(Gash)'),
#     ... ]
def parse_subtitles(filename):
	subtitles = []
	with open(filename) as f:
		lines = f.read()
	count = 0

	reg_quote_str = r"^- "
	reg_quote = re.compile(reg_quote_str, re.MULTILINE);

	reg_group_str = r"([0-9]+)\n([:,0-9]+ --> [:,0-9]+)\n(.*?)\n\n\n"
	reg_group = re.compile(reg_group_str, re.MULTILINE | re.DOTALL)

	groups = reg_group.findall(lines);
	for group in groups:
		quotes = re.split(reg_quote, group[2])
		for quote in quotes:
			if quote == '':
				continue
			quote = quote.replace("\n", ' ').rstrip()
			subtitles.append((group[0], group[1], count, quote))
			count += 1

	return subtitles;

# Turns manual alignment file with format
#  0 x
#  1 5
# Into an array with format
#  ['x', '5']
def manual_align_to_dict(filename):
	align = [];

	reg_align_str = r"^[0-9]+\t(x|[0-9]+)$"
	reg_align = re.compile(reg_align_str, re.MULTILINE);
	with open(filename) as f:
		lines = f.read()

	return re.findall(reg_align, lines);

# Turns transcript file with format
#  JAIME_LANNISTER : The things I do for love.
# Into an array with format
# [('JAIME_LANNISTER', 'The things I do for love.'), ...]
def transcripts_to_list(filename):
	script = []

	reg_quote_str = r"^([^ ]+) : (.*)$"
	reg_quote = re.compile(reg_quote_str, re.MULTILINE);

	with open(filename) as f:
		lines = f.read()
	return re.findall(reg_quote, lines);


quotes = parse_subtitles(subtitle_file)
align = manual_align_to_dict(manual_align_file)
script = transcripts_to_list(transcripts_file)

absent = 0

for sub in quotes:                           # for all quotes in the subtitle file
	abs_index = sub[2]                       # get the quote index that correspond
	if align[abs_index] != 'x':              # if the quote has a match in the transcript
		script_index = int(align[abs_index]) # get the line number of the match in the transcript
		script_line = script[script_index]   # get the (name, text) from the transcript
		subs_quote = sub[3]                  # get the (text) from the subtitles
		subs_quote = re.sub(r"^\([^)]+\) ", "", subs_quote) # trim the eventual parenthesis

		print "%s %s" % (script_line[0], subs_quote) # print in the format of aligned_transcript
	else:
		absent += 1

sys.stderr.write("absent lines: "+str(absent)+"\n")
sys.stderr.write("total  lines: "+str(sub[2])+"\n")
sys.stderr.write("+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~")
sys.stderr.write("+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+\n\n")