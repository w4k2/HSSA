# -*- coding: utf-8 -*-
import scipy.io
import numpy as np
import weles
import operator

"""
A class to store and to use hypersectral image.
"""
class HS:
    """
    ## Initialization
    """
    def __init__(self, dictionary):
        # Loading image, ground truth and establishing informations.
        self.image = self.loadMatFromTuple(dictionary['image'])
        self.gt = self.loadMatFromTuple(dictionary['gt'])
        self.name = dictionary['name']
        self.classes = dictionary['classes']

        #print type(self.image[(0,0)][0])

        # Getting in shape.
        shape = np.shape(self.image)
        self.rows = shape[0]
        self.cols = shape[1]
        self.bands = shape[2]

        # Normalize
        self.normA = []
        self.normB = []
        for sliceIdx in xrange(self.bands):
            slice = self.slice(sliceIdx)
            #print sliceIdx
            minimum = np.min(slice)
            maximum = np.max(slice)
            self.normA.append(minimum)
            self.normB.append(maximum)
            #print slice
            #print 'min %i max %i' % (minimum, maximum)
        self.normB = map(operator.sub, self.normB, self.normA)
        #print self.normA
        #print self.normB


        # Searching for maximum value
        self.max = np.amax(self.image)
        self.maxlabel = np.amax(self.gt)

        self.reverseClasses = None
        self.prepareReverse()

    ## Operators

    """
    ### Getting sample
    """
    def sample(self, location):
        return weles.Sample(
            self.signature(location),
            self.label(location))

    """
    ### Getting signature
    """
    def signature(self, location):
        return (self.image[location].astype(float) - self.normA) / self.normB

    """
    ### Getting label
    """
    def label(self, location):
        return int(np.copy(self.gt[location]))

    """
    ### Getting slice
    """
    def slice(self, band):
        return np.copy(self.image[:, :, band])

    ## Helper functions

    """
    ## Loading from .mat file
    """
    def loadMatFromTuple(self, entry):
        return scipy.io.loadmat(entry[0])[entry[1]]

    def prepareReverse(self):
        self.reverseClasses = {}
        for (x,y), value in np.ndenumerate(self.gt):
            label = self.label((x, y))
            if not label in self.reverseClasses:
                self.reverseClasses.update({label: len(self.reverseClasses)})

    """
    ## Exporting Weles dataset
    """
    def dataset(self):
        dataset = weles.Dataset()
        db_name = self.name
        source_samples = []
        self.reverseClasses = {}
        for x in xrange(self.rows):
            for y in xrange(self.cols):
                sample = self.sample((x, y))
                source_samples.append(sample)
                if not sample.label in self.reverseClasses:
                    self.reverseClasses.update({sample.label: len(self.reverseClasses)})
                sample.label = self.reverseClasses[sample.label]
        dataset.fill(
            db_name,
            source_samples,
            self.reverseClasses
        )
        print '# Classes\n%s' % self.reverseClasses
        return dataset


    """
    ## Be verbose, man
    """
    def __str__(self):
        return '%s image, %i classes, %i samples of %i bands' % (
            self.name,
            len(self.classes),
            self.rows * self.cols,
            self.bands)
