import matplotlib.pyplot as plt
import numpy as np

diff = ['4','5']
size = ['1', '5', '10']
nodes = ['5', '10']

tt = []
for d in diff:
    tt.append([])
    for s in size:
        tt[-1].append([])
        for n in nodes:
            with open(f'times/mining{d}{s}{n}.txt') as f:
                tt[-1][-1].append(f.readlines())
print(tt)