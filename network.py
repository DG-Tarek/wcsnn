# Last edit : Friday 06/24/2021.
# Created on Python 3.9(64bit).

from os import RTLD_NODELETE
import numpy as np # already exist in library .
import time # already exist in library .
import pickle # already exist in library .
import math # already exist in library .
from dictionary import getSerialNumber as get_serial_number


# The pickle module implements binary protocols for serializing and de-serializing a Python object structure.

# Binary Search https://runestone.academy/runestone/books/published/pythonds/SortSearch/TheBinarySearch.html.

# class Network : - Creating a network from learning pre-sorted comments (Serial numbers) and returun a network pickle file.
            
        # Methods :
        # 1 def read_roots_file(self): -> Read roots from a roots pickle file .
        # 2 def read_network_file(self): -> Read network from a network pickle file .
        # 3 def write_network(self): -> Write network pickle file (save as Matrix (in binary)).
        # 4 def create_neuron(self,neuron): -> Creating a neuron with a 0 weight .
        # 5 def add_neighbor(self,neuron,neighbor): -> add a neuron as a neighbor to the list of neighbors .
        # 6 def isNeighbor(self,neuron,neighbor): -> return index if this neuron is a neighbor.
        # 7 def getWeight(self,neuron,neighbor): -> get weight value between neuron and his neighbor.
        # 8 def setWeight(self,neuron,neighbor,weight): -> set this weight value between neuron and his neighbor.
        # 9 def stdp(self,deltaT): -> return STPD value.
        # 10 def learn_serial_number(self,serial_number): -> Learn this serial number.
        # 11 def network_info(self): -> show network informations.
        # 12 def creating_network(self): -> creating a network from learning serial numbers (Comments) .
        # 13 def standardization(self): -> standardization of weights (Normalisaion) (->log()).
        # 14 def network_total_weight(self): -> return network total weight (sum of all weights in the network).
        # 15 def get_neuron_weight(self,neuron): -> retutn the sum of weights of a neuron with its neighbor.
        # 16 def network_re(self): -> return the sum of relations between neurons and neighbors. 
        # 17 def get_max_weight(self): -> return the max weight value in this network. 
        # 18 def neurons_I(self): -> return neurons that have total_I > 3.56 . 
        # 19 def most_used_roots(self,roots,n): -> return most used roots in this network. 


def isInList(list,target):
    #Binary Search 
    left = 0
    right = len(list) - 1
    while left <= right:
        mid = (left + right) // 2
        if target == list[mid][0]:
            return mid
        elif target < list[mid][0]:
            right =  mid - 1
        else:
            left = mid + 1
    return None

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



