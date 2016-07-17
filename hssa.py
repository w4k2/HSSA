#!/usr/bin/env python

import scipy.io
import numpy as np
hs = scipy.io.loadmat('data/SalinasA.mat')
hs_gt = scipy.io.loadmat('data/SalinasA_gt')

image = hs['salinasA_corrected']
gt = hs_gt['salinasA_gt']

length = np.shape(image)[2]

labels = np.max(gt) + 1
signatures = []
for label in xrange(0,labels):
	stack = []
	for x, row in enumerate(gt):
		for y, value in enumerate(row):
			if value == label:
				stack.append(image[x][y])
	if len(stack) != 0:
		signature = np.mean(stack,0)
		signatures.append(signature)
	
width = np.shape(signatures)[1]
count = np.shape(signatures)[0]

for i in xrange(0,width):
	row = str(i)
	for j in xrange(0,count):
		row += ", %i" % signatures[j][i]
	print row