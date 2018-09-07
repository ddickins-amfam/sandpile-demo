from __future__ import print_function
import unittest
from sandpile import Sandpile, grid_edges
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def main(n,n_iter):
    G = Sandpile(grid_edges(n))
    s = {i:6 for i in range(n**2)}
    G.set_state(s)
    history = G.stabilize(hist=False)
    # print('stable:',G.is_stable())
    # print(G.get_state())
    # print(history)

    np.random.seed(987)
    nodes = np.random.randint(0,n**2,size=n_iter,dtype=int)
    fires = map(G.add_chip,nodes)
    fire_lengths = map(lambda x: len(x),fires)
    plt.figure()
    plt.hist(fire_lengths,bins=25)

    plt.savefig('soc_plots/power_rule.png')
    plt.close()
    idxs = np.random.choice([i for i,x in enumerate(fire_lengths) if x > 0],size=20,replace=False)
    # idxs.sort()
    for idx in idxs:
        plt.figure()
        toplot = np.zeros((n,n))
        h = map(lambda x: (int(x/n),x%n),fires[idx].keys())
        for r,c in h:
            toplot[r,c]=1
        plt.imshow(toplot)
        plt.savefig('soc_plots/avalanche_{}.png'.format(idx))
        plt.close()




if __name__ == '__main__':
    main(n=40,n_iter=10000)
