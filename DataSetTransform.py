from DataSet import DataSet
from DataSetOperacion import  DataSetOperacion
from OperacionAcoFu import OperacionACOFungus
import math
import random


import pandas as pd

class DataSetTransform:

    def __init__(self):
        self.objOperacion = DataSetOperacion()
        self.objDataSet =  DataSet()
        self.datos  = pd.DataFrame()
        self.dataAirport = []
        self.listaBases = []
        self.dictnary_Base_Aer = {}

    def setDatos(self):
        self.objDataSet.cargaDataset()
        self.datos = self.objDataSet.cargaDatosPorcentaje(1)

    def getDatos(self):
        return self.datos

    def init_transform(self):
        self.setDatos()
        self.feromonaInicial('feromona')
        self.visibilidadPeso('costo')
        self.vueloNopenalizable('noPenalizable',0)
        self.penalizacionVuelo('penalVuelo',0)
        self.penalizacionDuty('penalDuty',0)
        self.estadoIncidente('incidente',0)
        self.vueloAccidentado(1)
        self.objOperacion.distintData2(' airport_dep ', self.datos)
        self.objOperacion.crearDiccionario()
        self.dataAirport = self.objOperacion.getDataAirport()
        self.listaBases = self.objOperacion.getListaBases()
        self.dictnary_Base_Aer = self.objOperacion.getBasesConexiones()

    def feromonaInicial(self, nombreCol):
        self.datos = self.objOperacion.crearColumnaDataF(nombreCol, self.datos)

    def visibilidadPeso(self, nombreCol):
        self.datos = self.objOperacion.crearColumVisibilidad(nombreCol,self.datos)

    def penalizacionVuelo(self, nombreCol, valor):
        self.datos = self.objOperacion.createColumn(nombreCol, valor)

    def penalizacionDuty(self, nombreCol, valor):
        self.datos = self.objOperacion.createColumn(nombreCol, valor)

    def estadoIncidente(self, nombreCol, valor):
        self.datos = self.objOperacion.createColumn(nombreCol, valor)

    def vueloNopenalizable(self, nombreCol, valor):
        self.datos = self.objOperacion.createColumn(nombreCol, valor)

    def vueloAccidentado(self, porcentaje):
        size = len(self.datos.index)
        porcentajeAccidente = round((size * porcentaje)/ 100)
        print('Vuelos Infectados (Probabilidad de Incidente): ', porcentajeAccidente)

        for i in range (porcentajeAccidente):
            aleatorio = random.randint(0, size-1)
            self.datos.loc[aleatorio,'incidente'] = -1



