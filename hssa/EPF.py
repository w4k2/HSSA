# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp

"""
## Entropodynamic Percentyle Filter
"""
class EPF:
    def __init__(self, hs, ksize, percentile):
        self.hs = hs
        self.ksize = ksize
        self.percentile = percentile

        # Kostka graniczna
        self.edges3 = self.edges3(self.ksize)

        # Filtr
        epf = self.epf(self.edges3, percentile)

        self.entropy = epf[0]
        self.meanEntropy = epf[1]
        self.entropyDynamics = epf[2]
        self.meanDynamics = epf[3]

        self.filter = epf[4]

    def __str__(self):
        return "EPF on %s image, k = %s, p = %i (%i / %i)" % (
            self.hs.name,
            self.ksize,
            self.percentile,
            sum(self.filter),
            self.hs.bands
        )

    def edges3(self, ksize):
        edges3 = np.zeros(np.shape(self.hs.image))
        for sid in xrange(self.hs.bands):
            # Gather slice
            slice = self.hs.slice(sid)

            # Assign
            edges3[:,:,sid] = self.edges2(slice, ksize)

        return edges3

    def edges2(self, map, ksize, margins = 20):
        # Establish tensor
        tensor = self.dynamicsTensor(map, ksize)

        # Calculate denivelation
        edges2 = np.subtract(
            np.percentile(tensor, 100 - margins, axis=2),
            np.percentile(tensor, margins, axis=2)
        )

        # Normalization
        a = np.min(edges2)
        b = np.max(edges2)
        edges2 = np.divide(np.subtract(edges2, a), b - a)

        return edges2

    def dynamicsTensor(self, slice, ksize):
        layers = ksize[0] * ksize[1]
        tensor = np.zeros((self.hs.rows, self.hs.cols, layers))
        i = 0

        # Moving Spermatozoid
        for x in xrange(ksize[0]):
            for y in xrange(ksize[1]):
                kernel = np.zeros(ksize)
                kernel[x,y] = 1.

                smoothed = sp.ndimage.convolve(
                    slice,
                    kernel,
                    mode='reflect',
                    cval=0.0
                )
                tensor[:,:,i] = smoothed
                i += 1

        return tensor

    def epf(self, edges3, percentile):
        # Calculate entropy
        pert = np.percentile(
            np.percentile(
                edges3, percentile, axis = 0),
            percentile, axis = 0)

        bert = np.median(np.median(edges3, axis = 0))

        entropy = np.absolute(np.subtract(pert, bert))
        entropy = np.absolute(
            np.subtract(
                entropy, np.median(entropy)))

        # mean entropy filter
        mef = entropy < np.percentile(entropy, percentile)
        meanEntropy = np.zeros(len(entropy))
        meanEntropy[mef] = True

        # Entropy dynamics
        entropyDynamics = np.copy(entropy)
        val = entropyDynamics[0]
        entropyDynamics = np.delete(entropyDynamics, 0)
        entropyDynamics = np.append(entropyDynamics, entropyDynamics[-1])
        entropyDynamics = np.subtract(entropy, entropyDynamics)
        entropyDynamics = np.absolute(entropyDynamics)

        # Mean dynamics filter
        med = entropyDynamics < np.percentile(entropyDynamics, percentile)
        meanDynamics = np.zeros(len(entropy))
        meanDynamics[med] = True

        # Union filter
        union = [a and b for a,b in zip(meanEntropy, meanDynamics)]

        return (entropy, meanEntropy, entropyDynamics, meanDynamics, union)

    def bordersMap(self, source = None, filter = None):
        if not filter:
            filter = self.filter
        if not source:
            source = self.edges3

        filteredEdges = np.squeeze(source[:,:,np.where(filter)])

        bordersMap = np.max(filteredEdges, 2)
        bordersMap = sp.ndimage.median_filter(
            bordersMap,
            size=(2, 2)
        )
        bordersMap = sp.ndimage.grey_dilation(bordersMap, size=(3,3))
        return bordersMap

    def bordersMask(self, source = None, filter = None, percentile = None):
        if not filter:
            filter = self.filter
        if not source:
            source = self.bordersMap(filter = filter)
        if not percentile:
            percentile = self.percentile

        edgesMask = np.zeros(np.shape(source))
        lvi = source > np.percentile(source, percentile)
        edgesMask[lvi] = True
        struct2 = sp.ndimage.generate_binary_structure(2, 1)
        edgesMask = sp.ndimage.binary_dilation(edgesMask, structure = struct2)
        return edgesMask.astype(bool)
