import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}          # ArtistId -> Name
        self._popolarita = {}

    def getAllGenres(self):
        return DAO.getAllGenres()

    def buildGraph(self, genre):
        self._graph.clear()       # riparto pulito se ricreo il grafo
        nodes = DAO.getAllNodes(genre)
        self._idMap = {n["ArtistId"]: n["Name"] for n in nodes}
        self._popolarita = DAO.getPopolarita(genre)

        # nodi
        self._graph.add_nodes_from(self._idMap.keys())

        # archi (verso e peso decisi qui con la popolarità)
        for a, b in DAO.getAllEdges(genre):
            popA = self._popolarita.get(a, 0)
            popB = self._popolarita.get(b, 0)
            peso = popA + popB
            if popA > popB:
                self._graph.add_edge(a, b, weight=peso)
            elif popA < popB:
                self._graph.add_edge(b, a, weight=peso)
            else:                          # stessa popolarità -> doppio arco
                self._graph.add_edge(a, b, weight=peso)
                self._graph.add_edge(b, a, weight=peso)

    def getNumNodes(self):
        return self._graph.number_of_nodes()

    def getNumEdges(self):
        return self._graph.number_of_edges()

    def getMostInfluential(self):
        # influenza = peso archi uscenti - peso archi entranti
        best, bestInflu = None, None
        for n in self._graph.nodes():
            out = sum(d["weight"] for _, _, d in self._graph.out_edges(n, data=True))
            inc = sum(d["weight"] for _, _, d in self._graph.in_edges(n, data=True))
            influ = out - inc
            if bestInflu is None or influ > bestInflu:
                best, bestInflu = n, influ
        return best, bestInflu

    def getTop5Edges(self):
        edges = [(u, v, d["weight"]) for u, v, d in self._graph.edges(data=True)]
        edges.sort(key=lambda x: x[2], reverse=True)
        return edges[:5]

    def getArtistName(self, artistId):
        return self._idMap.get(artistId, artistId)