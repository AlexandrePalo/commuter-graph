from flask import jsonify
from app import app
from .main import config
from .requests import heatmap_requested, path_requested
import sys
import random

G = config()

@app.route('/heatmap/', methods=['GET'])
def heatmap():
    source = random.choice(list(G.nodes()))
    return jsonify({
        'status': 'OK',
        'data': {
            'source': source,
            'heatmap': heatmap_requested(G, source)}
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