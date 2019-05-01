import networkx as nx
import random
import matplotlib.pyplot as plt
from .requests import path_requested, heatmap_requested

from .nodes import get_nodes
from .edges import get_edges

# TODO : RER, TR

# CONFIG FUNCTION
def config():
    G = nx.Graph()
    # NODES
    get_nodes('./app/inputs/RATP_nodes - nodes_M.csv', G) # Metros
    # EDGES
    get_edges('./app/inputs/RATP_edges.csv', G)
    return G

'''
# REQUEST - HEAT MAP
print('---- REQUEST - HEAT MAP ----')
source = random.choice(list(G.nodes))
print(heatmap_requested(G, source))

# REQUEST - PATH
print('---- REQUEST - PATH ----')
source = random.choice(list(G.nodes))
target = random.choice(list(G.nodes))
print(path_requested(G, source, target))
'''