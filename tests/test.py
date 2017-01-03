from hssa import HSSA

import numpy as np


def blue():
    return "\033[92m"


def endcolor():
    return '\033[0m'


def test_hssa():
    hssa = HSSA(
        ('data/SalinasA.mat', 'salinasA_corrected'),
        ('data/SalinasA_gt', 'salinasA_gt'))
    assert 1 == 1
