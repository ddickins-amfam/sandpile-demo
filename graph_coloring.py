from __future__ import print_function
from sandpile import Sandpile, grid_edges
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def score(G):
    k = 'current'
    loss = sum([G.node[n0]['current'] == G.node[n1]['current'] for n0,n1 in G.edges()
            if n1 != 'sink'])
    return loss


def main(n,n_iter,colors):

    G = Sandpile(grid_edges(n))
    s = {i:6 for i in range(n**2)}
    G.set_state(s)
    history = G.stabilize(hist=False)
    np.random.seed(234)
    initial = np.random.choice(colors,size=n**2,replace=True)
    for node in range(n**2):
        if node != 'sink':
            G.node[node]['options'] = colors
            G.node[node]['current']  = str(initial[node])

    loss = score(G)
    loss0 = loss
    # print(initial)
    # for i in range(n):
    #     print(initial[i*n:i*n+n])
    # print(loss)
    for i_ in range(n_iter):
        if i_ % 10000 == 0:
            print(i_,loss)
        node = np.random.choice(range(n**2),size=1)
        fires = G.add_chip(node[0])
        if fires != {}:
            # print('#'*80)
            # print(fires)
            for v in fires.iterkeys():
                G.node[v]['previous'] = G.node[v]['current']
                G.node[v]['current'] = np.random.choice([x for x in G.node[v]['options'] if x != G.node[v]['previous']],size=1)[0]
            final = [G.node[node]['current'] for node in range(n**2)]
            # for i in range(n):
            #     print(final[i*n:i*n+n])
            loss1 = score(G)
            # print(loss1)
            if loss1 == 0:
                print('got to 0 after {}!'.format(i_))
                loss = loss1
                break
            elif loss1 <= loss:
                loss = loss1
                pass
            else:
                # print('reverting')
                for v in fires.iterkeys():
                    G.node[v]['current'] = G.node[v]['previous']
    final = [G.node[node]['current'] for node in range(n**2)]
    print('&'*80)
    print('started',loss0)
    for i in range(n):
        print(initial[i*n:i*n+n])
    print(loss)
    print('ended',loss)
    for i in range(n):
        print(final[i*n:i*n+n])

    # print('stable:',G.is_stable())
    # print(G.get_state())
    # print(history)

    # np.random.seed(987)
    # nodes = np.random.randint(0,n**2,size=n_iter,dtype=int)
    # fires = map(G.add_chip,nodes)
    # fire_lengths = map(lambda x: len(x),fires)
    # plt.figure()
    # plt.hist(fire_lengths,bins=25)
    #
    # plt.savefig('soc_plots/power_rule.png')
    # plt.close()
    # idxs = np.random.choice([i for i,x in enumerate(fire_lengths) if x > 0],
    #             size=20,replace=False)
    # # idxs.sort()
    # for idx in idxs:
    #     plt.figure()
    #     toplot = np.zeros((n,n))
    #     h = map(lambda x: (int(x/n),x%n),fires[idx].keys())
    #     for r,c in h:
    #         toplot[r,c]=1
    #     plt.imshow(toplot)
    #     plt.savefig('soc_plots/avalanche_{}.png'.format(idx))
    #     plt.close()




if __name__ == '__main__':
    colors = ['red','green',]#'blue','black','yellow']#,'magenta','cyan']
    main(n=20,n_iter=1000000,colors=colors)
