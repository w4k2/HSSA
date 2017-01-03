import scipy.io
import numpy as np


class HSSA:
    def __init__(self, hsSource, gtSource):
        # Loading image and ground truth
        image = scipy.io.loadmat(hsSource[0])[hsSource[1]]
        gt = scipy.io.loadmat(gtSource[0])[gtSource[1]]

    def learn(self):
        pass
