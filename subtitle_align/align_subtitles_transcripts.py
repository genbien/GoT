################################################################################
##
## align subttiles and transcripts - from https://gist.github.com/hbredin/a372df52a748f7f00dd0
##
################################################################################

from tvd import GameOfThrones
import re
import pprint
from pyannote.parser import SRTParser
from pyannote.algorithms.alignment.dtw import DynamicTimeWarping


dataset = GameOfThrones('../0_corpus/tvd/')


# This function generates a sequence of subtitles formatted in such a way it
# can be used with DTW
def dtwSubtitles(dataset, episode):

	sequence  = []

	parser    = SRTParser(split=True, duration=True)
	subtitles = parser.read(dataset.path_to_subtitles(episode))()


	for start, end, data in subtitles.ordered_edges_iter(data=True):

		if 'subtitle' not in data:
			continue

		# UTF8 encoding + strip
		subtitle = data['subtitle'].encode('utf8').strip()

		# remove leading "- "
		if subtitle[:2] == '- ':
			subtitle = subtitle[2:]


		# do not append empty subtitles
		if not subtitle:
			continue

		sequence.append((subtitle, start, end))

	# pprint.pprint(sequence)
	## ('He ran.', 3032.08, 3033.991),
	## ('Not very fast.', 3034.159, 3035.638)
	return sequence


# This function generates a sequence of transcript formatted in such a way it
# can be used with DTW
def dtwTranscript(dataset, episode):

	sequence   = []

	transcript = dataset.get_resource('transcript', episode)

	for start, end, data in transcript.ordered_edges_iter(data=True):

		if 'speaker' not in data:
			continue

		# UTF8 encoding + strip
		speech  = data['speech'].encode('utf8').strip()

		speaker = data['speaker']

		sequence.append((speech, speaker))

	# pprint.pprint(sequence)
	## ('A crown for a King.', u'KHAL_DROGO'),
	return sequence

# This function takes one element of each sequence and returns a distance based
# on the number of common words
def dtwDistance(subtitle, transcript):

	subtitle = subtitle[0]
	transcript = transcript[0]

	subtitle_words = set(subtitle.split())
	transcript_words = set(transcript.split())

	# number of unique words in subtitles - number of unique words in common
	return len(subtitle_words) - len(subtitle_words & transcript_words)



dtw        = DynamicTimeWarping(distance_func=dtwDistance)
template   = '{start:.3f} {end:.3f} {speaker} {speech}\n'
output     = '../0_corpus/tvd/GameOfThrones/book/subtitles/{episode}.txt'
tuple_file = '../1_scripts/GoT_git/precision_recall/auto_subtitles_transcripts/auto_aligned_{episode}.txt'

for episode in dataset.episodes[:10]:

	# extract subtitles and transcript sequences
	subtitles  = dtwSubtitles(dataset, episode)
	transcript = dtwTranscript(dataset, episode)

	# dynamic time warping
	alignment = set(dtw(subtitles, transcript))
	# pprint.pprint(alignment)


	with open(tuple_file.format(episode=episode), 'w') as file:
		# alignment.sort(key=lambda tup: tup[1])
		alignment = sorted(alignment)
		for a in alignment:
			file.write(str(a[0])+"\t"+str(a[1])+"\n")


	# follow the optimal path and dump to file
	with open(output.format(episode=episode), 'w') as f:
		for s, t in alignment:
			data = {
				'start': subtitles[s][1],
				'end': subtitles[s][2],
				'speaker': transcript[t][1],
				'speech': subtitles[s][0]
			}
			f.write(template.format(**data))