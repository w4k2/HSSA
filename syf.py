def bordersMap(self, source = None, filter = None):
      if filter is None:
          filter = self.filter
      if not source:
          source = self.edges3

      filteredEdges = source[:,:,filter]

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

      edgesMask = np.zeros(np.shape(source)).astype(bool)
      lvi = source > np.percentile(source, percentile)
      edgesMask[lvi] = True
      edgesMask = morphology.dilation(edgesMask, square(3))
      edgesMask = morphology.skeletonize(edgesMask)
      edgesMask = morphology.dilation(edgesMask, square(3))
      edgesMask = morphology.binary_closing(edgesMask)
      edgesMask = morphology.dilation(edgesMask, square(3))
      edgesMask = morphology.skeletonize(edgesMask)
      #edgesMask = morphology.remove_small_objects(edgesMask, min_size = 25, connectivity = 1)
      edgesMask = morphology.dilation(edgesMask, square(3))
      return edgesMask.astype(bool)
