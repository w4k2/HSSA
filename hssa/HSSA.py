import scipy.io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from HS import *
from HSFrame import *


class HSSA:
    def __init__(self, hs, threshold, limit):
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
        print 'Showing image at iteration %i' % (self.iteration)
        img = [[[0, 1, 0]]]
        imgplot = plt.imshow(img)
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
