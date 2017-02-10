#!/usr/bin/env python
import json, weles, hssa
import matplotlib.pyplot as plt

imagesDirectory = 'data/hsimages/'
with open('%s%s' % (imagesDirectory, 'salinasA.json')) as data_file:
    dictionary = json.load(data_file)
print 'Hello.'

img = hssa.HS(dictionary)
print img

edges = img.edges((3, 3))

print edges
