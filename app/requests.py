import networkx as nx
import sys
from .utils import nodesDurationFromSource, interpolatedValueIfClose

# print('Hello world!', file=sys.stderr)


def stations_requested(G):
    '''
    Generate a list
    with all stations and lines associated.
    '''
    stations_requested = []

    for n in G.nodes():
        exist = False

        for (i, s) in enumerate(stations_requested):
            if s['uuid'] == G.nodes[n]['station']:
                stations_requested[i]['latitude'] = (
                    stations_requested[i]['latitude'] + G.nodes[n]['latitude']) / 2
                stations_requested[i]['longitude'] = (
                    stations_requested[i]['longitude'] + G.nodes[n]['longitude']) / 2
                stations_requested[i]['lines'].append(G.nodes[n]['line'])
                exist = True

        if not exist:
            stations_requested.append({
                'uuid': G.nodes[n]['station'],
                'latitude': G.nodes[n]['latitude'],
                'longitude': G.nodes[n]['longitude'],
                'lines': [G.nodes[n]['line']],
                'name': G.nodes[n]['station_name']
            })

    return stations_requested


def edges_requested(G):
    '''
    Generate a list
    with all edges between stations.
    '''
    edges_requested = []

    for e in G.edges():

        exist = False

        s1 = G.nodes[e[0]]['station']
        s2 = G.nodes[e[1]]['station']

        # Avoid change edge
        if not G.edges[e]['by'].startswith('CHANGE'):
            for (i, es) in enumerate(edges_requested):
                # Bidirectional edges
                if (es['from'] == s1 and es['to'] == s2) or (es['from'] == s2 and es['to'] == s1):
                    exist = True
        else:
            exist = True

        if not exist:
            edges_requested.append({
                'from': s1,
                'to': s2,
                'by': G.edges[e]['by']
            })

    return edges_requested


def heatmap_requested(G, source):
    '''
    Generate a dictionnary
    with each station as key and duration from source as value

    !!! source must be a node and not a station !!!
    '''
    heatmap_requested = {}
    heatmap_nodes = {}

    # With nodes
    heatmap_nodes = nodesDurationFromSource(source, G)

    # Consolidate for station
    for n in heatmap_nodes:
        exists = False
        for s in heatmap_requested:
            if G.nodes[n]['station'] == s:
                exists = True
                # Mean
                heatmap_requested[s] = (
                    heatmap_requested[s] + heatmap_nodes[n]) / 2
        if not exists:
            heatmap_requested[G.nodes[n]['station']] = heatmap_nodes[n]
    return heatmap_requested


def heatmap_interpolated_requested(G, source, nLat, nLon):
    '''
    source must be a node and not a station.

    n: number of lat and lon points. Total: nb^2 points
    '''
    # Min max bounds and steps
    latBounds = {
        'min': min([G.nodes[n]['latitude'] for n in G.nodes()]),
        'max': max([G.nodes[n]['latitude'] for n in G.nodes()])
    }
    lonBounds = {
        'min': min([G.nodes[n]['longitude'] for n in G.nodes()]),
        'max': max([G.nodes[n]['longitude'] for n in G.nodes()])
    }
    latBounds['step'] = (latBounds['max'] - latBounds['min']) / (nLat - 1)
    lonBounds['step'] = (lonBounds['max'] - lonBounds['min']) / (nLon - 1)

    heatmap_interpolated = []

    # Generate interpolated grid
    heatmap_nodes = nodesDurationFromSource(source, G)

    for i in range(0, nLat):
        for j in range(0, nLon):
            latitude = latBounds['min'] + latBounds['step'] * i
            longitude = lonBounds['min'] + lonBounds['step'] * j
            duration = interpolatedValueIfClose({
                'latitude': latitude,
                'longitude': longitude
            }, G, heatmap_nodes, 1000)
            if duration != False:
                heatmap_interpolated.append({
                    'latitude': latitude,
                    'longitude': longitude,
                    'duration': duration
                })

    return {
        'data': heatmap_interpolated,
        'latStep': latBounds['step'],
        'lonStep': lonBounds['step']
    }


def path_requested(G, source, target):
    '''
    Generate an array with path information to be exported to front end.
    source and target must be nodes and not stations.
    '''
    path_requested = []

    nodes_path = nx.dijkstra_path(G, source, target, weight='weight')

    for i, n in enumerate(nodes_path):
        if i > 0:
            step = {
                'from': {
                    'station': G.nodes[nodes_path[i - 1]]['station'],
                    'stop_line': G.nodes[nodes_path[i - 1]]['line']
                },
                'to': {
                    'station': G.nodes[nodes_path[i]]['station'],
                    'stop_line': G.nodes[nodes_path[i]]['line']
                },
                'duration': G.edges[nodes_path[i - 1], nodes_path[i]]['weight']
            }
            if G.edges[nodes_path[i - 1], nodes_path[i]]['by'] in ['CHANGE_SAME', 'CHANGE_DIFF']:
                step['by'] = 'WALK'
            else:
                step['by'] = G.nodes[nodes_path[i]]['line']

            path_requested.append(step)

    # Prevent change on first and last station, it makes no sense as front-end request source and target stations and not nodes.
    if (path_requested[0]['by'] == 'WALK'):
        path_requested.pop(0)
    if (path_requested[len(path_requested) - 1]['by'] == 'WALK'):
        path_requested.pop(len(path_requested) - 1)

    return path_requested
