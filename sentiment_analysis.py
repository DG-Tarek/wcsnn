# Last edit : Friday 14/09/2021.
# Created on Python 3.9(64bit).
# tarek.dg.dz@gmail.com


from math import ldexp
from math import log
from types import resolve_bases
import numpy as np
import pickle
import random
from matplotlib import pyplot as plt
from dictionary import getSerialNumber as get_serial_number 
import time
import threading


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


class SentimentAnalysis:
    def __init__(self,first_net_path,second_net_path):
        
        self.first_network = self.read_network_file(first_net_path)
        self.second_network = self.read_network_file(second_net_path)

        #izhikevich
        self.Ne = max(len(self.first_network),len(self.second_network))
        self.I = np.zeros((self.Ne))
        self.a = np.concatenate([0.02*np.ones(self.Ne)])
        self.b = np.concatenate([0.2*np.ones(self.Ne)])
        self.c = np.concatenate([-65*np.ones(self.Ne)])
        self.d = np.concatenate([8*np.ones(self.Ne)])
        self.v = -65*np.ones(self.Ne)
        self.u = self.b * self.v
        
        self.Tmax = 500
        self.fired =[]
        self.tabo= []
        self.waveActivation=[]
        self.buffer = []
        for i in range(30):
            self.buffer += [[]]
        self.score=0
        
    # Recoveryr estore defaults parameters of connectome.
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
        

    # wave propagation.
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
       

    # wave propagation wave.
    def show(self):
        lissedWaveActivation = []
        window = 10
        for i in range(len(self.waveActivation)-window):
            lissedWaveActivation += [np.average(self.waveActivation[i:i+10])]
        self.score = np.sum(lissedWaveActivation)
        
        #plt.plot(lissedWaveActivation)
        #plt.show()
   
    # get neuron fitness.
    def neuron_fitness(self,network,neuron):
        if len(network[neuron])>0:
            return network[neuron][-1][0]*1.05+network[neuron][-1][1]*1.2
        else:
            return 0
       
    
    # doubt rate before neuron activation .
    def doubt(self):
        return random.random() < 0.075 


    # activate the connectome over a period of time (Tmax).
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
            self.u = self.u + dt * (self.a * (self.b * self.v - self.u));

            #self.v[self.tabo]=0;
            #self.I[self.tabo]=0

        self.show()
        return self.score

                

    


if __name__ == "__main__":
    if True : 

        # comment=("bravo koulchi mbrouk alikem  :3 .") This is just an example .
        # Enter your comment and get the result.
        # Enjoy it (^_^) .

        # negative connectome.
        def negative_connectome(text):
            start = time.time()
            print('Negative connectome score: '+str(int(NEGATIVE.activate(text))))
            print('Negative connectome run time: '+str(time.time()-start)+'\n')

        # positive connectome. 
        def positive_connectome(text):
            start=time.time()
            print('Positive connectome score: '+str(int(POSITIVE.activate(text))))
            print('Positive connectome run time: '+str(time.time()-start)+'\n')


        ROOTS=read_roots_file()
        # create positive connectome.
        POSITIVE = SentimentAnalysis(first_net_path='positive_network.pkl',second_net_path='negative_network.pkl') 
        # create negative connectome.
        NEGATIVE = SentimentAnalysis(first_net_path='negative_network.pkl',second_net_path='positive_network.pkl')


        # Enter your comment here comment = ......... 
        comment=("bravo koulchi mbrouk alikem  :3 .")
        print('\nYour comment "'+comment+'"\n')
        comment_serial_number=get_serial_number(text=comment,roots=ROOTS)

        # The comment belongs to the connectome with the highest score.
        pos_thr = threading.Thread(target=positive_connectome, args=(comment_serial_number,))
        pos_thr.start()
        neg_thr = threading.Thread(target=negative_connectome, args=(comment_serial_number,))
        neg_thr.start()


   