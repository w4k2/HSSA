# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as colors
import numpy as np
import weles

from HS import *
from HSFrame import *

"""
**HSSA** is a two-staged segmentation tool for hs images. It is based on consecutive division of image to decompose it into a set of homogenous segments. Later, according to labels assigned by an expert, the representation is prepared as an input for classification methods.
"""

class HSSA:
    """
    ## Initialization
    """
    def __init__(self, hs, threshold, limit=99):
        """
        Assign:

        - `hs` — hyperspectral image,
        - `threshold` — homogeneity threshold,
        - `limit` — iteration limiter,
        """
        self.hs = hs
        self.threshold = threshold
        self.limit = limit

        """
        And initialize:

        - `iteration` — number of current iteration,
        - `isComplete` — completion flag,
        - `segments` - segments counter
        """
        self.iteration = 0
        self.isComplete = False
        self.segments = 0

        # Initialize sets of frames and set up representation.
        self.heterogenous = []
        self.homogenous = []
        self.clean()

    """
    ## Single iteration
    """
    def step(self):
        self.iteration += 1
        self.separate()
        # self.merge()
        for frame in self.homogenous:
            frame.setHomo()
        self.isComplete = len(self.heterogenous) == 0

        # Breaking hetero
        newHeterogenous = []
        for frame in self.heterogenous:
            newHeterogenous.extend(frame.divide())
        self.heterogenous = newHeterogenous

    """
    ## Whole loop
    """
    def process(self):
        while not self.isComplete:
            if self.iteration == self.limit:
                break
            self.step()
        self.merge()

    """
    ## Merging process
    """
    def merge(self):
        for i in xrange(len(self.homogenous)):
            frame = self.homogenous[i]
            if frame.segment == -1:
                for j in xrange(i):
                    cmpFrame = self.homogenous[j]
                    similarity = \
                        1 - (np.mean(np.std([frame.signature, cmpFrame.signature], axis=0)) / self.hs.max)
                    if similarity > self.threshold:
                        frame.segment = cmpFrame.segment
                        break
                if frame.segment == -1:
                    frame.segment = self.segments
                    self.segments += 1

    """
    ## Algorithm output
    """
    def representation(self):
        result = []
        for frame in self.homogenous:
            # print frame
            multiplier = self.iteration - frame.fold - 1
            units = pow(2, multiplier * 2)
            for signature in frame.signatures(units):
                line = [frame.label]
                line.extend(signature)
                result.append(line)
        return result

    ## Helper functions

    """
    ### Preparing representation to work
    """
    def clean(self):
        self.iteration = 0
        self.heterogenous = [HSFrame(self.hs)]
        self.homogenous = []
        self.isComplete = False

    """
    ### Generating png preview
    """
    def image(self, title = False, labels = False):
        if not title:
            title = 'hssa_i%i_t%.0f.png' % (
                self.iteration,
                1000 * self.threshold)
        base = pow(2, self.iteration)
        img = np.ones((base, base, 3))
        minN = 9999
        maxN = 0
        for frame in self.heterogenous + self.homogenous:
            if frame.intensity < minN:
                minN = frame.intensity
            if frame.intensity > maxN:
                maxN = frame.intensity

        # Hetero
        for frame in self.heterogenous + self.homogenous:
            amount = pow(2, frame.fold)
            length = base / amount
            intensity = (frame.intensity - minN) / (maxN - minN)
            intensity = .25 + intensity / 2
            hue = 0
            if frame.isHomo:
                if labels:
                    hue = frame.label / float(2 * len(self.hs.classes))
                    if self.segments > 2 * len(self.hs.classes):
                        hue = frame.label / float(self.segments)
                else:
                    hue = frame.segment / float(2 * len(self.hs.classes))
                    if self.segments > 2 * len(self.hs.classes):
                        hue = frame.segment / float(self.segments)
            x = frame.location % amount
            y = frame.location / amount
            for i in xrange(length):
                for j in xrange(length):
                    if frame.isHomo:
                        img[length * x + i, length * y + j] = \
                            colors.hsv_to_rgb([hue, 1, .5 + intensity / 2])
                    else:
                        img[length * x + i, length * y + j] = \
                            colors.hsv_to_rgb([0, 0, intensity])

        imgplot = plt.imshow(img, interpolation="nearest")
        plt.savefig(title)

    """
    ### Separate frames
    """
    def separate(self):
        # separating
        self.homogenous.extend(
            [x for x in self.heterogenous if x.homogeneity > self.threshold])
        self.heterogenous = \
            [x for x in self.heterogenous if x.homogeneity <= self.threshold]

    """
    ### Postprocessing
    """
    def post(self):
        for segment in xrange(self.segments):
            labels = []
            for frame in self.homogenous:
                if frame.segment == segment:
                    labels.append(frame.label)
            label = max(set(labels), key=labels.count)
            for frame in self.homogenous:
                if frame.segment == segment:
                    frame.label = label
        # Removing the background
        self.heterogenous = []
        self.homogenous = \
            [x for x in self.homogenous if x.label != 0]
