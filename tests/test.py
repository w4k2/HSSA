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
    print hs
    assert 1 == 1

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
    print np.shape(signatures)
