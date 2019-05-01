import csv

def get_line_type(line):
    '''
    RER, TR, M, T
    '''
    if line[:2] == 'TR':
        return 'TR'
    elif line[:3] == 'RER':
        return 'RER'
    else:
        return line[:1]

def get_nodes(input_path, G):
    '''
    Get nodes from input path and add them to G graph.
    '''
    data_nodes = open(input_path, 'r')
    next(data_nodes, None) # Skip headers

    reader = csv.reader(data_nodes)
    for l in reader:
        uuid = l[1]
        node = {
            'uuid': uuid,
            'line': l[2],
            'line_type': get_line_type(l[2]),
            'name': l[3],
            'latitude': float(l[4].replace('"', '').replace(',', '.')),
            'longitude': float(l[5].replace('"', '').replace(',', '.')),
            'station': l[6]
        }
        G.add_node(uuid, **node)
    
    data_nodes.close()