class Network:

    def __init__(self,path,roots_path=None,network_name=None,learning=None,forbidden_roots=None):

        # path :
            # if creating a network : (path:str) comments pickle file path .
            # if reading a network from a network pickle file : (path:str) network pickle file path .
        # roots_path : 
            # if creating a network :(path:str) roots pickle file path .
            # if reading a network from a network pickle file : None .
        # network_name : 
            # if creating a network : (String) name for network pickle file will return . 
            # if reading a network from a network pickle file : None .
        # learning :
            # if creating a network : not None (True).
            # if reading a network from a network pickle file : None .
        # forbidden_roots :
            # if creating a network : text(String) contains forbidden roots .
            # if reading a network from a network pickle file : None .
            


        if learning is not None :
            self.path = path
            self.roots_path=roots_path
            self.network_name = network_name
            self.forbidden_roots = forbidden_roots           
            self.network = []
            self.STDP=[1,0.5,0.5,0.5]
            self.ROOTS = self.read_roots_file()
            self.creating_network()
            self.standardization()
            self.write_network()
            self.network_info()
        else :
            self.path = path
            self.network = self.read_network_file()
            self.network_info()


    # Read roots from a roots pickle file .
    def read_roots_file(self):
        try:
            open_file = open(self.roots_path, "rb")
            roots = pickle.load(open_file)
            open_file.close()
            return np.array(roots)
        except :
            print(" System -> [error] Downloading roots failed ! .")

    # Read network from a network pickle file .
    def read_network_file(self):
        try:
            network = []
            print("\n\n\n System -> Start ... ")
            open_file = open(self.path, "rb")
            file = pickle.load(open_file)
            open_file.close()
            for line in file :
                network+=[line]
            return network    
        except :
            print(" System -> [error] Downloading network failed ! .")

    # Creating a neuron with a 0 weight .
    def create_neuron(self,neuron):
        return [neuron,0]
    
    # add a neuron as a neighbor to the list of neighbors .
    def add_neighbor(self,neuron,neighbor):
        self.network[neuron].append(self.create_neuron(neuron=neighbor))
        self.network[neuron].sort()

    # return index if this neuron is a neighbor.        
    def isNeighbor(self,neuron,neighbor):
        return isInList(list=self.network[neuron],target=neighbor)

    # get weight value between neuron and his neighbor.
    def getWeight(self,neuron,neighbor):
        return self.network[neuron][isInList(list=self.network[neuron],target=neighbor)][1]

    # set this weight value between neuron and his neighbor.
    def setWeight(self,neuron,neighbor,weight):
         self.network[neuron][isInList(list=self.network[neuron],target=neighbor)][1]= weight
    
    # get STPD value .
    def stdp(self,deltaT):
        return self.STDP[deltaT]

    # Learn this serial number.
    def learn_serial_number(self,serial_number):

        for i in range(len(serial_number)) :
            if serial_number[i] not in self.forbidden_roots:
                neuron_neighbors=[]
                k=i+1
                while k<i+3:
                    try:
                        if serial_number[k] not in self.forbidden_roots:
                            neuron_neighbors.append(serial_number[k])
                    except:
                        pass
                    k+=1
                distance=0
                for j in neuron_neighbors:
                    if self.isNeighbor(neuron=serial_number[i],neighbor=j)== None:
                        self.add_neighbor(neuron=serial_number[i],neighbor=j)
                        self.setWeight(neuron=serial_number[i],
                                    neighbor=j,
                                    weight=self.stdp(distance))
                    else:
                        self.setWeight(neuron=serial_number[i],
                                    neighbor=j,
                                    weight=self.getWeight(neuron=serial_number[i],neighbor=j)+self.stdp(distance))
                    distance+=1

            
    # show network informations.
    def network_info(self):
        print("\n System -> Network information .\n")
        print(" System -> Neuron number : " + str (len(self.network)))
        print(" System -> Max weight : " + str (self.get_max_weight()))
        print(" System -> Total weight : " + str (self.network_total_weight()))
        print(" System -> Number of relations : " + str (self.network_re()))
        print(" System -> Living neurons : " + str (self.number_of_living_neurons()))
        print(" System -> Nourons with I>3.56 : " + str (self.neurons_I()))

        print('\n')
    




    # Write network pickle file (save as Matrix (in binary)).
    def write_network(self):
        try:
            open_file=open(self.network_name+'.pkl', 'wb')
            pickle.dump(self.network, open_file)
            open_file.close()

        except:
            print(" System -> [error] Network ("+str(self.network_name)+") Creating failed!")


    # creating a network from learning serial numbers(Comments) .
    def creating_network(self):
        p=0
        k,kk=0,0
        words_nbr=0
        words_max_nbr = 224552
        comment_max_lenght = 0
        for i in range(len(self.ROOTS)):
            self.network+=[[]]

        print("\n\n\n System -> Start learning comments ... ")
        open_file = open(self.path, "rb")
        COMMENTS = np.array(pickle.load(open_file))
        print(len(COMMENTS))
        open_file.close()
        start =time.time()
        for j in range(1): # how many times you will learn this network...
            for comment in COMMENTS:


                    if words_nbr > words_max_nbr:
                        break;

                    if len(comment)>comment_max_lenght:
                        comment_max_lenght=len(comment)

                    words_nbr +=len(comment)
                    p+=1
                    self.learn_serial_number(serial_number=comment)
                    
                    k=int((p*100)/len(COMMENTS))
                    if k > kk :
                        
                        print("        ->  learning  ... " + str(k)+'% ('+str(int((time.time()-start)/60))+
                        ' min '+str(int((time.time()-start)%60))+' s).')
                        kk=k

        print('Words nomber : '+str(words_nbr/p))  
        print('Comment max lenght : '+str(comment_max_lenght))
        print(" System -> learning comments Finished.")
    
    # standardization of weights (Normalisaion) (->log()).
    def standardization(self):
        self.get_max_weight()
        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                self.network[i][j][1]=math.log(1+self.network[i][j][1])*0.615
        self.get_max_weight()

    # return network total weight (sum of all weights in the network .)
    def network_total_weight(self):
        weight=0
        for neuron in self.network:
            for neighbor in neuron:
                weight +=neighbor[1]
        return weight

    # retutn the sum of weights of a neuron with its neighbor.
    def get_neuron_total_weight(self,neuron):
        weight=0
        for neighbor in self.network[neuron]:
            weight+=neighbor[1]
        return weight

    # return the sum of relations between neurons and neighbors
    def network_re(self):
        re=0
        for neuron in self.network:
            re +=len(neuron)
        return re

    # return the max weight value in this network
    def get_max_weight(self):
        weight=0
        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                if self.network[i][j][1]>weight:
                    weight=self.network[i][j][1]
        return weight

    # return neurons that have total_I > 3.56 .
    def neurons_I(self):
        I = np.zeros(len(self.network))
        for neuron in self.network:
            for neighbor in neuron:
                I[neighbor[0]]+=neighbor[1]
        I = np.where(I>3.56)[0]
        return len(I)



    # return a list of neurons have the largest number of neighbors.
    def neurons_with_largest_neighbours(self,n):
        n_max_neighbor = [0 for i in range(n)]
        n_max_index = [0 for i in range(n)]
        c = 0
        for i in self.network:
            if len(i)>min(n_max_neighbor):
                n_max_index[n_max_neighbor.index(min(n_max_neighbor))] = c
                n_max_neighbor[n_max_neighbor.index(min(n_max_neighbor))] = len(i)
            c += 1
        n_max_neighbor.sort(reverse=True)
        index=[]
        for i in n_max_neighbor:
            for j in n_max_index:
                
                if len(self.network[j])==i:
                    index.append(j)
                    n_max_index.remove(j)

        return index,n_max_neighbor


    # return most used roots in this network.
    def most_used_roots(self,roots,n):
        n_max_index , n_max_neighbor =self.neurons_with_largest_neighbours(n)
        j=0
        for i in n_max_index:
            if j==0:
                print('[ (i) , roots , neigbors , neuron_weight ]')
            print('[ ('+str(i)+') , '+roots[i]+' , '+str(n_max_neighbor[j])+' , '+str(self.get_neuron_total_weight(i))+' ]')
            j+=1
        print('None for what ?!')
    
    def number_of_living_neurons(self):
        n=0
        for i in self.network:
            if len(i)>0:
                n+=1
        return n
        
        

        
      



