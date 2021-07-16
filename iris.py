from neuroWave import NeuroWave
from visualisation import Visualisation
from random import shuffle
import numpy as np


def format(e):
    return [float(e[0]),float(e[1]),float(e[2]),float(e[3]),e[4][0:-1]]
irisFile = open('iris.data','r')
lines = irisFile.readlines()

data = [[],[],[]]
indexes = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica':2}
for i in lines[:-1]:    
    entry = format(i.split(','))
    print(entry)
    data[indexes[entry[4]]] += [entry]

#print(data)
dim = 4
u = np.zeros(dim)
s = np.zeros(dim)

for d in range(dim):
    dimValues = [j[d] for i in data for j in i]
    u[d] = sum(dimValues)/len(dimValues)

for d in range(dim):
    dimValues = [(j[d]-u[d])**2 for i in data for j in i]
    s[d] = np.sqrt(sum(dimValues)/len(dimValues))

print(u)
print(s)

nNeurons = 10
neurons = np.zeros((nNeurons, dim))

for d in range(dim):
    n = np.random.normal(u[d], s[d], nNeurons) 
    neurons[:,d]=n

print(neurons)

brain = NeuroWave(neurons, ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
brain.test()


"""
epochs = 100
for epoch in range(epochs):
    for i in range(3):
        shuffle(data[i])
        brain.train(indexes[i], data[i])
"""
#print(brain.connectoms)
