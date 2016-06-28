# https://linanqiu.github.io/2015/10/07/word2vec-sentiment/

# setup
import numpy as np
import scipy.spatial.distance
from tvd import GameOfThrones
import re
import pprint
from pyannote.parser import SRTParser
from pyannote.algorithms.alignment.dtw import DynamicTimeWarping

# ---
# configure this part for which episode you want to doc2vec (1, 2, 3, 4, or 5)
ep = 1
# ---

dataset = GameOfThrones('../../../0_corpus/tvd')
recaps_txt_dir = '../../../0_corpus/recaps/recaps_txt'

# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

# numpy
import numpy

# random
from random import shuffle

# classifier
from sklearn.linear_model import LogisticRegression


class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that values are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences


def createDistanceMatrix(sentences):
    trans_labels = []
    scene_labels = []
    for i in sentences:
        label = i[1][0]
        if label.startswith('TRANSCRIPTS0'+str(ep)+'_'):
            trans_labels.append(label)
        elif label.startswith('SCENES0'+str(ep)+'_'):
            scene_labels.append(label)

    dist_matrix = []
    for t in trans_labels:
        row = []
        for s in scene_labels:
            row.append(1 - (model.docvecs.similarity(t, s)))
        dist_matrix.append(row)

    # print dist_matrix

    dist_matrix = np.array(dist_matrix)
    nan_loc = np.isnan(dist_matrix)
    dist_matrix[nan_loc] = 1000
    print "SHAPE ["+str(dist_matrix.shape)+"]"
    return dist_matrix


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


# doc2vec stuff -- train model
# all the sources are used for training
sources = {

    '../../../0_corpus/recaps/recaps_txt/cleaned/GameOfThrones.Season01.Episode01.txt':'SCENES01',
    '../../../0_corpus/manual_transcripts/cleaned/GameOfThrones.Season01.Episode01.txt':'TRANSCRIPTS01',

    '../../../0_corpus/recaps/recaps_txt/cleaned/GameOfThrones.Season01.Episode02.txt':'SCENES02',
    '../../../0_corpus/manual_transcripts/cleaned/GameOfThrones.Season01.Episode02.txt':'TRANSCRIPTS02',

    '../../../0_corpus/recaps/recaps_txt/cleaned/GameOfThrones.Season01.Episode03.txt':'SCENES03',
    '../../../0_corpus/manual_transcripts/cleaned/GameOfThrones.Season01.Episode03.txt':'TRANSCRIPTS03',

    '../../../0_corpus/recaps/recaps_txt/cleaned/GameOfThrones.Season01.Episode04.txt':'SCENES04',
    '../../../0_corpus/manual_transcripts/cleaned/GameOfThrones.Season01.Episode04.txt':'TRANSCRIPTS04',

    '../../../0_corpus/recaps/recaps_txt/cleaned/GameOfThrones.Season01.Episode05.txt':'SCENES05',
    '../../../0_corpus/manual_transcripts/cleaned/GameOfThrones.Season01.Episode05.txt':'TRANSCRIPTS05',

    '../../../0_corpus/books/cleaned/AClashOfKings.txt':'CLASHOFKINGS',
    '../../../0_corpus/books/cleaned/ADanceWithDragons.txt':'DANCEWITHDRAGONS',
    '../../../0_corpus/books/cleaned/AGameOfThrones.txt':'GAMEOFTHRONES',
    '../../../0_corpus/books/cleaned/AStormOfSwords.txt':'STROMOFSWORDS',

    '../../../0_corpus/summaries/long_summary/cleaned/GameOfThrones.S01E01.en.txt': 'SUM01',
    '../../../0_corpus/summaries/long_summary/cleaned/GameOfThrones.S01E02.en.txt': 'SUM02',
    '../../../0_corpus/summaries/long_summary/cleaned/GameOfThrones.S01E03.en.txt': 'SUM03',
    '../../../0_corpus/summaries/long_summary/cleaned/GameOfThrones.S01E04.en.txt': 'SUM04',
    '../../../0_corpus/summaries/long_summary/cleaned/GameOfThrones.S01E05.en.txt': 'SUM05',
    '../../../0_corpus/summaries/long_summary/cleaned/GameOfThrones.S01E06.en.txt': 'SUM06',
    '../../../0_corpus/summaries/long_summary/cleaned/GameOfThrones.S01E07.en.txt': 'SUM07',
    '../../../0_corpus/summaries/long_summary/cleaned/GameOfThrones.S01E08.en.txt': 'SUM08',
    '../../../0_corpus/summaries/long_summary/cleaned/GameOfThrones.S01E09.en.txt': 'SUM09',
    '../../../0_corpus/summaries/long_summary/cleaned/GameOfThrones.S01E10.en.txt': 'SUM10',
}

sentences = LabeledLineSentence(sources)
model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=2)
model.build_vocab(sentences.to_array())

for epoch in range(10):
    model.train(sentences.sentences_perm())

# model.save('./got.d2v')
# model = Doc2Vec.load('./got.d2v')


# scenes are vertical and transcripts are horizontal
# make sure that DTW doesn't align a transcript to multiple scenes by adding no_vertical=True
# dtw        = DynamicTimeWarping(distance_func=dtwDistance, no_vertical=True)
dtw        = DynamicTimeWarping(no_vertical=True)
template   = '\t\ttranscript: {transcript}\nscene: {scene}\n\n'
output     = '../../../1_scripts/GoT_git/recap_aligned/doc2vec_auto_align/{episode}.txt'
tuple_file = '../../../1_scripts/GoT_git/recap_aligned/doc2vec_auto_align/tuples/auto_aligned_{episode}.txt'

# for episode in dataset.episodes[:1]:
for episode in dataset.episodes[(ep - 1):ep]:
    # extract scene and transcript sequences
    scene      = dtwScenes(dataset, episode)
    transcript = dtwTranscript(dataset, episode)

    # confirm correct shape
    print "len(transcript)", len(transcript)
    print "len(scene)", len(scene)

    # make a pretty distance matrix for the dtw to use
    dist_matrix = createDistanceMatrix(sentences)
    # confirm correct shape
    print(dist_matrix.shape)

    # dynamic time warping, wooo
    # transform matrix (flip it so scenes are on x and transcripts are on y)
    alignment = set(dtw(scene, transcript, distance=dist_matrix.T))

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
