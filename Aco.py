import random as rn
import numpy as np
import matplotlib.pyplot as plt
import random as random
import pandas as pd
import time


#from numpy.random import choice as np_choice
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
from Graficas import Grafica
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
        self.dataEvaluacion = {}
        self.verticesCopy = {}
        self.cultivoACO = []
        self.listaPenalizacion = []
        self.listaEvaluacion = []
        self.contadorVuelos = []
        self.contadorEmparejamientos = []
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
        self.objGraficas = Grafica()

        self.nodosVisitados = set()

        self.contadorB1 = 0
        self.contadorB2 = 0
        self.contadorB3 = 0

        #self.contadorIterLocalVuelo = 0
        #self.contadorIterLocalEmpareja = 0
        self.contadorIterGlobalVuelo = 0
        self.contadorIterGlobalEmpareja = 0

        self.ficheroEvaluacionGlobal = open("dataGraficar/dataEvaluacionGlobal.txt", 'w')

    def run(self):
        self.setTipoHojas(self.nodosBases)
        self.hojasCultivo = self.objCultivo.controlCultivoGlobal(self.vertices)
        print('\nVuelos Operar:', self.hojasCultivo)
        #self.objHistorial.parametrosInciales(self.n_iterations, self.n_ants, self.aprendizajeQ, self.alpha, self.bet
        iteracionParada = 0
        numeroIteracionesGlobales = 0
        listaItera = []
        dicDatos = {}
        Inicio = time.time()

        all_paths = []
        all_paths_general = []

        ficheroLocal = open("dataGraficar/dataLocal.txt", 'w')
        ficheroLocalGeneral = open("dataGraficar/dataLGeneral.txt", 'w')
        ficheroEvaluacionLocal = open("dataGraficar/dataEvaluacionLocal.txt", 'w')
        ficheroGlobal = open("dataGraficar/dataGlobal.txt", 'w')

        ficheroTiempoEjecucionLocal = open("dataGraficar/dataEjecucionLocal.txt", 'w')
        ficheroTiempoEjecucionGlobal = open("dataGraficar/dataEjecucionGlobal.txt", 'w')
        ficheroCrecimientoCultivo = open("dataGraficar/dataCrecimientoCultivo.txt", 'w')


        while (self.hojasCultivo > 0):
            print('Iteracion: ', numeroIteracionesGlobales)
            listaItera.append(numeroIteracionesGlobales)
            InicioGlobal = time.time()

            for i in range(self.n_iterations):
                InicioLocal = time.time()
                itera = i
                all_paths = self.gen_all_paths()
                finLocal = time.time()
                tiempoEjecucionLocal = round((finLocal-InicioLocal),2)

                ficheroTiempoEjecucionLocal.write(str(itera))
                ficheroTiempoEjecucionLocal.write(',')
                ficheroTiempoEjecucionLocal.write(str(tiempoEjecucionLocal)+"\n")

                empareja, vuelos = self.estadisticaIteracionesLocales(all_paths)
                ficheroLocal.write(str(itera))
                ficheroLocal.write(',')
                ficheroLocal.write(str(empareja))
                ficheroLocal.write(',')
                ficheroLocal.write(str(vuelos)+"\n")

                evaluacion = self.estadisticasEvaluaciones(all_paths)
                ficheroEvaluacionLocal.write(str(itera))
                ficheroEvaluacionLocal.write(',')
                ficheroEvaluacionLocal.write(str(evaluacion)+"\n")


                self.vertices = self.objFeromona.evaporacionGlobalFeromona(self.nodos, self.vertices)

            finGlobal = time.time()
            tiempoEjecucionGlobal = round((finGlobal- InicioGlobal), 2)

            ficheroTiempoEjecucionGlobal.write(str(numeroIteracionesGlobales))
            ficheroTiempoEjecucionGlobal.write(',')
            ficheroTiempoEjecucionGlobal.write(str(tiempoEjecucionGlobal)+"\n")

            print(all_paths)

            empareja2, vuelos2 = self.estadisticaIteracionesLocales(all_paths)
            ficheroLocalGeneral.write(str(numeroIteracionesGlobales))
            ficheroLocalGeneral.write(',')
            ficheroLocalGeneral.write(str(empareja2))
            ficheroLocalGeneral.write(',')
            ficheroLocalGeneral.write(str(vuelos2)+"\n")


            """evaluacionGobal = self.estadisticasEvaluaciones(all_paths)
            ficheroEvaluacionGlobal.write(str(numeroIteracionesGlobales))
            ficheroEvaluacionGlobal.write(',')
            ficheroEvaluacionGlobal.write(str(evaluacionGobal)+"\n")"""

            #devuelve los vuelos a cultivar, y la mejor evaluacon por base
            self.cultivoACO, dicDatos  = self.objCultivo.cultivar(all_paths)

            if len(self.cultivoACO) == 0:
                iteracionParada+=1
            else:
                iteracionParada = 0

            print('*****Nodos Cultivo***\n',self.cultivoACO)

            #lo que cumple con restricciones
            emparejamientosCultivo, vuelosCultivo = self.estadisticaCultivo(self.cultivoACO)
            ficheroCrecimientoCultivo.write(str(numeroIteracionesGlobales))
            ficheroCrecimientoCultivo.write(',')
            ficheroCrecimientoCultivo.write(str(emparejamientosCultivo))
            ficheroCrecimientoCultivo.write(',')
            ficheroCrecimientoCultivo.write(str(vuelosCultivo)+"\n")



            contadorEm, contadorVu = self.objCultivo.getContadores()
            #
            # evaluacion de lo mejor en el cultivo
            self.agregarDataTipoI(dicDatos, numeroIteracionesGlobales)
            #emparejami,vuelo que vieene del cultov
            self.agregarDataTipoII(contadorEm, contadorVu)

            self.vertices = self.objFeromona.eliminarNodos(self.cultivoACO, self.vertices)
            self.inyectarFeromona()
            print('**************NODOS EN EL CULTIVO************')
            self.controlCultivo(self.vertices)

            numeroIteracionesGlobales+=1

            if iteracionParada == 20:
                break

        ficheroLocal.close()
        ficheroLocalGeneral.close()
        ficheroEvaluacionLocal.close()
        ficheroGlobal.close()
        self.ficheroEvaluacionGlobal.close()
        ficheroTiempoEjecucionLocal.close()
        ficheroTiempoEjecucionGlobal.close()
        ficheroCrecimientoCultivo.close()

        cultivoCosechar, empareja = self.objCultivo.getCultivoClasificado()
        objCultivoNotificador =  CultivoNotificador(cultivoCosechar)
        objRegistroIncidente  = RegistroIncidente('incidente')
        objRegistroEjecucion = RegistroEjecucion('ejecucion')
        objCultivoNotificador.registrarObserver(objRegistroIncidente)
        objCultivoNotificador.registrarObserver(objRegistroEjecucion)
        objCultivoNotificador.initCultivo()

        fin = time.time()
        tiempoEjecucion = round((fin-Inicio),2)
        print('Vuelos sin cubrir:', self.controlCultivo(self.vertices))
        print('Tiempo de ejecución: ', tiempoEjecucion)
        print('Data: ', self.hojasCultivo, ' Vuelos.')
        print('Emparejamientos: ', empareja)

        #self.objGraficas.dibujarGraficaLineasTipoI(listaItera, self.dataEvaluacion)
        self.objGraficas.dibujarGraficaLineasTipoIII(listaItera, self.contadorEmparejamientos, 'Emparejamientos')
        self.objGraficas.dibujarGraficaLineasTipoIII(listaItera, self.contadorVuelos, 'Vuelos')

    def gen_all_paths(self):
        all_paths = []

        for i in range(self.n_ants):
            baseInicio = self.randomBase()

            path = self.gen_path(baseInicio)
            #print(path)

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
        contadorVuelos = 0

        while True:
            saltoVuelo, aeroDestino, idVuelo, fechaArr, horaDep = self.objProbabilidad.obtenerSiguienteNodo()

            while idVuelo in self.nodosVisitados:
                saltoVuelo, aeroDestino, idVuelo, fechaArr, horaDep = self.objProbabilidad.obtenerSiguienteNodo()

            self.nodosVisitados.add(idVuelo)

            contadorVuelos+=1
            prev = aeroDestino
            self.nodosRecorridosAnt  = self.nodosRecorridosAnt.append(saltoVuelo)

            if contadorVuelos >= 12 and base == prev:
                #print('Llego a base y numero de vuelos')
                break

            if fechaArr >= ' 2000-02-01':
                #print('fecha mayor a enero')
                break


            self.nodosAdyacentes = self.vertices.get(prev)
            #print("NODOS ADYACENTES***\n", self.nodosAdyacentes)
            if self.nodosAdyacentes is None:
                print('***********None**********')
                break
            else:
                #print('*****NODOS ADYACENTES ANTES DE AGRUPAR ****\n',self.nodosAdyacentes)
                self.agruparFecha(fechaArr, horaDep)

            self.copiaNodosAdyacentes = self.nodosAdyacentes.copy()

            if len(self.copiaNodosAdyacentes.index) == 0:
                self.nodosAdyacentes = self.vertices.get(prev)
                self.agruparSinFecha(fechaArr, horaDep)
                self.copiaNodosAdyacentes = self.nodosAdyacentes.copy()
    #sque el if un nivel mas
                if len(self.copiaNodosAdyacentes.index) == 0:
                    #print('Sin vuelos programadoss')
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
        if len(self.nodosAdyacentes.index) == 1:
            self.nodosAdyacentes = self.nodosAdyacentes.reset_index(drop=True)
            self.nodosAdyacentes.loc[0,'noPenalizable'] = 1
        #print('*****NODOS ADYACENTES AGRUPADOS ****',self.nodosAdyacentes)

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

    def setTipoHojas(self, tipoHojas):
        cultivoData = dict.fromkeys(tipoHojas)
        bases = cultivoData.keys()
        for i in bases:
            self.dataEvaluacion[i] = []

    def agregarDataTipoI(self, dataEntrante, iterglobal):
        valoresEvaluacion = dataEntrante.values()
        self.ficheroEvaluacionGlobal.write(str(iterglobal))
        for valor in valoresEvaluacion:
            self.ficheroEvaluacionGlobal.write(',')
            self.ficheroEvaluacionGlobal.write(str(int(valor)))
        self.ficheroEvaluacionGlobal.write(str("\n"))
        """for i in self.nodosBases:
            datosAnteriores = self.dataEvaluacion[i]
            datoNuevo = int(dataEntrante[i])
#            print(type(datosAnteriores))
            datosAnteriores.append(datoNuevo)
            self.dataEvaluacion[i] = datosAnteriores"""


    def agregarDataTipoII(self, data1, data2):
        self.contadorEmparejamientos.append(data1)
        self.contadorVuelos.append(data2)

    def estadisticaIteracionesLocales(self, lista):
        listaDistintos = []
        contadorIterLocalEmpareja2 = 0
        contadorIterLocalVuelo2 = 0

        for i in range(len(lista)):
            tupla = lista[i]
            dataFrame = tupla[1]
            evaluacion = tupla[2]
            listaDistintos.append(evaluacion)
            aux  = len(dataFrame.index)
            contadorIterLocalVuelo2 += aux

        listaDistintos = list(set(listaDistintos))
        contadorIterLocalEmpareja2 = len(listaDistintos)
        return contadorIterLocalEmpareja2, contadorIterLocalVuelo2

    def estadisticasEvaluaciones(self, data):
        listaEvaluacion = []
        for i in range(len(data)):
            tupla = data[i]
            dataFrame = tupla[1]
            evaluacion = tupla[2]
            listaEvaluacion.append(evaluacion)

        listaEvaluacion = list(set(listaEvaluacion))
        menorEvaluacion = min(listaEvaluacion)
        return menorEvaluacion

    def estadisticaCultivo(self, data):
        numEmparejamientos = len(data)
        numVuelos = 0
        for i in range(len(data)):
            emparejamiento = data[i]
            vuelos = len(emparejamiento.index)
            numVuelos += vuelos
        return numEmparejamientos, numVuelos


objManipulacion = DataSetTransform()
objManipulacion.init_transform()
vertices = objManipulacion.dictnary_Base_Aer
nodos = objManipulacion.dataAirport

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

ant_colony = AntColony(vertices, nodos, 100, 0, 20 , 0.05, alpha=2, beta=1 , apre=0.8)
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