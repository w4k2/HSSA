# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as plt
import itertools as it
import scipy as sp
from collections import Counter

from sets import Set
from EPF import *

class AP:
    def __init__(self, hs, k, percentile, bpercentile, bins = 64, quantization = 16):
        self.hs = hs
        self.k = k
        self.percentile = percentile
        self.bpercentile = bpercentile
        self.bins = bins
        self.quantization = quantization

        print '- establishing EPF'
        self.epf = EPF(hs, k, percentile)
        self.filter = np.squeeze(np.where(self.epf.filter))
        self.hs.setFilter(self.filter)
        print '- gathering cube'
        self.cube = hs.cube()

        self.channels = None
        self.channelNames = []
        print '- computing channels'
        self.computeChannels()
        print '- normalizing channels'
        self.normalizeChannels()
        print '- establishing histograms'
        self.histograms = [np.histogram(self.channels[:,:,idx], bins = self.bins)[0] for idx in xrange(np.shape(self.channels)[2])]

        # Posterize histogram
        print '- posterizing histograms'
        for i in xrange(15):
            histogram = self.histograms[i]
            histogram = histogram.astype(float) / np.amax(histogram)
            histogram *= self.quantization
            histogram = histogram.astype(int)
            self.histograms[i] = histogram

        print '- preparing a combination rank'
        self.rank = self.searchForTheBest()
        print '- done'

    def searchForTheBest(self):
        rank = [(x, self.colorIndex(x)) for x in it.combinations(xrange(15), 3)]
        rank.sort(key=lambda tup: tup[1], reverse=False)
        return rank

    # Calculate number of colors
    '''
    def colorIndex(self, tup):
        colors = Set()

        a = Counter([ str([
                self.histograms[tup[0]][bin],
                self.histograms[tup[1]][bin],
                self.histograms[tup[2]][bin]]) for bin in xrange(self.bins)])

        for bin in xrange(self.bins):
            color = str([
                self.histograms[tup[0]][bin],
                self.histograms[tup[1]][bin],
                self.histograms[tup[2]][bin]
            ])
            colors.add(str(color))
        #print "CI(%s) = %i" % (str(tup), len(colors))

        #print colors
        return len(colors)

    def colorIndex(self, tup, limit = 1):
        a = dict(Counter([ str([
                self.histograms[tup[0]][bin],
                self.histograms[tup[1]][bin],
                self.histograms[tup[2]][bin]]) for bin in xrange(self.bins)]))
        return len(list((a[x] for x in a if a[x] > limit )))

    '''

    def colorIndex(self, tup, limit = 1):
        image = np.dstack((
            self.channels[:,:,tup[0]],
            self.channels[:,:,tup[1]],
            self.channels[:,:,tup[2]]
        ))

        denivelation = np.subtract(np.percentile(image, 75, axis = 2), np.percentile(image, 25, axis = 2))

        #print np.shape(denivelation)
        #print np.mean(denivelation)

        a = dict(Counter([ str([
                self.histograms[tup[0]][bin],
                self.histograms[tup[1]][bin],
                self.histograms[tup[2]][bin]]) for bin in xrange(self.bins)]))
        factor = len(list((a[x] for x in a if a[x] > limit )))

        return np.absolute(.1 - (np.mean(denivelation) * float(factor)))

    def visualization(self, limit = None):
        if not limit:
            limit = int(len(self.rank) / 10)
        print 'bziium'
        print limit
        image = self.channels[:,:,self.rank[0][0]]
        for i in xrange(1,limit):
            if i >= len(self.rank):
                break
            impact = self.rank[0][1] / self.rank[i][1]
            #print impact
            image += impact * self.channels[:,:,self.rank[i][0]]
        #image /= limit
        normA = np.min(image)
        normB = np.max(image)
        normB -= normA
        image = (image - normA) / normB
        return image


    def computeHistograms(self):
        for idx in xrange(np.shape(self.channels)[2]):
            print idx

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
                size=(3, 3)
            )
            self.channels[:,:,idx] = channel

    def computeChannels(self):
        # First, the colors
        # red
        red = np.mean(self.cube[:,:,xrange(
            0,
            1 * len(self.filter) / 3)], axis = 2)
        self.channelNames.append('red')
        # green
        green = np.mean(self.cube[:,:,xrange(
            1 * len(self.filter) / 3,
            2 * len(self.filter) / 3)], axis = 2)
        self.channelNames.append('green')
        # blue
        blue = np.mean(self.cube[:,:,xrange(
            2 * len(self.filter) / 3,
            3 * len(self.filter) / 3)], axis = 2)
        self.channelNames.append('blue')
        rgb = np.dstack((
            red,
            green,
            blue
        ))

        # Later, HSV conversion
        hsv = plt.colors.rgb_to_hsv(np.multiply(rgb, -255))

        # hue
        hue = hsv[:,:,0]
        self.channelNames.append('hue')
        # saturation
        saturation = hsv[:,:,1]
        self.channelNames.append('saturation')
        # brightness
        brightness = hsv[:,:,2]
        self.channelNames.append('brightness')

        #quartiles
        q1 = np.percentile(self.cube, 25, axis = 2)
        median = np.median(self.cube, axis = 2)
        q3 = np.percentile(self.cube, 75, axis = 2)
        interquartileRange = q3 - q1
        self.channelNames.extend(['1st quartile', 'median', '3rd quartile', 'Interquartile range'])


        # Regular stats
        # minimum
        minimum = np.amin(self.cube, axis = 2)
        self.channelNames.append('minimum')
        # maximum
        maximum = np.amax(self.cube, axis = 2)
        self.channelNames.append('maximum')
        # mean
        mean = np.mean(self.cube, axis = 2)
        self.channelNames.append('mean')
        # median
        self.channelNames.append('median')
        # stdDev
        std = np.std(self.cube, axis = 2)
        self.channelNames.append('standard deviation')
        # variance
        var = np.var(self.cube, axis = 2)
        self.channelNames.append('variance')

        # Collecting
        self.channels = np.dstack((
            rgb, hsv,
            q1, median, q3,
            interquartileRange,
            minimum,
            maximum,
            mean,
            std,
            var
        ))

    def __str__(self):
        return "AP on %s image, k = %s, p = %i, bp = %i" % (
            self.hs.name,
            self.k,
            self.percentile,
            self.bpercentile
        )
