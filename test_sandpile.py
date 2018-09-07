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
        edges = [(i,'sink') for i in range(4)] + [(x,y) for x,y in zip(range(3),range(1,4))] + [(3,0)]
        G = Sandpile(edges)
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
        history = G.stabilize()
        self.assertTrue(history=={})
        s[0] = 2
        G.set_state(s)
        self.assertFalse(G.is_stable())
        history = G.stabilize()
        self.assertTrue(history=={i:1 for i in range(4)})
        self.assertTrue(G.get_state()=={0:1})

    def test_add(self):
        G = Sandpile()
        G.add_edges_from([(i,'sink') for i in range(4)])
        G.add_edges_from([(x,y) for x,y in zip(range(3),range(1,4))])
        G.add_edge(3,0)
        G.final()
        G.set_state()
        G.add_chip(0)
        self.assertTrue(G.get_state()=={0:1})
        G.add_chip(0,stabilize=False)
        self.assertTrue(G.get_state()=={0:2})
        history = G.stabilize()
        self.assertTrue(history=={0:1})
        self.assertTrue(G.get_state()=={1:1})
        history = G.add_chip(1,2)
        self.assertTrue(history=={1:1})
        self.assertTrue(G.get_state()=={1:1,2:1})





if __name__ == '__main__':
    unittest.main()
#
