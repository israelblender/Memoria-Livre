# -*- coding: cp1252 -*-
#Verifica memoria disponivel em disco
#Compatível com 2.7

#Autor: Israel Gomes
#Data Upload: 23/10/2017
#Data Criação: 18/02/2017

from psutil import disk_usage #python27
from time import sleep
import Tkinter as t
import threading as td

from sys import version
if version[0] == "2":#Importação compatível com py 2.7
    import Tkinter as t
    import requests
elif version[0] == "3":#Importação compatível com py 3
    import tkinter as t
    import urllib.request
    

class janela(t.Frame):
    def __init__(self, master=None, fundo="#000000", *args, **kwargs):
        t.Frame.__init__(self, master=None, background=fundo, padx=5, pady=5, *args, **kwargs)
        
        root.title = "aplicativo"
        
        root.resizable(False, False)

        larguraTela, alturaTela = root.winfo_screenwidth(), root.winfo_screenheight()
        
        #root.attributes('-toolwindow', 0)
        root.attributes('-topmost', 1)
        root.attributes('-alpha', 0.7)
        
        #root.protocol("WM_DELETE_WINDOW", self.quebrarEvento)
        root.overrideredirect(1)
        #root.transient(self)
        
        
        t.Label(self, text="Info.", font=("Arial", 7), background=fundo, foreground="white").grid(row=0, column=0)
        t.Label(self, text="de", font=("Arial", 7), background=fundo, foreground="white").grid(row=0, column=1)
        t.Label(self, text="memória", font=("Arial", 7), background=fundo, foreground="white").grid(row=0, column=2)

        t.Label(self, text="Livre", background='green', font=("Arial", 7), width=8).grid(row=1, column=1)
        t.Label(self, text="Ocupado", background='red', font=("Arial", 7), width=8).grid(row=1, column=2)
        t.Label(self, text="Total", background='blue', font=("Arial", 7), width=8, foreground="white").grid(row=1, column=3)
        t.Label(self, text="%Ocup.", background='orange', font=("Arial", 7), width=6, foreground="black").grid(row=1, column=4)

        t.Button(self, text="X", font=("Arial", 7), command=self.quebrarEvento, background=fundo, padx=2).grid(row=1, column=5)
        
        self.disco_antigo = None
        self.desligar = False

        self.listStringVar = {}
        for row, disk in enumerate(self.getDisk_partitions(), 2):
            svlivre, svocupado, svtotal, svpercent = t.StringVar(), t.StringVar(), t.StringVar(), t.StringVar()
            self.listStringVar[disk[0]] = svlivre, svocupado, svtotal , svpercent
            if disk[1] == "NTFS":
                alocacao = "Disco"
            elif disk[1] == "CDFS":
                alocacao = "CD-R"
            elif disk[1] == "FAT32":
                alocacao = "PenD."
                
            t.Label(self, text="{}:{}".format(alocacao, disk[0]), font=("Arial", 7), width=8).grid(row=row, column=0)
            t.Label(self, textvariable=svlivre, font=("Arial", 7), background=fundo, foreground="white").grid(row=row, column=1)
            t.Label(self, textvariable=svocupado, font=("Arial", 7), background=fundo, foreground="white").grid(row=row, column=2)
            t.Label(self, textvariable=svtotal, font=("Arial", 7), background=fundo, foreground="white").grid(row=row, column=3)
            t.Label(self, textvariable=svpercent, font=("Arial", 7), background=fundo, foreground="white").grid(row=row, column=4)
            

        root.configure(background=fundo)
        self.CheckMemoryThread()
        sleep(2)
        self.pack()
        root.update()
        print root.winfo_width(), root.winfo_height()
        root.geometry("%ix%i+%i+%i"%(root.winfo_width(), root.winfo_height(), larguraTela-root.winfo_width(), alturaTela-root.winfo_height()-30))
        

    def CheckMemoryThread(self):        
        t = td.Thread(target=self.initCheck, kwargs={'time':1})
        t.start()
            
    def initCheck(self, time=None):
        self.evento = td.Event()
         
        while True:
            if self.desligar: break
            
            sleep(time)

            for disk in self.listStringVar:
                try:
                    ds = (disk_usage(path=disk))
                
                    self.listStringVar.get(disk)[0].set("%.3f GBs"%(ds.free / 1024.0 / 1024.0 / 1024.0))
                    self.listStringVar.get(disk)[1].set("%.3f GBs"%(ds.used / 1024.0 / 1024.0 / 1024.0))
                    self.listStringVar.get(disk)[2].set("%.3f GBs"%(ds.total / 1024.0 / 1024.0 / 1024.0))
                    self.listStringVar.get(disk)[3].set("%i%%"%(ds.percent))
                except:
                    print "erro"
            

            #virtual_memory().free/1024.0/1024.0/1024.0#memoria virtual livre
        self.evento.set()
        
    def getDisk_partitions(self):
        partitions = []
        for disk in disk_partitions():
            #print(disk.fstype)
            if disk.fstype == "NTFS" or disk.fstype == "CDFS" or disk.fstype == "FAT32":# device, mountpoint, fstype (filesysten type), opts
                partitions.append((disk.device, disk.fstype))
        return tuple(partitions)

        
    def quebrarEvento(self):
        self.desligar = True
        root.destroy()
        
    
        
            
        
        
root = t.Tk()
app = janela(master=root)
app.mainloop()
