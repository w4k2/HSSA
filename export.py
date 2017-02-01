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

dataset.export('salinasA.csv')
