import scipy.io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as colors
import numpy as np

from HS import *
from HSFrame import *


class HSSA:
    def __init__(self, hs, threshold, limit=99):
        # Assign image
        self.hs = hs
        # Set homogeneity threshold
        self.threshold = threshold
        # Set iteration limiter
        self.limit = limit
        # Iteration number
        self.iteration = 0
        # Is done?
        self.isComplete = False
        # segments count
        self.segments = 0

        # Initialize set of frames
        self.heterogenous = []
        self.homogenous = []
        # Set up representation
        self.clean()

    def image(self):
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
        plt.savefig('hssa_i%i_t%.0f.png' % (
            self.iteration,
            1000 * self.threshold))

    def process(self):
        while not self.isComplete:
            if self.iteration == self.limit:
                break
            self.step()

    def split(self):
        # Splitting
        self.homogenous.extend(
            [x for x in self.heterogenous if x.homogeneity > self.threshold])
        self.heterogenous = \
            [x for x in self.heterogenous if x.homogeneity <= self.threshold]

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
        # print '# SHOWING SEGMENTS'
        # for frame in self.homogenous:
        #     print frame

    def step(self):
        self.iteration += 1
        self.split()
        self.merge()
        for frame in self.homogenous:
            frame.isHomo = True
        self.isComplete = len(self.heterogenous) == 0

        # Breaking hetero
        newHeterogenous = []
        for frame in self.heterogenous:
            newHeterogenous.extend(frame.divide())
        self.heterogenous = newHeterogenous

    def clean(self):
        self.iteration = 0
        self.heterogenous = [HSFrame(self.hs)]
        self.homogenous = []
        self.isComplete = False
