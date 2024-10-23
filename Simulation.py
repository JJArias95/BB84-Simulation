# -*- coding: utf-8 -*-
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import matplotlib.gridspec as gridspec
import numpy as np
import pylab
import random
import os
import shutil
from bb84_protocol_module import *

pylab.rcParams.update({"text.usetex": True,
        "font.family": "serif",
        "font.serif":["Computer Modern"]})

class grafica(wx.Frame):
    title = 'Simulations of parameters into the QKD BB84 protocol'
    def __init__(self,):
        wx.Frame.__init__(self, None, -1, self.title, size=(400,400))
        
        ## Simulation 1 ## 
        self.NumSimSim1=500 ## Number of simulations
        self.NumBitsSim1=600 ## Number of bits per simulation 
        #################

        ## Simulation_2 ## 
        self.NumSimSim2=3 ## Number of simulations
        self.NumBitsMax=1000 ## Maximum number of bits per simulation
        self.ProbEve=1 # Probability of Eve appearing on the communication 
        #################

        self.dpi = 1000
        self.NamePlots=['Sim 1a','Sim 1b','Sim 1c','Sim 1d','Sim 1e',
                        'Sim 2a','Sim 2b',"Save all plots"]
        
        self.create_menu()
        self.create_main_panel()

    ## Simulation 1: Distribution of bits in the raw key list, bases 
    ##               in the RanBases list, matching and non-matching bases 
    ##               between Alice's and Bob's bases in the RanBases list,
    ##               and Qbits in the Qbits list.

    def simulation_1(self):

        RecIndexes=[]
        DiaIndexes=[]
        OnesIndexes=[]
        ZerosIndexes=[]
        AgreeBasesIndex=[]
        DisagreeBasesIndex=[]
        HIndex=[]
        Indexes45 = []
        VIndexes = []
        Indexes135 = []

        ## x-axis for the simulation 1 
        self.XSim1 = np.linspace(0,self.NumBitsSim1-1,num=self.NumBitsSim1)
        print("Simulation 1-start")

        # Loop through simulations
        for i in range(self.NumSimSim1):
            RawKey=raw_key(self.NumBitsSim1) 
            AliceBases=random_bases(self.NumBitsSim1)
            Qbits=encode(RawKey,AliceBases)
            BobBases=random_bases(self.NumBitsSim1)
            
            for j in range(self.NumBitsSim1):
                (OnesIndexes if RawKey[j] == 1 else ZerosIndexes).append(j)
                (RecIndexes if AliceBases[j]=="Rec" else DiaIndexes).append(j)
                (AgreeBasesIndex if AliceBases[j]==BobBases[j] 
                 else DisagreeBasesIndex).append(j)
                if Qbits[j]==0:
                    HIndex.append(j)
                elif Qbits[j]==45:
                    Indexes45.append(j)
                elif Qbits[j]==90:
                    VIndexes.append(j)
                else:
                    Indexes135.append(j)
                
        # Define bin ranges once
        bins = range(self.NumBitsSim1 + 1)

        # Histogram calculations
        self.HistOnes,_= np.histogram(OnesIndexes,bins=bins)
        self.HistZeros,_=np.histogram(ZerosIndexes,bins=bins)
        self.HistRec,_=np.histogram(RecIndexes,bins=bins)
        self.HistDia,_=np.histogram(DiaIndexes,bins=bins)
        self.HistAgreeBases,_=np.histogram(AgreeBasesIndex,bins=bins)
        self.HistDisagreeBases,_=np.histogram(DisagreeBasesIndex,bins=bins)
        self.HistH,_= np.histogram(HIndex,bins=bins)
        self.Hist45,_= np.histogram(Indexes45,bins=bins)
        self.HistV,_= np.histogram(VIndexes,bins=bins)
        self.Hist135,_= np.histogram(Indexes135,bins=bins)
        
        print("Simulation 1-end\n")


    ## Simulation 2: Evolution of the complete Qber with respect to the length  
    ##               of the RawKey (With a probability of Eve of self.ProbEve)
    def simulation_2(self):

        print("Simulation 2-start")

        #################
        self.BinsBit = np.linspace(0,100-1,num=100)
        self.MeanQbers=[]
        self.MeanBers=[]
        self.TheoBer=25+12.5*self.ProbEve
        self.TheoQber=25*self.ProbEve
        self.NumBitsList=np.linspace(90,self.NumBitsMax+90,
                                     num=self.NumBitsMax+1,dtype=int)
        #################

        for NumBits in self.NumBitsList:
            if NumBits%100==0:
                print("NumBits: "+str(NumBits))
            Qbers=[]
            Bers=[]
            for _ in range(self.NumSimSim2):
                ## Alice ##
                RawKey=raw_key(NumBits)
                AliceBases=random_bases(NumBits)
                Qbits=encode(RawKey,AliceBases)

                EveChecker=random.uniform(-(1-self.ProbEve),self.ProbEve)
                if EveChecker>0:
                    ## Eve ##
                    EveBases=random_bases(int(NumBits))
                    EveBits=decode(Qbits,EveBases)
                    NewQbits=encode(EveBits,EveBases)
                else:
                    NewQbits=Qbits

                ## Bob ##
                BobBases=random_bases(int(NumBits))
                BobBits=decode(NewQbits,BobBases)

                #Qber
                Qber=qber(RawKey,BobBits,AliceBases,BobBases)
                Qbers.append(Qber)

                #Ber
                Ber=ber(RawKey,BobBits)
                Bers.append(Ber)
            self.MeanQbers.append(np.mean(Qbers)*100)
            self.MeanBers.append(np.mean(Bers)*100)

        print("Simulation 2")
        print("Mean value of Qber: "+str(np.mean(self.MeanQbers)))
        print("Mean value of Ber: "+str(np.mean(self.MeanBers)))
        print("Simulation 2-end")


    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        m_expt2 = menu_file.Append(-1, "&Save config\tCtrl-R", "Save config.")
        self.Bind(wx.EVT_MENU, self.Write_report, m_expt2)
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
            if os.path.exists(path):
                os.remove(path)
            file = open(path,"a")
            file.write("=========================\n\n")
            file.write("Simulation 1:Distribution of bits in the raw key list, bases \n")
            file.write("             in the RanBases list, matching and non-matching bases \n")
            file.write("             between Alice's and Bob's bases in the RanBases list,\n")
            file.write("             and Qbits in the Qbits list.\n\n")
            file.write("Length of the Rawkey: "+str(self.NumBitsSim1)+"\n")
            file.write("Number of simulations: "+str(self.NumSimSim1)+"\n")
            file.write("\n=========================\n\n")
            file.write("Ejercicio 2: Evolution of the complete Qber with respect to the length  \n")
            file.write("             of the RawKey With a probability of Eve appearing on the communication.\n")
            file.write("Maximum length of the Rawkey: "+str(self.NumBitsMax)+"\n")
            file.write("Number of simulations: "+str(self.NumSimSim2)+"\n")
            file.write("Probability of Eve: "+str(self.ProbEve)+"\n")
            file.write("\n=========================")

            file.close()

    def on_save_plot(self,event):
        modal=wx.SingleChoiceDialog(None,"Which plot would you like to save?"
                                    ,"Plots",self.NamePlots)
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
                    NumPlot = [i for i, x in enumerate(self.NamePlots) 
                               if x == modal.GetStringSelection()][0]
                    self.canvas[NumPlot].print_figure(dlg.GetPath(), 
                                                      dpi=self.dpi)
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
                    for i in range(7):
                        path = os.path.join(DirPath, self.NamePlots[i]+".pdf") 
                        self.canvas[i].print_figure(path, dpi=self.dpi)

        modal.Destroy()

    def on_exit(self, event):
        for i in range(7):
            pylab.close(self.figs[i]) 
        self.Destroy()

    def create_main_panel(self):
        self.panel = wx.Panel(self,id=-1, pos=(500,500),size=(1000,1000))
        
        self.Vbox=wx.BoxSizer(wx.VERTICAL) 
        ######
        self.figs=[]
        self.axes=[]
        for i in range(7):
            auxfigs = pylab.figure(figsize=(10, 5))
            self.figs.append(auxfigs)
            # Create subplots with specific positions
            gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])#Adjust width ratios
            auxaxes1 = self.figs[i].add_subplot(gs[0])  # First plot gets more space
            auxaxes2 = self.figs[i].add_subplot(gs[1])  # Second plot
            self.axes.append(auxaxes1)
            self.axes.append(auxaxes2)
            
        ####
        self.nb = wx.Notebook(self.panel,size=(2000,700),pos=(0,0),
                              style=wx.NB_MULTILINE)
        ####
        self.canvas=[]
        for i in range(7):
            self.canvas.append(FigCanvas(self.nb, -1, self.figs[i]))
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
        for i in range(7):
            self.axes[i].cla()

        self.simulation_1()
        self.simulation_2()

        #######################################################################
        ################################# Plots ###############################
        #######################################################################

        ####################
        ### Simulation 1 ###
        ####################

        self.axes[0].plot(
            self.XSim1,self.HistOnes*100*((self.NumSimSim1)**(-1)),'r',
            self.XSim1,self.HistZeros*100*((self.NumSimSim1)**(-1)),'b',
            [0, self.NumBitsSim1],[50,50],'limegreen')
        
        self.axes[1].hist(self.HistOnes*100*((self.NumSimSim1)**(-1)),
                          bins=20,color=(1,0,0,0.5),orientation="horizontal",
                          edgecolor="black",linewidth=1.5 )
        self.axes[1].hist(self.HistZeros*100*((self.NumSimSim1)**(-1)),
                          bins=20,color=(0,0,1,0.5),orientation="horizontal",
                          edgecolor="black",linewidth=1.5)
        self.axes[1].plot([0, 200],[50,50],'limegreen')
        
        self.axes[2].plot(
            self.XSim1,self.HistRec*100*((self.NumSimSim1)**(-1)),'r',
            self.XSim1,self.HistDia*100*((self.NumSimSim1)**(-1)),'b',
            [0, self.NumBitsSim1],[50,50],'limegreen')
        
        self.axes[3].hist(self.HistRec*100*((self.NumSimSim1)**(-1)),
                          bins=20,color=(1,0,0,0.5),orientation="horizontal",
                          edgecolor="black",linewidth=1.5 )
        self.axes[3].hist(self.HistDia*100*((self.NumSimSim1)**(-1)),
                          bins=20,color=(0,0,1,0.5),orientation="horizontal",
                          edgecolor="black",linewidth=1.5)
        self.axes[3].plot([0,self.NumBitsSim1],[50,50],'limegreen')

        self.axes[4].plot(
            self.XSim1,self.HistAgreeBases*100*((self.NumSimSim1)**(-1)),'r',
            self.XSim1,self.HistDisagreeBases*100*((self.NumSimSim1)**(-1)),'b',
            [0, self.NumBitsSim1],[50,50],'limegreen')
        self.axes[5].hist(self.HistAgreeBases*100*((self.NumSimSim1)**(-1)),
                          bins=20,color=(1,0,0,0.5),orientation="horizontal",
                          edgecolor="black",linewidth=1.5 )
        self.axes[5].hist(self.HistDisagreeBases*100*((self.NumSimSim1)**(-1)),
                          bins=20,color=(0,0,1,0.5),orientation="horizontal",
                          edgecolor="black",linewidth=1.5)
        self.axes[5].plot([0,self.NumBitsSim1],[50,50],'limegreen')
        
        self.axes[6].plot(
            self.XSim1,self.HistH*100*((self.NumSimSim1)**(-1)),'r',
            self.XSim1,self.HistV*100*((self.NumSimSim1)**(-1)),'b',
            [0, self.NumBitsSim1],[25,25],'limegreen')
        self.axes[7].hist(self.HistH*100*((self.NumSimSim1)**(-1)),
                          bins=20,color=(1,0,0,0.5),orientation="horizontal",
                          edgecolor="black",linewidth=1.5 )
        self.axes[7].hist(self.HistV*100*((self.NumSimSim1)**(-1)),
                          bins=20,color=(0,0,1,0.5),orientation="horizontal",
                          edgecolor="black",linewidth=1.5)
        self.axes[7].plot([0,self.NumBitsSim1],[25,25],'limegreen')

        self.axes[8].plot(
            self.XSim1,self.Hist45*100*((self.NumSimSim1)**(-1)),'r',
            self.XSim1,self.Hist135*100*((self.NumSimSim1)**(-1)),'b',
            [0, self.NumBitsSim1],[25,25],'limegreen')
        self.axes[9].hist(self.Hist45*100*((self.NumSimSim1)**(-1)),
                          bins=20,color=(1,0,0,0.5),orientation="horizontal",
                          edgecolor="black",linewidth=1.5 )
        self.axes[9].hist(self.Hist135*100*((self.NumSimSim1)**(-1)),
                          bins=20,color=(0,0,1,0.5),orientation="horizontal",
                          edgecolor="black",linewidth=1.5)
        self.axes[9].plot([0,self.NumBitsSim1],[25,25],'limegreen')

        ####################
        ### Simulation 2 ###
        ####################

        self.axes[10].plot(np.array(self.NumBitsList),self.MeanQbers,'r',
            [0, self.NumBitsMax],[self.TheoQber, self.TheoQber],'limegreen')
        self.axes[11].hist(self.MeanQbers,bins=20,color=(1,0,0,0.5),
                           orientation="horizontal",edgecolor="black",
                           linewidth=1.5 )
        self.axes[11].plot([0, self.NumBitsMax],[self.TheoQber,self.TheoQber],
                           'limegreen')

        self.axes[12].plot(np.array(self.NumBitsList),self.MeanBers,'r',
            [0, self.NumBitsMax],[self.TheoBer, self.TheoBer],'limegreen')
        self.axes[13].hist(self.MeanBers,bins=20,color=(1,0,0,0.5),
                           orientation="horizontal",edgecolor="black",
                           linewidth=1.5 )
        self.axes[13].plot([0, self.NumBitsMax],[self.TheoBer,self.TheoBer],
                           'limegreen')

        #######################################################################
        ######################## To customize the plots #######################
        #######################################################################
        
        [self.figs[j].subplots_adjust(wspace=0.06, hspace=0.1) for j in range(7)]
        
        ####################
        ### Simulation 1 ###
        ####################

        self.axes[0].set_title("Distribution of ones and zeros in the raw " \
                               "key", fontsize=16)
        self.axes[0].set_xlabel("Bit position",fontsize=16)
        self.axes[0].set_xlim(left=0,right=self.NumBitsSim1)
        self.axes[0].set_xticks(range(0,self.NumBitsSim1+1,100))
        self.axes[0].set_xticks([j for j in range(0,self.NumBitsSim1+1,25)],minor=True)
        self.axes[0].set_ylabel("Probability [\%]",fontsize=16)
        self.axes[0].set_ylim(bottom=40,top=60)
        self.axes[0].set_yticks([j/10 for j in range(400,601,25)])
        self.axes[0].set_yticks([j/1000 for j in range(40000,60001,625)],
                                minor=True)
        self.axes[0].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[0].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[0].legend(["One","Zero","Theory"],loc='upper right',fontsize=13)

        self.axes[1].set_xlabel("Counts",fontsize=16)
        self.axes[1].minorticks_on()
        self.axes[1].set_xlim(left=0,right=100)
        self.axes[1].set_xticks([j for j in range(0,101,25)])
        self.axes[1].set_xticks([j/100 for j in range(0,10001,625)],minor=True)
        self.axes[1].set_ylim(bottom=40,top=60)
        self.axes[1].set_yticklabels([])
        self.axes[1].set_yticks([j/1000 for j in range(40000,60001,625)],minor=True)
        self.axes[1].tick_params(bottom=True,top=True,left=True,right=True, 
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[1].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[1].legend(["Theory","One","Zero"],loc='best',fontsize=13)
        
        self.axes[2].set_title("Distribution of conjugate bases in the bases "\
                                "list", fontsize=16)
        self.axes[2].set_xlabel("Basis position",fontsize=16)
        self.axes[2].set_xlim(left=0,right=self.NumBitsSim1)
        self.axes[2].set_xticks(range(0,self.NumBitsSim1+1,100))
        self.axes[2].set_xticks([j for j in range(0,self.NumBitsSim1+1,25)],minor=True)
        self.axes[2].set_ylabel("Probability [\%]",fontsize=16)
        self.axes[2].set_ylim(bottom=40,top=60)
        self.axes[2].set_yticks([j/10 for j in range(400,601,25)])
        self.axes[2].set_yticks([j/1000 for j in range(40000,60001,625)],
                                minor=True)
        self.axes[2].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[2].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[2].legend(["Rectilinear", "Diagonal","Theory"],loc='upper right',fontsize=13)

        self.axes[3].set_xlabel("Counts",fontsize=16)
        self.axes[3].minorticks_on()
        self.axes[3].set_xlim(left=0,right=100)
        self.axes[3].set_xticks([j for j in range(0,101,25)])
        self.axes[3].set_xticks([j/100 for j in range(0,10001,625)],minor=True)
        self.axes[3].set_ylim(bottom=40,top=60)
        self.axes[3].set_yticklabels([])
        self.axes[3].set_yticks([j/1000 for j in range(40000,60001,625)],minor=True)
        self.axes[3].tick_params(bottom=True,top=True,left=True,right=True, 
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[3].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[3].legend(["Theory","Rectilinear","Diagonal"],loc='best',fontsize=13)

        self.axes[4].set_title("Distribution of the agree bases and the" \
                               "disagree bases in the bases list",fontsize=16)
        self.axes[4].set_xlabel("Basis position",fontsize=16)
        self.axes[4].set_xlim(left=0,right=self.NumBitsSim1)
        self.axes[4].set_xticks(range(0,self.NumBitsSim1+1,100))
        self.axes[4].set_xticks([j for j in range(0,self.NumBitsSim1+1,25)],minor=True)
        self.axes[4].set_ylabel("Probability [\%]",fontsize=16)
        self.axes[4].set_ylim(bottom=40,top=60)
        self.axes[4].set_yticks([j/10 for j in range(400,601,25)])
        self.axes[4].set_yticks([j/1000 for j in range(40000,60001,625)],
                                minor=True)
        self.axes[4].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[4].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[4].legend(["Agree", "Disagree", "Theory"],loc='upper right',fontsize=13)

        self.axes[5].set_xlabel("Counts",fontsize=16)
        self.axes[5].minorticks_on()
        self.axes[5].set_xlim(left=0,right=100)
        self.axes[5].set_xticks([j for j in range(0,101,25)])
        self.axes[5].set_xticks([j/100 for j in range(0,10001,625)],minor=True)
        self.axes[5].set_ylim(bottom=40,top=60)
        self.axes[5].set_yticklabels([])
        self.axes[5].set_yticks([j/1000 for j in range(40000,60001,625)],minor=True)
        self.axes[5].tick_params(bottom=True,top=True,left=True,right=True, 
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[5].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[5].legend(["Theory","Agree","Disagree"],loc='best',fontsize=13)

        self.axes[6].set_title("Distribution of states $|\\rm{H}\\rangle$ "\
                               "and $|\\rm{V}\\rangle$ in the raw key",
                               fontsize=16)
        self.axes[6].set_xlabel("Qbit position",fontsize=16)
        self.axes[6].set_xlim(left=0,right=self.NumBitsSim1)
        self.axes[6].set_xticks(range(0,self.NumBitsSim1+1,100))
        self.axes[6].set_xticks([j for j in range(0,self.NumBitsSim1+1,25)],minor=True)
        self.axes[6].set_ylabel("Probability [\%]",fontsize=16)
        self.axes[6].set_ylim(bottom=15,top=35)
        self.axes[6].set_yticks([j/10 for j in range(150,351,25)])
        self.axes[6].set_yticks([j/1000 for j in range(15000,35001,625)],
                                minor=True)
        self.axes[6].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[6].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[6].legend(["$|\\rm{H}\\rangle$ ","$|\\rm{V}\\rangle$ ",
                             "Theory"],loc='upper right',fontsize=13)

        self.axes[7].set_xlabel("Counts",fontsize=16)
        self.axes[7].minorticks_on()
        self.axes[7].set_xlim(left=0,right=100)
        self.axes[7].set_xticks([j for j in range(0,101,25)])
        self.axes[7].set_xticks([j/100 for j in range(0,10001,625)],minor=True)
        self.axes[7].set_ylim(bottom=15,top=35)
        self.axes[7].set_yticklabels([])
        self.axes[7].set_yticks([j/1000 for j in range(15000,35001,625)],minor=True)
        self.axes[7].tick_params(bottom=True,top=True,left=True,right=True, 
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[7].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[7].legend(["Theory","$|\\rm{H}\\rangle$ ","$|\\rm{V}\\rangle$ "],
                             loc='best',fontsize=13)

        self.axes[8].set_title("Distribution of states $|45\\rangle$ and "\
                               "$|135\\rangle$ in the raw key", fontsize=16)
        self.axes[8].set_xlabel("Qbit position",fontsize=16)
        self.axes[8].set_xlim(left=0,right=self.NumBitsSim1)
        self.axes[8].set_xticks(range(0,self.NumBitsSim1+1,100))
        self.axes[8].set_xticks([j for j in range(0,self.NumBitsSim1+1,25)],minor=True)
        self.axes[8].set_ylabel("Probability [\%]",fontsize=16)
        self.axes[8].set_ylim(bottom=15,top=35)
        self.axes[8].set_yticks([j/10 for j in range(150,351,25)])
        self.axes[8].set_yticks([j/1000 for j in range(15000,35001,625)],
                                minor=True)
        self.axes[8].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[8].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[8].legend(["$|45\\rangle$","$|135\\rangle$","Theory"],
                            loc='upper right',fontsize=13)

        self.axes[9].set_xlabel("Counts",fontsize=16)
        self.axes[9].minorticks_on()
        self.axes[9].set_xlim(left=0,right=100)
        self.axes[9].set_xticks([j for j in range(0,101,25)])
        self.axes[9].set_xticks([j/100 for j in range(0,10001,625)],minor=True)
        self.axes[9].set_ylim(bottom=15,top=35)
        self.axes[9].set_yticklabels([])
        self.axes[9].set_yticks([j/1000 for j in range(15000,35001,625)],minor=True)
        self.axes[9].tick_params(bottom=True,top=True,left=True,right=True, 
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[9].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[9].legend(["Theory","$|45\\rangle$","$|135\\rangle$"],
                             loc='best',fontsize=13)

        # ####################
        # ### Simulation 2 ###
        # ####################

        self.axes[10].set_title("Dependence of Qber on the length of raw key "
                                "for "+r'$\lambda$'+"="+str(self.ProbEve), 
                                fontsize=16)
        self.axes[10].set_xlabel("Raw key length",fontsize=16)
        self.axes[10].set_xlim(left=0,right=self.NumBitsMax)
        self.axes[10].set_xticks(range(0,self.NumBitsMax+1,100))
        self.axes[10].set_xticks([j for j in range(0,self.NumBitsMax+1,25)],minor=True)
        self.axes[10].set_ylabel("Qber [\%]",fontsize=16)
        self.axes[10].set_ylim(bottom=15,top=35)
        self.axes[10].set_yticks([j/10 for j in range(150,351,25)])
        self.axes[10].set_yticks([j/1000 for j in range(15000,35001,625)],
                                minor=True)
        self.axes[10].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[10].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[10].legend(["Theory","Simulation"],
                            loc='upper right',fontsize=13)

        self.axes[11].set_xlabel("Counts",fontsize=16)
        self.axes[11].minorticks_on()
        self.axes[11].set_xlim(left=0,right=100)
        self.axes[11].set_xticks([j for j in range(0,201,50)])
        self.axes[11].set_xticks([j/10 for j in range(0,2001,125)],minor=True)
        self.axes[11].set_ylim(bottom=15,top=35)
        self.axes[11].set_yticklabels([])
        self.axes[11].set_yticks([j/1000 for j in range(15000,35001,625)],minor=True)
        self.axes[11].tick_params(bottom=True,top=True,left=True,right=True, 
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[11].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[11].legend(["Theory","Simulation"],
                             loc='best',fontsize=13)

        self.axes[12].set_title("Dependence of Ber on the length of raw key "\
                                "for "+r'$\lambda$'+"="+str(self.ProbEve), 
                                fontsize=16)
        self.axes[12].set_xlabel("Raw key length",fontsize=16)
        self.axes[12].set_xlim(left=0,right=self.NumBitsMax)
        self.axes[12].set_xticks(range(0,self.NumBitsMax+1,100))
        self.axes[12].set_xticks([j for j in range(0,self.NumBitsMax+1,25)],minor=True)
        self.axes[12].set_ylabel("Ber [\%]",fontsize=16)
        self.axes[12].set_ylim(bottom=25,top=45)
        self.axes[12].set_yticks([j/10 for j in range(250,451,25)])
        self.axes[12].set_yticks([j/1000 for j in range(25000,45001,625)],
                                minor=True)
        self.axes[12].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[12].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[12].legend(["Theory","Simulation"],
                            loc='upper right',fontsize=13)

        self.axes[13].set_xlabel("Counts",fontsize=16)
        self.axes[13].minorticks_on()
        self.axes[13].set_xlim(left=0,right=100)
        self.axes[13].set_xticks([j for j in range(0,201,50)])
        self.axes[13].set_xticks([j/10 for j in range(0,2001,125)],minor=True)
        self.axes[13].set_ylim(bottom=25,top=45)
        self.axes[13].set_yticklabels([])
        self.axes[13].set_yticks([j/1000 for j in range(25000,45001,625)],minor=True)
        self.axes[13].tick_params(bottom=True,top=True,left=True,right=True, 
                                direction='in',which="major", 
                                length=9,width=1,labelsize=14)
        self.axes[13].tick_params(bottom=True,top=True,left=True,right=True,
                                direction='in',which="minor", 
                                length=3,width=1)
        self.axes[13].legend(["Theory","Simulation"],
                             loc='best',fontsize=13)

        ###########
    
        for i in range(7):
            self.axes[i].relim()
            self.axes[i].autoscale_view()
            self.canvas[i].draw()

if __name__ == '__main__':
    app = wx.App()
    app.frame = grafica()
    app.frame.Show()
    app.MainLoop()