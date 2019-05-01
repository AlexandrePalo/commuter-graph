import csv

def get_edge_weight(edge_type):
    weights = {
        'M1': 1.5,
        'M2': 1.38,
        'M3': 1.29,
        'M3BIS': 1.33,
        'M4': 1.12,
        'M5': 1.62,
        'M6': 1.15,
        'M7': 1.49,
        'M7BIS': 1.29,
        'M8': 1.41,
        'M9': 1.44,
        'M10': 1.45,
        'M11': 1.25,
        'M12': 1.36,
        'M13': 1.55,
        'M14': 1.88,
        'T1': 1.83,
        'T2': 1.96,
        'T3A': 1.75,
        'T3B': 2.0,
        'T4': 2.0,
        'T5': 1.47,
        'T6': 2.0,
        'T7': 1.82,
        'T8': 2.0,
        'T11': 2.5,
        'RERA': 3.11,
        'RERB': 2.78,
        'CHANGE_SAME': 3.0,
        'CHANGE_DIFF': 3.0
    }
    return weights[edge_type]

def get_edges(input_path, G):
    '''
    Get edges from input path and add them to G graph.
    '''
    data_edges = open(input_path, 'r')
    next(data_edges, None) # Skip headers

    reader = csv.reader(data_edges)
    
    for l in reader:
        uuid1 = l[0]
        uuid2 = l[1]
        edge = {
            'uuid1': uuid1,
            'uuid2': uuid2,
            'by': l[2],
            'weight': get_edge_weight(l[2])
        }
        if uuid1 in list(G.nodes) and uuid2 in list(G.nodes):
            G.add_edge(uuid1, uuid2, **edge)

    data_edges.close()