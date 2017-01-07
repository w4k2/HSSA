from hssa import *
import json

with open('pavia.json') as data_file:
    hs = HS(json.load(data_file))
threshold = .99
hssa = HSSA(hs, threshold)
while not hssa.isComplete:
    hssa.image()
    hssa.step()
hssa.image()
