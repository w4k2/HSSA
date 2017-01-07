from hssa import *
import json

with open('salinas.json') as data_file:
    hs = HS(json.load(data_file))
threshold = .995
hssa = HSSA(hs, threshold)
while not hssa.isComplete:
    hssa.image()
    hssa.step()
hssa.image()
