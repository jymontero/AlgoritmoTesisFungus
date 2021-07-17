import logging
import pprint

class Historial():

    def __init__(self):
        self.configuracionLog()


    def configuracionLog(self):
        logging.basicConfig(filename= 'historial.log',
                            filemode= 'w',
                            level= logging.INFO
                            )

    def parametrosInciales(self, iteraciones, hormigas, aprendizaje, alfa, beta):
        logging.info("Numero de iteraciones: " + str(iteraciones))
        logging.info("Numero de hormigas:"+ str(hormigas))
        logging.info("Parametro de Aprendizaje:"+ str(aprendizaje))
        logging.info("Parametro Alfa:"+ str(alfa))
        logging.info("Parametro BeTa:"+ str(beta))


    def generarHistorial(self, mensaje, data):
        logging.info(mensaje + str(data))
