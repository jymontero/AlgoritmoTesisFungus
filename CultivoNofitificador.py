from datetime import datetime
from InterNotificadora import InterNotificadora
from InterObserver import InterObserver
import random
import pandas as pd

class CultivoNotificador(InterNotificadora):

    def __init__(self, cultivo):
        pd.set_option('display.max_columns', None)
        self.cultivoTratar = cultivo
        #self.vueloEjecutados = pd.DataFrame()
        self.listaOrdenada = []
        self._observers = []
        self.listaVuelosEjecutados = []

    def tratarCultivo(self):
        dataValues = self.cultivoTratar.values()
        listaAux = []
        for data in dataValues:
            listaAux = data
            self.listaOrdenada = self.listaOrdenada + listaAux

        self.listaOrdenada = sorted(self.listaOrdenada, key= self.sortByDate)
        print('TamanioListORdenda',len(self.listaOrdenada))
        print(self.listaOrdenada)
        print('***********FIN LISTA ORDENADA *********')


    def sortByDate(self, elem):
        return datetime.strptime(elem[1],' %Y-%m-%d ')
        #lista.sort(key= sortByDate)

    def ejecutarCultivo(self):
        for vuelos in self.listaOrdenada:
            self.iterarVuelos(vuelos)

    def iterarVuelos(self, vuelo):
        print('VUELOS COSECHAR\n', vuelo)
        vueloEjecutados = pd.DataFrame()
        vueloData = vuelo[0]
        fechaSalida = vuelo[1]
        base = vuelo[2]
        numeroEmparejamiento = vuelo[3]
        contador = 0

        for i in range(len(vueloData.index)):
            incidente = int(vueloData['incidente'][i])
            if incidente == 0:
                contador+=1
                vueloEjecutado = vueloData.iloc[i]
                vueloEjecutados = vueloEjecutados.append(vueloEjecutado)
                print(contador)
                print(len(vueloData.index)-1)
                if contador == len(vueloData.index) - 1:
                    self.listaVuelosEjecutados.append(vueloEjecutados)
                    tuplaInfo = (vueloEjecutados, base, numeroEmparejamiento)
                    self.notificarObserver('ejecucion', tuplaInfo)
                    self.actualizarDatosCultivo(base, numeroEmparejamiento)

            if incidente == -1:
                self.listaVuelosEjecutados.append(vueloEjecutados)
                tuplaInfo = (vueloEjecutados, base, numeroEmparejamiento)
                self.notificarObserver('ejecucion', tuplaInfo)
                self.actualizarDatosCultivo(base, numeroEmparejamiento)
                vueloIncidente= vueloData.iloc[i:len(vueloData.index) + 1]
                tuplaIncidente = (vueloIncidente, fechaSalida, base, numeroEmparejamiento)
                self.notificarObserver('incidente', tuplaIncidente)
                self.buscarEmparejamiento(tuplaIncidente)
                break

    def buscarEmparejamiento(self, tupla):
        vuelosInfectados = tupla[0]
        fechaSalida = tupla[1]
        base = tupla[2]
        numEmparejamiento = tupla[3] + 1

        listaVuelosBase = self.cultivoTratar.get(base)
        for data in listaVuelosBase:
            posicion = data[3]
            if posicion == numEmparejamiento:
                #print(data)
                print('')

    def estruturarVuelos(self, tupla):
        pass



    def actualizarDatosCultivo(self, base, posicionEmparj):
        listaVuelosBase = self.cultivoTratar.get(base)
        listaAux = []
        for data in listaVuelosBase:
            posicion = data[3]
            if posicion != posicionEmparj:
                listaAux.append(data)

        self.cultivoTratar[base] = listaAux

    def initCultivo(self):
        self.tratarCultivo()
        self.ejecutarCultivo()

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



