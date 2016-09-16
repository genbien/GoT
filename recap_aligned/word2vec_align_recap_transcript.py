################################################################################
##
## Align transcripts with scene recaps using DTW.
## Script forked from: https://gist.github.com/hbredin/a372df52a748f7f00dd0
## Distance #4 - word2vec with all word vec in a doc summed for comparison with
##   summed word vecs from a second doc
##
################################################################################

# setup
from spacy.en import English
nlp = English()
import numpy as np
np.set_printoptions(threshold=np.nan)
import scipy.spatial.distance
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

# This function generates a sequence of scenes formatted in such a way it
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
    # ("walking through the red keep eddard is intercepted", 19),
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
    ## ('a crown for a king', u'KHAL_DROGO'),
    return sequence


# This function creates a distance matrix to be used with DTW
# It takes the distances between the word vectors for words that are in
# each scene and transcript
def createDistanceMatrix(scene, transcript):
    scene_matrix = []
    for s in scene:
        s = unicode(s[0], encoding="utf-8")
        scene_words = nlp(s)
        s_vectors   = [word.vector for word in scene_words]
        X_scene  = np.array(s_vectors)
        s_vector = np.sum(X_scene, axis=0)
        scene_matrix.append(s_vector)
    scene_matrix = np.array(scene_matrix)

    transcript_matrix = []
    for t in transcript:
        t = unicode(t[0], encoding="utf-8")
        transcript_words = nlp(t)
        t_vectors     = [word.vector for word in transcript_words]
        X_transcript  = np.array(t_vectors)
        t_vector      = np.sum(X_transcript, axis=0)
        transcript_matrix.append(t_vector)
    transcript_matrix = np.array(transcript_matrix)

    # find the distance between the vectors of the scenes and transcripts
    # in their matrices, using the cosine distance
    dist_matrix = scipy.spatial.distance.cdist(scene_matrix, transcript_matrix, "cosine")

    # replace nan vectors with highest distance vectors and avoid NoneType errors
    nanmax = np.nanmax(dist_matrix)
    dist_matrix[np.isnan(dist_matrix)] = nanmax

    return dist_matrix


# scenes are vertical and transcripts are horizontal
# make sure that DTW doesn't align a transcript to multiple scenes by adding no_vertical=True
# dtw        = DynamicTimeWarping(distance_func=dtwDistance, no_vertical=True)
dtw        = DynamicTimeWarping( no_vertical=True)
template   = '\t\ttranscript: {transcript}\nscene: {scene}\n\n'
output     = '../../../1_scripts/GoT_git/recap_aligned/word2vec_auto_align/{episode}.txt'
tuple_file = '../../../1_scripts/GoT_git/recap_aligned/word2vec_auto_align/tuples/auto_aligned_{episode}.txt'
dist_file  = '../../../1_scripts/GoT_git/recap_aligned/word2vec_auto_align/dist_matrix/dist_matrix_{episode}.txt'

for episode in dataset.episodes[:5]:
    # extract scene and transcript sequences
    scene      = dtwScenes(dataset, episode)
    transcript = dtwTranscript(dataset, episode)

    # make a pretty distance matrix for the dtw to use
    dist_matrix = createDistanceMatrix(scene, transcript)

    # dynamic time warping, wooo
    alignment = set(dtw(scene, transcript, distance=dist_matrix))

    # save distance matrix
    with open(dist_file.format(episode=episode), 'w') as file:
        np.save(file, dist_matrix)

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

    print episode

