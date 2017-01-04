import scipy.io
import numpy as np

from HS import *
from HSFrame import *

class HSSA:
    def __init__(self, hs):
        self.hs = hs
        self.heterogenous = []
        self.homogenous = []

        self.clean()

    def clean(self):
        self.heterogenous = [HSFrame()]
        self.homogenous = []
