# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as plt

from EPF import *

class AP:
    def __init__(self, hs, k, percentile, bpercentile):
        self.hs = hs
        self.k = k
        self.percentile = percentile
        self.bpercentile = bpercentile

        self.epf = EPF(hs, k, percentile)
        self.filter = np.squeeze(np.where(self.epf.filter))
        self.hs.setFilter(self.filter)
        self.cube = hs.cube()

        self.channels = None
        self.channelNames = []
        self.computeChannels()
        self.normalizeChannels()

    def normalizeChannels(self):
        for idx in xrange(np.shape(self.channels)[2]):
            channel = self.channels[:,:,idx]
            normA = np.min(channel)
            normB = np.max(channel)
            normB -= normA
            self.channels[:,:,idx] = (channel - normA) / normB

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
