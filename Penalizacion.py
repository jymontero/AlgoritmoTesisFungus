import pandas as pd
from Restriccion import Restriccion
from Historial import Historial


class Penalizacion():

    llegaAbase = True

    def __init__(self, historial):
        self.objHistorial = Historial()
        self.objHistorial = historial
        self.objRestriccion = Restriccion()
        self.dataR = pd.DataFrame()
        self.estadoBase = False

#Hora de presentacion de la tripulacion por lo general 1 hora antes

    def tiempoBrief(self):
        hora_salida = self.dataR.iloc[0][' hour_dep ']
        listaHora = self.objRestriccion.splitHora(hora_salida)
        horaPresentacion = self.objRestriccion.horaPresentacion(listaHora)
        return horaPresentacion

    def tiempoDebrief(self):
        horaLlegada = self.dataR.iloc[-1][' hour_arr']
        listahora = self.objRestriccion.splitHora(horaLlegada)
        horaDebrief =self.objRestriccion.horaDebrief(listahora)
        return horaDebrief

    def tiempoConexion(self):
        size = (len(self.dataR))
        listaConexionPenal = []
        sumaPenalizacion = 0
        tiempoConexiones = 0
        penalizacion = 0

        for i in range(size - 1):
            horaLLegadaVueloActual =  self.dataR.loc[i][' hour_arr']
            fechaLlegadaVueloActual = self.dataR.loc[i][' date_arr ']

            horaSalidaProxVuelo = self.dataR.loc[i+1][' hour_dep ']
            fechaSalidaProxVuelo = self.dataR.loc[i+1][' date_dep ']
            leg = self.dataR.loc[i+1]['#leg_nb ']

            horaLL = self.objRestriccion.concatenarSegundos(horaLLegadaVueloActual)
            horaSS = self.objRestriccion.concatenarSegundos(horaSalidaProxVuelo)

            dateLLegada = fechaLlegadaVueloActual + horaLL
            dateSalida = fechaSalidaProxVuelo + horaSS

            #tiempoEspera = self.objRestriccion.tiempoVuelo(listaHoraSalida, listaHoraLlegada)
            dias, tiempoEspera = self.objRestriccion.restarFechas(dateLLegada, dateSalida)
            #tiempoConexiones += tiempoEspera
            penalizacion = self.objRestriccion.tiempoConexion(tiempoEspera, dias)
            self.dataR.loc[i,'estado'] = self.estadoDeVuelo(penalizacion)
            #sumaPenalizacion += penalizacion

            #penalizacionActual  = self.dataR.loc[i]['penalVuelo']
            #OJO LO CAMBIE EL COMPORTAMIENTO DE LA PENALIZACION
            penalizacionActual  = self.dataR.loc[i+1]['penalVuelo']
            self.dataR.loc[i+1,'penalVuelo'] = penalizacionActual +  penalizacion
            #listaConexionPenal.append((fechaSalida,fechaLlegada,tiempoEspera,penalizacion))
            listaConexionPenal.append((leg, tiempoEspera, penalizacion))
            penalizacion = 0
            penalizacionActual = 0

        #return sumaPenalizacion
        return listaConexionPenal, tiempoConexiones

    def estadoUtlimoVuelo(self, estado):
        ultimaPosicion = len(self.dataR) - 1
        if estado == 0:
            self.dataR.loc[ultimaPosicion,'estado'] = 'BASE'
        else:
            self.dataR.loc[ultimaPosicion,'estado'] = 'DEAD'

    def estadoDeVuelo(self, estado):
        if estado == 0:
            return 'SIT'
            #self.dataR.loc[indice,'estado'] = 'SIT'
        else:
            #self.dataR.loc[indice,'estado'] = 'REST'
            return 'REST'


    def dutyServicios(self):
        penalizacion = 0
        listaDutyPenal = []
        serieConcurrencia = self.concurrenciaFecha()
        size = len(serieConcurrencia)
        nombre = serieConcurrencia.index

        for i in range(size):
            vuelos = serieConcurrencia.iloc[i]
            penalizacion = self.objRestriccion.duty(vuelos)
            fecha = nombre[i]
            self.setPenalizacion(fecha, penalizacion)
            listaDutyPenal.append((fecha, vuelos, penalizacion))

        return listaDutyPenal

    def concurrenciaFecha(self):
        serieConcurrencia = self.dataR[' date_dep '].value_counts(sort = False)
        return serieConcurrencia

    def setPenalizacion(self, fecha, penalizacion):
        for i in range(len(self.dataR)):
            if self.dataR.loc[i,' date_dep '] == fecha:
                acumulado = self.dataR.loc[i]['penalDuty']
                self.dataR.loc[i,'penalDuty'] = penalizacion + acumulado
                acumulado = 0

    def setPenalizacionDuty(self, penalizacion):
            for i in range(len(self.dataR)):
                acumulado = self.dataR.loc[i]['penalDuty']
                self.dataR.loc[i,'penalDuty'] = penalizacion + acumulado
                acumulado = 0

    def tiempoVueloServicio(self):
        listaTiempoDuty = []
        serieConcurrencia = self.concurrenciaFecha()
        nombre = serieConcurrencia.index
        penalizacion = 0

        for i in range(len(nombre)):
            fecha = nombre[i]
            inFecha = self.dataR[' date_dep '] == fecha
            dataFechaAux = self.dataR[inFecha]
            dataFechaAux = dataFechaAux.reset_index(drop = True)

            tiempoServicioDuty = 0
            for j in range(len(dataFechaAux)):
                horaSalida = dataFechaAux.loc[j][' hour_dep ']
                horaLLegada = dataFechaAux.loc[j][' hour_arr']
                listaHoraLlegada = self.objRestriccion.splitHora(horaLLegada)
                listaHoraSalida = self.objRestriccion.splitHora(horaSalida)
                tempo_Vuelo = self.objRestriccion.tiempoVuelo(listaHoraLlegada,listaHoraSalida)
                tiempoServicioDuty += tempo_Vuelo

            penalizacion = self.objRestriccion.tiempoVueloServicio(tiempoServicioDuty)
            self.setPenalizacion(fecha, penalizacion)
            listaTiempoDuty.append((fecha, tiempoServicioDuty, penalizacion))
            penalizacion = 0

        return listaTiempoDuty

    def tiempoEnServicio(self, tiempoVuelos, tiempoTransito):
        return self.objRestriccion.tiempoEnServicio(tiempoVuelos, tiempoTransito)

    def dutiesMaximo(self):
        serieConcurrencia = self.concurrenciaFecha()
        penalizacion =self.objRestriccion.dutiesMaximo(len(serieConcurrencia))
        self.setPenalizacionDuty(penalizacion)

    def llegaBase(self):
        ultimaPosicion = len(self.dataR) - 1
        nodoSalida = self.dataR.loc[0][' airport_dep ']
        nodoLlegada = self.dataR.loc[ultimaPosicion][' airport_arr ']
        penalizacionActual = self.dataR.loc[ultimaPosicion]['penalVuelo']
        penalizacion = self.objRestriccion.llegaBase(nodoSalida,nodoLlegada)
        self.setEstadoBase(penalizacion)
        self.estadoUtlimoVuelo(penalizacion)
        self.dataR.loc[ultimaPosicion,'penalVuelo'] = penalizacionActual + penalizacion

    def setEstadoBase(self, estado):
        if estado == 0:
            self.estadoBase = True
        else:
            self.estadoBase = False

    def estadisticaPenalizacion(self):
        penalVuelo = self.dataR['penalVuelo'].sum()
        penalDuty = self.dataR['penalDuty'].sum()
        evaluacion = penalDuty + penalVuelo
        return evaluacion

    def totalPenalizacion(self):
        for i in range(len(self.dataR)):
            penalVuelo = self.dataR.loc[i]['penalVuelo']
            penalDuty = self.dataR.loc[i]['penalDuty']
            self.dataR.loc[i,'penalizacion'] = penalDuty + penalVuelo
            penalVuelo = 0
            penalDuty = 0

    def evaluarRestriccion(self, data):
        self.dataR = data

        self.dataR['penalizacion'] = 0
        self.dataR['estado'] = ''

        self.tiempoConexion()
        self.dutyServicios()
        self.tiempoVueloServicio()
        self.dutiesMaximo()
        self.llegaBase()
        self.totalPenalizacion()
        evaluacion = self.estadisticaPenalizacion()
        self.generarLogPenalizacion()

        return self.dataR, evaluacion, self.estadoBase

    def informacionEmparejamiento(self):
            pass

    def generarLogPenalizacion(self):
        data = self.dataR
        #data = data.drop(columns=[' date_arr ',' hour_dep ',' hour_arr',' date_dep '])
        #self.objHistorial.generarHistorial('Penalizacion\n', data)

"""print('Timepo Vuelo: ', tiempoTotalVuelo)
print('Tiempo Transito: ', tiempoTransito)
print('Tiempo en servicio: ', self.objRestriccion.tiempoEnServicio(tiempoTotalVuelo,tiempoTransito))
print('Hora Debrief: ', self.objRestriccion.tiempoDebrief(path))
"""