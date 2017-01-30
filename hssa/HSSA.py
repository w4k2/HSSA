# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as colors
from operator import attrgetter
import numpy as np
import weles
import operator

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

        # Merge procedure at every iteration
        self.merge()

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
    ### Status string
    """
    def __str__(self):
        return "%s %s, iteration %i, %i heterogenous, %i homogenous" % (
            "complete" if self.isComplete else "in progress",
            self.hs.name,
            self.iteration,
            len(self.heterogenous),
            len(self.homogenous)
        )

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
    def png(self, title = False, labels = False):
        # Join FLR-s
        union = self.heterogenous + self.homogenous

        # Generate title if not provided.
        if not title:
            title = 'hssa_i%i_t%.0f.png' % (
                self.iteration,
                1000 * self.threshold)

        # Establish base resolution on a iterated power of 2.
        base = pow(2, self.iteration)
        img = np.ones((base, base, 3))

        # Scale intensivity according to values in FLR-s.
        minN = min(union, key=attrgetter('intensity')).intensity
        maxN = max(union, key=attrgetter('intensity')).intensity

        # Iterate every frame
        for frame in union:
            amount = pow(2, frame.fold)
            length = base / amount
            intensity = (frame.intensity - minN) / (maxN - minN)
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
                        if labels:
                            img[length * x + i, length * y + j] = \
                                colors.hsv_to_rgb([hue, .75, .75])
                        else:
                            img[length * x + i, length * y + j] = \
                                colors.hsv_to_rgb([hue, 1, .5 + intensity / 2])
                    else:
                        img[length * x + i, length * y + j] = \
                            colors.hsv_to_rgb([0, 0, intensity])

        # Plot
        plt.imshow(img, interpolation="nearest")
        plt.axis('off')
        plt.title('%s image, iteration %i, t = %.3f\n%i homo / %i hetero / %i segments' % (
            self.hs.name,
            self.iteration,
            self.threshold,
            len(self.homogenous),
            len(self.heterogenous),
            self.segments
        ))
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
        # Analyzing segment by segment
        for segment in xrange(self.segments):
            labels = []
            for frame in self.homogenous:
                if frame.segment == segment:
                    labels.append((frame.label, frame.fold, frame.homogeneity))

            votes = {}
            sizeOfSegment = 0
            for label in labels:
                # print label
                value = pow(4, self.iteration - label[1] - 1)
                sizeOfSegment += value
                value *= label[2]
                if not label[0] in votes:
                    votes[label[0]] = value
                else:
                    votes[label[0]] += value

            label = max(votes.iteritems(), key=operator.itemgetter(1))[0]


            print "Segment %i of size %i labeled as %i" % (
                segment, sizeOfSegment, label)
            #print 'Votes: %s gives us decision %i' % (votes, label)
            for frame in self.homogenous:
                if frame.segment == segment:
                    frame.label = label

        # Removing the background
        self.heterogenous = []
        self.homogenous = \
            [x for x in self.homogenous if x.label != 0]
