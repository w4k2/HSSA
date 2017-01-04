from hssa import *

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
    assert 'Salinas A image, 7 classes, 7138 samples of 204 bands' == str(hs)

def test_signature():
    """Do we receive signatures?"""
    hs = loadImage()
    signature = hs.signature(10,10)
    assert len(signature) == hs.bands

def test_slice():
    """Do we receive slices?"""
    hs = loadImage()
    slice = hs.slice(10)
    assert (hs.rows, hs.cols) == np.shape(slice)

def test_signatures():
    """Are we able to summary classes?"""
    hs = loadImage()
    signatures = hs.signatures()
    assert (len(hs.classes), hs.bands) == np.shape(signatures)

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
    assert len(frame.signature) == hs.bands
