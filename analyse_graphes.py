import pickle


def read_network_file(network_path):
        try:
            network = []
            print("\n\n\n System -> Start ... ")
            open_file = open(network_path, "rb")
            file = pickle.load(open_file)
            open_file.close()
            for line in file :
                network+=[line]
            #print(" System -> Network : Downloaded Successfully.")
            return network    
        except :
            print(" System -> Downloading network failed!") 

network_path = 'positive_network.pkl'
net = read_network_file(network_path)
n = 30
n_max_neighbour = [0 for i in range(n)]
n_max_index = [0 for i in range(n)]
c = 0
print('Positive :')
for i in net:
    if len(i)>min(n_max_neighbour):
        n_max_index[n_max_neighbour.index(min(n_max_neighbour))] = c
        n_max_neighbour[n_max_neighbour.index(min(n_max_neighbour))] = len(i)
    c += 1
print(n_max_index)
print(n_max_neighbour) 



network_path = 'negative_network.pkl'
net = read_network_file(network_path)
n_max_neighbour = [0 for i in range(n)]
n_max_index = [0 for i in range(n)]
c = 0
print('Negative :')
for i in net:
    if len(i)>min(n_max_neighbour):
        n_max_index[n_max_neighbour.index(min(n_max_neighbour))] = c
        n_max_neighbour[n_max_neighbour.index(min(n_max_neighbour))] = len(i)
    c += 1
print(n_max_index)
print(n_max_neighbour) 
