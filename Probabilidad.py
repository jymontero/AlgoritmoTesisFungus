import pandas as pd
from OperacionAcoFu import OperacionACOFungus
from Historial import Historial


class Probabilidad():

    def __init__(self, alpha, beta, historial):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        self.dataP = pd.DataFrame()
        self.objOperacionFungus = OperacionACOFungus()
        self.alpha = alpha
        self.beta = beta
        self.listaAbsulta= []
        self.objHistorial = Historial()
        self.objHistorial =  historial


    def calcuFeroVisib(self, row):
        pheronoma = (row['feromona'])
        visibilidad = 1.0 / (row['costo'])
        rowInfo = (pheronoma ** self.alpha) * (visibilidad ** self.beta)
        return rowInfo

    def calculoNumProbabilidad(self):
        self.dataP['visibilidad'] = self.dataP.apply(self.calcuFeroVisib, axis=1)

    def sumarFeroVisi(self):
        return self.dataP['visibilidad'].sum()

    def probabilidadNodos(self):
        suma = self.sumarFeroVisi()
        self.dataP['probabilidad'] = self.dataP['visibilidad'].apply(lambda x:(x/suma))
    def sumaAcumuladaProbabilidad(self):
        self.dataP['sumAcumu'] = self.dataP['probabilidad'].cumsum()

    def obtenerSiguienteNodo(self):
        aleatorio = self.objOperacionFungus.generarAleatorio()
        #self.objHistorial.generarHistorial('\nAleatorio:', aleatorio)
        busquedaProb = self.objOperacionFungus.busquedaBinaria(self.listaAbsulta, aleatorio)
        self.objHistorial.generarHistorial('Busqueda#PRobablidad:', busquedaProb)
        saltoVuelo, aeroDestino, idVuelo, fechaArr, horaDepa = self.objOperacionFungus.getSalto(busquedaProb, self.dataP)
        #self.objHistorial.generarHistorial('Proximo Nodo:\n', saltoVuelo)
        return saltoVuelo, aeroDestino, idVuelo, fechaArr, horaDepa

    def evaluarProbabilidad(self, data):
        self.dataP = data
        self.dataP['visibilidad'] = 0
        self.dataP['probabilidad'] = 0
        self.dataP['sumAcumu'] = 0
        self.calculoNumProbabilidad()
        self.probabilidadNodos()
        self.sumaAcumuladaProbabilidad()
        serie = self.dataP['sumAcumu']
        self.listaAbsulta = serie.tolist()

        self.generarLog()


    def generarLog(self):
        #self.data = pd.DataFrame()
        data = self.dataP
        data = data.drop(columns=[' date_arr ',' hour_dep ',' hour_arr',' date_dep '])
        suma = self.sumarFeroVisi()
        self.objHistorial.generarHistorial('\nSumaTotal:', suma)
        self.objHistorial.generarHistorial('\nProbabilidades\n', data)
