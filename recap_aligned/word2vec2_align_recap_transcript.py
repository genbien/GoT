################################################################################
##
## Align transcripts with scene recaps using DTW.
## Script forked from: https://gist.github.com/hbredin/a372df52a748f7f00dd0
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

dataset = GameOfThrones('../../../0_corpus/tvd')
recaps_txt_dir = '../../../0_corpus/recaps/recaps_txt'

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
            sequence.append((scene, nb))
            nb += 1
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
        speaker = data['speaker']
        sequence.append((speech, speaker))
    ## ('A crown for a King.', u'KHAL_DROGO'),
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
    s_vec_matrix = {}

    # make vector matrices for each scene
    for sidx, s in enumerate(scene):
        s = unicode(s[0], encoding="utf-8")
        scene_words = nlp(s)
        s_vec_matrix[sidx] = np.array([s_word.vector for s_word in scene_words])

    # make vector matrices for each transcript
    t_vec_matrix = {}
    for tidx, t in enumerate(transcript):
        t = unicode(t[0], encoding="utf-8")
        trans_words = nlp(t)
        t_vec_matrix[tidx] = np.array([t_word.vector for t_word in trans_words])


    # get distance of most similar word for scene and transcript
    dist_matrix = np.empty((len(scene), len(transcript)))
    for sidx, s in enumerate(scene):
       for tidx, t in enumerate(transcript):
            dist_matrix[sidx][tidx] = fancy_dist(s_vec_matrix[sidx], t_vec_matrix[tidx])


    return dist_matrix


# scenes are vertical and transcripts are horizontal
# make sure that DTW doesn't align a transcript to multiple scenes by adding no_vertical=True
# dtw        = DynamicTimeWarping(distance_func=dtwDistance, no_vertical=True)
dtw        = DynamicTimeWarping( no_vertical=True)
template   = '\t\ttranscript: {transcript}\nscene: {scene}\n\n'
output     = '../../../1_scripts/GoT_git/recap_aligned/word2vec2_auto_align/{episode}.txt'
tuple_file = '../../../1_scripts/GoT_git/recap_aligned/word2vec2_auto_align/tuples/auto_aligned_{episode}.txt'
dist_file  = '../../../1_scripts/GoT_git/recap_aligned/word2vec2_auto_align/dist_matrix/dist_matrix_{episode}.txt'

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

