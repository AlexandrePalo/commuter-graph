# GENERATE WALK CHANGES
'''
for n in G.nodes:
    generate_walk_changes(G.nodes[n], G)
'''
# DRAW
'''
nx.draw_networkx_nodes(G, {n: (G.nodes[n]['latitude'], G.nodes[n]['longitude']) for n in G.nodes}, node_size=5)
nx.draw_networkx_edges(G, {n: (G.nodes[n]['latitude'], G.nodes[n]['longitude']) for n in G.nodes})
nx.draw_networkx_labels(G, {n: (G.nodes[n]['latitude'], G.nodes[n]['longitude']) for n in G.nodes}, {n: G.nodes[n]['name'] for n in G.nodes}, font_size=5)
plt.show()
'''