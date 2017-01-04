import scipy.io
import numpy as np

class HSFrame:
    def __init__(self, hs):
        # Assign image
        self.hs = hs
        # iteration, when segment was created
        self.fold = 0
        # unique frame identifier
        self.frame = 0
        # segment identifier, resulting from the merging procedure
        self.segment = 0
        # class label given by the expert for region
        self.label = 0
        # homogeneity measure
        self.homogeneity = 0

        # mean frame signature
        self.signature = []
