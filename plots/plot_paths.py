import matplotlib.pyplot as plt
import numpy as np

episode = 'GameOfThrones.Season01.Episode02.txt'
# what kind of alignment was done
# align_t = 'lemma'
# align_t = 'word2vec'
align_t = 'word2vec2'
# align_t = 'word2vec3'
# manually aligned file
reference_file  = '../recap_aligned/manual_align/manual_aligned_'+episode
# word2vec aligned file
hypothesis_file = '../recap_aligned/'+align_t+'_auto_align/tuples/auto_aligned_'+episode
# previously created distance matrix
# dist_matrix = '../recap_aligned/'+align_t+'_auto_align/dist_matrix/dist_matrix_'+episode

ref = []
hyp = []

def make_plot_points(filename, listname):
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            # skip commentary
            if line.startswith('%'):
                continue
            else:
                line = line.split('\t')
                # skip non-aligned elements
                if line[0] != 'x' and line[1] != 'x':
                    listname.append((line[0], line[1]))


# make hypothesis and reference lists
make_plot_points(hypothesis_file, hyp)
make_plot_points(reference_file, ref)

# plot lists of x,y tuples
plt.plot(*zip(*ref), lw=1, label="reference")
plt.plot(*zip(*hyp), lw=1, label="hypothesis")
# add labels and legend
# plt.legend(loc=2)
plt.title(episode)
plt.xlabel('transcripts')
plt.ylabel('scenes')

# save to folder
plt.savefig(align_t+'_path_plots/plot_'+episode+'.eps', format='eps', dpi=1000)
# plt.show()