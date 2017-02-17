#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, weles, hssa
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

imagesDirectory = 'data/hsimages/'
with open('%s%s' % (imagesDirectory, 'paviaC.json')) as data_file:
    dictionary = json.load(data_file)

k = (3, 3)
percentile = 50

hs = hssa.HS(dictionary)
ap = hssa.AP(hs, k, percentile, 0, bins = 256, quantization = 4)
print ap.epf

mask = ap.epf.bordersMask()

plt.figure(figsize=(10, 15))
colors = ['#CC2222', '#22CC22', '#2222CC']

for idx in xrange(np.shape(ap.channels)[2]):
    a = divmod(idx,3)[0]
    b = divmod(idx,3)[1]
    plt.subplot(9,5,13 + 5 * a + b)
    channel = ap.channels[:,:,idx]
    channel[0,0] = 0
    channel[-1,-1] = 1
    plt.imshow(channel, cmap='gray'); plt.axis('off');
    plt.title("%s (%i)" % (ap.channelNames[idx], ap.colorIndex((idx,idx,idx))))

for idx in xrange(0, np.shape(ap.channels)[2], 3):
    row = list(xrange(idx, idx + 3))
    colorrow = ap.channels[:,:,row]
    plt.subplot(9,5,12 + 5 * divmod(idx, 3)[0]);
    plt.imshow(colorrow); plt.axis('off');
    plt.title(row)

    plt.subplot(9,5,11 + 5 * divmod(idx, 3)[0]);
    for c, idx in enumerate(row):
        plt.plot(ap.histograms[idx], color = colors[c])
        plt.axis('off');
    plt.title(ap.colorIndex(row))


for idx in xrange(0, np.shape(ap.channels)[2] / 5):
    col = list(xrange(idx, np.shape(ap.channels)[2], 3))
    cola = col[0:3]
    colb = col[2:]

    colorcola = ap.channels[:,:,cola]
    colorcolb = ap.channels[:,:,colb]

    plt.subplot(9,5,8 + idx);
    plt.imshow(colorcola); plt.axis('off');
    plt.title(cola)

    plt.subplot(9,5,3 + idx);
    for c, idxx in enumerate(cola):
        plt.plot(ap.histograms[idxx], color = colors[c])
        plt.axis('off');
    plt.title(ap.colorIndex(cola))


    plt.subplot(9,5,38 + idx);
    plt.imshow(colorcolb); plt.axis('off');
    plt.title(colb)

    plt.subplot(9,5,43 + idx);
    for c, idxx in enumerate(colb):
        plt.plot(ap.histograms[idxx], color = colors[c])
        plt.axis('off');
    plt.title(ap.colorIndex(colb))

# Winner
plt.subplot(9,5,1)
a = [r[1] for r in ap.rank]
plt.plot(a)
winner = 0
loser = -1
plt.title(winner)
print ap.rank[winner]

plt.subplot(9,5,2)
image = ap.channels[:,:,ap.rank[winner][0]]
plt.imshow(image); plt.axis('off');
plt.title('BEST')

plt.subplot(9,5,7)
image = ap.channels[:,:,ap.rank[loser][0]]
plt.imshow(image); plt.axis('off');
plt.title('WORST')

plt.subplot(9,5,6)
plt.imshow(mask, cmap='gray'); plt.axis('off');


plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig('foo.png')










plt.figure(figsize=(20, 20))

cols = 14
rows = 8
step = 4


cols = 5
rows = 2
step = 1

for i in xrange(cols):
    rank = i
    if rank >= len(ap.rank):
        break
    ci = ap.rank[rank][1]
    tup = ap.rank[rank][0]
    image = ap.channels[:,:,tup]

    #plt.subplot(rows + 1, cols, 1 + i)

    plt.subplot(rows, cols, 1 + i)
    plt.imshow(image); plt.axis('off');
    plt.title("%i - %s - %f" % (
        rank + 1,
        tup,
        ci))


    rank = len(ap.rank) - 1 - i
    ci = ap.rank[rank][1]
    tup = ap.rank[rank][0]
    image = ap.channels[:,:,tup]

    plt.subplot(rows, cols, cols + 1 + i)
    plt.imshow(image); plt.axis('off');
    plt.title("%i - %s - %f" % (
        rank + 1,
        tup,
        ci))


plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig('bar.png')


plt.figure(figsize=(10, 10))

plt.subplot(223)
plt.imshow(ap.visualization())
plt.axis('off'); plt.title('10%% from bell.')
plt.imsave('%s.png' % ap.hs.name, ap.visualization())

plt.subplot(221)
plt.imshow(ap.visualization(1))
plt.axis('off'); plt.title('Only leader')

plt.subplot(222)
plt.imshow(ap.visualization(500))
plt.axis('off'); plt.title('All')

plt.subplot(224)
a = [r[1] for r in ap.rank]
plt.plot(a)

'''
plt.subplot(223)
# plot the cumulative histogram
# some fake data
data = np.random.randn(1000)
print data[:6]

values, base = np.histogram(data, bins=len(ap.rank))
cumulative = np.cumsum(values)
plt.plot(base[:-1], cumulative, c='blue')

plt.title('Rank distribution')
'''

#plt.tight_layout(pad=0, w_pad=0, h_pad=0)
plt.savefig('rank.png')
