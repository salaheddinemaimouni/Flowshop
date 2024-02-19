from fonctions import *
import tkinter as tk 
from tkinter import ttk
import customtkinter as ct
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
class Tableaux(ct.CTk):
    def __init__(self,endJ,startJ,endP,startP,TFR_TAR,TW,TWA,TWAN,TBF,tasks,seq,prep,block,nowait,noidel,TFT,TT,Tm,use_TT):
        super().__init__()
        self.title("resultat de Gantt")
        self.endJ = endJ
        self.startJ = startJ
        self.endP = endP
        self.startP = startP
        self.T_FA_R = TFR_TAR
        self.TW = TW
        self.TWA = TWA
        self.TWAN = TWAN
        self.tasks = tasks
        self.seq = seq
        self.prep = prep
        self.block = block
        self.TBF = TBF
        self.cas = 1
        self.nowait = nowait
        self.noidel = noidel
        self.TFT = TFT
        self.TT = TT
        self.Tm = Tm
        self.use_TT = use_TT
        for i in range(len(self.T_FA_R)):
            for j in range(len(self.T_FA_R[0])):
                var=round(self.T_FA_R[i][j]*100,2)
                self.T_FA_R[i][j]=str(var)+"%"
        self.tab_control = ct.CTkTabview(self,width=1400,height=800)

        if self.prep == 1 and self.block == 0:
            self.tab_full_names=["Diagramme de Gaintt"
                                ,"Dates de fin des Jobs"
                                ,"Dates de début des Jobs"
                                ,"Dates de fin des temps de preparation"
                                ,"Dates de début des temps de preparation"
                                ,"temps de fonctionnement  réel \n et temps d'arret réel et temps d'arret de préparation \n cas 1 : preparation = arret"
                                ,"Temps d'attente des Jobs"
                                ,"Temps d'attente des Jobs à cause de preparation"
                                ,"Temps d'attente des Jobs à cause de fonctionnement"]
            self.tab_names=["Gantt","FinJ","DébutJ","FinP","DébutP","T_FA_R","TA","TAP","TAF"]
            for name in self.tab_names:
                self.tab_control.add(name)
                self.tab_control.pack(side=tk.LEFT, fill='y')
            cas1_btn = ct.CTkButton(master=self.tab_control.tab("T_FA_R"), text= "Preparation = Arret", command=self.cas1_fun)
            cas1_btn.grid(row=1,column=0, padx=40, pady=20)
            cas2_btn = ct.CTkButton(master=self.tab_control.tab("T_FA_R"), text= "Preparation = Travail", command=self.cas2_fun)
            cas2_btn.grid(row=2,column=0, padx=40, pady=20)
            self.plot_gantt()
            self.create_endJ()
            self.create_startJ()
            self.create_endP()
            self.create_startP()
            self.create_T_FA_R()
            self.create_TW()
            self.create_TWA()
            self.create_TWAN()
        elif self.prep == 0 and self.block == 0:
            self.T_FA_R = transpose_matrix(self.T_FA_R)
            self.tab_full_names=["Diagramme de Gaintt"
                                ,"Dates de fin des Jobs"
                                ,"Dates de début des Jobs"
                                ,"temps de fonctionnement/arret réel"
                                ,"Temps d'attente des Jobs"]
            self.tab_names=["Gantt","FinJ","DébutJ","T_FA_R","TA"]
            for name in self.tab_names:
                self.tab_control.add(name)
                self.tab_control.pack(side=tk.LEFT, fill='y')
            self.plot_gantt()
            self.create_endJ()
            self.create_startJ()
            self.create_T_FA_R()
            self.create_TW()
        elif self.prep == 0 and self.block == 1:
            self.T_FA_R = transpose_matrix(self.T_FA_R)
            self.tab_full_names=["Diagramme de Gaintt"
                                ,"Dates de fin des Jobs"
                                ,"Dates de début des Jobs"
                                ,"temps de fonctionnement/arret réel"
                                ,"Temps de blocage des Jobs"]
            self.tab_names=["Gantt","FinJ","DébutJ","T_FA_R","TB"]
            for name in self.tab_names:
                self.tab_control.add(name)
                self.tab_control.pack(side=tk.LEFT, fill='y')
            self.plot_gantt()
            self.create_endJ()
            self.create_startJ()
            self.create_T_FA_R()
            self.create_TW()
        elif self.prep == 1 and self.block == 1:
            self.tab_full_names=["Diagramme de Gaintt"
                                ,"Dates de fin des Jobs"
                                ,"Dates de début des Jobs"
                                ,"Dates de fin des temps de preparation"
                                ,"Dates de début des temps de preparation"
                                ,"temps de fonctionnement  réel \n et temps d'arret réel et temps d'arret de préparation \n cas 1 : preparation = arret"
                                ,"Temps de blocage des Jobs"
                                ,"Temps de blocage des Jobs à cause de preparation"
                                ,"Temps de blocage des Jobs à cause de blocage"
                                ,"Temps de blocage des Jobs à cause de fonctionnement"]
            self.tab_names=["Gantt","FinJ","DébutJ","FinP","DébutP","T_FA_R","TB","TBP","TBB","TBF"]
            for name in self.tab_names:
                self.tab_control.add(name)
                self.tab_control.pack(side=tk.LEFT, fill='y')
            cas1_btn = ct.CTkButton(master=self.tab_control.tab("T_FA_R"), text= "Preparation = Arret", command=self.cas1_fun)
            cas1_btn.grid(row=1,column=0, padx=40, pady=20)
            cas2_btn = ct.CTkButton(master=self.tab_control.tab("T_FA_R"), text= "Preparation = Travail", command=self.cas2_fun)
            cas2_btn.grid(row=2,column=0, padx=40, pady=20)
            self.plot_gantt()
            self.create_endJ()
            self.create_startJ()
            self.create_endP()
            self.create_startP()
            self.create_T_FA_R()
            self.create_TW()
            self.create_TWA()
            self.create_TWAN()
            self.create_TBF()
        if self.use_TT==1:
            self.tab_control.add('T')
            self.tab_control.pack(side=tk.LEFT, fill='y')
            self.create_Tm()

    def create_endJ(self):
        self.create_regular_tab(self.endJ,self.tab_names[1],self.tab_full_names[1])

    def create_startJ(self):
        self.create_regular_tab(self.startJ,self.tab_names[2],self.tab_full_names[2])

    def create_endP(self):
        self.create_regular_tab(self.endP,self.tab_names[3],self.tab_full_names[3])

    def create_startP(self):
        self.create_regular_tab(self.startP,self.tab_names[4],self.tab_full_names[4])

    def create_T_FA_R(self):
        if self.prep == 1:
            TFAR = transpose_matrix([self.T_FA_R[0],self.T_FA_R[1],self.T_FA_R[4]])
            print(TFAR,"TFAR")
            self.create_regular_tab(TFAR,self.tab_names[5],self.tab_full_names[5])
        else:
            self.create_regular_tab(self.T_FA_R,self.tab_names[3],self.tab_full_names[3])

    def create_TW(self):
        if self.prep ==1:
            self.create_regular_tab(self.TW,self.tab_names[6],self.tab_full_names[6])
        else:
            self.create_regular_tab(self.TW,self.tab_names[4],self.tab_full_names[4])

    def create_TWA(self):
        self.create_regular_tab(self.TWA,self.tab_names[7],self.tab_full_names[7])

    def create_TWAN(self):
        self.create_regular_tab(self.TWAN,self.tab_names[8],self.tab_full_names[8])
    
    def create_TBF(self):
        self.create_regular_tab(self.TBF,self.tab_names[9],self.tab_full_names[9])

    def create_Tm(self):
        self.create_regular_tab([self.Tm],"T","total flow time (TFT="+str(self.TFT)+ ") / Tardiness of jobs (Tj) / Total tardness (TT="+str(self.TT)+")")

    def create_regular_tab(self , tab, name, full_name):
        n , m = len(tab[0]) , len(tab)
        table_label = ct.CTkLabel(self.tab_control.tab(name),text=full_name)
        tree = ttk.Treeview(self.tab_control.tab(name), columns=list(range(n+1)),show='headings')
        if name == "FinJ" or name =="DébutJ" or name =="FinP" or name =="DébutP" or name == "T":
            table_label.pack(side=tk.TOP)
            for j in range(n+1):
                if j!=0:
                    tree.heading(j, text=f'Job {self.seq[j-1]}')
                else:
                    tree.heading(j, text="Machines")
                tree.column(j, width=80)

            for i in range(m):
                if type(tab[i]) != list:
                    if name == 'T':
                        tree.insert("", "end", values=['M'+str(len(self.endJ)-1)]+tab[i])
                    else:
                        tree.insert("", "end", values=['M'+str(i)]+tab[i].tolist())
                else:
                    if name == 'T':
                        tree.insert("", "end", values=['M'+str(len(self.endJ)-1)]+tab[i])
                    else:
                        tree.insert("", "end", values=['M'+str(i)]+tab[i])
            tree.pack()
        elif name == "T_FA_R":
            self.table_labelt = ct.CTkLabel(self.tab_control.tab(name),text=full_name)
            self.treet = ttk.Treeview(self.tab_control.tab(name), columns=list(range(n+1)),show='headings')
            table_label.grid(row=0,column=0,columnspan=5)
            self.treet.heading(0, text="Machines")
            self.treet.column(0, width=80)
            self.treet.heading(1, text="TFR")
            self.treet.column(1, width=80)
            self.treet.heading(2, text="TAR")
            self.treet.column(2, width=80)
            TFR_TAR_plt = [[float(t.strip('%')) for t in lst] for lst in tab]
            TFR_TAR_plt = np.array(TFR_TAR_plt).T.tolist()
            categories = np.arange(len(TFR_TAR_plt[0]))
            bar_width = 0.25
            names=["TFR","TAR","TAP"]
            fig, ax = plt.subplots()
            plt.figure(figsize=(20, 20))
            for i, t_list in enumerate(TFR_TAR_plt):
                print(names,i,"tttt")
                bars = ax.bar(categories + i * bar_width, t_list, label=names[i], width=bar_width, alpha=0.7)
                for bar, prob in zip(bars, t_list):
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f'{prob:.2f}%', ha='center', va='bottom')
                if i ==2:
                    self.treet.heading(3, text="TPR")
                    self.treet.column(3, width=80)
            ax.set_xlabel('Machines')
            ax.set_ylabel('Performances(%)')
            ax.set_title("temps de fonctionnement réel(TFR) et Temps d'arret réel/préparation (TAR/TAP)")
            ax.set_xticks(categories)
            legend = ax.legend(loc='lower right')
            legend.set_draggable(True)
            self.canvas_T = FigureCanvasTkAgg(fig, master=self.tab_control.tab(name))
            self.canvas_T_widget = self.canvas_T.get_tk_widget()
            self.canvas_T_widget.place(x=500,y=200)
            self.canvas_T.draw()
            self.canvas_T.flush_events()
            self.treet.grid(row=3,column=0,rowspan=3)
            for i in range(m):
                self.treet.insert("", "end", values=['M'+str(i)]+tab[i])
        elif name =="TA" or name =="TAP" or name =="TAF":
            table_label.pack(side=tk.TOP)
            for j in range(n+1):
                if j!=0:
                    if self.nowait==1:
                        tree.heading(j, text=f'Job'+ str(self.seq[j-1])+"/"+str(self.seq[j]))
                    else:
                        tree.heading(j, text=f'Job {self.seq[j-1]}')
                else:
                    tree.heading(j, text="Machines")
                tree.column(j, width=80)

            for i in range(m):
                if self.nowait==1:
                    if type(tab[i]) != list:
                        tree.insert("", "end", values=['M'+str(i)]+tab[i].tolist())
                    else:
                        tree.insert("", "end", values=['M'+str(i)]+tab[i]) 
                else:
                    if type(tab[i]) != list:
                        tree.insert("", "end", values=['M'+str(i)+"/"+str(i+1)]+tab[i].tolist())
                    else:
                        tree.insert("", "end", values=['M'+str(i)+"/"+str(i+1)]+tab[i])
            tab = transpose_matrix(tab)
            sums=[sum(lst) for lst in tab]
            tree.insert("", "end", values=["somme"]+sums)
            tree.pack()
        elif name == "TB" or name == "TBP" or name == "TBF" or name == "TBB":
            table_label.pack(side=tk.TOP)
            for j in range(n+1):
                if j!=0:
                    tree.heading(j, text=f'Job {self.seq[j-1]}')
                else:
                    tree.heading(j, text="Machines")
                tree.column(j, width=80)

            for i in range(m):
                if type(tab[i]) != list:
                    tree.insert("", "end", values=['M'+str(i)]+tab[i].tolist())
                else:
                    tree.insert("", "end", values=['M'+str(i)]+tab[i])
            tab = transpose_matrix(tab)
            sums=[sum(lst) for lst in tab]
            tree.insert("", "end", values=["somme"]+sums)
            tree.pack()
    
    def cas1_fun(self):
        if self.cas == 2:
            self.table_labelt.destroy()
            self.treet.destroy()
            self.create_T_FA_R()
            self.cas = 1
        else:
            pass
        
    def cas2_fun(self):
        if self.cas == 1:
            self.table_labelt.destroy()
            self.treet.destroy()
            self.create_regular_tab(transpose_matrix([self.T_FA_R[2],self.T_FA_R[3]]),self.tab_names[5],"temps de fonctionnement  réel \n et temps d'arret réel et temps d'arret de préparation \n cas 2 : preparation = travail")
            self.cas = 2
        else:
            pass
    
    def plot_gantt(self):
        tasks = self.tasks

        fig, ax = plt.subplots()
        # Configuration de l'axe Y
        ax.set_yticks(range(len(tasks)))
        ax.set_yticklabels(tasks.index)

        # Flattening the lists of lists
        all_start_times = [time for times_list in tasks['Start'] for times in times_list for time in times]
        all_end_times = [time for times_list in tasks['End'] for times in times_list for time in times]

        # Configuration de l'axe X
        ax.set_xticks(np.arange(min(all_start_times), max(all_end_times) + 1, step=1))
        ax.set_xlim(min(all_start_times), max(all_end_times) + 1)

        self.canvas_gantt = FigureCanvasTkAgg(fig, master=self.tab_control.tab("Gantt"))
        self.canvas_gantt_widget = self.canvas_gantt.get_tk_widget()
        self.canvas_gantt_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Tracé des tâches
        for i, task in enumerate(tasks.itertuples()):
            for start_times, end_times, color, label in zip(task.Start, task.End, task.Color, task.Label):
                for start, end, text in zip(start_times, end_times, label):
                    # Check if the color is a valid color name or hexadecimal code
                    try:
                        mcolors.to_rgba(color)
                    except ValueError:
                        color = 'blue'  # Default to blue if an invalid color is provided
                    ax.barh(i, end - start, left=start, color=color, alpha=0.7)
                    text_x = start + (end - start) / 2
                    text_y = i
                    ax.text(text_x, text_y, label, ha='center', va='center', color='white', fontweight='bold')

                    # Add an arrow at the end of each job except for the first one
                    if i > 0 and self.nowait==1:
                        arrow_start = end
                        arrow_end = end  # The arrow origin is at the bottom of the job
                        ax.arrow(arrow_start, text_y-0.4, 0, -0.1, head_width=0.2, head_length=0.1, fc=color, ec=color)

        # Configuration des étiquettes
        ax.set_xlabel('Axe de temps')
        if self.use_TT==1:
            ax.set_title('Diagramme de Gantt \n Total flow tmie (TFT) = '+str(self.TFT)+"\n Cmax = "+str(self.endJ[-1][len(self.endJ[0])-1])+"\n Total Tardiness (TT) = "+str(self.TT))
        else:
            ax.set_title('Diagramme de Gantt \n Total flow tmie (TFT) = '+str(self.TFT)+"\n Cmax = "+str(self.endJ[-1][len(self.endJ[0])-1]))
        plt.grid()

        self.canvas_gantt.draw()
        self.canvas_gantt.flush_events()
