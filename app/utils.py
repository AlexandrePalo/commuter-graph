from math import acos, cos, sin, pi
import networkx as nx
import sys

def nodesDurationFromSource(source, G):
    nodesDuration = {}

    for n in G.nodes():
        if n == source:
            nodesDuration[n] = 0.0
        else:
            nodesDuration[n] = nx.dijkstra_path_length(G, source, n, weight='weight')

    return nodesDuration

def interpolatedValue(x, G, heatmap_nodes):
    n = len(G.nodes())
    p = 1

    nominator = 0
    denominator = 0

    for n in G.nodes():
        d = geodesical_distance(x, G.nodes[n])
        # TODO : HANDLE D = 0
        if d > 0:
            nominator = nominator + heatmap_nodes[n] / pow(d, p)
            denominator = denominator + 1 / pow(d, p)

    return nominator / denominator

def geodesical_distance(x, y):
    # Calculate the geodesical distance between point x and y
    # in metter
    r_earth = 6378137 # m
    x_lat_rad = x['latitude'] * pi / 180
    y_lat_rad = y['latitude'] * pi / 180
    d_long = (abs(y['longitude'] - x['longitude'])) * pi / 180

    geodesical_distance = acos(sin(x_lat_rad)*sin(y_lat_rad) + cos(x_lat_rad)*cos(y_lat_rad)*cos(d_long)) * r_earth
    return geodesical_distance
    