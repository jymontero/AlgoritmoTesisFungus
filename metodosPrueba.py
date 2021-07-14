from datetime import datetime, date, time, timezone, timedelta
from DataSetTransform import DataSetTransform
import pprint
import pandas as pd
from IPython.core.display import display
import random

class Metodo():
    def __init__(self):
        pass

    def sumarDia(self,fecha, dias):
        FORMATO = ' %Y-%m-%d '
        dateSelect = datetime.strptime(fecha, FORMATO)
        delta  = dateSelect + timedelta(days = dias)
        delta  = datetime.date(delta)
        delta2 = delta.strftime(' %Y-%m-%d ')

    #def restarFechas(self, fecha1, hora1, fecha2, hora2):
    def restarFechas(self, fecha1,fecha2):
        fechaSalida = fecha1
        fechaLLegada = fecha2
        FORMATO = '%Y-%m-%d %H:%M'
        date = datetime.strptime(fechaSalida,FORMATO)
        date2 = datetime.strptime(fechaLLegada,FORMATO)
        #restarFecha = date2 - date
        restarFecha = date2 - date
        dias = restarFecha.days
        segundos = restarFecha.seconds
        minutos = (restarFecha.seconds)/60
        horas =  (restarFecha.seconds)//3600
        print('Dias: ', dias)
        print('Segundos:',segundos )
        print('Minutos: ', minutos)
        print('Horas:', horas)


    def aleatorio(self):
        for i in range(50):
            print('Iteracion: ', i)
            print(random.triangular(0,1,0.5))
            print(random.random())

#objManipulacion = DataSetTransform()
#objManipulacion.init_transform()

#pd.set_option('display.max_columns', None)
#pd.option_context('display.max_columns',None)


##vertices = objManipulacion.dictnary_Base_Aer
#nodos = objManipulacion.dataAirport

"""def displaydf(dataframe, cols = None, rows = None):
    with pd.option_context("display.max_columns", cols):
        with pd.option_context("display.max_rows", rows):
            display(dataframe)
    return True
for nodo in nodos:
    vertice = vertices[nodo]
    displaydf(vertice)

pprint.pprint(vertices, width=80, compact=False, depth=3)

"""
objMEtodo = Metodo()
"""#objMEtodo.restarFechas(' 2000-01-26 ',' 23:55', ' 2000-01-27 ', ' 23:20')
objMEtodo.restarFechas('2000-01-10 00:22', '2000-01-11 23:00')
#objMEtodo.sumarDia(' 2000-01-23 ',15)"""
objMEtodo.aleatorio()