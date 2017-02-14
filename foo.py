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
with open('%s%s' % (imagesDirectory, 'salinasA.json')) as data_file:
    dictionary = json.load(data_file)

k = (2, 2)
percentile = 50

hs = hssa.HS(dictionary)
print hs

epf = hssa.EPF(hs, k, percentile)
print epf

noFilter = [True] * hs.bands

print 'Filter windows = %i' % np.sum(epf.filter)

#
gt = np.copy(hs.gt)
gt[0,0] = 17

# Spłaszczona kostka wypadkowa
a = epf.bordersMap(filter = noFilter)
b = epf.bordersMask(filter = noFilter)
gtb = np.copy(gt)
gtb[b] = 17

# Odfiltrowana spłaszczona kostka wypadkowa
c = epf.bordersMap()
d = epf.bordersMask()
gtd = np.copy(gt)
gtd[d] = 17


# foo.png
plt.figure(figsize=(6, 6))
gs1 = gridspec.GridSpec(2, 2)
gs1.update(wspace=0, hspace=0) # set the spacing between axes.

plt.subplot(gs1[0]); plt.imshow(a, cmap='gray'); plt.axis('off')
plt.subplot(gs1[1]); plt.imshow(gtb, cmap=materialized); plt.axis('off')

plt.subplot(gs1[2]); plt.imshow(c, cmap='gray'); plt.axis('off')
plt.subplot(gs1[3]); plt.imshow(gtd, cmap=materialized); plt.axis('off')

plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.savefig('foo.png')












# bar.png
plt.figure(figsize=(8, 6))
gs1 = gridspec.GridSpec(3, 1)
gs1.update(wspace=0, hspace=0) # set the spacing between axes.

# First
ax1 = plt.subplot(gs1[0])
entropy = epf.entropy
wherePass = np.squeeze(np.where(epf.meanEntropy))
whereEntropyFail = np.squeeze(np.where(np.logical_not(epf.meanEntropy)))

entropyPass = np.copy(entropy)
entropyPass[whereEntropyFail] = np.nan

plt.plot(xrange(hs.bands), entropy,
    color = '#FEBABA', linestyle = 'dashed', lw = 1)
plt.plot(xrange(hs.bands), entropyPass,
    color = '#CC2222', lw = 1)
#plt.title('entropy with filter')

for item in whereEntropyFail:
    ax1.add_patch(
        patches.Rectangle(
            (item-.5, -10),   # (x,y)
            1,          # width
            20,          # height
            color = '#FEE5E5'
        )
    )

# Second
ax2 = plt.subplot(gs1[1])
entropyDynamics = epf.entropyDynamics
whereDynamicsFail = np.squeeze(np.where(np.logical_not(epf.meanDynamics)))
wherePass = np.squeeze(np.where(epf.meanDynamics))

entropyDynamicsPass = np.copy(entropyDynamics)
entropyDynamicsPass[whereDynamicsFail] = np.nan

plt.plot(xrange(hs.bands), entropyDynamics,
    color = '#BABAFE', linestyle = 'dashed', lw = 1)
plt.plot(xrange(hs.bands), entropyDynamicsPass,
    color = '#2222CC', lw = 1)
#plt.title('entropy dynamics with filter')
for item in whereDynamicsFail:
    ax2.add_patch(
        patches.Rectangle(
            (item-.5, -10),   # (x,y)
            1,          # width
            20,          # height
            color = '#E5E5FE'
        )
    )
for item in whereEntropyFail:
    ax2.add_patch(
        patches.Rectangle(
            (item-.5, -10),   # (x,y)
            1,          # width
            20,          # height
            color = '#FEE5E5'
        )
    )


# Forth
ax3 = plt.subplot(gs1[2])
whereFail = np.squeeze(np.where(np.logical_not(epf.filter)))
wherePass = np.squeeze(np.where(epf.filter))
signatures = hs.signatures()
for item in signatures:
    signature = signatures[item]
    signaturePass = np.copy(signature)
    signaturePass[whereFail] = np.nan
    plt.plot(
        xrange(hs.bands), signature,
        color = '#BABABA', linestyle = 'dashed', lw = 1)
    plt.plot(xrange(hs.bands), signaturePass,
        lw = 1)

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
