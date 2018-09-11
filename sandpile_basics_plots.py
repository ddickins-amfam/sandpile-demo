import numpy as np
import matplotlib.pyplot as plt
# import matplotlib
import networkx as nx
from sandpile import Sandpile, grid_edges



def draw_state(G,pos,nodelist,edgelist,filename,node_color=None):
    s1 = {n0:int(v) for n0,v in G.get_state().iteritems()}
    if node_color is None:
        node_color = []
        for n0 in nodelist:
            try:
                node_color.append(s1[n0])
            except KeyError:
                node_color.append(0)
                s1[n0] = 0
    plt.figure()
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
    # G.fire_node(0)
    # draw_state(G,pos,nodelist,edgelist,filepath.format('simple_1'),node_color='b')

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


    nodelist = [n0 for n0 in G.nodes() if n0 != 'sink']
    edgelist = [e for e in G.edges() if e[1] != 'sink']
    np.random.seed(562)
    for j in range(5):
        s1 = {i:int(v) for i,v in enumerate(np.random.randint(0,10,n**2))}
        G.set_state(s1)
        draw_state(G,pos,nodelist,edgelist,filepath.format('rand_state_%i'%j))

    G.set_state(s)
    draw_state(G,pos,nodelist,edgelist,filepath.format(0))
    i = 1
    while not G.is_stable():
        node1 = np.argmax(G._state >= G._s)
        G.fire_node(node1)
        draw_state(G,pos,nodelist,edgelist,filepath.format(i))
        i+=1






if __name__ == '__main__':
    # matplotlib.use('Agg')
    filepath = 'presentations/sandpile_basics/images/sandpile_{}.jpg'
    main(3,filepath)


#
