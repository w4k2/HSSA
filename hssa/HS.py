import scipy.io
import numpy as np

class HS:
    def __init__(self, dictionary):
        # Loading image and ground truth
        self.image = self.loadMatFromTuple(dictionary['image'])
        self.gt = self.loadMatFromTuple(dictionary['gt'])

        # Searching for maximum
        self.max = np.amax(self.image)

        # Getting in shape
        shape = np.shape(self.image)
        self.rows = shape[0]
        self.cols = shape[1]
        self.bands = shape[2]
        self.name = dictionary['name']
        self.classes = dictionary['classes']

    def loadMatFromTuple(self, entry):
        return scipy.io.loadmat(entry[0])[entry[1]]

    def __str__(self):
        return '%s image, %i classes, %i samples of %i bands' % (
            self.name,
            len(self.classes),
            self.rows * self.cols,
            self.bands)

    def signature(self, row, col):
        return np.copy(self.image[row,col])

    def slice(self, band):
        return np.copy(self.image[:,:,band])

    def signatures(self):
        labels = np.max(self.gt) + 1
        signatures = []
        for label in xrange(0, labels):
            stack = []
            for x, row in enumerate(self.gt):
                for y, value in enumerate(row):
                    if value == label:
                        stack.append(self.signature(x,y))
            if len(stack) != 0:
                signature = np.mean(stack, 0)
                signatures.append(signature)

        return signatures
