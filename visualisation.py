
import networkx as nx
from matplotlib import pyplot as plt


class Visualisation:

    def __init__(self, graph, root, maxLevel):
        self.G = nx.Graph()
        self.buffer = [root]
        self.node_sizes = [len(graph[root])]
        self.graph = graph
        self.maxLevel = maxLevel
        self.generateGraph(root, 1)        
    
    def display(self):
        nx.draw(self.G, edgecolors='black', node_size=self.node_sizes)
        plt.show()
        
    def appendSubGraph(self, root):
        self.generateGraph(root, 1)

    def generateGraph(self, r, level):
        if (level<=self.maxLevel):
            self.G.add_node(r)     
            #print(r)           
            for v in self.graph[r]:
                self.G.add_edges_from([(r, v[0])])
                if (not v[0] in self.buffer):
                    self.buffer += [v[0]]
                    self.node_sizes += [len(self.graph[v[0]])]
                    self.generateGraph(v[0],level+1)
        else :
            return
