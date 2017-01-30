# Tests for HSSA.
import hssa
import weles
import csv
import numpy as np
import json

imagesDirectory = 'data/hsimages/'


def blue():
    return "\033[92m"


def endcolor():
    return '\033[0m'


def loadImage():
    with open('%s%s' % (imagesDirectory, 'salinasA.json')) as data_file:
        dictionary = json.load(data_file)

    return hssa.HS(dictionary)


def test_loading():
    """Is image loading?"""
    hs = loadImage()
    # assert 'Salinas image, 7 classes, 111104 samples of 204 bands' == str(hs)
    assert 'Salinas A image, 7 classes, 7138 samples of 204 bands' == str(hs)


def test_signature():
    """Do we receive signatures?"""
    hs = loadImage()
    location = (10, 10)
    signature = hs.signature(location)
    assert len(signature) == hs.bands


def test_slice():
    """Do we receive slices?"""
    hs = loadImage()
    slice = hs.slice(10)
    assert (hs.rows, hs.cols) == np.shape(slice)


def test_hssa_init():
    """Can we create HSSA?"""
    hs = loadImage()
    threshold = .5
    limit = 3
    hssa.HSSA(hs, threshold, limit)


def test_hssa_frame_signature():
    """Can we establish frame signature?"""
    hs = loadImage()
    threshold = .5
    limit = 3
    sgm = hssa.HSSA(hs, threshold, limit)
    frame = sgm.heterogenous[0]
    print frame
    assert len(frame.signature) == hs.bands


def test_hssa_homogeneity_measure():
    """Can we establish homogeneity measure?"""
    hs = loadImage()
    threshold = .5
    limit = 3
    sgm = hssa.HSSA(hs, threshold, limit)
    frame = sgm.heterogenous[0]
    assert frame.homogeneity > 0 and frame.homogeneity < 1


def test_is_dividing_working():
    """Can we divide a frame properly?"""
    hs = loadImage()
    threshold = .5
    limit = 3
    sgm = hssa.HSSA(hs, threshold, limit)
    frame = sgm.heterogenous[0]

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
    jthreshold = .98
    limit = 2
    sgm = hssa.HSSA(hs, threshold, jthreshold, limit)
    while not sgm.isComplete:
        sgm.step()

    assert len(sgm.homogenous) > 0 and len(sgm.heterogenous) == 0


def test_limit_hssa():
    """Is HSSA working with limits?"""
    hs = loadImage()
    threshold = .98
    jthreshold = .98
    limit = 4
    sgm = hssa.HSSA(hs, threshold, jthreshold, limit)
    sgm.process()

    assert len(sgm.homogenous) > 0 and len(sgm.heterogenous) > 0


def test_hssa_final():
    """Production!"""
    hs = loadImage()
    threshold = .995
    jthreshold = .995
    limit = 6
    sgm = hssa.HSSA(hs, threshold, jthreshold, limit)
    sgm.process()
    sgm.post()
    representation = sgm.representation()
    print len(representation)
    myfile = open('result.csv', 'wb')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for row in representation:
        wr.writerow(row)

def test_weles_pass():
    """Passing image as dataset to Weles!"""
    img = loadImage()
    dataset = img.dataset()
    configuration = {
        'k': 20
    }
    clf = weles.sklKNN(dataset, configuration).quickLoop()
    print clf
    clf = weles.sklDTC(dataset, configuration).quickLoop()
    print clf
    clf = weles.sklMLP(dataset, configuration).quickLoop()
    print clf
