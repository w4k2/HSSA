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


k = (4, 4)
reductor = 16.


ap = hssa.AP(img, k, reductor)

# foo.png
plt.figure(figsize=(6, 12))

noFilter = [True] * img.bands

# Spłaszczona kostka wypadkowa
plt.subplot(221); plt.imshow(ap.edgesFlat(noFilter), cmap='gray'); plt.axis('off')
plt.subplot(223); plt.imshow(ap.edgesMask(noFilter), cmap='gray'); plt.axis('off')

# Odfiltrowana spłaszczona kostka wypadkowa
plt.subplot(222); plt.imshow(ap.edgesFlat(), cmap='gray'); plt.axis('off')
plt.subplot(224); plt.imshow(ap.edgesMask(), cmap='gray'); plt.axis('off')

plt.savefig('foo.png')


# bar.png
plt.figure(figsize=(6, 6))

plt.subplot(311)
plt.plot(xrange(img.bands), ap.entropy)
plt.plot(xrange(img.bands), ap.meanEntropy)
plt.axis('off')
plt.title('Filtering')

plt.subplot(312)
plt.plot(xrange(img.bands), ap.entropyDynamics)
plt.plot(xrange(img.bands), ap.meanDynamics)
plt.axis('off')
plt.title('entropyDynamics and meanDynamics')

plt.subplot(313)
plt.plot(xrange(img.bands), ap.entropy)
plt.plot(xrange(img.bands), ap.filter)
plt.axis('off')
plt.title('entropy and union')


plt.axis('off')
plt.savefig('bar.png')
