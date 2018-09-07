from __future__ import print_function
import networkx as nx
import numpy as np


class Sandpile(nx.MultiDiGraph):
    def __init__(self,edges=None,**kwargs):
        """Abelian Sandpile model.  Subclass of `networkx.DiGraph`.
        Parameters
        ----------

        Returns
        -------

        Attributes
        ----------

        """
        self._final = False
        super(Sandpile,self).__init__(**kwargs)
        if edges is not None:
            self.add_edges_from(edges)
            self.final()

    def final(self):
        """Finalize state of the graph.  Most operations will not work until
        after this method has been called.
        """
        self._final = True
        self._nodes = sorted([n for n in self.nodes() if n!='sink']) + ['sink']
        self._idx = {n:i for i,n in enumerate(self._nodes[:-1])}
        self._n = len(self.nodes) - 1
        L = self.reduced_laplacian()
        self._t = {n:L[i] for i,n in enumerate(self._nodes[:-1])}
        self._s = np.diag(L)

    def reduced_laplacian(self):
        """Compute the reduced laplacian of the graph.
        Parameters
        ------

        Returns
        -------
        L : numpy.array
            2 dimensional numpy array containing the reduced laplacian of the
            graph.
        """
        assert self._final
        D = np.eye(self._n)
        for n in self._nodes[:-1]:
            D[n,n] = self.degree(n)
        A = np.asarray(nx.adjacency_matrix(self,self._nodes).todense())
        D = np.diag(A.sum(axis=1))
        #[:-1,:-1]
        return D[:-1,:-1] - A[:-1,:-1]

    def set_state(self,s=None):
        """Set the configuration (number of chips per node on the graph).  Can't
        be run until after `self.final`.

        Parameters
        ----------
        s : None or dict (optional, default=None)
            Dictionary with key, value pairs of node ID and value.  If `None`,
            sets configuration to be all zeroes.

        Returns
        -------
        """
        assert self._final
        self._state = np.zeros(self._n)
        if s is not None:
            for k,v in s.iteritems():
                self._state[k] = v

    def get_state(self,out_format='dict'):
        """Get the current configuration (number of chips one each node).  Can't
        be run until after `self.final` is called.

        Parameters
        ----------
        out_format : str (optional, default=`dict`)
            If `dict`, return a sparse dictionary.  If 'np' return numpy array.
            Otherwise raises a ValueError.

        Returns
        -------
        config : dict or `numpy.array`
        """
        assert self._final
        if out_format == 'dict':
            return {n:v for (n,v) in zip(self._nodes[:-1],self._state) if v != 0}
        elif out_format == 'np':
            return self._state
        else:
            raise ValueError('out_format must be one of {}, you passed {}'.format(['dict','np'],out_format))

    def is_stable(self):
        """Check whether current configuration is stable or not.  Can't be run
        until after set_state.

        Parameters
        ----------

        Returns
        -------
        stable : bool
            If stable returns True, otherwise False
        """
        return np.all(self._state < self._s)

    def fire_node(self,node):
        """Fires node `node` if unstable, otherwise raise AssertionError.

        Parameters
        ----------
        node : type used when adding nodes to graph
            Node to fire.

        Returns
        -------
        """
        idx = self._idx[node]
        assert self._state[idx] >= self._s[idx]
        self._state -= self._t[idx]

    def stabilize(self,hist=True):
        """Fire all nodes until configuration is stable. If configuration is
        stable, raise ValueError.

        Parameters
        ----------
        hist : bool (optional, default=True)
            Return history or not.

        Returns
        -------
        history : dict
            Key, value pairs of node ID and number of times it fired while
            stabilizing.
        """
        if self.is_stable():
            if hist:
                return {}
            return None
            # raise ValueError('current configuration is stable')
        history = {}
        while not self.is_stable():
            to_fire = self._nodes[np.argmax(self._state >= self._s)]
            self.fire_node(to_fire)
            try:
                history[to_fire] += 1
            except:
                history[to_fire] = 1
        if hist:
            return history
        else:
            return None

    def add_chip(self,node,chips=1,stabilize=True,hist=True):
        """Add a number of chips specified with `chips` to node `node`.

        Parameters
        ----------
        node : type used when adding nodes to graph
            Node to add chips to.

        chips : int, optional (default=1)
            Number of chips to add to `node`.

        stabilize : bool, optional (default=True)
            Stabilize the pile immediately after adding chip.

        hist : bool, optional (default=True)
            If stabilize, return history.

        Returns
        -------
        history : dict or None
            If `stabilize` and `hist` are set to True, returns firing history
            otherwise returns None.

        """
        self._state[self._idx[node]] += chips
        if stabilize:
            return self.stabilize(hist=hist)
        return None


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


if __name__ == '__main__':
    import itertools
    G = Sandpile()
    G.add_edges_from([(x,y) for x,y in zip(range(9),range(1,10))])
    G.add_edge(9,0)
    G.add_edges_from([(i,'sink') for i in range(10)])
    print(G.edges())
    print(G.nodes())
    print(nx.adjacency_matrix(G))

    G = Sandpile()
    G.add_edges_from([(i,'sink') for i in range(4)])
    G.add_edges_from([(x,y) for x,y in zip(range(3),range(1,4))])
    G.add_edge(3,0)
    G.final()
    print(np.diag(G.reduced_laplacian()))
    print(G._t)


        # """
        #
        # Parameters
        # ----------
        #
        # Returns
        # -------
        # """
#
