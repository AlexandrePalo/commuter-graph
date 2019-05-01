from math import acos, cos, sin, pi

change_waiting_duration = 3

def generate_walk_changes(node, G, threshold=10):
    # Return a list of edges between the node and all possible nodes
    # if the walk duration is under the threshold (min)
    # TODO : in addition to the walk duration, add a change time
    # TODO : do the same for proper changes or completely remove changes ??
    for n in G.nodes:
        n = G.nodes[n]
        if n != node:
            duration = (walk_duration(geodesical_distance(
                {'latitude': node['latitude'], 'longitude': node['longitude']},
                {'latitude': n['latitude'], 'longitude': n['longitude']})))
            if node['line'] != n['line']: # avoid walking on the same line
                duration = duration + change_waiting_duration
                if duration <= threshold:
                    print('%s,%s,WALK,%i' % (node['uuid'], n['uuid'], duration))
    return None

def geodesical_distance(x, y):
    # Calculate the geodesical distance between point x and y
    # in metter
    r_earth = 6378137 # m
    x_lat_rad = x['latitude'] * pi / 180
    y_lat_rad = y['latitude'] * pi / 180
    d_long = (abs(y['longitude'] - x['longitude'])) * pi / 180

    geodesical_distance = acos(sin(x_lat_rad)*sin(y_lat_rad) + cos(x_lat_rad)*cos(y_lat_rad)*cos(d_long)) * r_earth
    return geodesical_distance

def walk_duration(distance):
    # Calculate the walk duration for the given distance (in m)
    # in min
    walk_speed = 83.33 # m/min
    walk_duration = distance / walk_speed
    return walk_duration
