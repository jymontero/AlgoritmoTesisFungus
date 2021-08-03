from datetime import datetime
from InterNotificadora import InterNotificadora
from InterObserver import InterObserver
import random
import pandas as pd
import time
from EstructuraVuelo import EstructuraVuelo

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
        print('***********FIN LISTA ORDENADA *********\n')


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
                #print(contador)
                #print(len(vueloData.index)-1)
                if contador == len(vueloData.index):
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

                InicioReparacion = time.time()
                self.buscarEmparejamiento(tuplaIncidente)
                FinReparacion = time.time()
                tiempoRespuesta = FinReparacion - InicioReparacion
                print('Tiempo Respuesta: ', tiempoRespuesta)
                break

    def buscarEmparejamiento(self, tupla):
        tuplaInfectada = tupla
        vuelosInfectados = tuplaInfectada[0]
        fechaSalida = tuplaInfectada[1]
        base = tuplaInfectada[2]
        numEmparejamiento = tuplaInfectada[3] + 1

        listaVuelosBase = self.cultivoTratar.get(base)
        if numEmparejamiento < len(listaVuelosBase):
            for data in listaVuelosBase:
                posicion = data[3]
                if posicion == numEmparejamiento:
                    self.estructuraVuelos(data, tuplaInfectada)
        else:
            print('No hay donde ubicar los emparejamientos\n')

    def estructuraVuelos(self, tupla, tuplaInfect):
        objEstructuraVueos = EstructuraVuelo()
        objEstructuraVueos.estructurasVuelos(tupla, tuplaInfect)

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



