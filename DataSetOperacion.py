import pandas as pd
from OperacionAcoFu import OperacionACOFungus

class DataSetOperacion:

    def __init__(self):
        self.objOperacionACO  = OperacionACOFungus()
        self.dataFrameOpera = pd.DataFrame()
        self.dataAirport = []
        self.listaBases = []
        self.dictnary_Base_Aer = {}

    def uniqueColumn(self,nameColum,data):
        data3 = pd.DataFrame()
        data3 = data[nameColum]
        return data3

#Metod que filtra todas las filas de un datafram
#nameColumn: nombre de la columna por el cual filtrar
#conditional: condicion de filtrado
    def uniqueData(self,nameColum, conditional):
        data3 = pd.DataFrame()
        database = pd.DataFrame()

        data3 = self.data_Frame[nameColum] == conditional
        database = self.data_Frame[data3]
        return database

    def uniqueData(self,nameColum, conditional, data):
        data3 = pd.DataFrame()
        database = pd.DataFrame()

        data3 = data[nameColum] == conditional
        database = data[data3]
        return database

#Metodo que filtra datos de acuerdo a una columna del dataframe
    def distintData(self, columnNam):
        self.dataAirport = pd.unique(self.data_Frame[columnNam])
        aux = pd.DataFrame()

        for base in self.dataAirport:
            aux = self.uniqueData(columnNam,base)
            aux = aux.reset_index(drop=True)
            self.listaBases.append(aux)

    def distintData2(self, columnNam, data):
        self.dataAirport = pd.unique(data[columnNam])
        aux = pd.DataFrame()

        for base in self.dataAirport:
            aux = self.uniqueData(columnNam,base, data)
            #aux.sort_values(' date_dep ', ascending= False)
            aux = aux.sort_values([' date_dep ',' hour_dep '], ascending= True)
            aux = aux.reset_index(drop=True)
            self.listaBases.append(aux)

#Metodo que recorre un dataFrame
    def recorrerDataFrame(self, dataF):
            aux = pd.DataFrame()
            for indiceF, fila in  aux.iterrows():
                print(fila)

    def createColumn(self, nameColum, valorDefecto):
        self.dataFrameOpera[nameColum] = valorDefecto
        return self.dataFrameOpera

    def crearColumnaDataF(self, nombreCol, data):
        self.dataFrameOpera = data
        self.dataFrameOpera[nombreCol] = self.dataFrameOpera.apply(self.objOperacionACO.inyeccionFeromona, axis = 1)
        return self.dataFrameOpera

    def crearColumVisibilidad(self, nombreCol, data):
        self.dataFrameOpera = data
        self.dataFrameOpera[nombreCol] = self.dataFrameOpera.apply(self.objOperacionACO.inyeccionVisibilidad, axis= 1)
        return self.dataFrameOpera

#Metodo que crear un diccionario Clave:nombre de aeropuerto obase
#valor es el listado de todos los vuelos que parten  de aeropuerto o base
    def crearDiccionario(self):
        self.dictnary_Base_Aer = dict(zip(self.dataAirport,self.listaBases))

#Retorna el datafraeme
    def getDataFrame(self):
        return self.data_Frame

    def getDataAirport(self):
        return self.dataAirport

#retorna listadebases
    def getListaBases(self):
        return self.listaBases

    def getBasesConexiones(self):
        return self.dictnary_Base_Aer
