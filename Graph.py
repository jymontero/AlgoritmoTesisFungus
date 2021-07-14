import networkx as nx
import matplotlib.pyplot as plt
from loadData import LoadData

class Grafo:

    def __init__(self, nodo, aristas):
        self.vertices  = nodo
        self.aristas = aristas
        self.gradoD = nx.MultiDiGraph()
        self.objLoadData = LoadData()

    def existeNodo(self, nodo):
        if nodo in self.vertices:
            return True
        return False

    def getGrafo(self):
        return self.gradoD

    def addVertex(self, nodo):
        pass

    def addArista(self):
        dictedges = {}
        columns = ['#leg_nb', ' airport_arr ']
        for base in self.aristas:
            aux = self.aristas.get(base)
            consultaColum = self.objLoadData.uniqueColumn(' airport_arr ', aux)
            consultaColum2 = self.objLoadData.uniqueColumn('#leg_nb ', aux)
            for destino, vuelo in zip(consultaColum, consultaColum2):
                self.gradoD.add_edge(base, destino, vuelo)

        dictedges = self.gradoD.edges
        print (len((self.gradoD.edges)))
        print(dictedges)

    def addNode(self):
        nodoBases = [' BASE1 ', ' BASE2 ', 'BASE3 ']
        for nodo in self.vertices:
            if nodo in nodoBases:
                self.gradoD.add_node(nodo)

    def drawGraph(self):
        self.gradoD.add_nodes_from(self.vertices)
        self.addArista()
        pos = nx.spring_layout(self.gradoD)
        plt.figure()
        nx.draw(self.gradoD, pos, edge_color = 'black', width = 1, linewidths =2,
                node_size= 1500 , node_color = 'purple', alpha= 0.7,ax=None)

        nx.draw_networkx_labels(self.gradoD,pos,
                                labels= {node: node for node in self.gradoD.nodes()},
                                font_size=9, alpha=1, horizontalalignment='center',verticalalignment='center'
                                ,ax=None)

        #nx.draw_networkx_edge_labels(self.gradoD,pos,edge_labels={(u,v):
        #self.gradoD[u][v] for u,v in self.gradoD.edges()} ,font_color='red')
        #nx.draw_networkx_labels(self.gradoD, pos, font_size=20,
        #font_family='sans-serif')

        plt.axis('off')
        plt.show()



objload = LoadData()
objload.cargaDataset()
print(objload.getBasesConexiones())
objgrafo = Grafo(objload.getDataAirport(),objload.getBasesConexiones())
objgrafo.drawGraph()




