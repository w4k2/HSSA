#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, weles, hssa
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

imagesDirectory = 'data/hsimages/'
with open('%s%s' % (imagesDirectory, 'salinas.json')) as data_file:
    dictionary = json.load(data_file)
print 'Hello.'

img = hssa.HS(dictionary)
print img

k = (2,2)

# Kostka graniczna
edges3d = img.edges3d(k)
print '- edges3d shape = %s' % str(np.shape(edges3d))

# Filtr
edgesFilter = img.edgesFilter(edges3d)
entropy = edgesFilter[0]
meanEntropy = edgesFilter[1]
entropyDynamics = edgesFilter[2]
meanDynamics = edgesFilter[3]
union = edgesFilter[4]

# Spłaszczona kostka
edgesFlat = img.edgesFlat(edges3d)
print '- edgesFlat shape = %s' % str(np.shape(edgesFlat))


# Maska
edgesMask = img.edgesMask(edgesFlat)
print '- edgesMask shape = %s' % str(np.shape(edgesMask))

plt.figure(figsize=(16,8))

plt.subplot(431)
plt.imshow(edgesFlat, cmap='gray')
plt.title('edgesFlat')
plt.axis('off')

plt.subplot(432)
plt.imshow(edgesMask, cmap='gray')
plt.title('edgesMask')
plt.axis('off')


plt.subplot(412)
plt.plot(xrange(img.bands), entropy)
plt.plot(xrange(img.bands), meanEntropy)
plt.title('entropy and meanEntropy')

plt.subplot(413)
plt.plot(xrange(img.bands), entropyDynamics)
plt.plot(xrange(img.bands), meanDynamics)
plt.title('entropyDynamics and meanDynamics')

plt.subplot(414)
plt.plot(xrange(img.bands), entropy)
plt.plot(xrange(img.bands), union)
plt.title('entropy and union')

'''
edgesMask = img.edgesMask(k)


plt.imshow(edgesMask, cmap='gray')
plt.axis('off')

'''
plt.savefig('foo.png')
