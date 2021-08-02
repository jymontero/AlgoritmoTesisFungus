from Graficas import Grafica

class Datos():

    def __init__(self):
        self.objGrafico = Grafica()
        self.DataEjeX = []
        self.DataEjeY = []

    def agregarDatos(self, datoX, datoY):
        self.DataEjeX = self.DataEjeX.append(datoX)
        self.DataEjeY = self.DataEjeY.append(datoY)

    def agregarDatoEjeY(self, datos):
        datosValores = datos.values()
        #self.DataEjeY = self.DataEjeY.append(dato)




