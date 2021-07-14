import pandas as pd
import os

RUTA_DATASET = 'dataset/'

class DataSet:

   def __init__(self):
      self.data_FrameP = pd.DataFrame()
      #self.dataAirport = []
      #self.listaBases = []
      #self.dictnary_Base_Aer = {}

#Metodo que devuelve el dataSet
   def getDataFramePP(self):
      return self.data_FrameP

#Metodo que listael conido de un directorio
   def sizeDirectory(self):
      contenido = os.listdir(RUTA_DATASET)
      return contenido

#Descripción = Metodo que carga el dataframe de un directorio
#Parametrros =
   def cargaDataset(self):

      try:
         contenido = self.sizeDirectory()

         for data in contenido:
               dataRead = pd.read_csv(RUTA_DATASET + data, keep_default_na = True)
               self.data_FrameP = pd.concat([self.data_FrameP,dataRead])
               self.data_FrameP.reset_index(drop=False)

         self.data_FrameP = self.data_FrameP.reset_index(drop=True)
         #self.data_FrameP.reindex()
      #self.addTimeFly()
      #self.createColumn('pheromone')
      #self.distintData(' airport_dep ')
      #self.crearDiccionario()
         print('Dataset cargado...')

         return self.data_FrameP

      except:
         return print("Ruta del dataSet no encontrada...")

"""
carga  = DataSet()
carga.cargaDataset()
"""


'''
   def printed(self, data):
      const = len(data)
      for data3 in data:
         print(data3)

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

#Metodo que filtra datos de acuerdo a una columna del dataframe
   def distintData(self, columnNam):
      self.dataAirport = pd.unique(self.data_Frame[columnNam])
      aux = pd.DataFrame()

      for base in self.dataAirport:
         aux = self.uniqueData(columnNam,base)
         self.listaBases.append(aux)

#Metodo que recorre un dataFrame
   def recorrerDataFrame(self, dataF):
         aux = pd.DataFrame()
         for indiceF, fila in  aux.iterrows():
            print(fila)

#Metodo que obtiene el tiempo de vuelo
   def getTimeFly(self, row):
      hora_dep = (row[' hour_dep '])
      hora_arr = (row[' hour_arr'])
      listHora_dep = hora_dep.lstrip().split(sep=':')
      listHora_arr = hora_arr.lstrip().split(sep= ':')
      minuto = self.horasObj.tiempoVuelo(listHora_arr,listHora_dep)
      return minuto

   def createColumn(self,nameColum):
      self.data_Frame[nameColum] = self.data_Frame.apply(self.getPheromona,axis=1)

   def getPheromona(self,row):
      tiempo_vuelo = (row['time_fly'])
      #return 1/ self.data_Frame.size
      return 0.1


#Metodo que agrega una columna con el tiempo de vuelo
   def addTimeFly(self):
      self.data_Frame['time_fly']= self.data_Frame.apply(self.getTimeFly,axis=1)

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
'''
