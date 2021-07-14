from tkinter import ttk
from tkinter import *


window = Tk()

window.resizable(False, False)  # This code helps to disable windows from resizing
window_height = 800
window_width = 1000

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

window.title('Algoritmo ACO_Fungus')

frameGrafo = Frame(window)
frameGrafo.config(width= (window_width/2 + ((window_width/2))/2), height = (window_height/2)-10)
frameGrafo.config(bg = 'red')
frameGrafo.pack(side= LEFT)
frameGrafo.pack(anchor = NW)


frameConfig = Frame(window)
frameConfig.config(width= window_width/2, height = (window_height/2)-10)
frameConfig.config(bg = 'blue')
frameConfig.pack(side= RIGHT)
frameConfig.pack(anchor = NE)
#creando un frame containe"""
"""frameConfiguracion = ttk.LabelFrame(window, text = 'Configuracion')
#frameConfiguracion.grid(row = 1, column = 0, columnspan = 3, pady= 20)
frameConfiguracion.pack(fill='both', expand = 'yes', side = RIGHT, anchor= NW)

frameBotones = ttk.LabelFrame(frameConfiguracion, text = 'Botones')
frameBotones.pack(fill='both', expand = 'yes', side = BOTTOM)"""

frameEmparejamiento = Frame(window)
frameEmparejamiento.config(width= window_width, height = (window_height/2))
frameEmparejamiento.config(bg = 'green')
frameEmparejamiento.pack(side = BOTTOM)
frameEmparejamiento.pack(anchor = SE)

la = Label(frameEmparejamiento, text = 'Hola')
la.pack(side= BOTTOM)
window.mainloop()