import uuid

def generate_stations(G):
    '''
    By default: the station name is the name of the stop
    '''
    stations = {}

    for n in list(G.nodes):
        # Check if there is already a station with that name
        exists = False
        for s in stations:
            if G.nodes[n]['name'] == stations[s]['name']:
                exists = True
                # Mean latitude and longitude
                stations[s]['latitude'] = (stations[s]['latitude'] + G.nodes[n]['latitude']) / 2
                stations[s]['longitude'] = (stations[s]['longitude'] + G.nodes[n]['longitude']) / 2
        
        if not exists:
            uid = str(uuid.uuid4())
            stations[uid] = {
                'uuid': uid,
                'name': G.nodes[n]['name'],
                'latitude': G.nodes[n]['latitude'],
                'longitude': G.nodes[n]['longitude']
            }

    for s in stations:
        print('%s;%s;%f;%f' % (stations[s]['uuid'], stations[s]['name'], stations[s]['latitude'], stations[s]['longitude']))