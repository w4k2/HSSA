import scipy.io
import numpy as np
import random

SEED = 123
random.seed(SEED)


class HSFrame:
    def __init__(self, hs, points=250, fold=0, location=0):
        # Get amount of points to create mean signature
        self.points = points
        # Assign image
        self.hs = hs
        # iteration, when segment was created
        self.fold = fold
        # iteration based frame location
        self.location = location
        # segment identifier, resulting from the merging procedure
        self.segment = -1
        # class label given by the expert for region
        self.label = -1
        # homogeneity measure
        self.homogeneity = 0
        self.isHomo = False
        # intensity measure
        self.intensity = 0
        # mean frame signature
        self.signature = []

        # Fill
        self.window = self.window()
        self.calculate()

    def divide(self):
        # Bases
        base = pow(2, self.fold)
        newBase = pow(2, self.fold + 1)

        # Counting overlines
        overlines = self.location / base

        # Establishing start
        x = 2 * (self.location + self.location / base * base)

        # Creating new frames
        frames = []
        frames.append(
            HSFrame(self.hs, self.points, self.fold + 1, x))
        frames.append(
            HSFrame(self.hs, self.points, self.fold + 1, x + 1))
        frames.append(
            HSFrame(self.hs, self.points, self.fold + 1, x + newBase))
        frames.append(
            HSFrame(self.hs, self.points, self.fold + 1, x + newBase + 1))
        return frames

    def window(self):
        # Getting base
        base = pow(2, self.fold)

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
        # Getting window parameters
        width = self.window['width']
        height = self.window['height']
        top = self.window['top']
        left = self.window['left']

        # Calculating index range
        stop = height * width
        points = self.points
        if self.points > stop:
            points = stop

        # Getting signatures
        signatures = [self.hs.signature(left, top)]
        if stop:
            for item in xrange(0, self.points):
                index = random.randrange(stop)
                x = int(index / width)
                y = int(index % width)
                signature = self.hs.signature(left + x, top + y)
                signatures.append(signature)
                # print '%03i - %05i - %02i:%02i' % (item, index, x, y)
        self.signature = np.mean(signatures, axis=0)
        # homogeneity as a mean standardDeviation
        self.homogeneity = \
            1 - (np.mean(np.std(signatures, axis=0)) / self.hs.max)

        self.intensity = np.mean(self.signature)

    def __str__(self):
        return "F%i|L%i|S%i|L%i|H%.3f" % (
            self.fold,
            self.location,
            self.segment,
            self.label,
            self.homogeneity)
