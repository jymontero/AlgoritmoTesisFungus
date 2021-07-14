import pandas as pd
from InterObserver import InterObserver
import time

class RegistroEjecucion(InterObserver):

    def __init__(self, name):
        InterObserver.__init__(self, name)
        self.listaEjecucion = []
        self.dataFrameOpera = pd.DataFrame()
        self.nodosRecorridosAnt  = pd.DataFrame()

    def notify_changes(self, data):
        tuplaInfo = data
        print('\n****REGISTRO EJECUCION****\n')
        print('Base De salida: ', tuplaInfo[1])
        print('Emparejamiento: ', tuplaInfo[2])
        print('Vuelos en Ejecucion.....')
        time.sleep(10)
        print('Vuelos Ejecutados: \n', tuplaInfo[0])

    def getVuelosEjecutados(self):
        pass
