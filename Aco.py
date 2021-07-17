import random as rn
import numpy as np
import matplotlib.pyplot as plt
import random as random
import pandas as pd

from numpy.random import choice as np_choice
from math import sqrt
from DataSetTransform import DataSetTransform
from OperacionAcoFu import OperacionACOFungus
from Probabilidad import Probabilidad
from Restriccion import Restriccion
from Penalizacion import Penalizacion
from Feromona import Feromona
from Cultivo import Cultivo
from Historial import Historial
from InterObserver import InterObserver
from InterNotificadora import InterNotificadora
from CultivoNofitificador import CultivoNotificador
from registroEjecucion import RegistroEjecucion
from registroIncicente import RegistroIncidente
class AntColony(object):

    def __init__(self, vertices, nodos, n_ants, n_best, n_iterations, decay, alpha=1, beta=1, apre=1):

        pd.set_option('display.max_columns', None)

        self.vertices = vertices
        self.nodos = nodos
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.aprendizajeQ = apre
        self.hojasCultivo = 0

        self.dicHormigas = {}
        self.verticesCopy = {}
        self.cultivoACO = {}
        self.listaPenalizacion = []
        self.listaEvaluacion = []
        self.nodosBases = (' BASE1 ', ' BASE2 ', ' BASE3 ')

        self.nodosAdyacentes = pd.DataFrame()
        self.copiaNodosAdyacentes = pd.DataFrame()
        self.nodosRecorridos = pd.DataFrame()
        self.dataHormigaNodos = pd.DataFrame()
        self.objHistorial = Historial()
        self.objOperacionFungus = OperacionACOFungus()
        self.objRestriccion = Restriccion()
        self.objPenalizacion = Penalizacion(self.objHistorial)
        self.objCultivo = Cultivo(self.nodosBases)
        self.objFeromona = Feromona(self.decay, self.aprendizajeQ, self.objHistorial)
        self.objProbabilidad = Probabilidad(self.alpha, self.beta, self.objHistorial)

        self.nodosVisitados = set()

        self.contadorB1 = 0
        self.contadorB2 = 0
        self.contadorB3 = 0

    def run(self):
        self.hojasCultivo = self.objCultivo.controlCultivoGlobal(self.vertices)
        print('\nVuelos Operar:', self.hojasCultivo)
        #self.objHistorial.parametrosInciales(self.n_iterations, self.n_ants, self.aprendizajeQ, self.alpha, self.beta)

        all_paths = []

        while (self.hojasCultivo > 850):
            for i in range(self.n_iterations):
                all_paths = self.gen_all_paths()
                self.vertices = self.objFeromona.evaporacionGlobalFeromona(self.nodos, self.vertices)

            self.cultivoACO = self.objCultivo.cultivar(all_paths)
            self.vertices = self.objFeromona.eliminarNodos(self.cultivoACO, self.vertices)
            self.inyectarFeromona()
            print('**************NODOS EN EL CULTIVO************')
            self.controlCultivo(self.vertices)

        cultivoCosechar = self.objCultivo.getCultivoClasificado()
        objCultivoNotificador =  CultivoNotificador(cultivoCosechar)
        objRegistroIncidente  = RegistroIncidente('incidente')
        objRegistroEjecucion = RegistroEjecucion('ejecucion')
        objCultivoNotificador.registrarObserver(objRegistroIncidente)
        objCultivoNotificador.registrarObserver(objRegistroEjecucion)
        objCultivoNotificador.initCultivo()

    def gen_all_paths(self):
        all_paths = []

        for i in range(self.n_ants):
            baseInicio = self.randomBase()
            path = self.gen_path(baseInicio)
            path, evaluacion, estadoBase = self.objPenalizacion.evaluarRestriccion(path)
            path = self.objFeromona.cantidadFeromonaDepositar(path)

            self.vertices = self.objFeromona.actualizarDataVertices(path, self.vertices)
            path = path.drop(columns=['penalVuelo', 'penalDuty', 'penalizacion'])
            all_paths.append((i, path, evaluacion, baseInicio, estadoBase))

        return all_paths

    def gen_path(self, start):

        self.nodosRecorridosAnt = pd.DataFrame()
        self.nodosVisitados.add(start)

        base = start
        prev = start

        self.nodosAdyacentes = self.vertices.get(prev)
        #fecha = self.nodosAdyacentes.loc[0][' date_dep ']
        #self.agrupar(fecha)
        self.copiaNodosAdyacentes = self.nodosAdyacentes.copy()
        self.objProbabilidad.evaluarProbabilidad(self.copiaNodosAdyacentes)
        contador = 0

        while True:
            saltoVuelo, aeroDestino, idVuelo, fechaArr, horaDep = self.objProbabilidad.obtenerSiguienteNodo()

            while idVuelo in self.nodosVisitados:
                saltoVuelo, aeroDestino, idVuelo, fechaArr, horaDep = self.objProbabilidad.obtenerSiguienteNodo()

            self.nodosVisitados.add(idVuelo)
            contador+=1
            prev = aeroDestino
            self.nodosRecorridosAnt  = self.nodosRecorridosAnt.append(saltoVuelo)

            if contador >= 12 and base == prev:
                break
            if fechaArr >= ' 2000-02-01':
                break

            self.nodosAdyacentes = self.vertices.get(prev)
            self.agruparFecha(fechaArr, horaDep)

            self.copiaNodosAdyacentes = self.nodosAdyacentes.copy()

            if len(self.copiaNodosAdyacentes.index) == 0:
                self.nodosAdyacentes = self.vertices.get(prev)
                self.agruparSinFecha(fechaArr, horaDep)
                self.copiaNodosAdyacentes = self.nodosAdyacentes.copy()

                if len(self.copiaNodosAdyacentes.index) == 0:
                    break

            self.objProbabilidad.evaluarProbabilidad(self.copiaNodosAdyacentes)

        self.nodosVisitados.clear()
        self.nodosRecorridosAnt = self.nodosRecorridosAnt.reset_index(drop=True)
        self.nodosRecorridosAnt = self.nodosRecorridosAnt.drop(columns=['visibilidad','probabilidad','sumAcumu'])

        return self.nodosRecorridosAnt

