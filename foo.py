#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, weles, hssa
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

solarized = LinearSegmentedColormap.from_list(
    'solarized', ['#FFFFFF', '#002b36', '#073642', '#586e75', '#657b83', '#839496', '#93a1a1', '#eee8d5', '#fdf6e3', '#b58900', '#cb4b16', '#dc322f', '#d33682', '#6c71c4', '#268bd2', '#2aa198', '#859900', '#EEEEEE'])
materialized = LinearSegmentedColormap.from_list(
    'materialized', ['#fafafa', '#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#03a9f4', '#00bcd4', '#009688', '#4caf50', '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107', '#ff9800', '#ff5722', '#000000'])

imagesDirectory = 'data/hsimages/'
with open('%s%s' % (imagesDirectory, 'salinas.json')) as data_file:
    dictionary = json.load(data_file)
print 'Hello.'

img = hssa.HS(dictionary)
print img

k = (2, 2)
percentile = 50
ap = hssa.AP(img, k, percentile)

noFilter = [True] * img.bands

print 'Filter windows = %i' % np.sum(ap.filter)

# Spłaszczona kostka wypadkowa
a = ap.bordersMap(noFilter)
b = ap.bordersMask(noFilter)

# Odfiltrowana spłaszczona kostka wypadkowa
c = ap.bordersMap()
d = ap.bordersMask()

#
gt = np.copy(img.gt)
gt[0,0] = 17
gta = np.copy(img.gt)
gta[d] = 17

# foo.png
plt.figure(figsize=(6, 6))

plt.subplot(231); plt.imshow(a, cmap='gray'); plt.axis('off')
plt.subplot(234); plt.imshow(b == False, cmap='gray'); plt.axis('off')
plt.subplot(232); plt.imshow(c, cmap='gray'); plt.axis('off')
plt.subplot(235); plt.imshow(d == False, cmap='gray'); plt.axis('off')
plt.subplot(233); plt.imshow(gt, cmap=materialized); plt.axis('off')
plt.subplot(236); plt.imshow(gta, cmap=materialized); plt.axis('off')
#plt.tight_layout(pad=-0.0, w_pad=-2.0, h_pad=-4.0)
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig('foo.png')













# bar.png
plt.figure(figsize=(8, 6))
gs1 = gridspec.GridSpec(3, 1)
gs1.update(wspace=0, hspace=0) # set the spacing between axes.

# First
ax1 = plt.subplot(gs1[0])
entropy = ap.entropy
wherePass = np.squeeze(np.where(ap.meanEntropy))
whereFail = np.squeeze(np.where(np.logical_not(ap.meanEntropy)))

entropyPass = np.copy(entropy)
entropyPass[whereFail] = np.nan

plt.plot(xrange(img.bands), entropy,
    color = '#BABAFE', linestyle = 'dashed', lw = 1)
plt.plot(xrange(img.bands), entropyPass,
    color = '#2222CC', lw = 1)
#plt.title('entropy with filter')

for item in whereFail:
    ax1.add_patch(
        patches.Rectangle(
            (item-.5, -10),   # (x,y)
            1,          # width
            20,          # height
            color = '#F5F5FE'
        )
    )

# Second
ax2 = plt.subplot(gs1[2])
entropyDynamics = ap.entropyDynamics
whereFail = np.squeeze(np.where(np.logical_not(ap.meanDynamics)))
wherePass = np.squeeze(np.where(ap.meanDynamics))

entropyDynamicsPass = np.copy(entropyDynamics)
entropyDynamicsPass[whereFail] = np.nan

plt.plot(xrange(img.bands), entropyDynamics,
    color = '#FEBABA', linestyle = 'dashed', lw = 1)
plt.plot(xrange(img.bands), entropyDynamicsPass,
    color = '#CC2222', lw = 1)
#plt.title('entropy dynamics with filter')
for item in whereFail:
    ax2.add_patch(
        patches.Rectangle(
            (item-.5, -10),   # (x,y)
            1,          # width
            20,          # height
            color = '#FEF5F5'
        )
    )

# Forth
ax3 = plt.subplot(gs1[1])
whereFail = np.squeeze(np.where(np.logical_not(ap.filter)))
wherePass = np.squeeze(np.where(ap.filter))
signatures = img.signatures()
for item in signatures:
    signature = signatures[item]
    signaturePass = np.copy(signature)
    signaturePass[whereFail] = np.nan
    plt.plot(
        xrange(img.bands), signature,
        color = '#BABABA', linestyle = 'dashed', lw = 1)
    plt.plot(xrange(img.bands), signaturePass,
        lw = 1)
#plt.title('mean signatures with union filter (%i / %i bands (%.2f%%))' % (
#    np.sum(ap.filter),
#    img.bands,
#    100 * np.sum(ap.filter) / float(img.bands)
#))

for item in whereFail:
    ax3.add_patch(
        patches.Rectangle(
            (item- .5, -10),   # (x,y)
            1,          # width
            20,          # height
            color = '#F5F5F5'
        )
    )


ax1.set_yticklabels([])
ax2.set_yticklabels([])
#ax3.set_yticklabels([])

ax1.get_xaxis().set_tick_params(direction='in')
ax1.get_yaxis().set_tick_params(direction='in')
ax2.get_xaxis().set_tick_params(direction='in')
ax2.get_yaxis().set_tick_params(direction='in')
ax3.get_xaxis().set_tick_params(direction='in')
ax3.get_yaxis().set_tick_params(direction='in')

plt.tight_layout(pad=1)
plt.savefig('bar.png')
