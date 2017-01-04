import scipy.io
import numpy as np
import random

SEED = 123
random.seed(SEED)

class HSFrame:
    def __init__(self, hs, points = 30):
        # Get amount of points to create mean signature
        self.points = points
        # Assign image
        self.hs = hs
        # iteration, when segment was created
        self.fold = 0
        # iteration based frame location
        self.location = 0
        # segment identifier, resulting from the merging procedure
        self.segment = -1
        # class label given by the expert for region
        self.label = -1
        # homogeneity measure
        self.homogeneity = 0

        # mean frame signature
        self.signature = []

        # Fill
        self.window = self.window()
        self.calculate()

    def window(self):
        # Getting base
        base = pow(2,self.fold)

        # Calculating size
        width = int(self.hs.cols / base)
        height = int(self.hs.rows / base)

        # Establishing position
        x = int(self.location / base)
        y = int(self.location % base)
        top = width * x
        left = height * y

        return {'top': top, 'left': left, 'width': width, 'height': height}

    def calculate(self):
        print 'Calculating signature'
        # Getting window parameters
        width = self.window['width']
        height = self.window['height']
        top = self.window['top']
        left = self.window['left']

        # Calculating index range
        stop = height * width

        # Getting signatures
        signatures = []
        for item in xrange(0, self.points):
            index = random.randrange(stop)
            x = int(index / width)
            y = int(index % height)
            signature = self.hs.signature(left + x, top + y)
            signatures.append(signature)
            # print '%03i - %05i - %02i:%02i' % (item, index, x, y)
        self.signature = np.mean(signatures, axis=0)

    def __str__(self):
        return "F%i|L%i|S%i|L%i|H%.3f" % (self.fold, self.location, self.segment, self.label, self.homogeneity)
