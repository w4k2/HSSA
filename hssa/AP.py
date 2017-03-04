# -*- coding: utf-8 -*-
import collections as cl
import matplotlib as plt
import itertools as it
import numpy as np
import re
import colorsys as cs
import csv
import random
from skimage import io, color

from EPF import *

class AP:
    def __init__(self, hs, k = (3, 3), percentile = 80, bins = 256, quants = 4):
        # Assign AP parameters
        self.hs = hs                        # hyperspectral image
        self.bins = bins                    # number of range bins
        self.quants = quants    # number of color quants

        # Assign EPF parameters
        self.k = k                          # kernel size
        self.percentile = percentile        # filtering percentile

        # Establish EPF to gather filtered cube and establish channels
        self.epf = EPF(hs, k, percentile)
        self.cube = hs.cube()
        (self.channels, self.channelNames) = self.computeChannels()
        self.rawChannels = np.copy(self.channels)

        # Normalize channels
        self.normalizeChannels()

        # Establish and posterize histograms
        self.histograms = self.calculateHistograms()

        # Prepare a rank and visualisation
        self.rank = self.rankCombinations()
        self.impactVector = [self.rank[0][1] / cmp[1] for cmp in self.rank]
        self.visualisation = self.visualise()

    def export(self, filename, samples = 5000):
        # Open file
        with open('%s.csv' % filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            passer = random.sample(range(self.hs.rows * self.hs.cols), samples)
            i = 0
            for x in xrange(self.hs.rows):
                for y in xrange(self.hs.cols):
                    if i in passer:
                        features = self.channels[x,y]
                        label = self.hs.label((x,y))
                        writer.writerow(list(features) + [label])
                    i += 1

    @classmethod
    def cfgTag(cls, hs, k = (3, 3), percentile = 80, bins = 256, quants = 4):
        return 'ap_im_%s_k_%s_p_%i_b_%i_q_%i' % (
            re.sub('[ ]', '_', hs.name),
            re.sub('[(), ]', '', str(k)),
            percentile,
            bins,
            quants
        )

    '''
    Calculators
    '''
    def computeChannels(self):
        channelNames = []
        # First, the colors
        # red
        filterLength = len(self.epf.filter)

        rgb = np.dstack((
            np.mean(self.cube[:,:,xrange(
                0,
                1 * filterLength / 3)], axis = 2),
            np.mean(self.cube[:,:,xrange(
                1 * filterLength / 3,
                2 * filterLength / 3)], axis = 2),
            np.mean(self.cube[:,:,xrange(
                2 * filterLength / 3,
                3 * filterLength / 3)], axis = 2)))
        channelNames.extend(['red', 'green', 'blue'])

        # Later, CIELab conversion
        cie = color.rgb2lab(rgb)
        channelNames.extend(['CIE X', 'CIE Y', 'CIE Z'])

        #quartiles
        q1 = np.percentile(self.cube, 25, axis = 2)
        median = np.median(self.cube, axis = 2)
        q3 = np.percentile(self.cube, 75, axis = 2)
        interquartileRange = q3 - q1
        channelNames.extend(['1st quartile', 'median', '3rd quartile', 'Interquartile range'])

        # Regular stats
        # minimum
        minimum = np.amin(self.cube, axis = 2)
        channelNames.append('minimum')
        # maximum
        maximum = np.amax(self.cube, axis = 2)
        channelNames.append('maximum')
        # mean
        mean = np.mean(self.cube, axis = 2)
        channelNames.append('mean')
        # stdDev
        std = np.std(self.cube, axis = 2)
        channelNames.append('standard deviation')
        # variance
        var = np.var(self.cube, axis = 2)
        channelNames.append('variance')

        # Collecting
        channels = np.dstack((
            rgb, cie,
            q1, median, q3,
            interquartileRange,
            minimum,
            maximum,
            mean,
            std,
            var
        ))

        return (channels, channelNames)

    def normalizeChannels(self, masking = True):
        mask = self.epf.bordersMask()
        for idx in xrange(np.shape(self.channels)[2]):
            channel = np.copy(self.channels[:,:,idx])
            if masking:
                maskedchannel = np.copy(channel)
                maskedchannel[mask] = np.mean(channel)
                normA = np.min(maskedchannel)
                normB = np.max(maskedchannel)
            else:
                normA = np.min(channel)
                normB = np.max(channel)
            normB -= normA
            channel = (channel - normA) / normB
            channel[channel > 1] = 1
            channel[channel < 0] = 0
            channel = sp.ndimage.median_filter(
                channel,
                size=(5, 5)
            )
            self.channels[:,:,idx] = channel

    def calculateHistograms(self):
        return [(self.quants * histogram.astype(float) / np.amax(histogram)).astype(int)
            for histogram in [np.histogram(
                self.channel(idx),
                bins = self.bins)[0]
                for idx in xrange(len(self.channelNames))]]

    def rankCombinations(self):
        rank = [(x, self.colorIndex(x)) for x in it.combinations(xrange(15), 3)]
        rank.sort(key=lambda tup: tup[1], reverse=False)
        return rank

    def colorIndex(self, tup, limit = 1):
        image = self.imageFromTuple(tup)

        interquartileRange = np.subtract(np.percentile(image, 75, axis = 2), np.percentile(image, 25, axis = 2))

        a = dict(cl.Counter([str([
                self.histograms[tup[0]][bin],
                self.histograms[tup[1]][bin],
                self.histograms[tup[2]][bin]]) for bin in xrange(self.bins)]))
        factor = len(list((a[x] for x in a if a[x] > limit )))

        return np.absolute(.1 - (np.mean(interquartileRange) * float(factor)))

    '''
    Operators
    '''
    def channel(self, cid):
        return np.copy(self.channels[:,:,cid])

    def imageFromTuple(self, tup):
        return np.dstack((
            self.channel(tup[0]),
            self.channel(tup[1]),
            self.channel(tup[2])
        ))

    '''
    Decorators
    '''
    def visualise(self, limit = None, useImpact = True):
        if not limit:
            limit = int(len(self.rank) / 10)
        #print 'bziium'
        image = self.channel(self.rank[0][0])
        for i in xrange(1,limit):
            if i >= len(self.rank):
                break
            if useImpact:
                image += self.impactVector[i] * self.channel(self.rank[i][0])
            else:
                image += self.channel(self.rank[i][0])

        # Normalize
        normA = np.min(image)
        normB = np.max(image) - normA
        image = (image - normA) / normB
        hsv = plt.colors.rgb_to_hsv(image)

        # Obtain V
        origin_v = hsv[:,:,2]
        v = np.mean(self.cube, axis = 2)
        v = sp.ndimage.median_filter(
            v,
            size=(2, 2)
        )
        v = (origin_v + v) / 2
        hsv[:,:,2] = v
        image = plt.colors.hsv_to_rgb(hsv)
        return image

    def __str__(self):
        return "%s AP on %i bins and %i quants." % (
            self.epf,
            self.bins,
            self.quants
        )
