import numpy as np
import networkx as nx


def adjust(G):
    nodes_list = []
    for node in G.nodes:
        nodes_list.append(list(G.nodes[node]['pos']))
    coords = np.array(nodes_list)
    mean = np.mean(coords, axis=0)
    std_dev = np.std(coords, axis=0)

    lower_bound = mean - std_dev
    upper_bound = mean + std_dev

    adjusted_coords = np.clip(coords, lower_bound, upper_bound)
    i = 0
    for node in G.nodes:
        G.nodes[node]['pos'] = adjusted_coords[i]
        i += 1

    '''
    for num in range(len(nodes_list)):
        for _i in range(2):
            if nodes_list[num][_i] > mean[_i]:
                nodes_list[num][_i] = (3 * upper_bound[_i] + nodes_list[num][_i]) / 4
            else:
                nodes_list[num][_i] = (3 * lower_bound[_i] + nodes_list[num][_i]) / 4

    i = 0
    for node in G.nodes:
        G.nodes[node]['pos'] = nodes_list[i]
        i += 1
    '''
    return G
