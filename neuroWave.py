import numpy as np

class NeuroWave:
    
    connectoms = []
    neurons = []

    def __init__(self, neurons, ConnectomsNames):
        self.neurons = neurons
        emptyConnectom = [[] for i in range(len(neurons))]
        for name in ConnectomsNames:
            self.connectoms += [{'name': name, 'connectom': emptyConnectom}]

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

    def setWeight(self, connectomIndex, i, j , w):
        found = -1
        indexJ = 0
        for node in self.connectoms[connectomIndex]['connectom']:
            if node!=[] and node['id'] == j:
                #print(self.connectoms[connectomIndex])
                print('adding')
                self.connectoms[connectomIndex]['connectom'][indexJ]['weight'] += w
                found = 1
                continue
            indexJ += 1
        if found == -1:
            print('creating')
            self.connectoms[connectomIndex]['connectom'] += [{'id':j, 'weight': w}]
        
    
    def test(self):
        indexI = 0
        indexJ = 0
        for i in self.neurons:
            for j in self.neurons:
                d = np.sqrt(np.sum((i-j)**2))
                if (d<1):
                    self.setWeight(2, indexI, indexJ, d)
                indexJ += 1
            indexI += 1
        print(self.connectoms)



class Izhikevich:
    def __init__(self):
        pass

class STDP:
    def __init__(self):
        pass