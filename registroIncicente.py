from InterObserver import InterObserver
import pandas as pd

class RegistroIncidente(InterObserver):

    def __init__(self, name):
        InterObserver.__init__(self,name)

    def notify_changes(self, data):
        tuplaIncidente = data
        print('\n**** REGISTRO INCIDENTE ****\n')
        print('Base De salida: ', tuplaIncidente[2])
        print('Emparejamiento: ', tuplaIncidente[3])
        print('Vuelos Sin Ejecutadar: \n', tuplaIncidente[0])
        print('Reorganizando Vuelos.....')
