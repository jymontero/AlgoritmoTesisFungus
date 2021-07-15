from datetime import datetime
from InterNotificadora import InterNotificadora
from InterObserver import InterObserver
import random
import pandas as pd

class CultivoNotificador(InterNotificadora):

    def __init__(self, cultivo):
        self.cultivoTratar = cultivo
        #self.vueloEjecutados = pd.DataFrame()
        self.listaOrdenada = []
        #self.objNotificador = InterNotificadora()
        self._observers = []
        self.listaVuelosEjecutados = []

    def tratarCultivo(self, data):
        dataValues = data.values()
        lista = []
        for data in dataValues:
            listaAux = data
            lista = lista + listaAux

        listaOrdenaFecha = sorted(lista, key= self.sortByDate)
        print('TamanioListORdenda',len(listaOrdenaFecha))
        return listaOrdenaFecha

    def sortByDate(self, elem):
        return datetime.strptime(elem[1],' %Y-%m-%d ')
        #lista.sort(key= sortByDate)

    def generarAccidente(self, data):
        for i in range(5):
            elegido =  random.choice(data)
            dataNueva = self.vueloAccidenado(elegido,1)

    def vueloAccidenado(self, data, elegir):
#        dataAux = pd.DataFrame()
        dataAux = data[0]
        #self.dataNotificador = data1.copy()
        size = len(dataAux.index)
        #print('Tamanio dataframe:', size)
        aleatorio = random.randint(0, size-1)
        #print('# Aleatorio', aleatorio)

        for i in range(size - 1):
            if i == aleatorio:
                #dataAux = dataAux.sample(elegir)
                #data1['incidente'] = data1[''].apply(lambda x :((1 - self.decay)* x))
                dataAux.loc[aleatorio,'incidente'] = -1
                break
        return dataAux

    def ejecutarCultivo(self,data):
        for vuelos in data:
            self.iterarVuelos(vuelos)

    def iterarVuelos(self, vuelo):
        vueloEjecutados = pd.DataFrame()
        vueloData = vuelo[0]
        fechaSalida = [1]
        base = vuelo[2]
        numeroEmparejamiento = vuelo[3]

        for i in range(len(vueloData.index) - 1):
            incidente = int(vueloData['incidente'][i])
            if incidente == 0:
                vueloEjecutado = vueloData.iloc[i]
                vueloEjecutados = vueloEjecutados.append(vueloEjecutado)
            else:
                self.listaVuelosEjecutados.append(vueloEjecutados)
                tuplaInfo = (vueloEjecutados, base, numeroEmparejamiento)
                self.notificarObserver('ejecucion', tuplaInfo)
                self.actualizarDatosCultivo(base, numeroEmparejamiento)

                vueloIncidente= vueloData.iloc[i:len(vueloData.index) + 1]
                tuplaIncidente = (vueloIncidente, fechaSalida, base, numeroEmparejamiento)
                self.notificarObserver('incidente', tuplaIncidente)
                break

    def actualizarDatosCultivo(self, base, posicionEmparj):
        listaVuelosBase = self.cultivoTratar.get(base)
        listaVuelosBase = listaVuelosBase.pop(posicionEmparj)
        self.cultivoTratar[base] = listaVuelosBase

    def initCultivo(self):
        cultivoTratado = self.tratarCultivo(self.cultivoTratar)
        self.generarAccidente(cultivoTratado)
        self.ejecutarCultivo(cultivoTratado)

    def registrarObserver(self, observer: InterObserver):
        if observer not in self._observers:
            self._observers.append(observer)
        else:
            print("Fallo agregar Observador")

    def removerObserver(self, observer: InterObserver):
        try:
            self._observers.remove(observer)
        except ValueError:
            print("Fallo al eliminar")

    def notificarObserver(self, tipoEvento, value):
        evento = tipoEvento
        for observer in self._observers:
            if observer.name == evento:
                observer.notify_changes(value)
                break

    def notificarAllObserver(self, value):
        for observer in self._observers:
            observer.notify_changes(value)



