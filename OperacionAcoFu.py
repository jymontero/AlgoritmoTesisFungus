import random as rd
from Restriccion import Restriccion
from Historial import Historial
import numpy as np
import math
class OperacionACOFungus():

    def __init__(self):
        self.objRestriccion = Restriccion()
        self.objHistorial = Historial()


    def inyeccionFeromona(self, row):
        return 0.01

    def inyeccionVisibilidad(self, row):
        hora_dep = (row[' hour_dep '])
        hora_arr = (row[' hour_arr'])
        listHora_dep = self.objRestriccion.splitHora(hora_dep)
        listHora_arr = self.objRestriccion.splitHora(hora_arr)
        """listHora_dep = hora_dep.lstrip().split(sep=':')
        listHora_arr = hora_arr.lstrip().split(sep= ':')"""
        minuto = self.objRestriccion.tiempoVuelo(listHora_arr,listHora_dep)
        return minuto

    def generarAleatorio(self):
        #return (rd.uniform(0.001,1).__round__(6))
        #aleatorio = round((rd.random()),5)
        aleatorio = rd.uniform(0.0, 0.9999)
        return aleatorio

    def busquedaBinaria(self, lista, numero):
        #print('NumeroBuscar', numero)
        #print('LIsta', lista)
        #print('TamanioLista', len(lista))
        izq = 0
        der = len(lista) - 1
        mini = min(lista)
        #print(mini)
        maxo = max(lista)
        #print(maxo)
        aux = []

        if numero < lista[izq]:
            aux = lista[izq]
            return aux
        else:
            while (izq <= der) and (mini <= numero <= maxo):
                medio = math.floor((izq + der) / 2)

                if lista[medio] == numero:
                    return medio
                elif lista[medio] < numero:
                    izq = medio
                else:
                    der = medio

                aux = lista[izq:der+1]
                mini = min(aux)
                maxo = max(aux)

                if len(aux) <=2:
                    break
        return max(aux)

    def getSalto (self, probab, data):
        #self.objHistorial.generarHistorial('ProbabiliadaLista:', probab)
        data2 = data
        saltoVuelo = data2[data2.sumAcumu == probab]
        saltoVuelo = saltoVuelo.reset_index(drop=True)
        #self.objHistorial.generarHistorial('SaltoNodo \n', saltoVuelo)
        #print(saltoVuelo)
        aeropuertoDestino = saltoVuelo.iloc[0][' airport_arr ']
        idVuelo = saltoVuelo.iloc[0]['#leg_nb ']
        fechallegada = saltoVuelo.iloc[0][' date_arr ']
        #Se puede cambiar despues por la hora de llegada
        horaSalida = saltoVuelo.iloc[0][' hour_arr']
        #saltoVuelo = saltoVuelo.drop(columns = ['sumAcumu', 'probabilidad'])
        return saltoVuelo, aeropuertoDestino, idVuelo, fechallegada, horaSalida