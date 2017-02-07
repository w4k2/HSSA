import scipy.io
import numpy as np
import random
import weles
import math

SEED = 123
random.seed(SEED)

class Window:
    def __init__(self, frame):
        # Getting base
        base = pow(2, frame.fold)

        # Calculating size
        width = float(frame.hs.cols) / base
        height = float(frame.hs.rows) / base

        # Establishing position
        x = int(frame.location / base)
        y = int(frame.location % base)
        self.top = int(width * x)
        self.left = int(height * y)
        self.width = int(width)
        self.height = int(height)

        if self.width == 0:
            self.width = 1

        if self.height == 0:
            self.height = 1
        '''
        print '[C%i R%i L%i X%i Y%i] t:%i l:%i w:%i(%.2f) h:%i(%.2f)' %(
            frame.hs.cols, frame.hs.rows,
            frame.location, x, y,
            self.top, self.left,
            self.width, width,
            self.height, height
        )
        '''
    def __str__(self):
        return "T:%i L:%i W:%i H:%i" % (
            self.top, self.left, self.width, self.height
        )

class HSFrame:
    def __init__(self, hs, points=20, fold=0, location=0):
        self.points = points  # amount of points to create mean signature
        self.hs = hs  # image
        self.fold = fold            # iteration, when frame was created
        self.location = location    # iteration based frame location
        self.segment = -1  # segment identifier
        self.label = -1  # class label given by the expert for region
        self.homogeneity = 0  # homogeneity measure
        self.isHomo = False
        self.intensity = 0  # intensity measure
        self.signature = []  # mean frame signature

        # Fill
        self.window = Window(self)
        self.calculate()

    def setHomo(self):
        self.isHomo = True

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

    def signatures(self, amount):
        width = self.window.width
        height = self.window.height
        top = self.window.top
        left = self.window.left
        stop = height * width
        signatures = []
        for item in xrange(0, amount if amount < stop else stop):
            index = random.randrange(stop)
            x = int(index / width)
            y = int(index % width)
            signature = self.hs.signature((left + x, top + y))
            signatures.append(signature)
        return signatures

    def samples(self, amount):
        width = self.window.width
        height = self.window.height
        top = self.window.top
        left = self.window.left
        stop = height * width
        samples = []
        for item in xrange(0, amount):
            index = random.randrange(stop)
            x = int(index / width)
            y = int(index % width)
            sample = self.hs.sample((left + x, top + y))
            samples.append(sample)
        return samples

    def calculate(self):
        #print '### Calculate'
        # Getting window parameters
        width = self.window.width
        height = self.window.height
        top = self.window.top
        left = self.window.left

        # Calculating index range
        stop = height * width
        points = self.points
        if self.points > stop:
            points = stop

        # Getting signatures
        signatures = []
        labels = []
        for item in xrange(0, points):
            index = random.randrange(stop)
            x = int(index / width)
            y = int(index % width)
            signature = self.hs.signature((left + x, top + y))
            signatures.append(signature)
            labels.append(self.hs.label((left + x, top + y)))
            #print '## ITEM %s' % signature[:3]

        self.signature = np.mean(signatures, axis=0)
        #print '## SIGN %s' % self.signature[:3]

        self.label = max(set(labels), key=labels.count)
        # homogeneity as a mean standardDeviation
        self.homogeneity = \
            1 - np.mean(np.std(signatures, axis=0))
        #print '## HOMO %f' % self.homogeneity
        #print '%f' % (1 - np.mean(np.std(signatures, axis=0)))

        self.intensity = np.mean(self.signature)

    def __str__(self):
        return "F%i|L%i|S%i|L%i|H%.3f" % (
            self.fold,
            self.location,
            self.segment,
            self.label,
            self.homogeneity)
