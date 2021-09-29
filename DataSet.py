import pandas as pd
import os

RUTA_DATASET = 'dataPruebaS3/'
class DataSet:

   def __init__(self):
      pd.set_option('display.max_rows', None)
      self.data_FrameP = pd.DataFrame()
      self.datosPorcentaje = pd.DataFrame()

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

         #self.data_FrameP = self.cargaDatosPorcentaje(0.50)
         #return self.data_FrameP

      except:
         return print("Ruta del dataSet no encontrada...")

   def cargaDatosPorcentaje(self, porcentaje):
      if porcentaje == 1:
         return self.data_FrameP
      else:
         self.datosPorcentaje = self.data_FrameP.sample(frac = porcentaje, replace=False)
         self.datosPorcentaje = self.datosPorcentaje.reset_index(drop=True)
         return self.datosPorcentaje
