#!/usr/bin/env python
# Script to do quick experiments.

import os
import json
import hssa
import weles

# Say hello
os.system('clear')
print '# Let\'s play'

# Load salinasA image
print "- load image"
imagesDirectory = 'data/hsimages/'
with open('%s%s' % (imagesDirectory, 'salinasA.json')) as data_file:
    dictionary = json.load(data_file)
img = hssa.HS(dictionary)
print img

# Weles export
print "- export as Weles dataset"
dataset = img.dataset()
print dataset
print dataset.samples[0].features[:4]
print len(dataset.samples[0].features)

# HSSA loop
print "- do a HSSA loop"
t = .98
j = .992
l = 6
p = 9

sgm = hssa.HSSA(img, t, j, l, p)

sgm.png('figures/steps/i%i.png' % sgm.iteration, False)
while not sgm.isComplete:
    print sgm
    sgm.step()
    sgm.png('figures/steps/i%i.png' % sgm.iteration, False)

    if sgm.iteration == l:
        break

print sgm
sgm.png('figures/steps/p0.png', True)
sgm.post()
sgm.png('figures/steps/p1.png', True)
print sgm

# Pure KNN
configuration = {
    'k': 1
}
clf = weles.sklKNN(dataset, configuration).quickLoop()
print "%i samples [ACC = %.3f, BAC = %.3f]" % (
    len(dataset.samples),
    clf['acc'], clf['bac']
)

dataset.injectTrain(sgm.train(0))
clf = weles.sklKNN(dataset, configuration).quickLoop()
print "%4i samples [ACC = %.3f, BAC = %.3f]" % (
    len(dataset.samples),
    clf['acc'], clf['bac']
)

dataset.injectTrain(sgm.train(1))
clf = weles.sklKNN(dataset, configuration).quickLoop()
print "%4i samples [ACC = %.3f, BAC = %.3f]" % (
    len(dataset.samples),
    clf['acc'], clf['bac']
)

dataset.injectTrain(sgm.train(2))
clf = weles.sklKNN(dataset, configuration).quickLoop()
print "%4i samples [ACC = %.3f, BAC = %.3f]" % (
    len(dataset.samples),
    clf['acc'], clf['bac']
)
