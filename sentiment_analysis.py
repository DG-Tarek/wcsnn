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
# Testing modify
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


class SentimentAnalysis:
    def __init__(self,first_net_path,second_net_path):

        self.first_network = self.read_network_file(first_net_path)
        self.second_network = self.read_network_file(second_net_path)

        #izhikevich
        self.Ne = max(len(self.first_network),len(self.second_network))
        self.I = np.zeros((self.Ne))
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
        for i in range(50):
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
        for i in range(35):
            self.buffer += [[]]
        self.score=0


    # Read network from network pickle file .
    def read_network_file(self,path):
        try:
            network = []
            open_file = open(path, "rb")
            file = pickle.load(open_file)
            open_file.close()
            for line in file :
                network+=[line]
            return network    
        except :
            print(" System -> Downloading network failed!") 
        


    def _I(self):
        for f in self.fired :
            for neighbor in self.first_network[f]:
                if self.neuron_fitness(self.first_network,neighbor[0])>=self.neuron_fitness(self.second_network,neighbor[0]) or self.doubt():
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
        print(str(np.sum(lissedWaveActivation)))
        #plt.plot(lissedWaveActivation)
        #plt.show()
   

    def neuron_fitness(self,network,neuron):
        if len(network[neuron])>0:
            return network[neuron][-1][0]*1+network[neuron][-1][1]*1.2

        else:
            return 0
       
    

    def doubt(self):
        if random.random() < 0.075 :
            return True
        else:
            return False


    def activate(self,serial_number):
        for t in range(self.Tmax):
            if t==0:
                self.reset()
            
            self.I = 0 * (self.I>=10) + self.I * (self.I<10)
            self.fired  = np.where(self.v>30)[0]
            self.fired = [f for f in self.fired if isInList(self.tabo,f)==-1]
            self.waveActivation += [len(self.fired)]
            self._I()
            
            self.v = self.v * (self.v<30) + self.c * (self.v>=30)
            self.u = self.u * (self.v<30) + (self.u+self.d) * (self.v>=30)

            if t<15:
                for number in serial_number:
                    if self.neuron_fitness(self.first_network,number)>self.neuron_fitness(self.second_network,number) or self.doubt():
                        self.I[number]=15


            dt=0.1
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
        N=100
        pos_res =0
        neg_res=0

        positive_comments = read_comments_file('positive_comments.pkl')
        negative_comments = read_comments_file('negative_comments.pkl')
        
        positive_network = SentimentAnalysis(first_net_path='positive_network.pkl',second_net_path='negative_network.pkl')    
        negative_network = SentimentAnalysis(first_net_path='negative_network.pkl',second_net_path='positive_network.pkl')

        pos_list=random.sample(range(0, len(positive_comments)), N)
        neg_list=random.sample(range(0, len(negative_comments)-4500), N)
        print(pos_list)
        print(neg_list)
        pp=0
        nn=0
        i=0
        for c in pos_list:
            print('\ncomment '+str(i)+' :'+'\n')
            i+=1
            comment =positive_comments[c]
            p=positive_network.activate(comment)
            n=negative_network.activate(comment)
            if p>n:
                pos_res +=1
                print('positive')
                if p < 10:
                    pp+=1

            

        i = 0
        for c in neg_list:
            print('\ncomment '+str(i)+' :'+'\n')
            i+=1
            comment =negative_comments[c]
            n=negative_network.activate(comment)
            p=positive_network.activate(comment)   
            if n>p:
                neg_res +=1
                print('negative')
                if n <10:
                    nn+=1


        
        print('positive :' +str((pos_res*100)/N)+'%  ,  '+str(pp))
        print('negative :' +str((neg_res*100)/N)+'%  ,  '+str(nn))
        
        
    
        
