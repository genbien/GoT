################################################################################
##
## Align transcripts with scene recaps using DTW.
## Script forked from: https://gist.github.com/hbredin/a372df52a748f7f00dd0
## Distance #5.5 - word2vec comparing individual words (but only noun, verb,
##     and adjectives), keep min dist for comparison
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
from collections import defaultdict
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

def fancy_dist(s_vec_matrix, t_vec_matrix):
    # cosine distance of scene vectors and transscript vectors
    step_matrix  = scipy.spatial.distance.cdist(s_vec_matrix, t_vec_matrix, "cosine")
    # replace nans
    nan_loc = np.isnan(step_matrix)
    step_matrix[nan_loc] = 1000
    # find most similar word's distance
    f_dist = -(np.mean(1/(1+np.min(step_matrix, axis=0))))
    return f_dist

# This function creates a distance matrix to be used with DTW
# It takes the distances between the word vectors for words that are in
# each scene and transcript
def createDistanceMatrix(scene, transcript):
    dist_matrix  = []
    # look at words that only have one of these parts of speech
    pos = ['NOUN', 'ADJ', 'VERB']

    # make vector matrices for each scene
    # s_vec_matrix = {}
    s_vec_matrix = defaultdict(list)
    s_vectors = []
    for sidx, s in enumerate(scene):
        s = unicode(s[0], encoding="utf-8")
        scene_words = nlp(s)
        for word in scene_words:
            if any(p in word.pos_ for p in pos):
                print "scene", word, word.pos_
                s_vectors.append(word.vector)
        s_vec_matrix[sidx] = np.array(s_vectors)

    # make vector matrices for each transcript
    t_vec_matrix = defaultdict(list)
    t_vectors = []
    for tidx, t in enumerate(transcript):
        t = unicode(t[0], encoding="utf-8")
        trans_words = nlp(t)
        for word in trans_words:
            if any(p in word.pos_ for p in pos):
                print "transcript", word, word.pos_
                t_vectors.append(word.vector)
        t_vec_matrix[tidx] = np.array(t_vectors)

    # get distance of most similar word for scene and transcript
    dist_matrix = np.empty((len(scene), len(transcript)))
    for sidx, s in enumerate(scene):
       for tidx, t in enumerate(transcript):
            dist_matrix[sidx][tidx] = fancy_dist(s_vec_matrix[sidx], t_vec_matrix[tidx])


    return dist_matrix


# scenes are vertical and transcripts are horizontal
# make sure that DTW doesn't align a transcript to multiple scenes by adding no_vertical=True
dtw        = DynamicTimeWarping( no_vertical=True)
template   = '\t\ttranscript: {transcript}\nscene: {scene}\n\n'
output     = '../../../1_scripts/GoT_git/recap_aligned/pos2_auto_align/{episode}.txt'
tuple_file = '../../../1_scripts/GoT_git/recap_aligned/pos2_auto_align/tuples/auto_aligned_{episode}.txt'
dist_file  = '../../../1_scripts/GoT_git/recap_aligned/pos2_auto_align/dist_matrix/dist_matrix_{episode}.txt'

for episode in dataset.episodes[:5]:
    # extract scene and transcript sequences
    scene      = dtwScenes(dataset, episode)
    transcript = dtwTranscript(dataset, episode)

    # make a pretty distance matrix for the dtw to use
    dist_matrix = createDistanceMatrix(scene, transcript)

    # dynamic time warping, wooo
    alignment = set(dtw(scene, transcript, distance=dist_matrix))

    # # save distance matrix
    with open(dist_file.format(episode=episode), 'w') as file:
        np.save(file, dist_matrix)

    # # dump tuple alignment to file
    with open(tuple_file.format(episode=episode), 'w') as file:
        alignment = sorted(alignment)
        for a in alignment:
            file.write(str(a[1])+"\t"+str(a[0])+"\n")

    # # dump text alignement to file
    with open(output.format(episode=episode), 'w') as f:
        for s, t in alignment:
            data = {
                'transcript': transcript[t][0],
                'scene':  scene[s][0]
            }
            f.write(template.format(**data))

    print episode

