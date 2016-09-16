################################################################################
##
## Align transcripts with scene recaps using DTW.
## Script forked from: https://gist.github.com/hbredin/a372df52a748f7f00dd0
##
################################################################################

from tvd import GameOfThrones
import re
import pprint
from pyannote.parser import SRTParser
from pyannote.algorithms.alignment.dtw import DynamicTimeWarping
from contractions import *

dataset = GameOfThrones('../../../0_corpus/tvd')
recaps_txt_dir = '../../../0_corpus/recaps/recaps_txt'

def cleanText(text):
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
    return text

# This function generates a sequence of scene formatted in such a way it
# can be used with DTW
def dtwScenes(dataset, episode):
	sequence  = []
	with open(recaps_txt_dir+'/'+str(episode)+'.txt') as f:
		recap = f.read().replace('\n', '')
	recap = re.split(r'=== SCENE \d+ ===', recap)
	nb = 1
	for scene in recap:
		if scene:
			# preprocess
			scene = cleanText(scene)
			sequence.append((scene, nb))
			nb += 1

	# pprint.pprint(sequence)
	# ("Walking through the Red Keep, Eddard is intercepted ...", 19),
	return sequence


# This function generates a sequence of transcripts formatted in such a way it
# can be used with DTW
def dtwTranscript(dataset, episode):
	sequence   = []
	transcript = dataset.get_resource('transcript', episode)
	for start, end, data in transcript.ordered_edges_iter(data=True):
		if 'speaker' not in data:
			continue
		# UTF8 encoding + strip
		speech  = data['speech'].encode('utf8').strip()
		# preprocess
		speech = cleanText(speech)
		speaker = data['speaker']
		sequence.append((speech, speaker))
	# pprint.pprint(sequence)
	## ('A crown for a King.', u'KHAL_DROGO'),
	return sequence


# This function takes one element of each sequence and returns a distance based
# on the number of common words
def dtwDistance(scene, transcript):
	scene = scene[0]
	transcript = transcript[0]
	scene_words = set(scene.split())
	transcript_words = set(transcript.split())


	# 1.
	# number of unique words in scenes - number of unique words in common
	return len(scene_words) - len(scene_words & transcript_words)
	# 2. (best so far)
	# number of unique words in transcripts - number of unique words in common
	# return len(transcript_words) - len(transcript_words & scene_words)
	# 3.
	# number of unique words in scenes - number of unique words in common -- normalized
	# return (len(transcript_words) - len(transcript_words & scene_words)) / float(len(transcript_words))


# yay magic
# scene are vertical and transcripts are horizontal
# make sure that DTW doesn't align a transcript to multiple scenes by adding no_vertical=True
dtw        = DynamicTimeWarping(distance_func=dtwDistance, no_vertical=True)
template   = '\t\ttranscript: {transcript}\nscene: {scene}\n\n'
output     = '../../../1_scripts/GoT_git/recap_aligned/auto_align/{episode}.txt'
tuple_file = '../../../1_scripts/GoT_git/recap_aligned/auto_align/tuples/auto_aligned_{episode}.txt'

for episode in dataset.episodes[:5]:
	# extract scene and transcript sequences
	scene      = dtwScenes(dataset, episode)
	transcript = dtwTranscript(dataset, episode)

	# dynamic time warping, wooo
	alignment = set(dtw(scene, transcript))

	# dump tuple alignment to file
	with open(tuple_file.format(episode=episode), 'w') as file:
		alignment = sorted(alignment)
		for a in alignment:
			file.write(str(a[1])+"\t"+str(a[0])+"\n")

	# dump text alignement to file
	with open(output.format(episode=episode), 'w') as f:
		for s, t in alignment:
			data = {
				'transcript': transcript[t][0],
				'scene':  scene[s][0]
			}
			f.write(template.format(**data))


# fin