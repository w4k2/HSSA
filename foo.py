#!/usr/bin/env python
import json, weles, hssa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as colors

imagesDirectory = 'data/hsimages/'
with open('%s%s' % (imagesDirectory, 'indianpines.json')) as data_file:
    dictionary = json.load(data_file)
print 'Hello.'

img = hssa.HS(dictionary)
img.signaturesPNG('foo.png')
