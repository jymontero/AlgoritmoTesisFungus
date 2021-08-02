import matplotlib.pyplot as plt

class Grafica():

    def __init__(self):
        pass

    def dibujarGraficaLineasTipoI(self, datosEjeX, datosEjeY):
        datos = datosEjeY
        fig, ax = plt.subplots()
        ax.plot(datosEjeX, datos[' BASE1 '], color= 'tab:blue', label= "Base 1", linewidth=2.5)
        ax.plot(datosEjeX, datos[' BASE2 '], color = 'tab:purple', label = "Base 2", linewidth=2.5)
        ax.plot(datosEjeX, datos[' BASE3 '], color = 'tab:green',  label= "Base 3", linewidth=2.5)
        plt.legend(loc='upper right')
        plt.show()

    def dibujarGraficaLineasTipoII(self, datosEjeX, datosEjeY1, datosEjeY2):
        fig, ax = plt.subplots()
        ax.plot(datosEjeX, datosEjeY1, color= 'tab:blue', label= "Emparejamientos", linewidth=2.5)
        ax.plot(datosEjeX, datosEjeY2, color = 'tab:green',  label= "Vuelos", linewidth=2.5)
        plt.legend(loc='upper left')
        plt.show()

    def dibujarGraficaLineasTipoIII(self, datosEjeX, datosEjeY1, etiqueta):
        fig, ax = plt.subplots()
        ax.plot(datosEjeX, datosEjeY1, color= 'tab:blue', label= etiqueta, linewidth=2.5)
        plt.legend(loc='upper left')
        plt.show()

    def dibujarGraficaBarraVertical(self, datosEjeX, datosEjeY):
        fig, ax = plt.subplots()
        ax.bar(datosEjeX, datosEjeY)
        plt.show()

    def dibujarGraficaPie(self, datosEjeX):
        fig, ax = plt.subplots()
        ax.pie(datosEjeX)
        plt.show()

"""fig, ax = plt.subplots()
dias = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
temperaturas = {'Madrid':[28.5, 30.5, 31, 30, 28, 27.5, 30.5], 'Barcelona':[24.5, 25.5, 26.5, 25, 26.5, 24.5, 25]}
ax.plot(dias, temperaturas['Madrid'], color = 'tab:purple')
ax.plot(dias, temperaturas['Barcelona'], color = 'tab:green')
plt.show()"""
