from DataSet import DataSet
from DataSetOperacion import  DataSetOperacion
from OperacionAcoFu import OperacionACOFungus

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
        self.datos = self.objDataSet.cargaDataset()

    def getDatos(self):
        return self.datos

    def init_transform(self):
        self.setDatos()
        self.feromonaInicial('feromona')
        self.visibilidadPeso('costo')
        self.estadoIncidente('incidente',0)
        self.objOperacion.distintData2(' airport_dep ', self.datos)
        self.objOperacion.crearDiccionario()
        self.dataAirport = self.objOperacion.getDataAirport()
        self.listaBases = self.objOperacion.getListaBases()
        self.dictnary_Base_Aer = self.objOperacion.getBasesConexiones()
        #print(self.dictnary_Base_Aer)

    def feromonaInicial(self, nombreCol):
        self.datos = self.objOperacion.crearColumnaDataF(nombreCol, self.datos)

    def visibilidadPeso(self, nombreCol):
        self.datos = self.objOperacion.crearColumVisibilidad(nombreCol,self.datos)

    def estadoIncidente(self, nombreCol, valor):
        self.datos = self.objOperacion.createColumn(nombreCol, valor)



