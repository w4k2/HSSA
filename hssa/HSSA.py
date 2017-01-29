import scipy.io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as colors
import numpy as np

from HS import *
from HSFrame import *

"""
"**Pycco**" is a Python port of [Docco](http://jashkenas.github.com/docco/):
the original quick-and-dirty, hundred-line-long, literate-programming-style
documentation generator. It produces HTML that displays your comments
alongside your code. Comments are passed through
[Markdown](http://daringfireball.net/projects/markdown/syntax) and
[SmartyPants](http://daringfireball.net/projects/smartypants), while code is
passed through [Pygments](http://pygments.org/) for syntax highlighting.
This page is the result of running Pycco against its own source file.
If you install Pycco, you can run it from the command-line:
    pycco src/*.py
This will generate linked HTML documentation for the named source files,
saving it into a `docs` folder by default.
The [source for Pycco](https://github.com/pycco-docs/pycco) is available on GitHub,
and released under the MIT license.
To install Pycco, simply
    pip install pycco
Or, to install the latest source
    git clone git://github.com/pycco-docs/pycco.git
    cd pycco
    python setup.py install
"""

class HSSA:
    def __init__(self, hs, threshold, limit=99, cv=-1):
        # Assign image
        self.hs = hs
        # Set homogeneity threshold
        self.threshold = threshold
        # Set iteration limiter
        self.limit = limit
        # Iteration number
        self.iteration = 0
        # Is done?
        self.isComplete = False
        # segments count
        self.segments = 0

        # Initialize set of frames
        self.heterogenous = []
        self.homogenous = []
        # Set up representation
        self.clean()

    def image(self, title = False, labels = False):
        if not title:
            title = 'hssa_i%i_t%.0f.png' % (
                self.iteration,
                1000 * self.threshold)
        base = pow(2, self.iteration)
        img = np.ones((base, base, 3))
        minN = 9999
        maxN = 0
        for frame in self.heterogenous + self.homogenous:
            if frame.intensity < minN:
                minN = frame.intensity
            if frame.intensity > maxN:
                maxN = frame.intensity

        # Hetero
        for frame in self.heterogenous + self.homogenous:
            amount = pow(2, frame.fold)
            length = base / amount
            intensity = (frame.intensity - minN) / (maxN - minN)
            intensity = .25 + intensity / 2
            hue = 0
            if frame.isHomo:
                if labels:
                    hue = frame.label / float(2 * len(self.hs.classes))
                    if self.segments > 2 * len(self.hs.classes):
                        hue = frame.label / float(self.segments)
                else:
                    hue = frame.segment / float(2 * len(self.hs.classes))
                    if self.segments > 2 * len(self.hs.classes):
                        hue = frame.segment / float(self.segments)
            x = frame.location % amount
            y = frame.location / amount
            for i in xrange(length):
                for j in xrange(length):
                    if frame.isHomo:
                        img[length * x + i, length * y + j] = \
                            colors.hsv_to_rgb([hue, 1, .5 + intensity / 2])
                    else:
                        img[length * x + i, length * y + j] = \
                            colors.hsv_to_rgb([0, 0, intensity])

        imgplot = plt.imshow(img, interpolation="nearest")
        plt.savefig(title)

    def process(self):
        while not self.isComplete:
            if self.iteration == self.limit:
                break
            self.step()

    def split(self):
        # Splitting
        self.homogenous.extend(
            [x for x in self.heterogenous if x.homogeneity > self.threshold])
        self.heterogenous = \
            [x for x in self.heterogenous if x.homogeneity <= self.threshold]

    def merge(self):
        for i in xrange(len(self.homogenous)):
            frame = self.homogenous[i]
            if frame.segment == -1:
                for j in xrange(i):
                    cmpFrame = self.homogenous[j]
                    similarity = \
                        1 - (np.mean(np.std([frame.signature, cmpFrame.signature], axis=0)) / self.hs.max)
                    if similarity > self.threshold:
                        frame.segment = cmpFrame.segment
                        break
                if frame.segment == -1:
                    frame.segment = self.segments
                    self.segments += 1

    def post(self):
        for segment in xrange(self.segments):
            labels = []
            for frame in self.homogenous:
                if frame.segment == segment:
                    # print "%s - %i" % (frame, frame.label)
                    labels.append(frame.label)
            label = max(set(labels), key=labels.count)
            for frame in self.homogenous:
                if frame.segment == segment:
                    frame.label = label
        # Removing the background
        self.heterogenous = []
        self.homogenous = \
            [x for x in self.homogenous if x.label != 0]

    def representation(self):
        result = []
        for frame in self.homogenous:
            # print frame
            multiplier = self.iteration - frame.fold - 1
            units = pow(2, multiplier * 2)
            # print 'multiplier %i' % multiplier
            # print '%i units' % units
            for signature in frame.signatures(units):
                line = [frame.label]
                line.extend(signature)
                result.append(line)
        return result

    def step(self):
        self.iteration += 1
        self.split()
        self.merge()
        for frame in self.homogenous:
            frame.setHomo()
        self.isComplete = len(self.heterogenous) == 0

        # Breaking hetero
        newHeterogenous = []
        for frame in self.heterogenous:
            newHeterogenous.extend(frame.divide())
        self.heterogenous = newHeterogenous

    def clean(self):
        self.iteration = 0
        self.heterogenous = [HSFrame(self.hs)]
        self.homogenous = []
        self.isComplete = False
