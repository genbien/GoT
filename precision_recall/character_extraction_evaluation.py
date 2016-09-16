from __future__ import division
# ref
manual = [[150, 41, 113, 149], [150], [], [123, 127,62, 124, 125, 126], [121, 128, 85], [123, 127, 125, 124, 126, 62, 19, 49], [49, 19, 18, 123, 125, 127, 62, 150], [49, 19, 18, 123, 125, 127, 62], [65, 66, 3], [124], [124, 125], [124, 74], [127, 49, 62, 140], [124, 74, 123], [121, 23, 9], [124, 125, 74, 127, 49, 62, 123, 121, 23, 9, 126, 128, 18, 55, 12, 65, 19, 10, 13, 66], [125, 12], [66], [66, 69, 110], [125, 12], [133, 134], [133, 134, 83, 30], [133, 134, 83], [124, 128], [124, 12, 125], [62, 69, 122], [125, 127, 122], [124, 9, 128, 12, 65], [125, 66], [124, 127, 121], [124, 125, 74], [133, 134, 83, 30, 87], [133, 30], [125, 127, 49, 123, 23, 12, 69], [123, 65, 66]]

# hyp before adding character extractions
# auto = [ [113, 150, 41], [], [], [62], [85, 128], [125, 62, 127, 19, 124], [150, 125, 62, 123], [62, 49, 125, 127, 123, 19], [66, 65], [], [124, 125], [124, 74], [62, 49, 127], [124, 123], [], [124, 125, 121, 12, 128], [124, 12, 65, 121, 125], [], [69, 110, 66], [12, 125], [12, 134, 133, 83], [83, 134], [83, 134, 133], [128, 124], [128], [122, 62, 69], [122, 125, 127], [124, 65, 128], [125, 66], [66, 128, 127], [125, 124, 74], [134, 83, 87, 133], [30, 133], [23, 69, 12, 125, 123], [65, 66, 123]]


# hyp after adding character extractions
auto = [[113, 150, 41], [113], [], [41, 62, 64, 124, 125, 127], [85, 128, 121, 125], [85, 125, 62, 127, 19, 124, 121, 126], [150, 125, 62, 123], [62, 49, 125, 127, 123, 19], [49, 66, 65, 12], [66, 124], [66, 124, 125, 4, 5, 12], [124, 74, 65, 66, 69], [62, 49, 127, 140], [127, 124, 123, 125], [121], [124, 125, 121, 12, 128, 65, 66, 127], [124, 12, 65, 121, 125, 128], [12, 66, 69], [12, 69, 110, 66], [12, 125], [125, 12, 134, 133, 83], [83, 134, 133], [83, 134, 133], [128, 124, 125], [128, 12, 65, 124], [122, 62, 69], [69, 122, 125, 127], [127, 124, 65, 128, 12], [125, 66, 12], [66, 128, 127, 121, 124], [125, 124, 74, 4, 12], [74, 134, 83, 87, 133], [134, 30, 133], [23, 69, 12, 125, 123], [123, 65, 66]]


# print "manual", len(manual)
# print "auto", len(auto)

tp = 0
fp = 0
fn = 0

# for i, scene in enumerate(manual):
#     scene = set(scene)
#     auto[i] = set(auto[i])
#     tp += float(len(auto[i] & scene))
#     fp += float(len(auto[i] - scene))
#     fn += float(len(scene - auto[i]))

# precision = tp / (tp + fp)
# recall = tp / (tp + fn)

# fscore = (2 * ((precision * recall)/(precision + recall)))

# print "precision", precision
# print "recall", recall
# print "fscore", fscore

precisions = []
recalls = []
fscores = []


for i, scene in enumerate(manual):
    scene = set(scene)
    auto[i] = set(auto[i])
    tp = float(len(auto[i] & scene))
    fp = float(len(auto[i] - scene))
    fn = float(len(scene - auto[i]))

    if (tp + fp):
        precision = tp / (tp + fp)
    else:
        precision = 1.0
    if (tp + fn):
        recall = tp / (tp + fn)
    else:
        recall = 1.0

    if (precision + recall):
        fscore = (2 * ((precision * recall)/(precision + recall)))
    else:
        fscore = 0

    print "precision", precision
    print "recall", recall
    print "fscore", fscore
    precisions.append(precision)
    recalls.append(recall)
    fscores.append(fscore)



print "precision average", sum(precisions) / float(len(precisions))
print "recall average", sum(recalls) / float(len(recalls))
print "fscore average", sum(fscores) / float(len(fscores))