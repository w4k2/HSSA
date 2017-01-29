import scipy.io
import numpy as np
import random
import weles

SEED = 123
random.seed(SEED)

class Window:
    def __init__(self, frame):
        # Getting base
        base = pow(2, frame.fold)

        # Calculating size
        width = frame.hs.cols / base
        height = frame.hs.rows / base

        # Establishing position
        x = int(frame.location / base)
        y = int(frame.location % base)
        self.top = width * x
        self.left = height * y
        self.width = int(width)
        self.height = int(height)

class HSFrame:
    def __init__(self, hs, points=250, fold=0, location=0):
        self.points = points  # amount of points to create mean signature
        self.hs = hs  # image
        self.fold = fold            # iteration, when frame was created
        self.location = location  # iteration based frame location
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
        signatures = [self.hs.signature((left, top))]
        for item in xrange(0, amount - 1):
            index = random.randrange(stop)
            x = int(index / width)
            y = int(index % width)
            sample = self.hs.sample((left + x, top + y))
            signature = self.hs.signature((left + x, top + y))
            signatures.append(sample.features)
        return signatures

    def calculate(self):
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
        signatures = [self.hs.signature((left, top))]
        labels = [self.hs.label((left, top))]
        if stop:
            for item in xrange(0, points):
                index = random.randrange(stop)
                x = int(index / width)
                y = int(index % width)
                signature = self.hs.signature((left + x, top + y))
                signatures.append(signature)
                labels.append(self.hs.label((left + x, top + y)))
                # print '%03i - %05i - %02i:%02i' % (item, index, x, y)
        self.signature = np.mean(signatures, axis=0)

        self.label = max(set(labels), key=labels.count)
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
