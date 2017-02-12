#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, weles, hssa
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib.colors import LinearSegmentedColormap

solarized = LinearSegmentedColormap.from_list(
    'solarized', ['#FFFFFF', '#002b36', '#073642', '#586e75', '#657b83', '#839496', '#93a1a1', '#eee8d5', '#fdf6e3', '#b58900', '#cb4b16', '#dc322f', '#d33682', '#6c71c4', '#268bd2', '#2aa198', '#859900', '#EEEEEE'])
materialized = LinearSegmentedColormap.from_list(
    'materialized', ['#fafafa', '#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#03a9f4', '#00bcd4', '#009688', '#4caf50', '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107', '#ff9800', '#ff5722', '#eeeeee'])

imagesDirectory = 'data/hsimages/'
with open('%s%s' % (imagesDirectory, 'salinas.json')) as data_file:
    dictionary = json.load(data_file)
print 'Hello.'

img = hssa.HS(dictionary)
print img

k = (2, 2)
percentile = 75
ap = hssa.AP(img, k, percentile)

noFilter = [True] * img.bands

# Spłaszczona kostka wypadkowa
a = ap.edgesFlat(noFilter)
b = ap.edgesMask(noFilter)

# Odfiltrowana spłaszczona kostka wypadkowa
c = ap.edgesFlat()
d = ap.edgesMask()

#
gt = np.copy(img.gt)
gt[0,0] = 17
gta = np.copy(img.gt)
gta[d] = 17

# foo.png
plt.figure(figsize=(6, 6))

plt.subplot(231); plt.imshow(a, cmap='gray'); plt.axis('off')
plt.title('#noFilter')
plt.subplot(234); plt.imshow(b, cmap='gray'); plt.axis('off')
plt.subplot(232); plt.imshow(c, cmap='gray'); plt.axis('off')
plt.title('#filter')
plt.subplot(235); plt.imshow(d, cmap='gray'); plt.axis('off')
plt.subplot(233); plt.imshow(gt, cmap=materialized)
plt.axis('off')
plt.title('#gt')
plt.subplot(236); plt.imshow(gta, cmap=materialized)
plt.axis('off')

plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig('foo.png')


# bar.png
plt.figure(figsize=(6, 6))

# First
plt.subplot(311)
entropy = ap.entropy
whereFail = np.squeeze(np.where(np.logical_not(ap.meanEntropy)))

entropyPass = np.copy(entropy)
entropyPass[whereFail] = np.nan

plt.plot(xrange(img.bands), entropy,
    color = '#000000', linestyle = 'dashed', lw = .8)
plt.plot(xrange(img.bands), entropyPass,
    color = '#CC2222', lw = 1.5)
plt.title('Entropy with mean filter')

# Second
plt.subplot(312)
entropyDynamics = ap.entropyDynamics
whereFail = np.squeeze(np.where(np.logical_not(ap.meanDynamics)))

entropyDynamicsPass = np.copy(entropyDynamics)
entropyDynamicsPass[whereFail] = np.nan

plt.plot(xrange(img.bands), entropyDynamics,
    color = '#000000', linestyle = 'dashed', lw = .8)
plt.plot(xrange(img.bands), entropyDynamicsPass,
    color = '#CC2222', lw = 1.5)
plt.title('Entropy dynamics with mean filter')

# Third
plt.subplot(313)
whereFail = np.squeeze(np.where(np.logical_not(ap.filter)))

entropyPass = np.copy(entropy)
entropyPass[whereFail] = np.nan

plt.plot(xrange(img.bands), entropy,
    color = '#000000', linestyle = 'dashed', lw = .8)
plt.plot(xrange(img.bands), entropyPass,
    color = '#CC2222', lw = 1.5)
plt.title('Entropy with union filter')


plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig('bar.png')
