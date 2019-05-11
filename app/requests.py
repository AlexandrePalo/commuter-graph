import networkx as nx
import sys
from .utils import nodesDurationFromSource, interpolatedValueIfClose


def stations_requested(G):
    '''
    Generate a list
    with all stations and lines associated.
    TODO : edges between stations ?
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

    return path_requested
