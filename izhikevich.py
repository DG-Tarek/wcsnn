from math import ldexp
from math import log
from types import resolve_bases
import numpy as np
import pickle
import random
from matplotlib import pyplot as plt
from dictionary import getSerialNumber as get_serial_number 
import time


# Binary Search https://runestone.academy/runestone/books/published/pythonds/SortSearch/TheBinarySearch.html .
def isInList(list,target):
    #Binary Search 
    left = 0
    right = len(list) - 1
    while left <= right:
        mid = (left + right) // 2
        if target == list[mid]:
            return mid 
        elif target < list[mid]:
            right =  mid - 1
        else:
            left = mid + 1
    return -1



# Read roots from roots pickle file .
def read_roots_file():
    roots_path="roots.pkl"
    try:
        open_file = open(roots_path, "rb")
        roots = pickle.load(open_file)
        open_file.close()
        return np.array(roots)
    except :
        print(" System -> Downloading roots failed!")

def read_comments_file(comments_path):
    open_file = open(comments_path, "rb")
    comments = np.array(pickle.load(open_file))
    open_file.close()
    return comments


class izhikevich:
    def __init__(self,network_path):
        self.network_path = network_path
        self.NETWORK = self.read_network_file()
        #izhikevich
        self.Ne = len(self.NETWORK)#*100//100
        #self.Ni = len(self.NETWORK)-self.Ne
        self.I = np.zeros((self.Ne))#+self.Ni))
        #self.re = np.random.rand(self.Ne) 
        #self.ri = np.random.rand(self.Ni)

        self.a = np.concatenate([0.02*np.ones(self.Ne)])#, 0.02*self.ri]);
        self.b = np.concatenate([0.2*np.ones(self.Ne)])#, 0.2*self.ri]);
        self.c = np.concatenate([-65*np.ones(self.Ne)])#, -65*np.ones(self.Ni)]);
        self.d = np.concatenate([8*np.ones(self.Ne)])#, 8*np.ones(self.Ni)])
        self.v = -65*np.ones(self.Ne)#+self.Ni)
        self.u = self.b * self.v
        self.Tmax = 1000
        self.fired =[]
        self.tabo= []
        self.waveActivation=[]
        self.buffer = []
        for i in range(30):
            self.buffer += [[]]
        self.score=0
        
        
    def reset(self):
        self.v = -65*np.ones(self.Ne)#+self.Ni)
        self.u = self.b * self.v
        self.I = np.zeros((self.Ne))
        self.fired =[]
        self.tabo= []
        self.waveActivation=[]
        self.buffer = []
        for i in range(30):
            self.buffer += [[]]
        self.score=0


    # Read network from network pickle file .
    def read_network_file(self):
        try:
            network = []
            open_file = open(self.network_path, "rb")
            file = pickle.load(open_file)
            open_file.close()
            for line in file :
                network+=[line]
            return network    
        except :
            print(" System -> Downloading network failed!") 
        


    def _I(self):
        for f in self.fired :
            for neighbor in self.NETWORK[f]:
                self.I[neighbor[0]]+=neighbor[1]
        self.buffer = self.buffer + [self.fired]
        currentHead = self.buffer[0]
        self.buffer.pop(0)
        self.tabo += currentHead
        self.tabo.sort()
       


    def show(self):
        lissedWaveActivation = []
        window = 10
        for i in range(len(self.waveActivation)-window):
            lissedWaveActivation += [np.average(self.waveActivation[i:i+10])]

        self.score = np.sum(lissedWaveActivation)
        print('\n'+self.network_path+' '+str(np.sum(lissedWaveActivation))+'\n')
        plt.plot(lissedWaveActivation)
        plt.show()
   

   
    def activate(self,serial_number):
        for t in range(self.Tmax):
            if t==0:
                self.reset()
            #self.I=np.zeros((self.Ne))#+self.Ni))
            self.I = 0 * (self.I>=10) + self.I * (self.I<10)
            self.fired  = np.where(self.v>30)[0]
            self.fired = [f for f in self.fired if isInList(self.tabo,f)==-1]
            self.waveActivation += [len(self.fired)]
            self._I()
            
            self.v = self.v * (self.v<30) + self.c * (self.v>=30)
            self.u = self.u * (self.v<30) + (self.u+self.d) * (self.v>=30)

            if t<9:
                for number in serial_number:
                    self.I[number]=10 


            dt=0.2
            #self.I = 6 * (self.I>=6) + self.I * (self.I<6)
            self.v = self.v + dt * (0.04 * np.power(self.v,2) + 5 * self.v + 140 - self.u + self.I);
            self.u = self.u + self.a * (self.b * self.v - self.u);

            #self.v[self.tabo]=0;
            #self.I[self.tabo]=0

        self.show()
        return self.score

        
    


if __name__ == "__main__":
    if False : 
        ROOTS=read_roots_file()
        text=get_serial_number(text=" mabrouk yoyo bahri challah bel hne,",roots=ROOTS)
        print('\nText ROOTS:\n')
      
        print('\n'+str(text))
        start =time.time()
        positive_network = izhikevich(network_path='negative_network.pkl')
        positive_network.activate(text)
        print(f"Runtime  is : {time.time() - start}")


    if True:
        N=5
        pos_res =0
        neg_res=0

        positive_comments = read_comments_file('positive_comments.pkl')
        negative_comments = read_comments_file('negative_comments.pkl')
        
        positive_network = izhikevich(network_path='positive_network.pkl')    
        negative_network = izhikevich(network_path='negative_network.pkl')

        pos_list=random.sample(range(0, len(positive_comments)), N)
        neg_list=random.sample(range(0, len(negative_comments)-4500), N)
        print(pos_list)
        print(neg_list)
        i =0
        for c in pos_list:
            comment =positive_comments[c]
            if positive_network.activate(comment)>negative_network.activate(comment):
                pos_res +=1
                print('positive')
            i+=1
            print(i)
            if i ==N:break 
            

        i=0
        for c in neg_list:
            comment =negative_comments[c]
            if negative_network.activate(comment)>positive_network.activate(comment):
                neg_res +=1
                print('negative')
            i+=1
            print(i)
            if i ==N:break 

        
        print('positive :' +str((pos_res*100)/N)+'%')
        print('negative :' +str((neg_res*100)/N)+'%')
        
        
    
        
