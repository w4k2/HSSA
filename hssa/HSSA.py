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
    def __init__(self, hs, threshold, jThreshold, limit=99, points=20, stopAutomerge=False):
        """
        Assign:

        - `hs` — hyperspectral image,
        - `threshold` — homogeneity threshold,
        - `limit` — iteration limiter,
        """
        self.hs = hs
        self.threshold = threshold
        self.jThreshold = jThreshold
        self.limit = limit
        self.points = points

        self.stopAutomerge = stopAutomerge

        """
        And initialize:

        - `iteration` — number of current iteration,
        - `isComplete` — completion flag,
        - `segments` - segments counter
        """
        self.iteration = 0
        self.isComplete = False
        self.segments = 0
        self.classes = {}
        self.maxlabel = 0

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

        for frame in self.homogenous:
            frame.setHomo()
        self.isComplete = len(self.heterogenous) == 0

        # Breaking hetero
        newHeterogenous = []
        for frame in self.heterogenous:
            newHeterogenous.extend(frame.divide())
        self.heterogenous = newHeterogenous

        # Merge procedure at every iteration
        if not self.stopAutomerge:
            self.merge()

    """
    ## Whole loop
    """
    def process(self):
        while not self.isComplete:
            if self.iteration == self.limit:
                break
            self.step()
        self.post()

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
                        1 - np.mean(np.std([frame.signature, cmpFrame.signature], axis=0))
                    if similarity > self.jThreshold:
                        frame.segment = cmpFrame.segment
                        break
                if frame.segment == -1:
                    frame.segment = self.segments
                    self.segments += 1

    """
    ## Algorithm output

    - 0 — one mean signature from mean of frames
    - 1 — one mean signature per frame
    - 2 - n random signatures from every frame
    """
    def train(self, c):
        train = []
        for label in self.classes:
            collection = self.classes[label]
            #print '- %i frames for label %i:' % (
            #    len(collection),
            #    label
            #)

            # One per class
            if c == 0:
                buffer = []
                for frame in collection:
                    signature = frame.signature
                    buffer.append(signature)
                    #for sample in samples:
                    #    print "\t- %s" % sample.features[:3]
                signature = np.mean(buffer, axis=0)
                sample = weles.Sample(
                    signature,
                    self.hs.reverseClasses[label]
                    )
                train.append(sample)
            # One per frame
            elif c == 1:
                #buffer = []
                for frame in collection:
                    #samples = frame.samples(3)
                    signature = frame.signature # one
                    sample = weles.Sample(
                        signature,
                        self.hs.reverseClasses[label]
                        )
                    train.append(sample)
                    #print "\tS=%s:" % signature[:3]
                    #buffer.append(signature)
                    #for sample in samples:
                    #    print "\t- %s" % sample.features[:3]
            else:
                #buffer = []
                for frame in collection:
                    signatures = frame.signatures(c)
                    signature = frame.signature # one
                    for signature in signatures:
                        sample = weles.Sample(
                            signature,
                            self.hs.reverseClasses[label]
                            )
                        train.append(sample)


        # print self.classes
        return train

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
        return "%s %s, i = %i, %i het, %i hom, s = %i" % (
            "complete" if self.isComplete else "in progress",
            self.hs.name,
            self.iteration,
            len(self.heterogenous),
            len(self.homogenous),
            self.segments
        )

    """
    ### Preparing representation to work
    """
    def clean(self):
        self.iteration = 0
        self.heterogenous = [HSFrame(self.hs, self.points)]
        self.homogenous = []
        self.isComplete = False

    """
    ### Generating png preview
    """
    def png(self, title = False, labels = False, segments = False):
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

        if len(union):
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
                        hue = frame.label / float(self.hs.maxlabel)
                    else:
                        hue = frame.segment / 17.
                        if self.segments > 17:
                            hue = frame.segment / float(self.segments)
                x = frame.location % amount
                y = frame.location / amount
                for i in xrange(length):
                    for j in xrange(length):
                        if frame.isHomo:
                            # Homogeniczna poetykietowana
                            if labels:
                                img[length * x + i, length * y + j] = \
                                    colors.hsv_to_rgb([hue, .75, .75])
                            # Homogeniczna nieetykietowana
                            else:
                                if segments:
                                    # Homogeniczna z segmentami
                                    img[length * x + i, length * y + j] = \
                                        colors.hsv_to_rgb([hue, 1, .5 + intensity / 4])

                                else:
                                    # Homogeniczna naga
                                    img[length * x + i, length * y + j] = \
                                        colors.hsv_to_rgb([0, 0, .1 + intensity / 4])
                        else:
                            # Heterogeniczna
                            img[length * x + i, length * y + j] = \
                                colors.hsv_to_rgb([0, 0, .75 + intensity/4])

        # Plot
        plt.imshow(img, interpolation="nearest")
        plt.axis('off')
        #'''
        plt.title('%s image, iteration %i, t = %.3f\n%i homo / %i hetero / %i segments' % (
            self.hs.name,
            self.iteration,
            self.threshold,
            len(self.homogenous),
            len(self.heterogenous),
            self.segments
        ))
        #'''
        plt.savefig(title)

    """
    ### Separate frames
    """
    def separate(self):
        # separating
        #print 'Separating'
        #for frame in self.heterogenous:
        #    print frame
        self.homogenous.extend(
            [x for x in self.heterogenous if x.homogeneity > self.threshold])
        self.heterogenous = \
            [x for x in self.heterogenous if x.homogeneity <= self.threshold]

    """
    ### Postprocessing
    """
    def post(self):
        # Removing the background
        self.heterogenous = []
        self.homogenous = \
            [x for x in self.homogenous if x.label != 0]

        # Analyzing segment by segment
        for segment in xrange(self.segments):
            labels = []
            for frame in self.homogenous:
                if frame.segment == segment:
                    labels.append((frame.label, frame.fold, frame.homogeneity))

            if len(labels):
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

                # Zmniejszenie roli tła
                #print votes
                if 0 in votes:
                    # print "%f is too large" % votes[0]
                    votes[0] /= 3
                #print votes

                label = max(votes.iteritems(), key=operator.itemgetter(1))[0]
                if label > self.maxlabel:
                    self.maxlabel = label

                #print "Segment %i of size %i labeled as %i" % (
                #    segment, sizeOfSegment, label)
                #print 'Votes: %s gives us decision %i' % (votes, label)
                for frame in self.homogenous:
                    if frame.segment == segment:
                        frame.label = label
                        if not label in self.classes:
                            self.classes[label] = [frame]
                        else:
                            self.classes[label].append(frame)

        # Removing the background
        self.heterogenous = []
        self.homogenous = \
            [x for x in self.homogenous if x.label != 0]

        # print analysis
        # print "%i classes detected" % len(self.classes)

    def cfgTag(self):
        return 'hssa_im_%s_ht_%.3f_jt_%.3f_l_%i_p_%i' % (
            self.hs.name,
            self.threshold,
            self.jThreshold,
            self.limit,
            self.points
        )
