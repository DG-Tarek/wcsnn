import numpy as np
from copy import deepcopy

class NeuroWave:
    
    connectoms = []
    neurons = []

    def __init__(self, neurons, ConnectomsNames):
        self.neurons = neurons
        emptyConnectom = [[] for i in range(len(neurons))]
        self.connectoms = {k:[] for k in ConnectomsNames}
        for name in ConnectomsNames:
            self.connectoms[name] = deepcopy(emptyConnectom)
        print(self.connectoms)

    def loadNeurons(self):
        pass

    def getNearestNeuron(self, x):
        index = 0
        minIndex = 0
        minDistance = 100000000000000
        for i in self.neurons:
            d = np.sqrt(sum((x-i)**2))
            if d<minDistance:
                minDistance = d
                minIndex = index
            index += 1
        return minIndex

    def train(self, connectom, serie):
        pass

    def propagate(self):
        pass

    def setWeight(self, connectomName, i, j , w):
        found = -1
        indexJ = 0
        connectom = []
        connectom = self.connectoms[connectomName]
        
        for node in connectom[i]:
            if node!=[] and node['id'] == j:
                #print('adding')
                connectom[i][indexJ]['weight'] += w
                found = 1
                continue
            indexJ += 1

        if found == -1:
            #print('creating')
            connectom[i] += [{'id':j, 'weight': w}]
        
        self.connectoms[connectomName] = connectom
        
    
    def test(self, neuron):
        i = neuron[0]
        prec = self.getNearestNeuron(i)
        for j in neuron[1:]:
            bestIndex = self.getNearestNeuron(j)
            self.setWeight('Iris-setosa', prec, bestIndex, 1)
            prec = bestIndex
        
        #for i in self.connectoms['Iris-setosa']:
        #    print(len(i))        


class Izhikevich:
    def __init__(self):
        pass

class STDP:
    def __init__(self):
        pass