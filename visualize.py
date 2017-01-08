#!/usr/bin/env python
from hssa import *
import json

with open('salinas.json') as data_file:
    hs = HS(json.load(data_file))
threshold = .995
limit = 6
hssa = HSSA(hs, threshold, limit)
hssa.process()
hssa.image('hssa_0_background')
hssa.post()
hssa.image('hssa_1_no_background')
hssa.image('hssa_2_labels.png', True)
