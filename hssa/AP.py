# -*- coding: utf-8 -*-

class AP:
    def __init__(self, img, ksize, reductor):
        self.img = img
        self.ksize = ksize
        self.reductor = reductor

        # Kostka graniczna
        self.edges3d = img.edges3d(ksize)

        # Filtr
        edgesFilter = img.edgesFilter(self.edges3d, reductor)

        self.entropy = edgesFilter[0]
        self.meanEntropy = edgesFilter[1]
        self.entropyDynamics = edgesFilter[2]
        self.meanDynamics = edgesFilter[3]

        self.filter = edgesFilter[4]

    def edgesFlat(self, filter = None):
        if not filter:
            filter = self.filter

        edgesFlat = self.img.edgesFlat(self.edges3d, filter)
        return edgesFlat

    def edgesMask(self, filter = None):
        if not filter:
            filter = self.filter

        edgesFlat = self.edgesFlat(filter)
        edgesMask = self.img.edgesMask(edgesFlat)

        return edgesMask
