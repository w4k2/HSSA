import scipy.io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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

        # Initialize set of frames
        self.heterogenous = []
        self.homogenous = []
        # Set up representation
        self.clean()

    def image(self):
        print 'Showing image at iteration %i' % self.iteration
        # img = np.ones((self.hs.cols + 1, self.hs.rows + 1, 3))
        base = 512
        img = np.ones((base, base, 3))
        minN = 9999
        maxN = 0
        for frame in self.heterogenous:
            if frame.intensity < minN:
                minN = frame.intensity
            if frame.intensity > maxN:
                maxN = frame.intensity
        for frame in self.homogenous:
            if frame.intensity < minN:
                minN = frame.intensity
            if frame.intensity > maxN:
                maxN = frame.intensity
        # print '%f - %f' % (minN, maxN)

        # Hetero
        for frame in self.heterogenous:
            amount = pow(2,frame.fold)
            length = base / amount
            intensity = (frame.intensity - minN) / (maxN - minN)
            x = frame.location % amount
            y = frame.location / amount
            for i in xrange(length):
                for j in xrange(length):
                    img[length * x + i, length * y + j] = [
                        intensity, 0, 0]
        # Homo
        for frame in self.homogenous:
            amount = pow(2,frame.fold)
            length = base / amount
            intensity = (frame.intensity - minN) / (maxN - minN)
            x = frame.location % amount
            y = frame.location / amount
            for i in xrange(length):
                for j in xrange(length):
                    img[length * x + i, length * y + j] = [
                        0, intensity, 0]
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

    def step(self):
        self.iteration += 1
        self.split()
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
