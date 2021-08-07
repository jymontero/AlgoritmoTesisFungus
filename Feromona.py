import pandas as pd
from Historial import Historial

class Feromona():

    def __init__(self, decay, aprendizajeQ, historial):
        self.dataF = pd.DataFrame()
        self.copiaNodosAdyacentes = pd.DataFrame()
        self.nodos = []
        self.dictAeroFeromona = {}

        self.objHistorial = Historial()
        self.objHistorial = historial

        self.aprendizajeQ = aprendizajeQ
        self.decay = decay

#metodo de tasa de dispisacion fernooma
    def evaporacionGlobalFeromona(self, nodos, vertices):
        self.dictAeroFeromona = vertices
        for aeropuerto in nodos:
            self.dataF = self.dictAeroFeromona.get(aeropuerto)
            self.listaDisipacion = self.dataF.copy()
            self.listaDisipacion['feromona'] = self.listaDisipacion['feromona'].apply(lambda x :((1 - self.decay)* x))
            self.dictAeroFeromona[aeropuerto] = self.listaDisipacion
            #self.objHistorial.generarHistorial("Evaporacion: ", self.dictAeroFeromona[aeropuerto])

        return self.dictAeroFeromona

#metodo rastro de feronoma x cada hormiga
    def cantidadFeromonaDepositar(self, data):
        self.dataF = data
        cantHeuristica = 0
        for i in range((len(self.dataF))):
            costo = self.dataF.loc[i]['costo']
            penalizacion= self.dataF.loc[i]['penalizacion']
            feronomaActual = self.dataF.loc[i]['feromona']

            #cantHeuristica = costo - penalizacion
            cantHeuristica = int(costo + penalizacion)
            #print('Cantidad', cantHeuristica)
            #self.objHistorial.generarHistorial('\ncantidadHeuristica: ', cantHeuristica)
            cantFeromonaADespositar = self.aprendizajeQ / (cantHeuristica)
            #self.objHistorial.generarHistorial('cantidadFeromona: ',cantFeromonaADespositar)
            self.dataF.loc[i,'feromona'] = feronomaActual + (cantFeromonaADespositar)

        #self.generarLog(self.dataF)
        return self.dataF

    def actualizarDataVertices(self, data, vertices):
        self.dictAeroFeromona = vertices
        for i in range(len(data)):
            idVuelo = data.loc[i]['#leg_nb ']
            aeroSalida = data.loc[i][' airport_dep ']
            feromona = data.loc[i]['feromona']
            dataActualizar = self.dictAeroFeromona.get(aeroSalida)
            dataActualizarCopia = dataActualizar.copy()
            dataActualizarCopia.loc[dataActualizarCopia['#leg_nb '] == idVuelo,['feromona']] = feromona
            self.dictAeroFeromona[aeroSalida] = dataActualizarCopia

            #self.objHistorial.generarHistorial('\nVerticesActualizados:\n', self.dictAeroFeromona[aeroSalida])
        return self.dictAeroFeromona

    def eliminarNodos(self, nodosEliminar, vertices):
        self.dictAeroFeromona = vertices
        dCopia = pd.DataFrame()
        vuelosEliminados = 0
        for i in range(len(nodosEliminar)):
            dataEmparejamiento = nodosEliminar[i]

            for j in range(len(dataEmparejamiento)):
                idVuelo =  dataEmparejamiento.loc[j]['#leg_nb ']
                nodoSalida = dataEmparejamiento.loc[j][' airport_dep ']

                dataEliminarNodos  = self.dictAeroFeromona.get(nodoSalida)
                dCopia = dataEliminarNodos.copy()
                #dCopia = dCopia.drop(dCopia.loc[dCopia['#leg_nb ']== idVuelo].index, inplace = True)
                dCopia = dCopia[dCopia['#leg_nb '] != idVuelo]
                dCopia = dCopia.reset_index(drop=True)
                vuelosEliminados +=1
                self.dictAeroFeromona[nodoSalida] =  dCopia
        print('VuelosEliminados: ', vuelosEliminados)
        return self.dictAeroFeromona

    def evaluarFeromona(self, data):
        self.dataF = data
        self.cantidadFeromonaDepositar()
        return self.dataF

    def generarLog(self,data):
        data = data.drop(columns=[' date_arr ',' hour_dep ',' hour_arr',' date_dep '])
        self.objHistorial.generarHistorial('CaminoFeromona', data)
