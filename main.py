import networkx as nx
import csv
import matplotlib.pyplot as plt

# TODO : RERB, RERC, RERD, TR...
displayed_M = ['1', '2', '3', '3BIS', '4', '5', '6', '7', '7BIS', '8', '9', '10', '11', '12', '13', '14']
displayed_T = ['1', '2', '3A', '4B', '5', '6', '7', '8', '11']
displayed_lines = ['M' + m for m in displayed_M] + ['T' + t for t in displayed_T]
G = nx.Graph()

# NODES
data_nodes = open('./inputs/RATP_nodes.csv', 'r')
next(data_nodes, None)
reader = csv.reader(data_nodes)

for line in reader:
    if line[2] in displayed_lines:
        G.add_node(line[1], line=line[2], name=line[3], latitude=float(line[4].replace('"', '').replace(',', '.')), longitude=float(line[5].replace('"', '').replace(',', '.')))

data_nodes.close()

# EDGES
data_edges = open('./inputs/RATP_edges.csv', 'r')
next(data_edges, None)
reader = csv.reader(data_edges)

def edge_weight(edge_type):
    if edge_type == 'CHANGE_SAME':
        return 5
    elif edge_type == 'CHANGE_DIFF':
        return 8
    else:
        return 3

for line in reader:
    if line[2] in displayed_lines:
        G.add_edge(line[0], line[1], type=line[2], weight=edge_weight(line[2]))

# Max, min latitude & longitude
latitude_bounds = {'min': float('inf'), 'max': 0.0}
longitude_bounds = {'min': float('inf'), 'max': 0.0}
for n in G.nodes:
    if G.nodes[n]['latitude'] > latitude_bounds['max']:
        latitude_bounds['max'] = G.nodes[n]['latitude']
    if G.nodes[n]['latitude'] < latitude_bounds['min']:
        latitude_bounds['min'] = G.nodes[n]['latitude']
    if G.nodes[n]['longitude'] > longitude_bounds['max']:
        longitude_bounds['max'] = G.nodes[n]['longitude']
    if G.nodes[n]['longitude'] < longitude_bounds['min']:
        longitude_bounds['min'] = G.nodes[n]['longitude']
print(latitude_bounds)
print(longitude_bounds)

pos = {}
for n in G.nodes:
    pos[n] = (G.nodes[n]['latitude'], G.nodes[n]['longitude'])

# DRAW
nx.draw_networkx_nodes(G, {n: (G.nodes[n]['latitude'], G.nodes[n]['longitude']) for n in G.nodes}, node_size=5)
nx.draw_networkx_edges(G, {n: (G.nodes[n]['latitude'], G.nodes[n]['longitude']) for n in G.nodes})
nx.draw_networkx_labels(G, {n: (G.nodes[n]['latitude'], G.nodes[n]['longitude']) for n in G.nodes}, {n: G.nodes[n]['name'] for n in G.nodes}, font_size=5)

plt.show()