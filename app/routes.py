from flask import jsonify
from app import app
from .main import config
from .requests import stations_requested, edges_requested, heatmap_requested, heatmap_interpolated_requested, path_requested
import sys
import random

# print('This is error output', file=sys.stderr)

G = config()


@app.route('/stations/', methods=['GET'])
def stations():
    return jsonify({
        'status': 'OK',
        'data': {
            'stations': stations_requested(G)
        }
    })


@app.route('/edges/', methods=['GET'])
def edges():
    return jsonify({
        'status': 'OK',
        'data': {
            'edges': edges_requested(G)
        }
    })


@app.route('/heatmap/interpolated/<station_source_uuid>/', methods=['GET'])
def heatmap_interpolated(station_source_uuid):
    # source must be a node and not a station
    source = [n for n in list(G.nodes()) if G.nodes[n]
              ['station'] == station_source_uuid][0]
    heatmap = heatmap_interpolated_requested(G, source, 50, 50)
    return jsonify({
        'status': 'OK',
        'data': {
            'source_node': source,
            'heatmap': heatmap['data'],
            'latStep': heatmap['latStep'],
            'lonStep': heatmap['lonStep']
        }
    })


@app.route('/path/<station_source_uuid>/<station_target_uuid>/', methods=['GET'])
def path(station_source_uuid, station_target_uuid):
    # source and target must be nodes and not stations
    source = [n for n in list(G.nodes()) if G.nodes[n]
              ['station'] == station_source_uuid][0]
    target = [n for n in list(G.nodes()) if G.nodes[n]
              ['station'] == station_target_uuid][0]
    return jsonify({
        'status': 'OK',
        'data': {
            'source_node': source,
            'target_node': target,
            'path': path_requested(G, source, target)}
    })
