# -*- coding: utf-8 -*-
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import numpy as np
import pylab
import random
import os
import shutil
from bb84_protocol_module import *

#matplotlib.use('WxAgg')

class grafica(wx.Frame):
    title = 'Simulations of parameters into the QKD BB84 protocol'
    def __init__(self,):
        wx.Frame.__init__(self, None, -1, self.title, size=(400,400))
        
        ## Simulation_1 ## 
        self.NumSimSim1=500
        self.NumBitsSim1=600
        self.XSim1 = np.linspace(0,self.NumBitsSim1-1,num=self.NumBitsSim1)
        #################

        ## Simulation_2 ## 
        self.lon22=600
        self.lon32=500
        self.hisX2 = np.linspace(0,self.lon22-1,num=self.lon22)
        #################

        ## Simulation_3 ## 
        self.lon23=600
        self.lon33=500

        self.hisX0 = np.linspace(0,self.lon23-1,num=self.lon23)
        #################

        ## Simulation_4 ## 
        self.lon24=1000
        self.lon34=3
        self.lambdaa4=1 # Probabilidad de que aparezca Eve en la señal 
        self.ML4=[]
        self.ML42=[]
        self.a4=0 # si es cero, no esta presente la despolarizacion en la señal puesto que no se despolariza ningun foton. Por otro lado, si esta entre 0 y 1, es el porcentaje de qbits que se despolarizan
        self.sen4="-"
        self.hisX4 = np.linspace(0,100-1,num=100)

        #Para salar la desviasion estandar
        self.STD4=[]
        self.XSTD4=[]
        self.NUM4=50

        self.STD42=[]
        self.XSTD42=[]
        self.NUM42=50

        self.BerT4=25+25*self.a4+12.5*self.lambdaa4
        self.QberT4=25*self.lambdaa4+50*self.a4
        #################

        ## Simulation_5 ## 
        self.lon25=9000
        self.lon35=3
        self.lambdaa5=0 # Probabilidad de que aparezca Eve en la señal 
        self.ML53=[]
        self.ML54=[]
        self.N_a5=11 ## numero de probabilidades de polarizacion a evaluar
        self.sen5="-"
        self.max_a5=0.1
        self.x5 = np.linspace(0,self.max_a5,num=self.N_a5)

        self.BerT5=25+25*self.x5+12.5*self.lambdaa5
        self.QberT5=25*self.lambdaa5+50*self.x5

        #################

        ## Simulation_6 ## 
        self.lon26=200
        self.lon36=100
        self.a6=0
        self.ML63=[]
        self.ML64=[]
        self.N_lambdaa6=11 ## numero de probabilidades de polarizacion a evaluar
        self.sen6="-"
        self.max_lambdaa6=1
        self.x6 = np.linspace(0,self.max_lambdaa6,num=self.N_lambdaa6)

        self.BerT6=25+25*self.a6+12.5*self.x6
        self.QberT6=25*self.x6+50*self.a6
        #################

        ## Simulation_7 ## 
        self.lon27=200
        self.lon37=100
        self.ML73=[]
        self.ML74=[]
        self.N_lambdaa7=11 ## numero de probabilidades de polarizacion a evaluar
        self.N_a7=11  ## numero de probabilidades de polarizacion a evaluar
        self.sen7="-"
        self.max_lambdaa7=1
        self.max_a7=0.1
        self.x7 = np.linspace(0,self.max_lambdaa7,num=self.N_lambdaa7)
        self.x72 = np.linspace(0,self.max_a7,num=self.N_a7)
        self.Z7=np.zeros((self.N_lambdaa7, self.N_a7))
        self.Z72=np.zeros((self.N_lambdaa7, self.N_a7))

        ## Para los ejes de Qber
        self.X = np.arange(0, 0.11, 0.01)
        self.xlen = len(self.X)
        self.Y = np.arange(0, 1.1, 0.1)
        self.ylen = len(self.Y)
        self.X, self.Y = np.meshgrid(self.X, self.Y)

        ## Para los ejes de Ber
        self.X2 = np.arange(0, 0.11, 0.01)
        self.Y2 = np.arange(0, 1.1, 0.1)
        self.X2, self.Y2 = np.meshgrid(self.X2, self.Y2)

        #################

        
        self.dpi = 1000
        self.NamePlots=['Sim 1a','Sim 1b','Ejer 2','Ejer 3a','Ejer 3b',
                        'Ejer 4a','Ejer 4b','Ejer 4c','Ejer 4d','Ejer 4e',
                        'Ejer 4f','Ejer 5a','Ejer 5b','Ejer 6a','Ejer 6b',
                        'Ejer 7a','Ejer 7b',"Save all plots"]
        

        self.create_menu()
        self.create_main_panel()

    ## Simulation 1:Distribution of the bits and bases in the RawKey list 
    ##              and the RanBases list, respectively.The theoretical value 
    ##              is 50%.

    def simulation_1(self):
        RecIndexesSim1=[]
        DiaIndexesSim1=[]
        OnesIndexesSim1=[]
        ZerosIndexesSim1=[]
        print("Simulation 1-start")
        for i in range(self.NumSimSim1):
            RawKey=raw_key(self.NumBitsSim1) 
            RanBases=random_bases(self.NumBitsSim1)
            for j in range(self.NumBitsSim1):
                (OnesIndexesSim1 if RawKey[j] == 1 else ZerosIndexesSim1).append(j)
                (RecIndexesSim1 if RanBases[j] == "Rec" else DiaIndexesSim1).append(j)
            
        self.HistOnesSim1, BinEdgeOnesSim1 = np.histogram(OnesIndexesSim1,bins = range(self.NumBitsSim1+1))
        self.HistZerosSim1, BinEdgeZerosSim1 = np.histogram(ZerosIndexesSim1,bins = range(self.NumBitsSim1+1))
        self.HistRecSim1, BinEdgeRecSim1 = np.histogram(RecIndexesSim1,bins = range(0,self.NumBitsSim1+1))
        self.HistDiaSim1, BinEdgeDiaSim1 = np.histogram(DiaIndexesSim1,bins = range(0,self.NumBitsSim1+1))
        print("Simulation 1-end\n")

    ## Simulation 2: Calculation if approximately 50% of the bases agree 
    ##               (Agree), the other approximately 50% of the bases 
    ##               do not agree.
    def simulation_2(self):
        print("Simulation 2-start")
        wf1=[]
        wf2=[]

        for i in range(0,self.lon32):
            M=random_bases(self.lon22)## Alice Bases
            R=random_bases(self.lon22)## Bob Bases

            for j in range(0,self.lon22):
                if M[j]==R[j]:
                    wf1.append(j)
                else:
                    wf2.append(j)

        self.hist22, self.bin_edge22 = np.histogram(wf1,bins = range(0,self.lon22+1))
        self.hist32, self.bin_edge32 = np.histogram(wf2,bins = range(0,self.lon22+1))

        ##Valor Teorico
        point12 = [0, 50]
        point22 = [self.lon22, 50]

        self.x_values21= [point12[0], point22[0]]
        self.y_values21= [point12[1], point22[1]]
        print("Simulation 2-end\n")


    ## Observar que si se cumple que aproximadamente el 25% de los angulos estan compuesto por 0, otro 25% por 45, otro 25% por 90 y otro 25% por 135 
    def Ejercicio3(self):
        print("Ejercicio 3-start")
        wf3=[]
        wf0=[]
        wf45=[]
        wf90=[]
        wf135=[]
        # for i in range(0,self.lon33):
        #     M3=RawKey(self.lon23)## Alice Bases
        #     R3=RandomBase(self.lon23)## Bob Bases
        #     N3=Encode(M3,R3)

        #     for j in range(0,self.lon23):
        #         wf3.append(N3[j])

        # #this is for doing that wf falls down in the first block of length lon2#
        # for O in range(0,self.lon23*self.lon33):
        #     if wf3[O]==0:
        #         wf0.append(O%self.lon23)#it's for selecting the indexs where there is a "0"
        #     elif wf3[O]==45:
        #         wf45.append(O%self.lon23)#it's for selecting the indexs where there is an "45"
        #     elif wf3[O]==90:
        #         wf90.append(O%self.lon23)#it's for selecting the indexs where there is an "90"
        #     elif wf3[O]==135:
        #         wf135.append(O%self.lon23)#it's for selecting the indexs where there is an "135"

        for i in range(0,self.lon33):
            M3=raw_key(self.lon23)## Alice Bases
            R3=random_bases(self.lon23)## Bob Bases
            N3=encode(M3,R3)
            
            for j in range(0,self.lon23):
                if N3[j]==0:
                    wf0.append(j)#it's for selecting the indexs where there is a "0"
                elif N3[j]==45:
                    wf45.append(j)#it's for selecting the indexs where there is an "45"
                elif N3[j]==90:
                    wf90.append(j)#it's for selecting the indexs where there is an "90"
                else:
                    wf135.append(j)

        self.hist0, self.bin_edge0 = np.histogram(wf0,bins = range(0,self.lon23+1))
        self.hist45, self.bin_edge45 = np.histogram(wf45,bins = range(0,self.lon23+1))
        self.hist90, self.bin_edge90 = np.histogram(wf90,bins = range(0,self.lon23+1))
        self.hist135, self.bin_edge135 = np.histogram(wf135,bins = range(0,self.lon23+1))

        ##Valor Teorico
        point13 = [0, 25]
        point23 = [self.lon23, 25]

        self.x_values31= [point13[0], point23[0]]
        self.y_values31= [point13[1], point23[1]]
        print("Ejercicio 3-end")

    ##Evolucion del Qber completo con respecto a la longuitud de la RawKey (Con una probabilidad de despolarizacion de a4 y de presencia de Eve de lambdaa4)
    def Ejercicio4(self):
        print("Ejercicio 4-start")
        self.x4=np.linspace(90,self.lon24+90,num=self.lon24+1)
        for i in self.x4:
            if i%100==0:
                print("i: "+str(i))
            RR1=[]
            RR2=[]
            for j in range(0,self.lon34):
                ## Alice ##
                L4=raw_key(int(i))
                M4=random_bases(int(i))
                N4=encode(L4,M4)

                r=random.uniform(-(1-self.lambdaa4)*10,self.lambdaa4*10)
                if r>0:
                    ## Canal Cuántico ##   
                    FF4=depolarization(N4,self.a4,self.sen4)
                    ## Eve ##
                    F4=random_bases(int(i))
                    D4=decode(FF4,F4)
                    A4=encode(D4,F4)
                    ## Canal Cuántico ##   
                    AA4=depolarization(A4,self.a4,self.sen4) 
                else:
                    AA4=depolarization(N4,self.a4,self.sen4)

                ## Bob ##
                R4=random_bases(int(i))
                E4=decode(AA4,R4)

                #Qber
                T4=qber(L4,E4,M4,R4)
                RR1.append(T4)

                #Ber
                T42=ber(L4,E4)
                RR2.append(T42)
            self.ML4.append(np.mean(RR1)*100)
            self.ML42.append(np.mean(RR2)*100)

        self.hist4, self.bin_edge4 = np.histogram(self.ML4,bins = range(0,100+1))
        self.hist42, self.bin_edge42 = np.histogram(self.ML42,bins = range(0,100+1))

        #### Esto es para observar el comportamiento de la Desviacion Estandar cada self.num4 de longuitud####

        for i in range(0,int(len(self.x4)*(self.NUM4**(-1)))):
            self.STD4.append(np.std(self.ML4[self.NUM4*i:self.NUM4*(i+1)]))
            self.XSTD4.append((i+1))

        for i in range(0,int(len(self.x4)*(self.NUM42**(-1)))):
            self.STD42.append(np.std(self.ML42[self.NUM42*i:self.NUM42*(i+1)]))
            self.XSTD42.append((i+1))


        ##Valor Teorico Qber
        point14 = [0, self.QberT4]
        point24 = [self.lon24, self.QberT4]

        self.x_values41= [point14[0], point24[0]]
        self.y_values41= [point14[1], point24[1]]

        ##Valor Teorico Qber Histograma
        self.L=np.amax(self.hist4)+500
        point34 = [self.QberT4, 0]
        point44 = [self.QberT4, self.L]

        self.x_values42= [point34[0], point44[0]]
        self.y_values42= [point34[1], point44[1]]

        ##Valor Teorico Ber
        self.L2=np.amax(self.hist42)+500
        point54 = [0, self.BerT4]
        point64 = [self.lon24, self.BerT4]

        self.x_values43= [point54[0], point64[0]]
        self.y_values43= [point54[1], point64[1]]

        ##Valor Teorico Qber Histograma
        point64 = [self.BerT4, 0]
        point74 = [self.BerT4, self.L2]

        self.x_values44= [point64[0], point74[0]]
        self.y_values44= [point64[1], point74[1]]

        print("Ejercicio 4")
        print("Valor promedio de Qber: "+str(np.mean(self.ML4)))
        print("Valor promedio de Ber: "+str(np.mean(self.ML42)))
        print("Ejercicio 4-end")


    ## Comportaiento del Qber y del Ber con respecto a a5 al dejar fijo el valor de lambdaa5. 
    ## Para ello, se hizo variar la simulacion lon35 con una longuitud de clave lon25 y se promedio tanto el Qber como el Ber sobre lon35
    def Ejercicio5(self):
        print("\n"+"Ejercicio 5-start"+"\n")

        for a5 in self.x5:
            ML5=[]
            ML52=[]
            for i in range(0,self.lon35):
                ## Alice ##
                L5=raw_key(self.lon25)
                M5=random_bases(self.lon25)
                N5=encode(L5,M5)

                r=random.uniform(-(1-self.lambdaa5)*10,self.lambdaa5*10)
                if r>0:
                    print("Si")
                    ## Canal Cuántico ##   
                    FF5=depolarization(N5,a5,self.sen5)
                    ## Eve ##
                    F5=random_bases(self.lon25)
                    D5=decode(FF5,F5)
                    A5=encode(D5,F5)
                    ## Canal Cuántico ##   
                    AA5=depolarization(A5,a5,self.sen5) 
                else:
                    AA5=depolarization(N5,a5,self.sen5)

                ## Bob ##
                R5=random_bases(self.lon25)
                E5=decode(AA5,R5)

                #Qber
                T5=qber(L5,E5,M5,R5)
                ML5.append(T5*100)

                #Ber
                T52=ber(L5,E5)
                ML52.append(T52*100)
            print("a5:"+str(a5))
            print("numero de elementos de ML5:"+str(len(ML5)))
            print("Valor minimo de ML5:"+str(np.amin(ML5)))
            print("numero de elementos de ML52:"+str(len(ML52)))
            print("Valor minimo de ML52:"+str(np.amin(ML52))+"\n")

            self.ML53.append(np.mean(ML5))
            self.ML54.append(np.mean(ML52))



        print("Esto es a5:"+str(self.x5))
        print("Esto es Qber:"+str(self.ML53))
        print("Esto es Ber:"+str(self.ML54))
        print("Ejercicio 5-end")


    ## Comportaiento del Qber y del Ber con respecto a lambdaa6 al dejar fijo el valor de a6. 
    ## Para ello, se hizo variar la simulacion lon36 con una longuitud de clave lon26 y se promedio tanto el Qber como el Ber sobre lon36
    def Ejercicio6(self):
        print("\n"+"Ejercicio 6-start"+"\n")
        for lambdaa6 in self.x6:
            print("lambdaa6: "+str(lambdaa6))
            ML6=[]
            ML62=[]
            for i in range(0,self.lon36):
                ## Alice ##
                L6=raw_key(self.lon26)
                M6=random_bases(self.lon26)
                N6=encode(L6,M6)

                r=random.uniform(-(1-lambdaa6)*10,lambdaa6*10)
                if r>0:
                    ## Canal Cuántico ##   
                    FF6=depolarization(N6,self.a6,self.sen6)
                    ## Eve ##
                    F6=random_bases(self.lon26)
                    D6=decode(FF6,F6)
                    A6=encode(D6,F6)
                    ## Canal Cuántico ##   
                    AA6=depolarization(A6,self.a6,self.sen6) 
                else:
                    AA6=depolarization(N6,self.a6,self.sen6)

                ## Bob ##
                R6=random_bases(self.lon26)
                E6=decode(AA6,R6)

                #Qber
                T6=qber(L6,E6,M6,R6)
                ML6.append(T6*100)

                #Ber
                T62=ber(L6,E6)
                ML62.append(T62*100)
            print("lambdaa6:"+str(lambdaa6))
            print("numero de elementos de ML6:"+str(len(ML6)))
            print("Valor minimo de ML6:"+str(np.amin(ML6)))
            print("numero de elementos de ML62:"+str(len(ML62)))
            print("Valor minimo de ML62:"+str(np.amin(ML62))+"\n")

            self.ML63.append(np.mean(ML6))
            self.ML64.append(np.mean(ML62))

        print("Esto es lambdaa6:"+str(self.x5))
        print("Esto es Qber:"+str(self.ML63))
        print("Esto es Ber:"+str(self.ML64))
        print("Ejercicio 6-start")

    ## Comportaiento del Qber y del Ber con respecto a lambdaa7 y a7. 
    ## Para ello, se hizo variar la simulacion lon37 con una longuitud de clave lon27 y se promedio tanto el Qber como el Ber sobre lon37
    def Ejercicio7(self):
        print("\n"+"Ejercicio 7-start"+"\n")
        j=0

        for lambdaa7 in self.x7:

            l=0
            for a7 in self.x72:
                ML7=[]
                ML72=[]
                L=0
                L2=0
                for i in range(0,self.lon37):
                    ## Alice ##
                    L7=raw_key(self.lon27)
                    M7=random_bases(self.lon27)
                    N7=encode(L7,M7)

                    r=random.uniform(-(1-lambdaa7)*10,lambdaa7*10)
                    if r>0:
                        ## Canal Cuántico ##   
                        FF7=depolarization(N7,a7,self.sen7)
                        ## Eve ##
                        F7=random_bases(self.lon27)
                        D7=decode(FF7,F7)
                        A7=encode(D7,F7)
                        ## Canal Cuántico ##   
                        AA7=depolarization(A7,a7,self.sen7) 
                    else:
                        AA7=depolarization(N7,a7,self.sen7)

                    ## Bob ##
                    R7=random_bases(self.lon27)
                    E7=decode(AA7,R7)

                    #Qber
                    T7=qber(L7,E7,M7,R7)
                    ML7.append(T7*100)

                    #Ber
                    T72=ber(L7,E7)
                    ML72.append(T72*100)
                L=np.mean(ML7)
                L2=np.mean(ML72)
                self.Z7[j][l]=L
                self.Z72[j][l]=L2
                l=l+1
            j=j+1
            print("Z7:"+str(self.Z7))
            print("Z72:"+str(self.Z72))



    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        m_expt2 = menu_file.Append(-1, "&Save config\tCtrl-R", "Save config.")
        self.Bind(wx.EVT_MENU, self.Write_report, m_expt2)
        m_expt3 = menu_file.Append(-1, "&Load config.", "Load config.")
        #self.Bind(wx.EVT_MENU, self.on_load_cfg, m_expt3)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        self.Bind(wx.EVT_CLOSE, self.on_exit)
                
        self.menubar.Append(menu_file, "&File")
        self.SetMenuBar(self.menubar)
    
    def Write_report(self,event):

        dlg2 = wx.FileDialog(
            self, 
            message="Save config...",
            defaultDir=os.getcwd(),
            defaultFile="Information_of_the_simulations.txt",
            wildcard="TXT (*.txt)|*.txt",
            style=wx.FD_SAVE)

        
        if dlg2.ShowModal() == wx.ID_OK:
            path = dlg2.GetPath()
            file = open(path,"a")
            file.write("\n=========================\n")
            file.write("Simulation 1:Distribution of the bits and bases in the RawKey list and the RanBases list, respectively.The theoretical value is 50%.\n")
            file.write("=========================\n\n")
            file.write("Length of the Rawkey: "+str(self.NumBitsSim1)+"\n")
            file.write("Number of simulations: "+str(self.NumSimSim1)+"\n")

            file.write("\n=========================\n")
            file.write("Ejercicio 2: Observar que si se cumple que aproximadamente el 50% de las bases concuerdan (Agree) y\n")
            file.write("y el otro aproximadamente 50% de las bases no concuerdan\n")
            file.write("=========================\n\n")
            file.write("Longuitud de la Rawkey: "+str(self.lon22)+"\n")
            file.write("Número de repeticiones: "+str(self.lon32)+"\n")

            file.write("\n=========================\n")
            file.write("Ejercicio 3: Observar que si se cumple que aproximadamente el 25% de los angulos estan compuesto por 0,\n")
            file.write("otro 25% por 45, otro 25% por 90 y otro 25% por 135\n")
            file.write("=========================\n\n")
            file.write("Longuitud de la Rawkey: "+str(self.lon23)+"\n")
            file.write("Número de repeticiones: "+str(self.lon33)+"\n")

            file.write("\n=========================\n")
            file.write("Ejercicio 4: Evolucion del Qber completo con respecto a la longuitud de la RawKey (Con una probabilidad de \n")
            file.write("despolarizacion de a4 y de presencia de Eve de lambdaa4)\n")
            file.write("=========================\n\n")
            file.write("Longuitud maxima de la Rawkey: "+str(self.lon24)+"\n")
            file.write("Número de repeticiones: "+str(self.lon33)+"\n")
            file.write("Valor de "+r'$\lambda$'+" : "+str(self.lambdaa4)+"\n")
            file.write("Valor de "+r'$\alpha$'+" : "+str(self.a4)+"\n")
            file.write("Sentido de la despolarización: "+str(self.sen4)+"\n")
            file.write("Numero de datos por cada grupo para la desviacion estandar para el Qber: "+str(self.NUM4)+"\n")
            file.write("Numero de datos por cada grupo para la desviacion estandar para el Ber: "+str(self.NUM42)+"\n")

            file.write("\n=========================\n")
            file.write("Ejercicio 5: Comportaiento del Qber y del Ber con respecto a a5 al dejar fijo el valor de lambdaa5.\n" )
            file.write("Para ello, se hizo variar la simulacion lon35 con una longuitud de clave lon25 y se promedio tanto el Qber como el Ber sobre lon35)\n")
            file.write("=========================\n\n")
            file.write("Longuitud de la Rawkey: "+str(self.lon25)+"\n")
            file.write("Número de repeticiones: "+str(self.lon35)+"\n")
            file.write("Valor de "+r'$\lambda$'+" : "+str(self.lambdaa5)+"\n")
            file.write("Sentido de la despolarización: "+str(self.sen5)+"\n")
            file.write("Valores de "+r'$\alpha$'+" : "+str(self.x5)+"\n")

            file.write("\n=========================\n")
            file.write("Ejercicio 6: Comportaiento del Qber y del Ber con respecto a lambdaa6 al dejar fijo el valor de a6. \n")
            file.write(" Para ello, se hizo variar la simulacion lon36 con una longuitud de clave lon26 y se promedio tanto el Qber como el Ber sobre lon36\n")
            file.write("=========================\n\n")
            file.write("Longuitud de la Rawkey: "+str(self.lon26)+"\n")
            file.write("Número de repeticiones: "+str(self.lon36)+"\n")
            file.write("Valor de "+r'$\alpha$'+" : "+str(self.a6)+"\n")
            file.write("Sentido de la despolarización: "+str(self.sen6)+"\n")
            file.write("Valores de "+r'$\lambdaa6$'+" : "+str(self.x6)+"\n")

            file.write("\n=========================\n")
            file.write("Ejercicio 7: Comportaiento del Qber y del Ber con respecto a lambdaa7 y a7. \n")
            file.write("Para ello, se hizo variar la simulacion lon37 con una longuitud de clave lon27 y se promedio tanto el Qber como el Ber sobre lon37\n")
            file.write("=========================\n\n")
            file.write("Longuitud de la Rawkey: "+str(self.lon27)+"\n")
            file.write("Número de repeticiones: "+str(self.lon37)+"\n")
            file.write("Sentido de la despolarización: "+str(self.sen6)+"\n")
            file.write("Valores de "+r'$\lambdaa6$'+" : "+str(self.x7)+"\n")
            file.write("Valores de "+r'$\alpha$'+" : "+str(self.x72)+"\n")

            file.write("\n--------------\n")

            file.close()

    def on_save_plot(self,event):
        modal=wx.SingleChoiceDialog(None,"Which plot would you like to save?","Plots",self.NamePlots)
        if modal.ShowModal()==wx.ID_OK:
            if modal.GetStringSelection()!=self.NamePlots[-1]:
                dlg = wx.FileDialog(
                    self, 
                    message="Save plot as...",
                    defaultDir=os.getcwd(),
                    defaultFile=modal.GetStringSelection(),
                    wildcard="PDF (*.pdf)|*.pdf",
                    style=wx.FD_SAVE)
                if dlg.ShowModal() == wx.ID_OK:
                    NumPlot = [i for i, x in enumerate(self.NamePlots) if x == modal.GetStringSelection()][0]
                    self.canvas[NumPlot].print_figure(dlg.GetPath(), dpi=self.dpi)
            else:
                dlg = wx.DirDialog(
                    self, 
                    message="Select directory...",
                    style=wx.DD_DEFAULT_STYLE)
                if dlg.ShowModal() == wx.ID_OK:
                    DirPath=os.path.join(dlg.GetPath(),"All_plots")
                    if os.path.exists(DirPath):
                        shutil.rmtree(DirPath)
                    os.mkdir(DirPath)
                    for i in range(17):
                        path = os.path.join(DirPath, self.NamePlots[i]+".pdf") 
                        self.canvas[i].print_figure(path, dpi=self.dpi)

        modal.Destroy()

        

    def on_exit(self, event):
        for i in range(17):
            pylab.close(self.figs[i]) 

        self.Destroy()

    def create_main_panel(self):
        self.panel = wx.Panel(self,id=-1, pos=(500,500),size=(1000,1000),name="hola")
        self.st = wx.Button(self.panel, id = 1, label ="Button", pos =(1000, 600), size =(100, 40),  name ="button")
        
        self.Vbox=wx.BoxSizer(wx.VERTICAL) 

        ######

        self.figs=[]
        self.axes=[]

        for i in range(17):
            if i<15:
                auxfigs,auxaxes=pylab.subplots(1)
            else:
                auxfigs=pylab.figure()
                auxaxes=auxfigs.add_subplot(projection='3d')
            self.figs.append(auxfigs)
            self.axes.append(auxaxes)

        ####
        self.nb = wx.Notebook(self.panel,size=(2000,700),pos=(0,0),style=wx.NB_MULTILINE)
        ####
        self.canvas=[]
        for i in range(17):
            self.canvas.append(FigCanvas(self.nb, -1, self.figs[i]))

        ####
        for i in range(17):
            self.nb.AddPage(self.canvas[i], self.NamePlots[i])

        #### 

        self.Vbox.Add(self.nb,0,wx.ALL,0)

        self.mainbox = wx.BoxSizer(wx.VERTICAL)

        self.mainbox.Add(self.Vbox,0,wx.ALL,0)

        self.panel.SetSizer(self.mainbox)
        self.mainbox.Fit(self)

        self.init_plot()
        #######################



    def init_plot(self):
        for i in range(17):
            self.axes[i].cla()

        self.simulation_1()
        self.simulation_2()
        self.Ejercicio3()
        self.Ejercicio4()
        self.Ejercicio5()
        self.Ejercicio6()
        self.Ejercicio7()

        self.axes[0].plot(
            self.XSim1,self.HistOnesSim1*100*((self.NumSimSim1)**(-1)),'r',
            self.XSim1,self.HistZerosSim1*100*((self.NumSimSim1)**(-1)),'b',
            self.XSim1,(self.HistOnesSim1+self.HistZerosSim1)*100*((self.NumSimSim1)**(-1)),'y',
            [0, self.NumBitsSim1],[50,50],'limegreen')
        self.axes[1].plot(
            self.XSim1,self.HistRecSim1*100*((self.NumSimSim1)**(-1)),'r',
            self.XSim1,self.HistDiaSim1*100*((self.NumSimSim1)**(-1)),'b',
            self.XSim1,(self.HistRecSim1+self.HistDiaSim1)*100*((self.NumSimSim1)**(-1)),'y',
            [0, self.NumBitsSim1],[50,50],'limegreen')
        self.axes[2].plot(
            self.hisX2,self.hist22*100*((self.lon32)**(-1)),'r',
            self.hisX2,self.hist32*100*((self.lon32)**(-1)),'b',
            self.x_values21,self.y_values21,'limegreen',
            self.hisX2,((self.hist22+self.hist32)*100*((self.lon32)**(-1))),'y')
        self.axes[3].plot(
            self.hisX0,self.hist0*100*((self.lon33)**(-1)),'r',
            self.hisX0,self.hist90*100*((self.lon33)**(-1)),'b',
            self.x_values31,self.y_values31,'limegreen',
            self.hisX0,((self.hist0+self.hist45+self.hist90+self.hist135)*100*((self.lon33)**(-1))),'y')
        self.axes[4].plot(
            self.hisX0,self.hist45*100*((self.lon33)**(-1)),'r',
            self.hisX0,self.hist135*100*((self.lon33)**(-1)),'b',
            self.x_values31,self.y_values31,'limegreen',
            self.hisX0,((self.hist0+self.hist45+self.hist90+self.hist135)*100*((self.lon33)**(-1))),'y')
        self.axes[5].plot(
            np.array(self.x4),self.ML4,'r',
            self.x_values41,self.y_values41,'limegreen')
        self.axes[6].bar(self.hisX4,self.hist4,facecolor='#FF0000')
        self.axes[6].plot(self.x_values42,self.y_values42,'limegreen')
        self.axes[7].plot(self.XSTD4,self.STD4,'r')
        self.axes[8].plot(
            np.array(self.x4),self.ML42,'r',
            self.x_values43,self.y_values43,'limegreen')
        self.axes[9].bar(self.hisX4,self.hist42,facecolor='#FF0000')
        self.axes[9].plot(self.x_values44,self.y_values44,'limegreen')
        self.axes[10].plot(self.XSTD42,self.STD42,'r')
        self.axes[11].plot(
            self.x5,self.ML53,'r',
            self.x5,self.QberT5,'limegreen')
        self.axes[12].plot(
            self.x5,self.ML54,'r',
            self.x5,self.BerT5,'limegreen')
        self.axes[13].plot(self.x6,self.ML63,'r')
        self.axes[14].plot(self.x6,self.ML64,'r')

        self.Dibujo12= self.axes[15].plot_surface(
            self.X,self.Y,self.Z7,cmap='hot',antialiased=False,alpha=0.6) 
        self.figs[15].colorbar(self.Dibujo12, shrink=0.5, aspect=5.5)
        
        self.Dibujo13= self.axes[16].plot_surface(
            self.X2,self.Y2,self.Z72,  cmap='hot',antialiased=False, rstride=1, cstride=1, alpha=0.6)
        self.figs[16].colorbar(self.Dibujo13, shrink=0.5, aspect=5.5)

        # # ### Para mejorar las graficas   
        # # #
        self.axes[0].set_xlabel("Posicion del bit", fontsize=16)
        self.axes[0].set_xlim(left=0, right=self.NumBitsSim1)
        #
        self.axes[0].set_ylabel("Probabilidad (%)", fontsize=16)
        self.axes[0].set_ylim(top=101, bottom=0)
        #
        self.axes[0].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[0].set_facecolor('black')
        self.axes[0].grid(True, color='gray')


        self.axes[1].set_xlabel("Posicion de la base", fontsize=16)
        self.axes[1].set_xlim(left=0, right=self.lon22)
        #
        self.axes[1].set_ylabel("Probabilidad (%)", fontsize=16)
        self.axes[1].set_ylim(top=101, bottom=0)
        #
        self.axes[1].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[1].set_facecolor('black')
        self.axes[1].grid(True, color='gray')


        self.axes[2].set_xlabel("Posicion de la base", fontsize=16)
        self.axes[2].set_xlim(left=0, right=self.lon22)
        #
        self.axes[2].set_ylabel("Probabilidad (%)", fontsize=16)
        self.axes[2].set_ylim(top=101, bottom=0)
        #
        self.axes[2].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[2].set_facecolor('black')
        self.axes[2].grid(True, color='gray')


        self.axes[3].set_xlabel("Posicion del Qbit", fontsize=16)
        self.axes[3].set_xlim(left=0, right=self.lon23)
        #
        self.axes[3].set_ylabel("Probabilidad (%)", fontsize=16)
        self.axes[3].set_ylim(top=101, bottom=0)
        #
        self.axes[3].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[3].set_facecolor('black')
        self.axes[3].grid(True, color='gray')


        self.axes[4].set_xlabel("Posicion del Qbit", fontsize=16)
        self.axes[4].set_xlim(left=0, right=self.lon23)
        #
        self.axes[4].set_ylabel("Probabilidad (%)", fontsize=16)
        self.axes[4].set_ylim(top=101, bottom=0)
        #
        self.axes[4].set_facecolor('black')
        self.axes[4].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[4].grid(True, color='gray')


        self.axes[5].set_xlabel("Longuitud de la RawKey", fontsize=16)
        self.axes[5].set_xlim(left=0, right=self.lon24)
        #
        self.axes[5].set_ylabel("Qber", fontsize=16)
        self.axes[5].set_ylim(top=101, bottom=0)
        #
        self.axes[5].tick_params(axis = 'both', which ='major', labelsize = 14)
        self.axes[5].set_facecolor('black')
        self.axes[5].grid(True, color='gray')


        self.axes[6].set_xlabel("Qber", fontsize=16)
        self.axes[6].set_xlim(left=10, right=40)
        #
        self.axes[6].set_ylabel("Numero de occurrencias", fontsize=16)
        self.axes[6].set_ylim(top=self.L, bottom=0)
        #
        self.axes[6].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[6].set_facecolor('black')
        self.axes[6].grid(True, color='gray')


        self.axes[7].set_xlabel('Numero de grupo', fontsize=16)
        self.axes[7].set_xlim(left=0, right=(self.lon24*(self.NUM4**-1))+10)
        #
        self.axes[7].set_ylabel('Desviacion Estandar', fontsize=16)
        self.axes[7].set_ylim(top=np.amax(self.STD4)+1, bottom=0)
        #
        self.axes[7].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[7].set_facecolor('black')
        self.axes[7].grid(True, color='gray')


        self.axes[8].set_xlabel("Longuitud de la RawKey", fontsize=16)
        self.axes[8].set_xlim(left=0, right=self.lon24)
        #
        self.axes[8].set_ylabel("Ber", fontsize=16)
        self.axes[8].set_ylim(top=101, bottom=0)
        #
        self.axes[8].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[8].set_facecolor('black')
        self.axes[8].grid(True, color='gray')


        self.axes[9].set_xlabel("Ber", fontsize=16)
        self.axes[9].set_xlim(left=20, right=50)
        #
        self.axes[9].set_ylabel("Numero de occurrencias", fontsize=16)
        self.axes[9].set_ylim(top=self.L2, bottom=0)
        #
        self.axes[9].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[9].set_facecolor('black')
        self.axes[9].grid(True, color='gray')


        self.axes[10].set_xlabel('Numero de grupo', fontsize=16)
        self.axes[10].set_xlim(left=0, right=(self.lon24*(self.NUM42**-1))+10)
        #
        self.axes[10].set_ylabel('Desviacion Estandar', fontsize=16)
        self.axes[10].set_ylim(top=np.amax(self.STD42)+1, bottom=0)
        #
        self.axes[10].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[10].set_facecolor('black')
        self.axes[10].grid(True, color='gray')


        self.axes[11].set_xlabel(r'$\alpha$', fontsize=16)
        self.axes[11].set_xlim(left=0, right=1.1*self.max_a5)
        #
        self.axes[11].set_ylabel("Qber", fontsize=16)
        self.axes[11].set_ylim(top=100, bottom=0)
        #
        self.axes[11].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[11].set_facecolor('black')
        self.axes[11].grid(True, color='gray')


        self.axes[12].set_xlabel(r'$\alpha$', fontsize=16)
        self.axes[12].set_xlim(left=0, right=1.1*self.max_a5)
        #
        self.axes[12].set_ylabel("Ber", fontsize=16)
        self.axes[12].set_ylim(top=100, bottom=0)
        #
        self.axes[12].tick_params(axis = 'both', which ='major', labelsize = 14)
        self.axes[12].set_facecolor('black')
        self.axes[12].grid(True, color='gray')


        self.axes[13].set_xlabel(r'$\lambda$', fontsize=16)
        self.axes[13].set_xlim(left=0, right=1.1*self.max_lambdaa6)
        #
        self.axes[13].set_ylabel("Qber", fontsize=16)
        self.axes[13].set_ylim(top=100, bottom=0)
        #
        self.axes[13].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[13].set_facecolor('black')
        self.axes[13].grid(True, color='gray')


        self.axes[14].set_xlabel(r'$\lambda$', fontsize=16)
        self.axes[14].set_xlim(left=0, right=1.1*self.max_lambdaa6)
        #
        self.axes[14].set_ylabel("Ber", fontsize=16)
        self.axes[14].set_ylim(top=100, bottom=0)
        #
        self.axes[14].tick_params(axis = 'both', which ='major', labelsize = 14)
        self.axes[14].set_facecolor('black')
        self.axes[14].grid(True, color='gray')

 
        self.axes[15].set_xlabel(r'$\alpha$', fontsize=16,labelpad=20)
        self.axes[15].set_xlim(left=0, right=1.1*self.max_a7)
        self.axes[15].tick_params(axis='x', which='major', pad=3)
        #
        self.axes[15].set_ylabel(r'$\lambda$', fontsize=16,labelpad=20)
        self.axes[15].set_ylim(bottom=0, top=1.1*self.max_lambdaa7)
        self.axes[15].tick_params(axis='y', which='major', pad=3)
        #
        self.axes[15].set_zlabel("Qber", fontsize=16,labelpad=15)
        self.axes[15].set_zlim(bottom=0, top=100)
        self.axes[15].tick_params(axis='z', which='major', pad=3)
        #
        self.axes[15].tick_params( axis = 'both', which ='major', labelsize = 14)
        self.axes[15].grid(True, color='gray')


        self.axes[16].set_xlabel(r'$\alpha$', fontsize=16,labelpad=20)
        self.axes[16].set_xlim(left=0, right=1.1*self.max_a7)
        self.axes[16].tick_params(axis='x', which='major', pad=3)
        #
        self.axes[16].set_ylabel(r'$\lambda$', fontsize=16,labelpad=20)
        self.axes[16].set_ylim(bottom=0, top=1.1*self.max_lambdaa7)
        self.axes[16].tick_params(axis='y', which='major', pad=3)
        #
        self.axes[16].set_zlabel("Ber", fontsize=16,labelpad=15)
        self.axes[16].set_zlim(bottom=0, top=100)
        self.axes[16].tick_params(axis='z', which='major', pad=3)
        #
        self.axes[16].tick_params(axis = 'both', which ='major', labelsize = 14)
        self.axes[16].grid(True, color='gray')
        
        ## Legends ##
        self.axes[0].legend(["Uno", "Cero","Teorico","Total"],loc= 'best', fontsize=13)
        self.axes[1].legend(["Rectilinea", "Diagonal","Teorico","Total"],loc= 'best', fontsize=13)
        self.axes[2].legend(["Agree", "Disagree", "Teorico","Total"],loc= 'best', fontsize=13)
        self.axes[3].legend(["0","90","Teorico","0+45+90+135"],loc= 'best', fontsize=13)
        self.axes[4].legend(["45","135","Teorico","0+45+90+135"],loc= 'best', fontsize=13)
        self.axes[5].legend(["Simulacion", "Teorico"],loc= 'best', fontsize=13)
        self.axes[6].legend(["Teorico", "Simulacion"],loc= 'best', fontsize=13)
        self.axes[7].legend(["Simulacion", "Teorico"],loc= 'best', fontsize=13)
        self.axes[8].legend(["Teorico", "Simulacion"],loc= 'best', fontsize=13)
        #############
        
        ## Title ##
        self.axes[0].set_title("Distribucion de unos y cero en la RawKey", fontsize=16)
        self.axes[1].set_title("Distribucion de las Bases conjugadas", fontsize=16)
        #
        self.axes[2].set_title("Distribucion de las bases que concuerdan y no concuerdan en la Rawkey", fontsize=16)
        #
        self.axes[3].set_title("Distribucion de los estados 0 y 45 en la Rawkey", fontsize=16)
        self.axes[4].set_title("Distribucion de los estados 90 y 135 en la Rawkey", fontsize=16)
        #
        self.axes[5].set_title("Dependencia del Qber con la longuitud de RawKey para "+r'$\alpha$'+"="+str(self.a4)+" y "+r'$\lambda$'+"="+str(self.lambdaa4), fontsize=16)
        self.axes[6].set_title("Histograma del Qber para "+r'$\alpha$'+"="+str(self.a4)+" y "+r'$\lambda$'+"="+str(self.lambdaa4), fontsize=16)
        self.axes[7].set_title("Desviacion estandar del Qber por grupo para "+r'$\alpha$'+"="+str(self.a4)+" y "+r'$\lambda$'+"="+str(self.lambdaa4), fontsize=16)
        self.axes[8].set_title("Dependencia del Ber con la longuitud de RawKey para "+r'$\alpha$'+"="+str(self.a4)+" y "+r'$\lambda$'+"="+str(self.lambdaa4), fontsize=16)
        self.axes[9].set_title("Histograma del Ber para "+r'$\alpha$'+"="+str(self.a4)+" y "+r'$\lambda$'+"="+str(self.lambdaa4), fontsize=16)
        self.axes[10].set_title("Desviacion estandar del Ber por grupo para "+r'$\alpha$'+"="+str(self.a4)+" y "+r'$\lambda$'+"="+str(self.lambdaa4), fontsize=16)
        #
        self.axes[11].set_title("Qber Vs probabilidad "+r'$\alpha$'+" de despolarizacion para "+r'$\lambda$'+"="+str(self.lambdaa5), fontsize=16)
        self.axes[12].set_title("Ber Vs probabilidad "+r'$\alpha$'+" de despolarizacion para "+r'$\lambda$'+"="+str(self.lambdaa5), fontsize=16)
        #
        self.axes[13].set_title("Qber Vs probabilidad "+r'$\lambda$'+" de aparicion de Eve para "+r'$\alpha$'+"="+str(self.a6), fontsize=16)
        self.axes[14].set_title("Ber Vs probabilidad "+r'$\lambda$'+" de aparicion de Eve para "+r'$\alpha$'+"="+str(self.a6), fontsize=16)
        #
        self.axes[15].set_title("Qber como funcion de  "+r'$\lambda$'+" y "+r'$\alpha$', fontsize=16,pad=15)
        self.axes[16].set_title("Ber como funcion de  "+r'$\lambda$'+" y "+r'$\alpha$', fontsize=16,pad=15)
        ###########
        
        for i in range(17):
            self.axes[i].relim()
            self.axes[i].autoscale_view()
            self.canvas[i].draw()

if __name__ == '__main__':
    app = wx.App()
    app.frame = grafica()
    app.frame.Show()
    app.MainLoop()