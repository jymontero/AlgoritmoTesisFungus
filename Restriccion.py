from datetime import datetime, date, time, timezone, timedelta

class Restriccion:

    BRIEF = 60
    DEBRIEF = 30

    TIEMPO_CONEXION_MIN =  30
    TIEMPO_CONEXION_MAX = 210

    DUTY_VUELOS_MAXIMO = 4
    DUTY_TIEMPO_MAXIMO = 480
    DUTY_PERIODO = 1440
    DUTY_MAX = 4

    DIAS_HOLGURA = 1

    def __init__(self):
        pass

    def sumarDia(self, fecha, dias):
        FORMATO = ' %Y-%m-%d '
        dateSelect = datetime.strptime(fecha, FORMATO)
        delta  = dateSelect + timedelta(days = dias)
        delta  = datetime.date(delta)
        delta2 = delta.strftime(' %Y-%m-%d ')
        return delta2

    def concatenarSegundos(self, hora):
        segundos = ':00'
        horaParcial = hora + segundos
        horaFinal = horaParcial.replace(" ","")
        return horaFinal

#    def restarFechas(self, fecha1, hora1, fecha2, hora2):
    def restarFechas(self, llegada, salida):
        fechaSalida = salida
        fechaLLegada = llegada
        FORMATO = ' %Y-%m-%d %H:%M:%S'
        dateSalida = datetime.strptime(fechaSalida,FORMATO)
        dateLlegada = datetime.strptime(fechaLLegada,FORMATO)
        restarFecha = dateSalida - dateLlegada
        dias = restarFecha.days
        segundos = restarFecha.seconds
        minutos = (restarFecha.seconds)/60
        horas =  (restarFecha.seconds)//3600
        return dias, minutos

    def restarHoras(self, horallegada, horaSalida):
        FORMATO = "%H:%M:%S"
        horaSalida = datetime.strptime(horaSalida,FORMATO)
        horallegad = datetime.strptime(horallegada,FORMATO)
        resultado = horallegad - horaSalida
        seconds = resultado.seconds
        minutos = (seconds/60)
        return minutos

    def horaMinSeparate(self, lista_horas):
        hora = int(lista_horas[0])
        minuto = int(lista_horas[1])
        return hora,minuto

    def splitHora(self, hora):
        listHora = hora.lstrip().split(sep=':')
        return listHora

# Tiempo total desde que la aeronave despega de un origen
# hasta que aterriza en un destino

    def tiempoVuelo(self,hour_arr, hour_dep):
        hora_arr,min_arr = self.horaMinSeparate(hour_arr)
        hora_dep,min_dep = self.horaMinSeparate(hour_dep)
        t_dep = str(time(hora_dep, min_dep))
        t_arr = str(time(hora_arr, min_arr))
        minutos = self.restarHoras(t_arr,t_dep)
        return int(minutos)

#Aumnto hora de Brief
    def horaPresentacion(self, horaSalida):
        FORMATO = "%H:%M:%S"
        hora_salida, min_salida = self.horaMinSeparate(horaSalida)
        objTime = str(time(hora_salida,min_salida))
        hora = datetime.strptime(objTime,FORMATO)
        horaPresentacion = hora - timedelta(min = self.BRIEF)
        horaPresentacion2 = datetime.time(horaPresentacion)
        return horaPresentacion2

#Aumento hora debrief
    def horaDebrief(self, horaLLegada):
        FORMATO = "%H:%M:%S"
        hora_salida, min_salida = self.horaMinSeparate(horaLLegada)
        objTime = str(time(hora_salida,min_salida))
        hora = datetime.strptime(objTime,FORMATO)
        horaPresentacion = hora - timedelta(min= self.DEBRIEF)
        horaPresentacion2 = datetime.time(horaPresentacion)
        return horaPresentacion2

#Connection time: Periodo de tiempo entre dos tramos de
# vuelo consecutivos, generalmente las aerolíneas
# consideran un tiempo mínimo de 30 minutos y un máximo de 3 horas a 3 horas y medio 210

    def tiempoConexion(self, tiempo, dias):
        penalConexionDias = ((dias * 24)*60)
        if tiempo >= self.TIEMPO_CONEXION_MIN and tiempo <= self.TIEMPO_CONEXION_MAX:
            return 0

        if tiempo < self.TIEMPO_CONEXION_MIN:
            return self.TIEMPO_CONEXION_MIN - tiempo

        #else:
        if tiempo > self.TIEMPO_CONEXION_MAX:
            #SE CAMBIO EL VALOR PARA LA PENAZALIZACION SE MULTIPLICA X10
            return ((tiempo + penalConexionDias) - self.TIEMPO_CONEXION_MAX) * 10

#Servicio o duty: Trayecto que recorre una aeronave haciendo
# escalas o no, durante un turno o jornada en el día, puede
# tener máximo 4 vuelos y tiene un tiempo máximo de 14 horas
# en un periodo de 24 horas.

    def duty(self, numeroVuelos):
        if numeroVuelos <= self.DUTY_VUELOS_MAXIMO:
            return 0
        else:
            #se cambio actulizacion 27/08/21 se aumento un *10 para probar comportamiento
            return (numeroVuelos - self.DUTY_VUELOS_MAXIMO)

#Tiempo de servicio: Tiempo total  desde que la tripulación
# entra en servicio (Brief), usualmente una hora antes de
# despegar el primer vuelo hasta finalizar el Debrief.

    def tiempoEnServicio(self, tiempoVuelos, tiempoTransito):
        tiempoTotal =  self.BRIEF + tiempoVuelos + tiempoTransito + self.DEBRIEF
        return tiempoTotal

#Tiempo de vuelo de un servicio:
# Suma de todos los tiempos de cada uno de los
# vuelos de un servicio, tiene un tiempo máximo de 8 horas

    def tiempoVueloServicio(self, tiempoVueloServicio):
        if tiempoVueloServicio <= self.DUTY_TIEMPO_MAXIMO:
            return 0
        else:
            #se le cambio a 10 estaba en 100 27/08/21
            return (tiempoVueloServicio - self.DUTY_TIEMPO_MAXIMO)*10


#Tiempo de un emparejamiento de la tripulación:
# Tiempo total que está constituido por uno o
# más servicios, incluidos los tiempos de descanso.

    def tiempoTotalEmparejamiento(self):
        pass

#total de duties o servicios que confirmoran un emparejamiento
#maximo son 4 duties por emparejamiento

    def dutiesMaximo(self, duties):
        if duties > self.DUTY_MAX:
            # se cambio actuliazion 29/08/21 se aument *10 para probar
            return  (duties - self.DUTY_MAX)
        else:
            return 0

##metodo que verifica si se llega a la base y penaliza

    def llegaBase(self, nodoBase, aeroLLegada):
        if nodoBase == aeroLLegada:
            return 0
        else:
            return 1000

    def limiteFecha(self, dias):
        if dias < self.DIAS_HOLGURA:
            return 0
        else:
            return dias * 10
