from __future__ import print_function
from sandpile import Sandpile, grid_edges
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools


def score(G):
    ninc = sum([G.node[n0]['current'] for n0 in G.nodes() if (n0 != 'sink')])
    if ninc == 0:
        print('no nodes included',[G.node[n0]['current'] for n0 in G.nodes() if (n0 != 'sink')])
        return np.inf
    loss = sum([G.node[n0]['value'] for n0 in G.nodes() if (n0 != 'sink') and
                (G.node[n0]['current']==1)])**2

    return loss


def main(n_iter):
    np.random.seed(258)
    low,high=(-1000,1000)
    size = 50
    vals = np.random.randint(low,high,size)
    initial = np.random.random_integers(0,1,size)
    print('start',initial)
    edges = [[i,j] for i,j in itertools.permutations(range(size),2)] + [[k,'sink'] for k in range(size)]
    G = Sandpile(edges)
    s = {i:size*2 for i in range(size)}
    G.set_state(s)
    history = G.stabilize(hist=False)
    # for n_ in np.random.choice(range(size),size=25):
    #     print(G.add_chip(n_))
    # print(G.get_state())
    for n0,val in enumerate(vals):
        G.node[n0]['value']  = val
        G.node[n0]['current'] = initial[n0]
        print(n0,G.node[n0])

    loss = score(G)
    loss0 = loss
    # print(initial)
    # for i in range(n):
    #     print(initial[i*n:i*n+n])
    # print(loss)
    for i_ in range(n_iter):
        if i_ % 10000 == 0:
            print(i_,loss)
            print([G.node[node]['current'] for node in range(size)])
        n0 = np.random.choice(range(size),size=1)
        fires = G.add_chip(n0[0])
        if fires != {}:
            for v in fires.iterkeys():
                G.node[v]['previous'] = G.node[v]['current']
                G.node[v]['current'] = 1-G.node[v]['current']
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
    final = np.array([G.node[node]['current'] for node in range(size)])
    print('&'*80)
    print(vals)
    print('started',loss0)
    print(initial)
    print(loss)
    print('ended',loss)
    print(final)
    print('should be smallest sum: ',final*vals)
    print((final*vals).sum())
    print('searched {} configurations out of {} ({}%)'.format(i_,2**size,float(i_*100)/(2**size)))

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
    main(n_iter=1000000)
