import pandas as pd
import os

RUTA_DATASET = 'dataset/'
class DataSet:

   def __init__(self):
      pd.set_option('display.max_rows', None)
      self.data_FrameP = pd.DataFrame()
      self.datos50 = pd.DataFrame()

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

         self.data_FrameP = self.data_FrameP.reset_index(drop=True)
         print('Dataset cargado...')

         self.cargaDataSet50(0.50)
         return self.data_FrameP

      except:
         return print("Ruta del dataSet no encontrada...")

   def cargaDataSet50(self, porcentaje):
      self.cargaDataSet50 = self.data_FrameP.sample(frac = porcentaje, replace=False)
      self.cargaDataSet50 = self.cargaDataSet50.reset_index(drop=True)
