import matplotlib.pyplot as plt
import numpy as np

diff = ['4', '5']
size = ['1', '5', '10']
nodes = ['5', '10']

t5 = []
t10 = []
for d in diff:
    t5.append([])
    t10.append([])
    for s in size:
        with open(f'times/mining{d}{s}5.txt') as f:
            t5[-1].append(np.average([float(x[:-1]) for x in f.readlines()]))
        with open(f'times/mining{d}{s}10.txt') as f:
            t10[-1].append(np.average([float(x[:-1]) for x in f.readlines()]))
        

print(t5)

print(t10)
plt.figure()
plt.plot([1, 5, 10], t5[0])
plt.plot([1, 5, 10], t10[0])
plt.ylabel("Time taken")
plt.title('Block mine times for difficulty 4')
plt.savefig('plots/plot4.pdf')
plt.figure()
plt.plot([1, 5, 10], t5[1])
plt.plot([1, 5, 10], t10[1])
plt.title('Time taken')
plt.title('Block mine times for difficulty 5')
plt.savefig('plots/plot5.pdf')


with open('times/time_total.txt') as f:
    s = f.readlines()