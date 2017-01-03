import scipy.io
import numpy as np


class HS:
    def __init__(self, hsSource, gtSource):
        # Loading image and ground truth
        self.image = scipy.io.loadmat(hsSource[0])[hsSource[1]]
        self.gt = scipy.io.loadmat(gtSource[0])[gtSource[1]]

        # Getting in shape
        shape = np.shape(self.image)
        self.rows = shape[0]
        self.cols = shape[1]
        self.bands = shape[2]

    def signature(self, row, col):
        signature = self.image[row][col]
        return signature
