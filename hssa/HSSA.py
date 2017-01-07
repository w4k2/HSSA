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
        base = 512
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
            x = frame.location % amount
            y = frame.location / amount
            for i in xrange(length):
                for j in xrange(length):
                    if frame.isHomo:
                        img[length * x + i, length * y + j] = [
                            intensity, 0, 0]
                    else:
                        img[length * x + i, length * y + j] = [
                            intensity, intensity, intensity]

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
