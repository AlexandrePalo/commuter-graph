from flask import jsonify
from app import app
from .main import config
from .requests import stations_requested, heatmap_requested, heatmap_interpolated_requested, path_requested
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


@app.route('/heatmap/<station_source_uuid>/', methods=['GET'])
def heatmap(station_source_uuid):
    # source must be a node and not a station
    # grab the first not for this station
    source = [n for n in list(G.nodes()) if G.nodes[n]
              ['station'] == station_source_uuid][0]

    return jsonify({
        'status': 'OK',
        'data': {
            'source': source,
            'heatmap': heatmap_requested(G, source)}
    })


@app.route('/heatmap/interpolated/<station_source_uuid>/', methods=['GET'])
def heatmap_interpolated(station_source_uuid):
    source = [n for n in list(G.nodes()) if G.nodes[n]
              ['station'] == station_source_uuid][0]
    heatmap = heatmap_interpolated_requested(G, source, 50, 50)
    return jsonify({
        'status': 'OK',
        'data': {
            'source': source,
            'heatmap': heatmap['data'],
            'latStep': heatmap['latStep'],
            'lonStep': heatmap['lonStep']
        }
    })


@app.route('/path/', methods=['GET'])
def path():
    source = random.choice(list(G.nodes()))
    target = random.choice(list(G.nodes()))
    return jsonify({
        'status': 'OK',
        'data': {
            'source': source,
            'target': target,
            'heatmap': path_requested(G, source, target)}
    })
