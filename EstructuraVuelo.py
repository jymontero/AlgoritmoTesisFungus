
from datetime import datetime, date, time, timezone, timedelta
import pandas as pd
import time

class EstructuraVuelo():

    def __init__(self):
        self.vuelosEmparejamiento = pd.DataFrame()
        self.vuelosIfectados = pd.DataFrame()

    def estructurasVuelos(self, data, dataInfectada):
        dataTupla = data
        self.vuelosEmparejamiento = dataTupla[0]
        print('\n*****DATA RECIBE VUELOS****\n')
        print('Base:', dataTupla[2])
        print('Emparejamiento', dataTupla[3])
        print(self.vuelosEmparejamiento)
        dataTuplaInfectada = dataInfectada
        self.vuelosIfectados = dataTuplaInfectada[0]

        for i in range(len(self.vuelosIfectados.index)-1):
            vuelos = self.vuelosIfectados.iloc[i: i+1]
            vueloSalidaInfectado = self.vuelosIfectados.iloc[i][' airport_dep ']
            print(vueloSalidaInfectado)
            vueloLlegadaInfectado = self.vuelosIfectados.iloc[i+1][' airport_arr ']
            print(vueloLlegadaInfectado)
            self.verificarAeropuertos(vueloSalidaInfectado, vueloLlegadaInfectado)

    def verificarAeropuertos(self, salidaInfectado, llegadaInfectado):
        for i in range(len(self.vuelosEmparejamiento.index)-1 ):
            #print(self.vuelosEmparejamiento.iloc[i])
            aeroLlegadaSano = self.vuelosEmparejamiento.iloc[i][' airport_arr ']

            if aeroLlegadaSano == salidaInfectado:
                aeropuertoSalida = self.vuelosEmparejamiento.iloc[i+1][' airport_dep ']
                print(aeropuertoSalida)
                #print(type(vuelosSiguiente))
                #aeropuertoSalida = vuelosSiguiente.iloc[0][' airport_dep ']
                print(self.secuenciaVuelos(aeropuertoSalida, llegadaInfectado))

    def secuenciaVuelos(self, salidaSano, llegadaInfectado):
        if salidaSano == llegadaInfectado:
            return True
        else:
            return False

    def verificarFechas(self, fecha1, fecha2):
        FORMATO = ' %Y-%m-%d '
        dateSelect = datetime.strptime(fecha1, FORMATO)
        dateSelect2 = datetime.strptime(fecha2, FORMATO)

        if dateSelect == dateSelect2:
            return True
        else:
            return False