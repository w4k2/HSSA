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

        # Initialize set of frames
        self.heterogenous = []
        self.homogenous = []
        # Set up representation
        self.clean()

    def clean(self):
        self.heterogenous = [HSFrame(self.hs)]
        self.homogenous = []
