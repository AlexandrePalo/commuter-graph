import networkx as nx

def heatmap_requested(G, source):
    '''
    Generate a dictionnary
    with each station as key and duration from source as value
    '''
    heatmap_requested = {}
    heatmap_nodes = {}

    # With nodes
    for n in G.nodes():
        if n != source:
            heatmap_nodes[n] = nx.dijkstra_path_length(G, source, n, weight='weight')
    # Consolidate for station
    for n in heatmap_nodes:
        exists = False
        for s in heatmap_requested:
            if G.nodes[n]['station'] == s:
                exists = True
                # Mean
                heatmap_requested[s] = (heatmap_requested[s] + heatmap_nodes[n]) / 2
        if not exists:
            heatmap_requested[G.nodes[n]['station']] = heatmap_nodes[n]
    return heatmap_requested

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