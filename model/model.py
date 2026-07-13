import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allEdges = None
        self._allNodes = None
        self._bestPath = None
        self._idMap = {}
        self._graph = nx.Graph()

    def buildGraph(self, genere):
        self._graph.clear()
        self._idMap.clear()
        self._allNodes = DAO.allNodes(genere)
        self._graph.add_nodes_from(self._allNodes)
        for n in self._allNodes:
            self._idMap[n.id] = n
        self._allPossibleEdges= DAO.allPossibleEdges()
        for e in self._allPossibleEdges:
            if e[0] in self._idMap.keys() and e[1] in self._idMap.keys():
                self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[2])

    def getAllGenere(self):
        allGenere=DAO.allObjectDD()
        allGenere.sort(key=lambda x: x)
        return allGenere

    def getGraph(self):
        return self._graph

    def detailGraph(self):
        return len(self._graph.nodes()), len(self._graph.edges())

    def edgesIsolati(self):
        lista=[]
        for n in self._graph.nodes():
            print(self._graph.degree(n))
            if self._graph.degree(n) == 0:
                lista.append(n)
                print(lista)
        return lista

    def getPath(self, nodoInizio):
        self._bestPath = []
        self._bestLun = 0
        self.ricorsione([nodoInizio])
        return self._bestPath, self._bestLun

    def ricorsione(self, parziale):
        lunghezza= len(parziale)
        if lunghezza == self._bestLun:
            if self.condizioneLunghezza(parziale):
                self._bestLun = lunghezza
                self._bestPath = copy.deepcopy(parziale)
        if lunghezza > self._bestLun:
            self._bestLun = lunghezza
            self._bestPath = copy.deepcopy(parziale)
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                if self.condizionePeso(parziale, n):
                    parziale.append(n)
                    self.ricorsione(parziale)
                    parziale.pop()

    def condizionePeso(self, parziale, n):
        if len(parziale)<2:
            return True
        pesoCorrente=self._graph.get_edge_data(parziale[-1], n)["weight"]
        pesoP=self._graph.get_edge_data(parziale[-2], parziale[-1] )["weight"]
        if pesoP>pesoCorrente:
            return True
        return False

    def condizioneLunghezza(self, parziale):
        sommaBest=0
        for i in range(len(self._bestPath)-1):
            sommaBest += self._graph.get_edge_data( self._bestPath[i], self._bestPath[i+1])["weight"]
        sommaParziale = 0
        for i in range(len(self._bestPath)-1):
            sommaParziale += self._graph.get_edge_data(parziale[i], parziale[i + 1])["weight"]
        if sommaBest < sommaParziale:
            return True
        return False