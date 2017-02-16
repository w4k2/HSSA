#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, weles, hssa
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

print 'AP!'

imagesDirectory = 'data/hsimages/'
with open('%s%s' % (imagesDirectory, 'salinasA.json')) as data_file:
    dictionary = json.load(data_file)

k = (3, 3)
percentile = 50

hs = hssa.HS(dictionary)
ap = hssa.AP(hs, k, percentile, 0)

print np.shape(ap.channels)

plt.figure(figsize=(7, 16))

color1 = ap.channels[:,:,xrange(0,3)]
color2 = ap.channels[:,:,xrange(3,6)]
color3 = ap.channels[:,:,xrange(6,9)]
color4 = ap.channels[:,:,xrange(9,12)]
color5 = ap.channels[:,:,xrange(12,15)]


for idx in xrange(np.shape(ap.channels)[2]):
    plt.subplot(7,4,6 + idx + divmod(idx,3)[0])
    plt.imshow(ap.channels[:,:,idx], cmap='gray'); plt.axis('off');
    plt.title(ap.channelNames[idx])


for idx in xrange(0, np.shape(ap.channels)[2], 3):
    row = list(xrange(idx, idx + 3))
    colorrow = ap.channels[:,:,row]
    plt.subplot(7,4,5 + 4 * divmod(idx, 3)[0]);
    plt.imshow(colorrow); plt.axis('off');

for idx in xrange(0, np.shape(ap.channels)[2] / 5):
    col = list(xrange(idx, np.shape(ap.channels)[2], 3))
    cola = col[0:3]
    colb = col[2:]

    colorcola = ap.channels[:,:,cola]
    colorcolb = ap.channels[:,:,colb]

    plt.subplot(7,4,2 + idx);
    plt.imshow(colorcola); plt.axis('off');
    plt.subplot(7,4,26 + idx);
    plt.imshow(colorcolb); plt.axis('off');

plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig('foo.png')

print '%i of %i bands used' % (
    np.shape(ap.cube)[2],
    np.shape(ap.hs.image)[2]
)
