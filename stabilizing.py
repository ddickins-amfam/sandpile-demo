from __future__ import print_function
import unittest
from sandpile import Sandpile
import networkx as nx
import numpy as np


# assertTrue
# assertFalse
# assertEqual
# assertIsInstance
# assertRaises

def grid_edges(n):
    edge_list = []
    for node in range(n*n):
        r = int(node/n)
        c = node%n
        if ((r % n) == 0):
            edge_list.append([node,'sink'])
        else:
            edge_list.append([node,node - n])
        if ((r % n) == n-1):
            edge_list.append([node,'sink'])
        else:
            edge_list.append([node,node + n])
        if ((c % n) == 0):
            edge_list.append([node,'sink'])
        else:
            edge_list.append([node,node - 1])
        if ((c % n) == n-1):
            edge_list.append([node,'sink'])
        else:
            edge_list.append([node,node + 1])

    return edge_list



def main():
    G = Sandpile()
    edge_list = grid_edges(3)
    print(edge_list)
    G.add_edges_from(edge_list)
    G.final()
    L = G.reduced_laplacian()
    print(L)
    s = np.diag(L)
    s = {i:v for i,v in enumerate(s)}
    G.set_state(s)
    print('stable:',G.is_stable())
    history = G.stabilize()
    print('stable:',G.is_stable())
    print(G.get_state())
    print(history)
    G.set_state(s)
    for node in [1,3,5,7,4,4]:
        G.fire_node(node)
    print('after {}'.format([1,3,5,7,4,4]))
    print(G.get_state())
    for node in [0,2,6,8]:
        G.fire_node(node)
    print('after {}'.format([0,2,6,8]))
    print(G.get_state())
    for node in [1,3,5,7]:
        G.fire_node(node)
    print('after {}'.format([1,3,5,7]))
    print(G.get_state())
    for node in [0,2,6,8,4]:
        G.fire_node(node)
    print('after {}'.format([0,2,6,8,4]))
    print(G.get_state())

    x = [1,3,5,7,4,4] + [0,2,6,8] + [1,3,5,7] + [0,2,6,8,4]
    d = {}
    for i in x:
        try:
            d[i]+=1
        except:
            d[i] = 1
    print('d',d)
    print('history',history)
    print(d==history)

class SandpileTestCase(unittest.TestCase):
    def test_create(self):
        G = Sandpile()
        self.assertIsInstance(G,nx.DiGraph)

    def test_final(self):
        G = Sandpile()
        G.add_edges_from([(i,'sink') for i in range(4)])
        G.add_edges_from([(x,y) for x,y in zip(range(3),range(1,4))])
        G.add_edge(3,0)
        with self.assertRaises(AssertionError):
            G.reduced_laplacian()
        G.final()
        self.assertTrue(G._final)

    def test_reduced_laplacian(self):
        G = Sandpile()
        G.add_edges_from([(i,'sink') for i in range(4)])
        G.add_edges_from([(x,y) for x,y in zip(range(3),range(1,4))])
        G.add_edge(3,0)
        G.final()
        L = G.reduced_laplacian()
        self.assertTrue(np.all(
                np.array([[2,-1,0,0],
                        [0,2,-1,0],
                        [0,0,2,-1],
                        [-1,0,0,2]])==L))


    def test_state(self):
        G = Sandpile()
        G.add_edges_from([(i,'sink') for i in range(4)])
        G.add_edges_from([(x,y) for x,y in zip(range(3),range(1,4))])
        G.add_edge(3,0)
        s = {i:1 for i in range(3)}
        with self.assertRaises(AssertionError):
            G.set_state(s)
        with self.assertRaises(AssertionError):
            G.get_state()
        G.final()
        with self.assertRaises(AttributeError):
            G.get_state()
        G.set_state(s)
        r = np.array([s[i] for i in range(3)] + [0])
        self.assertTrue(G.get_state()=={k:v for k,v in s.iteritems() if v != 0})
        self.assertTrue(np.all(G.get_state('np')==r))
        with self.assertRaises(ValueError):
            G.get_state('other')

    def test_stability(self):
        G = Sandpile()
        G.add_edges_from([(i,'sink') for i in range(4)])
        G.add_edges_from([(x,y) for x,y in zip(range(3),range(1,4))])
        G.add_edge(3,0)
        s = {i:1 for i in range(4)}
        G.final()
        G.set_state(s)
        self.assertTrue(G.is_stable())
        s[0] = 2
        G.set_state(s)
        self.assertFalse(G.is_stable())

    def test_fire(self):
        G = Sandpile()
        G.add_edges_from([(i,'sink') for i in range(4)])
        G.add_edges_from([(x,y) for x,y in zip(range(3),range(1,4))])
        G.add_edge(3,0)
        s = {i:1 for i in range(4)}
        G.final()
        G.set_state(s)
        with self.assertRaises(AssertionError):
            G.fire_node(0)
        s[0] = 2
        G.set_state(s)
        self.assertFalse(G.is_stable())
        G.fire_node(0)
        self.assertTrue(G.get_state()=={1:2,2:1,3:1})

    def test_stabilize(self):
        G = Sandpile()
        G.add_edges_from([(i,'sink') for i in range(4)])
        G.add_edges_from([(x,y) for x,y in zip(range(3),range(1,4))])
        G.add_edge(3,0)
        s = {i:1 for i in range(4)}
        G.final()
        G.set_state(s)
        with self.assertRaises(ValueError):
            G.stabilize()
        s[0] = 2
        G.set_state(s)
        self.assertFalse(G.is_stable())
        history = G.stabilize()
        self.assertTrue(history=={i:1 for i in range(4)})
        self.assertTrue(G.get_state()=={0:1})

if __name__ == '__main__':
    main()
#
