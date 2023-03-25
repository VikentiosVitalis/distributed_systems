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
    s = [line.split() for line in f.readlines()]
thr5 = []
for i in range(6):
    thr5.append(float(s[1+i][2])/float(s[1+i][0]))
thr10 = []
for i in range(6):
    thr10.append(float(s[8+i][2])/float(s[8+i][0]))
plt.figure()
plt.plot([1, 5, 10], thr5[:3], label='d=4,n=5')
plt.plot([1, 5, 10], thr5[3:], label='d=5,n=5')

plt.plot([1, 5, 10], thr10[:3], label='d=4,n=10')
plt.plot([1, 5, 10], thr10[3:], label='d=5,n=10')

plt.savefig('plots/throughput10.pdf')
