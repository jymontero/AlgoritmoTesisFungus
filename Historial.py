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


"""LOG_FILENAME = 'logging_example.out'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
)

logging.debug('This message should go to the log file')

with open(LOG_FILENAME, 'rt') as f:
    body = f.read()

print('FILE:')
print(body)"""