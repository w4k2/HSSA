import scipy.io
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

    def process(self):
        while not self.isComplete:
            if self.iteration == self.limit:
                break
            self.step()

    def step(self):
        self.iteration += 1

        # Splitting
        self.homogenous.extend(
            [x for x in self.heterogenous if x.homogeneity > self.threshold])
        self.heterogenous = \
            [x for x in self.heterogenous if x.homogeneity <= self.threshold]
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
