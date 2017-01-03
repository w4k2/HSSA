from hssa import *

import numpy as np


def blue():
    return "\033[92m"


def endcolor():
    return '\033[0m'


def test_loading():
    """Is image loading?"""
    hs = HS(
        ('data/SalinasA.mat', 'salinasA_corrected'),
        ('data/SalinasA_gt', 'salinasA_gt'))
    assert 1 == 1

def test_signature():
    """Do we receive signatures?"""
    hs = HS(
        ('data/SalinasA.mat', 'salinasA_corrected'),
        ('data/SalinasA_gt', 'salinasA_gt'))
    signature = hs.signature(10,10)
    assert len(signature) == hs.bands
