"""
Thank you card
==============

OK… Let's try this!!
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from grave import plot_network
from grave import use_attributes
import alphabet


network = nx.binomial_graph(100, .05)

text = "THANKYU"


def make_alphabet_nodes_and_edges(graph, text="TH"):
    text = text.upper()
    # Check that there aren't twice the same letter in the text right now
    _, c = np.unique(text, return_counts=True)
    if c.min() > 1:
        raise ValueError(
            "Can't deal with text containing twice the same letter")

    mapping = {}
    n_nodes_mapped = 0
    for letter in text:
        node_labels = alphabet.letter_nodes_mapping[letter]
        mapping.update({
            i + n_nodes_mapped: val for i, val in enumerate(node_labels)})
        n_nodes_mapped = len(mapping)

    graph = nx.relabel_nodes(graph, mapping)
    for letter in text:
        extra_edges = alphabet.letter_edges_mapping[letter]
        graph.add_edges_from(extra_edges)
    return graph


def alphabet_layout(graph):
    n_nodes = graph.number_of_nodes()
    random_state = np.random.RandomState(seed=0)
    xy = random_state.rand(n_nodes, 2)
    # Rescale so that it's spread across all the plot
    xy[:, 0] *= 9
    xy += 2.5 * random_state.randn(n_nodes, 2)
    pos = {k: xy[i] for i, k in enumerate(graph.nodes.keys())}
    pos.update(alphabet.letter_coordinate_mapping)
    return pos


def letter_edges(edge):
    if isinstance(edge[0], str):
        letter = edge[0][0]
        if edge in alphabet.letter_edges_mapping[letter]:
            return True
        else:
            return False
    else:
        return False


t_letter = make_alphabet_nodes_and_edges(network, text=text)

for node, node_attrs in t_letter.nodes(data=True):
    if isinstance(node, str):
        node_attrs['color'] = 'tab:blue'
        node_attrs['size'] = 30
        node_attrs["zorder"] = 10
    else:
        node_attrs['color'] = '0.7'
        node_attrs['size'] = 20


for node_1, node_2, edge_attrs in t_letter.edges(data=True):
    if letter_edges((node_1, node_2)):
        edge_attrs['color'] = 'black'
        edge_attrs['width'] = 2
    else:
        edge_attrs['color'] = '0.9'

pos = alphabet_layout(t_letter)

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_aspect(True)
plot_network(t_letter, layout=alphabet_layout, ax=ax,
             node_style=use_attributes(),
             edge_style=use_attributes())

# We can't set the zerod
nodes_to_rm = [i for i in t_letter.nodes() if isinstance(i, int)]
t_letter = t_letter.copy()
t_letter.remove_nodes_from(nodes_to_rm)
plot_network(t_letter, layout=alphabet_layout, ax=ax,
             node_style=use_attributes(),
             edge_style=use_attributes())

# Now plot the o
o_network = nx.complete_graph(8)


def o_layout(graph):
    pos = nx.circular_layout(graph)
    for k, v in pos.items():
        v += 1
        v *= 0.5
        v[0] += 6.8
        v[1] += 0.1
        pos[k] = v
    return pos
plot_network(o_network, layout=o_layout, ax=ax,
             node_style={"color": "tab:blue", "size": 30})
