def iterar(self, data):
        for i in self.nodos:
            for fila in data.iterrows():
                print(fila)

def recorrerTupla(self, lista):
        for i in range (len(lista)):
            tupla = lista[i]
            suma = 0
            for j in range(len(tupla)):
                print(tupla[j])

def sumarItemTupla(self, lista, posicion):
        suma = 0
        for i in range(len(lista)):
            tupla = lista[i]
            dato = tupla[posicion]
            suma += dato

        return suma
#ordenados = sorted(all_paths, key = lambda i : i[2])

"""def actualizarFeromona(self):
        for i in range(self.n_ants):
            #print('hotrmiga', i)
            self.dataHormiga = self.dicHormigas.get(i)
            for j in range(len(self.dataHormiga)):
                dataAux = self.dataHormiga.iloc[j]
                idvuelo,salida,depositar =  self.objOperacionFungus.getDatos(dataAux)
                dataActualizar = self.busquedaListaAdyacente(salida)
                data = self.objOperacionFungus.busquedaActualizar(dataActualizar,idvuelo,depositar)
                self.vertices[salida] = data
                #print(idvuelo,salida,depositar)
def busquedaActualizarFeronoma(self, data, idVuelo, depositar):
        dataAux = data.copy()
        fila = dataAux.loc[dataAux['#leg_nb '] == idVuelo]
        suma = fila.iloc[0]['disipacion']
        #print(suma)
        #print(depositar)
        sumaTotal = suma + depositar
        #print(sumaTotal)
        #print(sumaTotal)
        dataAux.loc[dataAux['#leg_nb '] == idVuelo,['disipacion']] = sumaTotal
        #print(dataAux)
        return dataAux"""

"""def busquedaBinaria(self, n):
            lista = self.generar()
        lista.sort()
        izq = 0
        der = len(lista) -1
        mini = min(lista)
        maxo = max(lista)
        aux = []
        print(lista)

        while (izq <= der) and (mini <= n <= maxo):
            medio = math.floor((izq + der) / 2)

            if lista[medio] == n:
                return medio
            elif lista[medio] < n:
                izq = medio
            else:
                der = medio

            aux = lista[izq:der+1]
            mini = min(aux)
            maxo = max(aux)

            if len(aux) <=2:
                break
        return aux"""

"""
#Hora de presentacion de la tripulacion por lo general 1 hora antes
    def tiempoBrief(self, data):
        hora_salida = data.iloc[0][' hour_dep ']
        listaHora = self.objOperacionProblem.splitHora(hora_salida)
        horaPresentacion = self.objOperacionProblem.horaPresentacion(listaHora)
        return horaPresentacion

    def tiempoDebrief(self, data):
        horaLlegada = data.iloc[-1][' hour_arr']
        listahora = self.objOperacionProblem.splitHora(horaLlegada)
        horaDebrief =self.objOperacionProblem.horaDebrief(listahora)
        return horaDebrief

    def tiempoConexion(self, data):
        size = (len(data))
        listaConexionPenal = []
        sumaPenalizacion = 0
        tiempoConexiones = 0

        for i in range(size -1 ):
            horaLLegada =  data.loc[i][' hour_arr']
            horaSalida = data.loc[i+1][' hour_dep ']
            fechaLlegada = data.loc[i][' date_arr ']
            fechaSalida = data.loc[i+1][' date_dep ']
            leg = data.loc[i+1]['#leg_nb ']

            listaHoraLlegada = self.objOperacionProblem.splitHora(horaLLegada)
            listaHoraSalida = self.objOperacionProblem.splitHora(horaSalida)

            tiempoEspera = self.objOperacionProblem.tiempoVuelo(listaHoraSalida, listaHoraLlegada)
            tiempoConexiones += tiempoEspera
            penalizacion = self.objOperacionProblem.tiempoConexion(tiempoEspera)
            sumaPenalizacion += penalizacion
            data.loc[i+1,'PenalVuelo'] = penalizacion
            #listaConexionPenal.append((fechaSalida,fechaLlegada,tiempoEspera,penalizacion))
            listaConexionPenal.append((leg, tiempoEspera,penalizacion))
        #return sumaPenalizacion
        return listaConexionPenal, tiempoConexiones, data


    def dutyServicios(self, data):
        penalizacion = 0
        listaDutyPenal = []
        serieConcurrencia = data[' date_dep '].value_counts(sort = False)
        size = len(serieConcurrencia)
        nombre = serieConcurrencia.index

        for i in range(size):
            vuelos = serieConcurrencia.iloc[i]
            penalizacion = self.objOperacionProblem.duty(vuelos)
            fecha = nombre[i]
            listaDutyPenal.append((fecha, vuelos, penalizacion))

        return listaDutyPenal

    def tiempoVueloServicio(self, data):
        listaTiempoDuty = []
        serieConcurrencia = data[' date_dep '].value_counts(sort = False)
        nombre = serieConcurrencia.index

        for i in range(len(nombre)):
            fecha = nombre[i]
            inFecha = data[' date_dep '] == fecha
            dataFechaAux = data[inFecha]
            dataFechaAux = dataFechaAux.reset_index(drop = True)

            tiempoServicio = 0
            for j in range(len(dataFechaAux)):
                horaSalida = dataFechaAux.loc[j][' hour_dep ']
                horaLLegada = dataFechaAux.loc[j][' hour_arr']
                listaHoraLlegada = self.objOperacionProblem.splitHora(horaLLegada)
                listaHoraSalida = self.objOperacionProblem.splitHora(horaSalida)
                tempo_Vuelo = self.objOperacionProblem.tiempoVuelo(listaHoraLlegada,listaHoraSalida)
                tiempoServicio += tempo_Vuelo

            penalizacion = self.objOperacionProblem.tiempoVueloServicio(tiempoServicio)
            listaTiempoDuty.append((fecha, tiempoServicio, penalizacion))

        return listaTiempoDuty
    def tiempoEnServicio(self, tiempoVuelos, tiempoTransito):
        return self.objOperacionProblem.tiempoEnServicio(tiempoVuelos, tiempoTransito)

    """

    
    """def tasaCrecimientoVuelosTipoHoja(self, lista):
        cantidadVuelos = 0
        for i in range(len(lista)):
            tupla = lista[i]
            dataVuelos = tupla[0]
            vuelos = len(dataVuelos.index)
            cantidadVuelos += vuelos

        return cantidadVuelos"""

    """def podarHojas(self, profundidadPoda):
        for tipoH in self.tipoHojas:
            dataPodar = self.dataCultivo.get(tipoH)
            for j in range(len(dataPodar)):
                tupla = dataPodar[j]
                estadoBase = tupla[4]
                if estadoBase == True:

                    #dataPodada = dataPodar[:profundidadPoda]
                    self.dataCultivo[tipoH] = dataPodada

        self.listaVuelosRetornar = self.limpiarDatos(self.dataCultivo)"""
