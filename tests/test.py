from hssa import *

import csv
import numpy as np
import json


def blue():
    return "\033[92m"


def endcolor():
    return '\033[0m'


def loadImage():
    with open('salinasA.json') as data_file:
        dictionary = json.load(data_file)

    return HS(dictionary)


def test_loading():
    """Is image loading?"""
    hs = loadImage()
    # assert 'Salinas image, 7 classes, 111104 samples of 204 bands' == str(hs)
    assert 'Salinas A image, 7 classes, 7138 samples of 204 bands' == str(hs)


def test_signature():
    """Do we receive signatures?"""
    hs = loadImage()
    signature = hs.signature(10, 10)
    assert len(signature) == hs.bands


def test_slice():
    """Do we receive slices?"""
    hs = loadImage()
    slice = hs.slice(10)
    assert (hs.rows, hs.cols) == np.shape(slice)

'''
def test_signatures():
    """Are we able to summary classes?"""
    hs = loadImage()
    signatures = hs.signatures()
    assert (len(hs.classes), hs.bands) == np.shape(signatures)
'''

def test_hssa_init():
    """Can we create HSSA?"""
    hs = loadImage()
    threshold = .5
    limit = 3
    hssa = HSSA(hs, threshold, limit)


def test_hssa_frame_signature():
    """Can we establish frame signature?"""
    hs = loadImage()
    threshold = .5
    limit = 3
    hssa = HSSA(hs, threshold, limit)
    frame = hssa.heterogenous[0]
    print frame
    assert len(frame.signature) == hs.bands


def test_hssa_homogeneity_measure():
    """Can we establish homogeneity measure?"""
    hs = loadImage()
    threshold = .5
    limit = 3
    hssa = HSSA(hs, threshold, limit)
    frame = hssa.heterogenous[0]
    assert frame.homogeneity > 0 and frame.homogeneity < 1


def test_is_dividing_working():
    """Can we divide a frame properly?"""
    hs = loadImage()
    threshold = .5
    limit = 3
    hssa = HSSA(hs, threshold, limit)
    frame = hssa.heterogenous[0]

    thirdStageLocations = []
    newFrames = frame.divide()
    newerFrames = []
    for frame in newFrames:
        newerFrames.extend(frame.divide())
    for frame in newerFrames:
        newestFrames = frame.divide()
        for nFrame in newestFrames:
            thirdStageLocations.append(nFrame.location)
    assert sorted(thirdStageLocations) == list(xrange(0, 64))


def test_dumb_hssa():
    """Is HSSA working?"""
    hs = loadImage()
    threshold = .98
    limit = 2
    hssa = HSSA(hs, threshold, limit)
    while not hssa.isComplete:
        hssa.step()

    assert len(hssa.homogenous) > 0 and len(hssa.heterogenous) == 0


def test_limit_hssa():
    """Is HSSA working with limits?"""
    hs = loadImage()
    threshold = .98
    limit = 4
    hssa = HSSA(hs, threshold, limit)
    hssa.process()

    assert len(hssa.homogenous) > 0 and len(hssa.heterogenous) > 0


def test_hssa_final():
    """Production!"""
    hs = loadImage()
    threshold = .995
    limit = 6
    hssa = HSSA(hs, threshold, limit)
    hssa.process()
    # hssa.image('hssa_pre.png')
    # hssa.image('hssa_pre_l.png', True)
    hssa.post()
    # hssa.image('hssa_post.png')
    # hssa.image('hssa_post_l.png', True)
    representation = hssa.representation()
    print len(representation)
    myfile = open('result.csv', 'wb')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for row in representation:
        wr.writerow(row)
