from datetime import datetime
class Cultivo():

    def __init__(self, tipoHojas):
        self.tipoHojas = tipoHojas
        self.listaVuelosRetornar = []
        self.dataCultivo = {}

        self.cultivoClasificado = {}
        self.controlTasaCutlivo = {}
        self.controlTasaTipoHoja = {}

        self.dataCultivo = self.setTipoHojas(self.tipoHojas)
        self.cultivoClasificado = self.setTipoHojas(self.tipoHojas)

        self.controlTasaCutlivo = self.inicilizarTasa(self.tipoHojas)
        self.controlTasaTipoHoja = self.inicilizarTasa(self.tipoHojas)

    def setTipoHojas(self, tipoHojas):
        cultivoData = dict.fromkeys(tipoHojas)
        bases = cultivoData.keys()
        for i in bases:
            cultivoData[i] = []
        return cultivoData

    def inicilizarTasa(self, tipoHojas):
        cultivoData = dict.fromkeys(tipoHojas)
        bases = cultivoData.keys()
        for i in bases:
            cultivoData[i] = [0,0]
        return cultivoData

    def agregarHojasCultivoFungus(self):

        for tipoH in self.tipoHojas:
            print('\nBase:', tipoH)
            hojaCultivar = self.dataCultivo.get(tipoH)
            if len(hojaCultivar)!=0:
                nodoMinimaEvaluacion = self.sacarMinimo(hojaCultivar)
                TuplaDatafecha = self.contruirTupla(nodoMinimaEvaluacion, tipoH)
                hojaCultivada = self.cultivoClasificado.get(tipoH)
                #hojaPreparada = (nodoMinimaEvaluacion,fechaInicioVuelo)
                #listaHojas = hojaCultivada.append(nodoMinimaEvaluacion)
                hojaCultivada.append(TuplaDatafecha)
                #self.cultivoClasificado[tipoH] = sorted(listaHojas, key = lambda i : i[1])
                cultivadaOrdenada = sorted(hojaCultivada, key= self.sortByDate)
                self.cultivoClasificado[tipoH] = cultivadaOrdenada
                self.dataCultivo[tipoH] = []

                """print('*******DATA ORDENADA INICIO******')
                print(ordenada)
                print('*******DATA ORDENADA FIN******')"""
                tasaCrecimiento = self.crecimientoVuelosTipoHoja(tipoH, nodoMinimaEvaluacion,1)
                print(tasaCrecimiento)

    def sortByDate(self, elem):
        return datetime.strptime(elem[1], ' %Y-%m-%d ')

    def sacarMinimo(self, data):
            minimo = min(data, key= lambda item:item[1])[0]
            #print(minimo)
            #tupla = self.obtenerFechaInicio(minimo)
            return minimo

    def contruirTupla(self, data, tipoH):
            fechaSalida = data.iloc[0][' date_dep ']
            tupla = (data, fechaSalida, tipoH)
            return tupla

    def crecimientoCultivoTipoHoja(self, tipoHoja, medirData, dias):
        medicionActual = len(medirData)
        tasaTupla = self.controlTasaCutlivo.get(tipoHoja)

        primeraMedicion = tasaTupla[0]
        segundaMedicion = medicionActual
        tasaCreciminento = (segundaMedicion - primeraMedicion) / dias
        tasaTupla[0] = segundaMedicion
        tasaTupla[1] = medicionActual

        return tasaCreciminento

    def crecimientoVuelosTipoHoja(self, tipoHoja, medirData, dias):
        cantidadVuelos =  len(medirData.index)
        tasaTupla = self.controlTasaTipoHoja.get(tipoHoja)

        primeraMedicion = tasaTupla[0]
        segundaMedicion = cantidadVuelos
        tasaCrecimiento = (segundaMedicion - primeraMedicion) / dias
        tasaTupla[0] = segundaMedicion
        tasaTupla[1] = cantidadVuelos

        return tasaCrecimiento


    def limpiarDatos(self, data):
        listaVuelos = []
        vuelosRetornar = data.values()
        vuelosRetornar = list(vuelosRetornar)

        for j in range(len(vuelosRetornar)):
            listaTupla = vuelosRetornar[j]
            for i in range(len(listaTupla)):
                tupla = listaTupla[i]
                vuelo = tupla[0]
                listaVuelos.append(vuelo)

        return listaVuelos

    def controlCultivoGlobal(self, data):
        contador = 0
        cantidadVuelos = data.values()
        cantidadVuelos = list(cantidadVuelos)

        for i in range(len(cantidadVuelos)):
            aeropuerto = cantidadVuelos[i]
            cantidad = len(aeropuerto)
            contador += cantidad

        return contador

    def ordenarHojas(self):
        for tipoH in self.tipoHojas:
            dataOrdenar = self.dataCultivo.get(tipoH)
            dataOrdenada = sorted(dataOrdenar, key = lambda i : i[2])
            #dataOrdenada = min(dataOrdenada)
            self.dataCultivo[tipoH] = dataOrdenada

#params data:lista de tuplas
    def clasificarHojas(self, data):
        for i in range(len(data)):
            infoTupla = data[i]
            dataVuelos = infoTupla[1]
            penal = infoTupla[2]
            base = infoTupla[3]
            estadoBase = infoTupla[4]
            self.clasificacionTipoHoja(base, infoTupla, estadoBase, dataVuelos, penal)

        #self.ordenarHojas()
        #self.podarHojas(5)
        self.listaVuelosRetornar = self.limpiarDatos(self.dataCultivo)
        self.agregarHojasCultivoFungus()

    def clasificacionTipoHoja(self, tipoHoja, hojaTupla, estadoBase, dataVuelos, penal):
        lista = self.dataCultivo.get(tipoHoja)
        numeroVuelosPermitidos = self.tamanioHojas(dataVuelos, 15)
        if estadoBase == True and numeroVuelosPermitidos == 0:
            lista.append((dataVuelos,penal))
            self.dataCultivo[tipoHoja] = lista

    def tamanioHojas(self, data, vuelosPermitido):
        numeroHojas = len(data.index)
        #verificar bien logica and o or
        if numeroHojas <= vuelosPermitido and numeroHojas >= 2:
            return  0
        else:
            return -1

    def iterar(self):
        for i in self.tipoHojas:
            print('\nBase:', i)
            lista = self.cultivoClasificado.get(i)
            print('Size:', len(lista))
            for j in range(len(lista)):
                tupla = lista[j]
                print('\nPenal', tupla[2])
                print('\n', tupla[1])

    def cultivarVuelos(self, data):
        listaHongo = []
        for i in range(len(data)):
            tupla = data[i]
            hongo = tupla[1]
            listaHongo.append(hongo)

        return listaHongo

    def cultivar(self, data):
        #print(data)
        self.clasificarHojas(data)
        return self.listaVuelosRetornar

    def armarTupla(self, data):
        dataLocal = data
        lista = []
        for i in range(len(dataLocal)):
            tupla =  dataLocal[i]
            vuelos = tupla[0]
            fechaIni = tupla[1]
            base = tupla[2]
            indice = i
            tuplaInfo = (vuelos, fechaIni, base, indice)
            lista.append(tuplaInfo)

        return lista

    def getCultivoClasificado(self):

        for tipoH in self.tipoHojas:
            dataValues = self.cultivoClasificado.get(tipoH)
            listaNueva = self.armarTupla(dataValues)
            self.cultivoClasificado[tipoH] = listaNueva

        return self.cultivoClasificado
