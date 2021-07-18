import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import matplotlib.pyplot as plt
import numpy as np

class CreateGrafic:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title('Gui For Grafic')
        self.master.geometry('500x300+250+150')
        self.master.resizable(False, False)
        self.data = list()
        variable = tk.StringVar()

        progress = ttk.Progressbar(self.master, length=200)
        progress.pack(pady=130)
        """
        num_plot = ttk.Combobox(self.master, value=[i for i in range(1, 10)], textvariable=variable)
        num_plot.pack()

        show_btn = ttk.Button(self.master, text='Show', command=self.preview)
        show_btn.pack()"""
    
    def preview(self):
        #numero grafici
        #tipi di grafici
        #numero seguenza per grafico
        #colori e dimensioni
        pass

if __name__== '__main__':
    gui = CreateGrafic()
    gui.master.mainloop()