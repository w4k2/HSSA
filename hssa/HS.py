# -*- coding: utf-8 -*-
import scipy.io
import numpy as np
import weles

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

        # Getting in shape.
        shape = np.shape(self.image)
        self.rows = shape[0]
        self.cols = shape[1]
        self.bands = shape[2]

        # Searching for maximum value
        self.max = np.amax(self.image)

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
        return np.copy(self.image[location])

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

    """
    ## Exporting Weles dataset
    """
    def dataset(self):
        dataset = weles.Dataset()
        db_name = self.name
        source_samples = []
        classes = {}
        for x in xrange(self.rows):
            for y in xrange(self.cols):
                sample = self.sample((x, y))
                source_samples.append(sample)
                if not sample.label in classes:
                    classes.update({sample.label: len(classes)})
                sample.label = classes[sample.label]
        dataset.fill(db_name, source_samples, classes)
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