#Elige una base para cada hormiga
    def randomBase(self):
        return (random.choice(self.nodosBases))

    def agruparFecha(self, fecha, hora):
        #mirar bien la logica se cambio a date_dep etsa ba en date_arr
        self.nodosAdyacentes = self.nodosAdyacentes[self.nodosAdyacentes[' date_dep '] == fecha]
        self.nodosAdyacentes = self.nodosAdyacentes[self.nodosAdyacentes[' hour_dep '] >= hora]

    def agrupar(self, fecha):
        self.nodosAdyacentes = self.nodosAdyacentes[self.nodosAdyacentes[' date_dep '] <= fecha]

    def agruparSinFecha(self, fecha, hora):
        fechaPosterior = self.objRestriccion.sumarDia(fecha, 1)
        self.nodosAdyacentes = self.nodosAdyacentes[self.nodosAdyacentes[' date_dep '] == fechaPosterior]
        self.nodosAdyacentes = self.nodosAdyacentes[self.nodosAdyacentes[' hour_dep '] <= hora]

    def inyectarFeromona(self):
        for nodo in self.nodos:
            data = self.vertices.get(nodo)
            dataCopia = data.copy()
            dataCopia['feromona'] = dataCopia.apply(self.objOperacionFungus.inyeccionFeromona, axis = 1)
            self.vertices[nodo] = dataCopia


    def controlCultivo(self, listaBorrar):
        self.hojasCultivo = self.objCultivo.controlCultivoGlobal(self.vertices)
        print('Cantidad Vuelos Actual:', self.hojasCultivo)

objManipulacion = DataSetTransform()
objManipulacion.init_transform()
vertices = objManipulacion.dictnary_Base_Aer
nodos = objManipulacion.dataAirport

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

ant_colony = AntColony(vertices, nodos, 50, 0, 5, 0.8, alpha=1, beta=3, apre=1)
ant_colony.run()

"""
    Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        Example:
            ant_colony = AntColony(distances, 100, 20, 2000, 0.95, alpha=1, beta=2)
"""