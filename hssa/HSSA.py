import scipy.io
import numpy as np

from HS import *
from HSFrame import *

class HSSA:
    def __init__(self, hs):
        # Assign image
        self.hs = hs
        # Initialize set of frames
        self.heterogenous = []
        self.homogenous = []
        # Set up representation
        self.clean()

    def clean(self):
        self.heterogenous = [HSFrame(hs)]
        self.homogenous = []
