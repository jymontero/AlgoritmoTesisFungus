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


    def tasaCrecimientoVuelosTipoHoja(self, lista):
        cantidadVuelos = 0
        for i in range(len(lista)):
            tupla = lista[i]
            dataVuelos = tupla[0]
            vuelos = len(dataVuelos.index)
            cantidadVuelos += vuelos

        return cantidadVuelos

    def podarHojas(self, profundidadPoda):
        for tipoH in self.tipoHojas:
            dataPodar = self.dataCultivo.get(tipoH)
            for j in range(len(dataPodar)):
                tupla = dataPodar[j]
                estadoBase = tupla[4]
                if estadoBase == True:

                    #dataPodada = dataPodar[:profundidadPoda]
                    self.dataCultivo[tipoH] = dataPodada

        self.listaVuelosRetornar = self.limpiarDatos(self.dataCultivo)

    def printed(self, data):
        const = len(data)
        for data3 in data:
            print(data3)

    def uniqueColumn(self,nameColum,data):
        data3 = pd.DataFrame()
        data3 = data[nameColum]
        return data3

    #Metod que filtra todas las filas de un datafram
    #nameColumn: nombre de la columna por el cual filtrar
    #conditional: condicion de filtrado
    def uniqueData(self,nameColum, conditional):
        data3 = pd.DataFrame()
        database = pd.DataFrame()

        data3 = self.data_Frame[nameColum] == conditional
        database = self.data_Frame[data3]
        return database

    #Metodo que filtra datos de acuerdo a una columna del dataframe
    def distintData(self, columnNam):
        self.dataAirport = pd.unique(self.data_Frame[columnNam])
        aux = pd.DataFrame()

        for base in self.dataAirport:
            aux = self.uniqueData(columnNam,base)
            self.listaBases.append(aux)

    #Metodo que recorre un dataFrame
    def recorrerDataFrame(self, dataF):
            aux = pd.DataFrame()
            for indiceF, fila in  aux.iterrows():
                print(fila)

    #Metodo que obtiene el tiempo de vuelo
    def getTimeFly(self, row):
        hora_dep = (row[' hour_dep '])
        hora_arr = (row[' hour_arr'])
        listHora_dep = hora_dep.lstrip().split(sep=':')
        listHora_arr = hora_arr.lstrip().split(sep= ':')
        minuto = self.horasObj.tiempoVuelo(listHora_arr,listHora_dep)
        return minuto

    def createColumn(self,nameColum):
        self.data_Frame[nameColum] = self.data_Frame.apply(self.getPheromona,axis=1)

    def getPheromona(self,row):
        tiempo_vuelo = (row['time_fly'])
        #return 1/ self.data_Frame.size
        return 0.1


    #Metodo que agrega una columna con el tiempo de vuelo
    def addTimeFly(self):
        self.data_Frame['time_fly']= self.data_Frame.apply(self.getTimeFly,axis=1)

    #Metodo que crear un diccionario Clave:nombre de aeropuerto obase
    #valor es el listado de todos los vuelos que parten  de aeropuerto o base
    def crearDiccionario(self):
        self.dictnary_Base_Aer = dict(zip(self.dataAirport,self.listaBases))

    #Retorna el datafraeme
    def getDataFrame(self):
        return self.data_Frame

    def getDataAirport(self):
        return self.dataAirport

    #retorna listadebases
    def getListaBases(self):
        return self.listaBases

    def getBasesConexiones(self):
        return self.dictnary_Base_Aer
"""

"""    def contadorBases(self, base):
            if base == ' BASE1 ':
                self.contadorB1 += 1
            if base == ' BASE2 ':
                self.contadorB2 += 1
            if base == ' BASE3 ':
                self.contadorB3 +=1
"""
#self.objHistorial.generarHistorial('\nBase Hormiga:'+ str(i), baseInicio)
"""dataHistorial = path
            dataHistorial = dataHistorial.drop(columns=['feromona', 'costo'])
            self.objHistorial.generarHistorial('\nCamino Hormiga:'+ str(i)+ '\n', dataHistorial)"""

            #self.objHistorial.generarHistorial('Cultivo',self.cultivoACO)