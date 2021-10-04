# Last edit : Friday 14/08/2021.
# Created on Python 3.9(64bit).
# tarek.dg.dz@gmail.com


from os import name
import networkx as nx
import pickle
from matplotlib import pyplot as plt
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




G=nx.Graph()
buffer = []
node_sizes = []
node_colors = [] 
colors = ['red', 'orange', 'yellow','green', 'blue','indego','violet']




def create_sub_graph(r, level):
    global G, graph, buffer, node_sizes, node_colors
    if (level<=1):
        G.add_node(r)     
           
        for v in graph[r]:
            G.add_edges_from([(r, v[0])])
            if (not v[0] in buffer):
                buffer += [v[0]]
                node_sizes += [len(graph[v[0]])]
                node_colors += [colors[level-1]]
                create_sub_graph(v[0],level+1)
    else :
        return


first_v = 8173
buffer = [first_v]
node_colors = ['blue']
node_sizes = [len(graph[first_v])]


create_sub_graph(first_v, 1)

print(len(node_sizes))

nx.draw(G , node_color=node_colors, edgecolors='black', node_size=node_sizes)
plt.show()

