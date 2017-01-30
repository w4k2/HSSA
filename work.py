#!/usr/bin/env python
# Script to do quick experiments.

import os
import json
import hssa

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
'''
print "- export as Weles dataset"
dataset = img.dataset()
print dataset

print dataset.samples[0].features[:4]
'''

# HSSA loop
print "- do a HSSA loop"
threshold = .98
limit = 2
sgm = hssa.HSSA(img, threshold, limit)

while not sgm.isComplete:
    print sgm
    sgm.step()

print sgm
