# -*- coding: utf-8 -*-

class AP:
    def __init__(self, img, ksize, percentile):
        self.img = img
        self.ksize = ksize
        self.percentile = percentile

        # Kostka graniczna
        self.edges3d = img.edges3d(ksize)

        # Filtr
        epf = img.epf(self.edges3d, percentile)

        self.entropy = epf[0]
        self.meanEntropy = epf[1]
        self.entropyDynamics = epf[2]
        self.meanDynamics = epf[3]

        self.filter = epf[4]

    def bordersMap(self, filter = None):
        if not filter:
            filter = self.filter
        bordersMap = self.img.bordersMap(self.edges3d, filter)
        return bordersMap

    def bordersMask(self, filter = None, percentile = 75):
        if not filter:
            filter = self.filter
        bordersMask = self.img.bordersMask(self.bordersMap(filter), percentile)
        return bordersMask
