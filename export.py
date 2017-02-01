#!/usr/bin/env python
# Script to export HS to Weles datasets.

import os
import json
import hssa
import weles

filenames = [
    'salinasA.json',
    'indianpines.json',
    'salinas.json',
    'pavia.json'
]

# Say hello
os.system('clear')
print '# Let\'s export all datasets to weles'

# Load salinasA image
imagesDirectory = 'data/hsimages/'

for filename in filenames:
    print "- loaded file (%s)" % filename
    with open('%s%s' % (imagesDirectory, filename)) as data_file:
        dictionary = json.load(data_file)
    img = hssa.HS(dictionary)
    print "- loaded image (%s)" % img
    dataset = img.dataset()
    print "- converted Weles dataset (%s)" % dataset
    csvFilename = '%s.csv' % filename[:-5]
    dataset.export(csvFilename)
    print '- saved to CSV (%s)' % csvFilename


'''

# Weles export
print dataset
print dataset.samples[0].features[:4]
print len(dataset.samples[0].features)

'''
