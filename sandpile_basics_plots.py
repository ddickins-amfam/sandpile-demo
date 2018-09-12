from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib
import networkx as nx
from sandpile import Sandpile, grid_edges
from presentation_template_strings import presentation_start, presentation_insert, presentation_end, presentation_history






def draw_state(G,pos,nodelist,edgelist,filename,node_color=None,figsize=None):
    s1 = {n0:int(v) for n0,v in G.get_state().iteritems()}

    if node_color is None:
        node_color = []
        for n0 in nodelist:
            try:
                node_color.append(s1[n0])
            except KeyError:
                node_color.append(0)
                s1[n0] = 0
    if 'sink' in nodelist:
        s1['sink'] = 'sink'
    if figsize is None:
        plt.figure()
    else:
        plt.figure(figsize=figsize)
    nx.draw(G,pos=pos,labels=s1,node_size=5000,node_color=node_color,
            nodelist=nodelist,cmap='Blues',vmin=-1,vmax=10,
            edgelist=edgelist,font_color='w',font_size=48,
            arrowstyle='-|>',arrowsize=35)
    # plt.colorbar()
    # plt.show()
    plt.savefig(filename)
    plt.close()



def main(n,filepath):

    G = Sandpile([[0,1],[1,2],[2,0],[2,1],['sink','sink']])
    s = {0:2}
    G.set_state(s)
    pos = {0:(0,0),1:(1,0.3),2:(0.3,1)}
    nodelist=[0,1,2]
    edgelist=[[0,1],[1,2],[2,0],[2,1]]
    draw_state(G,pos,nodelist,edgelist,filepath.format('simple_0'),node_color='b')
    G.fire_node(0)
    draw_state(G,pos,nodelist,edgelist,filepath.format('simple_1'),node_color='b')
    G.fire_node(0)
    draw_state(G,pos,nodelist,edgelist,filepath.format('simple_2p'),node_color='b')
    G.fire_node(1)
    draw_state(G,pos,nodelist,edgelist,filepath.format('simple_3'),node_color='b')
    G.fire_node(1)
    draw_state(G,pos,nodelist,edgelist,filepath.format('simple_4'),node_color='b')
    G.set_state({0:1,2:1})
    draw_state(G,pos,nodelist,edgelist,filepath.format('simple_2'),node_color='b')


    G = Sandpile(grid_edges(n))
    s = {i:6 for i in range(n**2)}
    G.set_state(s)
    pos = {i:(i%n,int(i/n)) for i in range(n**2)}
    pos['sink'] = (-1,-0.5)
    labels = {i:i for i in range(n**2)}
    labels['sink'] = 'sink'
    plt.figure()
    nx.draw(G,pos=pos,labels=labels,node_size=700,node_color='b',
            font_color='w')
    # plt.show()
    plt.savefig(filepath.format('base'))
    plt.close()

    L = G.reduced_laplacian()
    toprint = '\\\\\n'.join(['&'.join([str(x) for x in r]) for r in L])
    print(toprint)
    nodelist = [n0 for n0 in G.nodes() if n0 != 'sink']# + ['sink']
    nodelist.append('sink')
    edgelist = G.edges()#[e for e in G.edges() if e[1] != 'sink']#[e for e in G.edges()]
    np.random.seed(562)
    for j in range(5):
        s1 = {i:int(v) for i,v in enumerate(np.random.randint(0,10,n**2))}
        G.set_state(s1)
        draw_state(G,pos,nodelist,edgelist,filepath.format('rand_state_%i'%j)
                ,figsize=(10,10))

    G.set_state(s)
    draw_state(G,pos,nodelist,edgelist,filepath.format(0),figsize=(10,10))
    i = 1
    history = []
    presentation_images = [presentation_insert%(0,)]
    while not G.is_stable():
        node1 = np.argmax(G._state >= G._s)
        G.fire_node(node1)
        draw_state(G,pos,nodelist,edgelist,filepath.format(i),figsize=(10,10))
        presentation_images.append(presentation_insert%(i,))
        i+=1
        history.append(node1)
    print(history)
    hist = {}
    for node1 in history:
        try:
            hist[node1] += 1
        except KeyError:
            hist[node1] = 1

    print(hist)
    presentation_images = '\n'.join(presentation_images)
    presentation = '\n'.join([presentation_start,presentation_images,presentation_end])#,presentation_history%(history,hist)
    with open('presentations/sandpile_basics/sandpile_flipbook.tex','w') as outfile:
        outfile.write(presentation)

    G.set_state(s)
    i = 1
    history1 = []
    presentation_images = [presentation_insert%(0,)]
    for node1 in history:
        tofire = 8-node1
        G.fire_node(tofire)
        draw_state(G,pos,nodelist,edgelist,filepath.format(-i),figsize=(10,10))
        presentation_images.append(presentation_insert%(-i,))
        i+=1
        history1.append(tofire)
    print(history1)
    hist = {}
    for node1 in history1:
        try:
            hist[node1] += 1
        except KeyError:
            hist[node1] = 1

    print(hist)
    presentation_images = '\n'.join(presentation_images)
    presentation = '\n'.join([presentation_start,presentation_images,presentation_end])#,presentation_history%(history1,hist)
    with open('presentations/sandpile_basics/sandpile_flipbook_1.tex','w') as outfile:
        outfile.write(presentation)

    s1 = {i:3 for i in range(n**2)}
    G.set_state(s1)
    draw_state(G,pos,nodelist,edgelist,filepath.format('chip_fire_0')
            ,figsize=(10,10))
    history = G.add_chip(4)
    draw_state(G,pos,nodelist,edgelist,filepath.format('chip_fire_1')
            ,figsize=(10,10))
    print(history)
    G.add_chip(1)
    draw_state(G,pos,nodelist,edgelist,filepath.format('chip_fire_2')
            ,figsize=(10,10))
    G.set_state(s1)
    history = G.add_chip(1)
    draw_state(G,pos,nodelist,edgelist,filepath.format('chip_fire_1p')
            ,figsize=(10,10))
    G.add_chip(4)
    draw_state(G,pos,nodelist,edgelist,filepath.format('chip_fire_2p')
            ,figsize=(10,10))

if __name__ == '__main__':
    # matplotlib.use('Agg')
    filepath = 'presentations/sandpile_basics/images/sandpile_{}.jpg'
    main(3,filepath)


#
