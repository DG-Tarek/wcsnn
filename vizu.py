import pickle
from visualisation import Visualisation
import numpy as np

def read_roots_file(path):
        try:
            open_file = open(path, "rb")
            roots = pickle.load(open_file)
            open_file.close()
            return np.array(roots)
        except :
            print(" System -> [error] Downloading roots failed ! .")

def read_network_file(path):
    try:
        network = []
        print("\n\n\n System -> Start ... ")
        open_file = open(path, "rb")
        file = pickle.load(open_file)
        open_file.close()
        for line in file :
            network+=[line]
        return network    
    except :
        print(" System -> [error] Downloading network failed ! .")

roots = read_roots_file("roots.pkl")
graph = read_network_file('positive_network.pkl')

visu = Visualisation(graph=graph, root=7, maxLevel=2)
visu.display()