if __name__ == "__main__":
    x=11
    if x==1:
        ROOTS=read_roots_file()
        # Creating a negative_network pickle file from negative_comments.pkl .
        forbidden_roots='t7b slm wlh nchlh brv nchl n7b mrc'
        forbidden_roots=get_serial_number(text=forbidden_roots,roots=ROOTS)
        negative_network = Network(path='negative_comments.pkl',
                                   roots_path='roots.pkl',
                                   network_name='negative_network',
                                   learning=True,
                                   forbidden_roots=forbidden_roots) 
        negative_network.most_used_roots()

    if x==2:
        
        ROOTS=read_roots_file()
        # Creating a positive_network pickle file from positive_comments.pkl .
        forbidden_roots='mch'
        forbidden_roots=get_serial_number(text=forbidden_roots,roots=ROOTS)
        positive_network = Network(path='positive_comments.pkl',
                                   roots_path='roots.pkl',
                                   network_name='positive_network',
                                   learning=True,
                                   forbidden_roots=forbidden_roots)
        positive_network.most_used_roots()

    if x==3 :

        # THIS BLOCK FOR CREATING NETWORKS :

        ROOTS=read_roots_file()

        # Creating a normal_network pickle file from normal_comments.pkl .
        forbidden_roots=''
        forbidden_roots=get_serial_number(text=forbidden_roots,roots=ROOTS)
        normal_network = Network( path='normal_comments.pkl',
                                  roots_path='roots.pkl',
                                  network_name='normal_network',
                                  learning=True,
                                  forbidden_roots=forbidden_roots)


        # Creating a positive_network pickle file from positive_comments.pkl .
        forbidden_roots='mch'
        forbidden_roots=get_serial_number(text=forbidden_roots,roots=ROOTS)
        positive_network = Network(path='positive_comments.pkl',
                                   roots_path='roots.pkl',
                                   network_name='positive_network',
                                   learning=True,
                                   forbidden_roots=forbidden_roots)
        
        # Creating a negative_network pickle file from negative_comments.pkl .
        forbidden_roots='t7b slm wlh nchlh brv nchl n7b mrc'
        forbidden_roots=get_serial_number(text=forbidden_roots,roots=ROOTS)
        negative_network = Network(path='negative_comments.pkl',
                                   roots_path='roots.pkl',
                                   network_name='negative_network',
                                   learning=True,
                                   forbidden_roots=forbidden_roots) 

    if x==4 :

        # THIS BLOCK FOR READING NETWORKS FROM NETWORKS PICKLE FILES :

        start =time.time()
        normal_network = Network( path='normal_network.pkl')
        #print(normal_network.network)

        positive_network = Network( path='positive_network.pkl')
        #print(positive_network.network)


        negative_network = Network( path='negative_network.pkl')
        #print(negative_network.network)
      
        
        print(f"Runtime  is : {time.time() - start}")
    

    if True:
        
        # Testing BLOCK : 
        ROOTS=read_roots_file()

        network = Network( path='positive_network.pkl')

        print(network.most_used_roots(ROOTS,30))
        network = Network( path='negative_network.pkl')

        print(network.most_used_roots(ROOTS,30))
        
       


   










    

