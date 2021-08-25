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
print(roots)
graph = read_network_file('positive_network.pkl')


max_l = 0
i = 0
for vertex in graph:
    l = len(vertex)
    if l>max_l:
        print(i,l)
        max_l = l
    i += 1

G=nx.Graph()
buffer = []
node_sizes = []
node_colors = [] 
colors = ['red', 'green', 'blue','yellow', 'purple','black','pink','orange']
def create_sub_graph(r, level):
    global G, graph, buffer, node_sizes, node_colors
    if (level<=3):
        G.add_node(r)     
        #print(r)           
        for v in graph[r]:
            G.add_edges_from([(r, v[0])])
            if (not v[0] in buffer):
                buffer += [v[0]]
                node_sizes += [len(graph[v[0]])]
                node_colors += [colors[level-1]]
                create_sub_graph(v[0],level+1)
    else :
        return


first_v = 7405
buffer = [first_v]
node_colors = ['red']
node_sizes = [len(graph[first_v])]
create_sub_graph(first_v, 1)

print(len(node_sizes))

nx.draw(G , node_color=node_colors, edgecolors='black', node_size=node_sizes)
plt.show()

