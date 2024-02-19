import customtkinter as ct
from tkinter import filedialog
from PIL import Image
import os
from fonctions import *
from flow_shop import *
from tabs import *
from report import *

color_names = ['red', 'green', 'blue', 'navy' , 'orange', 'purple', 'pink', 'brown', 'cyan', 'magenta',
               'teal', 'lime', 'lavender', 'indigo', 'maroon', 'gold', 'olive', 'yellow']
color_names_prep = ['black','red','black', 'green','black', 'blue','black', 'yellow','black', 'orange','black', 'purple','black', 'pink','black', 'brown','black', 'cyan','black', 'magenta','black',
                    'teal','black', 'lime','black', 'lavender','black', 'indigo','black', 'maroon','black', 'gold','black', 'olive','black', 'navy','black', 'silver']

Q = [[2,4,5,3],[5,6,7,8],[3,2,3,2]]
H = [[9,3,5,6,4,8,6,2],[7,7,4,8,7,5,9,5]]
P = [[5,2,3,6,8,4,5,7],[2,4,4,5,3,9,6,3],[3,2,5,4,2,7,8,2]]
s = [2, 5, 6, 3, 0, 1, 4, 7]



class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ordonnancement")
        self.geometry("800x610")
        self.minsize(800, 610)
        self.maxsize(800, 610)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        # create navigation frame
        self.navigation_frame = ct.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
         # load images with light and dark mode image
        self.logo_image = ct.CTkImage(light_image=Image.open(os.path.join(image_path, "logo_light.png")),
                                      dark_image=Image.open(os.path.join(image_path, "logo_dark.png")), size=(40, 40))
        self.combinations_image = ct.CTkImage(light_image=Image.open(os.path.join(image_path, "combinations_light.webp")),
                                              dark_image=Image.open(os.path.join(image_path, "combinations_dark.png")), size=(40, 40))
        self.matrix_image = ct.CTkImage(light_image=Image.open(os.path.join(image_path, "matrix_light.webp")),
                                        dark_image= Image.open(os.path.join(image_path, "matrix_dark.png")), size=(40, 40))
        self.home_image = ct.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(40, 40))
        self.Gantt_image = ct.CTkImage(light_image=Image.open(os.path.join(image_path, "Gantt_light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "Gantt_dark.png")), size=(40, 40))
        self.sequence_image = ct.CTkImage(light_image=Image.open(os.path.join(image_path, "sequence_light.webp")),
                                                     dark_image=Image.open(os.path.join(image_path, "sequence_dark.png")), size=(40, 40))
        self.in_home_image = ct.CTkImage(Image.open(os.path.join(image_path, "home_image.png")), size=(500, 250))

        self.txt_image= ct.CTkImage(light_image=Image.open(os.path.join(image_path, "txt_light.webp")), 
                                          dark_image=Image.open(os.path.join(image_path, "txt_dark.png")),size=(200, 200))

          # title
        self.navigation_frame_label = ct.CTkLabel(self.navigation_frame, text=" Ordonnancement", image=self.logo_image,
                                                             compound="left", font=ct.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0)#, padx=20, pady=20)
        
                #home button
        self.home_button = ct.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0)#, sticky="ew")
                # matrix button
        self.matrix_btn = ct.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Insertion des données",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.matrix_image, anchor="w", command=self.matrix_button_event)
        self.matrix_btn.grid(row=2, column=0)#, sticky="ew")
                # sequence button
        self.seq_btn = ct.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=" Trouver la bonne sequence",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.sequence_image, anchor="w", command=self.sequence_button_event)
        self.seq_btn.grid(row=3, column=0)#, sticky="ew")
                # combinations button
        self.combinations_btn = ct.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Combinations",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.combinations_image, anchor="w", command=self.combinations_button_event)
        self.combinations_btn.grid(row=4, column=0)#, sticky="ew")
                # Gantt chart button
        self.Ganttt_btn = ct.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Diagramme de Gantt",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.Gantt_image, anchor="w",command=self.Gantt_button_event)
        self.Ganttt_btn.grid(row=5, column=0)#, sticky="ew")
                #temp de preparation
        self.checkbox_prep = ct.CTkCheckBox(master=self.navigation_frame, text= "utiluser les temps de preparation",command=self.checkbox_prep_fun)
        self.checkbox_prep.grid(row=6, column=0, padx=5, pady=5, sticky='ew')
                #blockage
        self.checkbox_block = ct.CTkCheckBox(master=self.navigation_frame, text= "utiluser la condition de bloquage",command=self.checkbox_block_fun)
        self.checkbox_block.grid(row=7, column=0, padx=5, pady=5, sticky='ew')
                #noidel
        self.checkbox_noidel = ct.CTkCheckBox(master=self.navigation_frame, text= "utiluser la condition de non arret",command=self.checkbox_noidel_fun)
        self.checkbox_noidel.grid(row=8, column=0, padx=5, pady=5, sticky='ew')
                #nowit
        self.checkbox_nowait = ct.CTkCheckBox(master=self.navigation_frame, text= "utiluser la condition de non attendre",command=self.checkbox_nowait_fun)
        self.checkbox_nowait.grid(row=9, column=0, padx=5, pady=5, sticky='ew')
                # tardiness
        self.checkbox_tardiness = ct.CTkCheckBox(master=self.navigation_frame, text= "utiluser les retards 'tardiness'",command=self.checkbox_tardiness_fun)
        self.checkbox_tardiness.grid(row=10, column=0, padx=5, pady=5, sticky='ew')
                # alerts
        self.alerts = ct.CTkLabel(self.navigation_frame,text="Alerts")
        self.alerts.grid(row=11, column=0)#, sticky="ew")
                #apparence mode menu
        self.appearance_mode_menu = ct.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light" , "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=12, column=0, padx=5, pady=5, sticky='ew')
                #language menu
        #self.language_menu = ct.CTkOptionMenu(self.navigation_frame, values=["Français", "English"],
        #                                                        command=self.fun)
        #self.language_menu.grid(row=10, column=0, padx=20, pady=20, sticky='ew')

                    # create home frame
        self.home_frame = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = ct.CTkLabel(self.home_frame, text="", image=self.in_home_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=40, pady=20)

        self.home_frame_large_label = ct.CTkLabel(self.home_frame, text="Créer par Salah Eddine Maimouni et Aya Kraimi\nDans cette application vous pouver faire\n la résolution des problèmes de production de type \nFlowshop où vous pouver ordonancer jobs sur des machines en série\n avec ou sans temps de préparation et avec ou sans blocage\navec condition de non attendre ou condition de non arret \n séparateur dicimale '.'\n séparateur dans les matrices et les séquences ','\n séparateur entre les matrices des préparation '-'\n 1) Entrer les donnée nécessaires \n 'temps de processus / temps de préparation / temps de delais / séquence'\n 2) vous pouver trouver la séquence optimisant Cmax on utilusant l'algorithme de jonhson ou CDS\n au cas d'avec aucune condition et sans temps de préparation\n 3) Vous pouver utiluser la fonction combinaisons soit pour\n tester des séquences spécifiques  ou pour trouver les séquences optimisant \n Cmax, Total Tardiness ou les deux \n4) la fonction Gantt permet de tracer le diagramme de Gantt \n et voir les performances de machines et d'autres detailes \n 5) Vous pouver extraire un rapport word daitailler \noù vous trouver toute étape de résolution de problème    ")
        self.home_frame_large_label.grid(row=1, column=0, padx=40, pady=20)


            # create matrix frame
        self.matrix_frame = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.matrix_frame.grid_columnconfigure(0, weight=1)


        # ajouter la tabview
        self.tabview = ct.CTkTabview(self.matrix_frame)
        self.tabview.grid(row=0, column=0, columnspan=2)#, padx=40, pady=20)
        #enter text matrix
        self.tabview.add("selectionner les fichiers txt")
        self.text_insert = ct.CTkLabel(self.tabview.tab("selectionner les fichiers txt"),image = self.txt_image,text="")
        self.text_insert.pack()
        self.text_insert_button1 = ct.CTkButton(self.tabview.tab("selectionner les fichiers txt"), text="temps des processus",command=self.txt_insert_event)
        self.text_insert_button1.pack(side=ct.LEFT)
        self.text_insert_button2 = ct.CTkButton(self.tabview.tab("selectionner les fichiers txt"), text="temps de preparation",command=self.prep_insert_event)
        self.text_insert_button2.pack(side=ct.RIGHT)
        #enter matrix
        """self.tabview.add("inserer la matrice")
        self.matrix_insert = ct.CTkLabel(self.tabview.tab("inserer la matrice"),image = self.matrix_image,text="")
        self.matrix_insert.pack()
        self.not_fic = ct.CTkLabel(self.tabview.tab("inserer la matrice"),text="clique pour ajouter la matrice")
        self.not_fic.pack()
        self.matrix_insert_button = ct.CTkButton(self.tabview.tab("inserer la matrice"), text="click",command=self.matrix_insert_event)
        self.matrix_insert_button.pack()"""
        self.matrix_text = ct.CTkTextbox(self.matrix_frame, width= 200, height= 220)
        self.matrix_text.grid(row=2, column=0, padx=20, pady=20)
        self.prep_text = ct.CTkTextbox(self.matrix_frame, width= 200, height= 220)
        self.prep_text.grid(row=2, column=1, padx=20, pady=20)

        self.save_txt_button = ct.CTkButton(self.matrix_frame, text="enregistrer \n les temps de processus",command=self.save_txt_event)
        self.save_txt_button.grid(row=3, column=0)

        self.save_prep_button = ct.CTkButton(self.matrix_frame, text="enregistrer \n les temps de preparation",command=self.save_prep_event)
        self.save_prep_button.grid(row=3, column=1)
        self.dj_label = ct.CTkLabel(self.matrix_frame, text="temps de délais 'dj' :")
        self.dj_entry = ct.CTkEntry(self.matrix_frame)
        self.dj_label.grid(row=4, column=0,padx=5, pady=5)
        self.dj_entry.grid(row=4, column=1,padx=5, pady=5)

            # create combinations frame
        self.combinations_frame = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.combination_test_btn= ct.CTkButton(self.combinations_frame, text="tester ces combinaisons",command=self.combinations_test_event)
        self.combination_test_btn.grid(row=0,column=0,columnspan=2)
        
        self.label_comb1 = ct.CTkLabel(self.combinations_frame, text="enter les combinaisons à tester")
        self.label_comb1.grid(row=1,column=0)
        self.combinations_entry_result = ct.CTkTextbox(self.combinations_frame, width= 200, height= 220)
        self.combinations_entry_result.grid(row=2,column=0, padx=20, pady=20)
        self.label_comb2 = ct.CTkLabel(self.combinations_frame, text="resultas de test")
        self.label_comb2.grid(row=1,column=1)
        self.combinations_test_result = ct.CTkTextbox(self.combinations_frame, width= 200, height= 220)
        self.combinations_test_result.grid(row=2,column=1, padx=20, pady=20)

        self.combination_btn= ct.CTkButton(self.combinations_frame, text="séquences avec \n minimisation de :",command=self.combinations_event)
        self.combination_btn.grid(row=3,column=0, padx=5, pady=10)
        self.critere_menu = ct.CTkOptionMenu(self.combinations_frame, values=["Cmax"])
        self.critere_menu.grid(row=3, column=1, padx=5, pady=10)
        self.combinations_result = ct.CTkTextbox(self.combinations_frame, width= 300, height= 220)
        self.combinations_result.grid(row=4,column=0,columnspan=2)

            # create sequence frame
        self.sequence_frame = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.Jonhson_button = ct.CTkButton(self.sequence_frame, text="Jonhson",command=self.Jonhson_event)
        self.Jonhson_button.pack(padx=5, pady=3)
        self.jonhson_result = ct.CTkTextbox(self.sequence_frame)
        self.jonhson_result.pack(padx=5, pady=3)

        self.CDS_btn= ct.CTkButton(self.sequence_frame, text="CDS",command=self.CDS_event)
        self.CDS_btn.pack(padx=5, pady=3)
        self.CDS_label = ct.CTkLabel(self.sequence_frame, text="K =")
        self.CDS_label.pack(padx=5, pady=3)
        self.k_entry = ct.CTkEntry(self.sequence_frame)
        self.k_entry.pack(padx=5, pady=3)
        self.checkbox_k = ct.CTkCheckBox(master=self.sequence_frame, text= "tous les k")#, variable = self.long_var)
        self.checkbox_k.pack(padx=5, pady=3)
        self.CDS_result = ct.CTkTextbox(self.sequence_frame)
        self.CDS_result.pack(padx=5, pady=3)
            # create Gantt frame
        self.Gantt_frame = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.seq_label = ct.CTkLabel(self.Gantt_frame, text="sequence = ")
        self.seq_label.pack(padx=5, pady=10)
        self.seq_entry = ct.CTkEntry(self.Gantt_frame)
        self.seq_entry.pack(padx=5, pady=10)
        self.Gantt_btn= ct.CTkButton(self.Gantt_frame, text="Diagramme de Gantt",command=self.Gantt_event)
        self.Gantt_btn.pack(padx=5, pady=10)
        self.report_frame = ct.CTkFrame(self.Gantt_frame, corner_radius=0)
        self.report_frame.pack(padx=120, pady=20,fill=ct.BOTH, expand=1)
        self.label_report = ct.CTkLabel(self.report_frame, text = "Génération de rapport:")
        self.label_report.pack()
        self.checkbox_regular_report = ct.CTkCheckBox(self.report_frame, text= "PFSP \n(Permutation Flow Shop Scheduling Problem)",command=self.checkbox_prep_fun)
        self.checkbox_regular_report.pack(padx=0, pady=3)   
        self.checkbox_prep_report = ct.CTkCheckBox(self.report_frame, text= "PFSP-SDST \n(Permutation Flow Shop Scheduling Problem \n with Sequence Depending Setup Time)",command=self.checkbox_prep_fun)
        self.checkbox_prep_report.pack(padx=0, pady=3)
        self.checkbox_block_report = ct.CTkCheckBox(master=self.report_frame, text= "BFSP \n(Blocking Flow Shop Scheduling Problem)",command=self.checkbox_block_fun)
        self.checkbox_block_report.pack(padx=0, pady=3)
        self.checkbox_prep_block_report = ct.CTkCheckBox(master=self.report_frame, text= "BFSP-SDST \n(Blocking Flow Shop Scheduling Problem \n with Sequence Depending Setup Time)",command=self.checkbox_block_fun)
        self.checkbox_prep_block_report.pack(padx=0, pady=3)
        self.checkbox_noidel_report = ct.CTkCheckBox(master=self.report_frame, text= "NIPFSP \n(No-Idel Permutation Flow Shop Scheduling Problem)",command=self.checkbox_noidel_fun)
        self.checkbox_noidel_report.pack(padx=0, pady=3)
        self.checkbox_nowait_report = ct.CTkCheckBox(master=self.report_frame, text= "NWPFSP \n(No-Wait Permutation Flow Shop Scheduling Problem)",command=self.checkbox_nowait_fun)
        self.checkbox_nowait_report.pack(padx=0, pady=3)
        self.checkbox_tardiness_report = ct.CTkCheckBox(master=self.report_frame, text= "Utiluser les retards 'tardiness'",command=self.checkbox_tardiness_fun)
        self.checkbox_tardiness_report.pack(padx=0, pady=3)
        self.checkbox_choosed_seq_report = ct.CTkCheckBox(master=self.report_frame, text= "Utiluser la séquence spécifique'",command=self.checkbox_tardiness_fun)
        self.checkbox_choosed_seq_report.pack(padx=0, pady=3)
        self.report_btn= ct.CTkButton(self.report_frame, text="générer un document",command=self.report_event)
        self.report_btn.pack(padx=5, pady=3)
        """
        self.report_frame.grid(row=0, column=0, sticky="nsew")
        self.report_frame.grid_rowconfigure(4, weight=1)"""
        #self.ctk_textbox_scrollbar = ct.CTkScrollbar(self.Gantt_frame)
        #self.ctk_textbox_scrollbar.pack(side=ct.LEFT)




            # select default frame
        self.select_frame_by_name("home")


    def fun(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")

    def change_appearance_mode_event(self, new_appearance_mode):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        ct.set_appearance_mode(new_appearance_mode)

    def select_frame_by_name(self, name):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "matrix":
            self.matrix_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.matrix_frame.grid_forget()
        if name == "combinations":
            self.combinations_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.combinations_frame.grid_forget()
        if name == "sequence":
            self.sequence_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sequence_frame.grid_forget()
        if name == "Gantt":
            self.Gantt_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.Gantt_frame.grid_forget()

    def home_button_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        self.select_frame_by_name("home")
        
    def matrix_button_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        self.select_frame_by_name("matrix")

    def combinations_button_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        self.select_frame_by_name("combinations")

    def sequence_button_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        self.select_frame_by_name("sequence")

    def Gantt_button_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        self.select_frame_by_name("Gantt")

    def txt_insert_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        path = get_file_path()
        print(path)
        f = open(path,"r")
        a=""
        for l in f:
            a=a+l+"\n"
        print(a)
        if type(ttm(a))==str:
            self.alerts.configure(text='le fichier est endomagé', fg_color="orange")
            return None
        self.matrix_text.delete(1.0,ct.END)
        self.matrix_text.insert(1.0,a)

    def prep_insert_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        path = get_file_path()
        print(path)
        f = open(path,"r")
        a=""
        for l in f:
            a=a+l+"\n"
        print(a)
        if type(char_to_lst(a))==str:
            self.alerts.configure(text='le fichier est endomagé', fg_color="orange")
            return None
        self.prep_text.delete(1.0,ct.END)
        self.prep_text.insert(1.0,a)

    """def matrix_insert_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        root = tk.Tk()
        window = MatrixEditor(root)
        root.mainloop()"""

    def save_txt_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        var = ttm(self.matrix_text.get(1.0,ct.END))
        if type(var)==str:
            self.alerts.configure(text=var, fg_color="orange")
            return None
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        print(var)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.matrix_text.get(1.0,ct.END))

    def save_prep_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        var = char_to_lst(self.prep_text.get(1.0,ct.END))
        if type(var)==str:
            self.alerts.configure(text='erreur de syntaxt', fg_color="orange")
            return None
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        print(var)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.prep_text.get(1.0,ct.END))

    def Jonhson_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        if self.checkbox_prep.get() == 1:
            self.alerts.configure(text='jonhson fonctionne seulement \n sans temps de preparation', fg_color="black")
            self.jonhson_result.delete(1.0,ct.END)
            return None
        if self.checkbox_block.get() == 1:
            self.alerts.configure(text='jonhson fonctionne seulement \n sans condition de blocage', fg_color="black")
            self.jonhson_result.delete(1.0,ct.END)
            return None
        if self.checkbox_noidel.get() == 1:
            self.alerts.configure(text='jonhson fonctionne seulement \n sans condition de non arret', fg_color="black")
            self.jonhson_result.delete(1.0,ct.END) 
            return None
        if self.checkbox_nowait.get() == 1:
            self.alerts.configure(text='jonhson fonctionne seulement \n sans condition de non attendre', fg_color="black")  
            self.jonhson_result.delete(1.0,ct.END)    
            return None
        matrix = ttm(self.matrix_text.get(1.0,ct.END))
        if type(matrix) == str:
            self.alerts.configure(text=matrix, fg_color="red")
            return None
        if matrix==[]:
            self.alerts.configure(text="la matrice n'existe pas", fg_color="red")
            return None 
        Ord = ordonnancement(M=matrix)
        out = Ord.Johnson()
        result = ""
        char_lst=["U = ","V = ","U_SPT = ","V_LPT = "]
        if len(matrix) != 2 and matrix != []:
            print(matrix)
            self.alerts.configure(text="Jonhson Algo ne fonctionne \n qu'avec deux machines ", fg_color="red")
            return None
        try:
            for o,char in zip(out,char_lst):
                result = result +char+str(o)
                result +="\n"
        except:
            self.alerts.configure(text="la matrice n'est pas exacte", fg_color="red")
            return None  
        L='\n'
        for lst in out[4]:
            char=""
            for i in range(len(lst)):
                if i!=len(lst)-1:
                    char+=str(lst[i])+","
                else:
                    char+=str(lst[i])
            L=L+char+'\n'
        result = result+"[UV] = "+L
        print(result)
        self.jonhson_result.delete(1.0,ct.END)
        self.jonhson_result.insert(1.0,result)

    def CDS_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        try:
            if self.checkbox_k.get()==0:
                int(self.k_entry.get())
        except ValueError:
            self.alerts.configure(text="k n'est pas valide", fg_color="red")
            return None
        if self.checkbox_prep.get() == 1:
            self.alerts.configure(text='CDS fonctionne seulement \n sans temps de preparation', fg_color="black")
            self.CDS_result.delete(1.0,ct.END)
            return None
        if self.checkbox_block.get() == 1:
            self.alerts.configure(text='CDS fonctionne seulement \n sans condition de blocage', fg_color="black")
            self.CDS_result.delete(1.0,ct.END)
            return None
        if self.checkbox_noidel.get() == 1:
            self.alerts.configure(text='CDS fonctionne seulement \n sans condition de non arret', fg_color="black")
            self.CDS_result.delete(1.0,ct.END) 
            return None
        if self.checkbox_nowait.get() == 1:
            self.alerts.configure(text='CDS fonctionne seulement \n sans condition de non attendre', fg_color="black")
            self.CDS_result.delete(1.0,ct.END)      
            return None
        matrix = ttm(self.matrix_text.get(1.0,ct.END))
        if type(matrix) == str:
            self.alerts.configure(text=matrix, fg_color="red")
            return None 
        if matrix==[]:
            self.alerts.configure(text="la matrice n'existe pas", fg_color="red")
            return None 
        if self.checkbox_k.get()==1:
            result = ""
            for k in range(1,len(matrix)):
                Ord = ordonnancement(M=matrix)
                out = Ord.CDS(k)
                L='\n'
                try:
                    for lst in out[4]:
                        char=""
                        for i in range(len(lst)):
                            if i!=len(lst)-1:
                                char+=str(lst[i])+","
                            else:
                                char+=str(lst[i])
                        L=L+char+'\n'
                except TypeError:
                    self.alerts.configure(text="CDS ne fonctionne qu'avec \n plus de deux machines", fg_color="red")
                    return None
                result = result + "k=" + str(k) + "->" + L +"\n"
            self.CDS_result.delete(1.0,ct.END)
            self.CDS_result.insert(1.0,result)
        else:
            if int(self.k_entry.get()) in range(1,len(matrix)):
                Ord = ordonnancement(M=matrix)
                try:
                    out = Ord.CDS(int(self.k_entry.get()))
                except:
                    self.alerts.configure(text="la matrice n'est pas exacte", fg_color="red")
                    return None 
                result = "pour k = "+str(self.k_entry.get())+"\n"
                char_lst=["U = ","V = ","U_SPT = ","V_LPT = "]
                try:
                    for o,char in zip(out,char_lst):
                        result = result +char+str(o)
                        result +="\n"
                except TypeError:
                    self.alerts.configure(text="CDS ne fonctionne qu'avec \n plus de deux machines", fg_color="red")
                    return None
                L='\n'
                for lst in out[4]:
                    char=""
                    for i in range(len(lst)):
                        if i!=len(lst)-1:
                            char+=str(lst[i])+","
                        else:
                            char+=str(lst[i])
                    L=L+char+'\n'
                result = result+"[UV] = "+L
                print(result)
                self.CDS_result.delete(1.0,ct.END)
                self.CDS_result.insert(1.0,result)
            else:
                self.alerts.configure(text="la valeur de k n'est pas exacte", fg_color="red")
                return None 

    def combinations_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        matrix = ttm(self.matrix_text.get(1.0,ct.END))
        matrix_prep = char_to_lst(self.prep_text.get(1.0,ct.END))
        if type(matrix) == str:
            self.alerts.configure(text=matrix, fg_color="red")
            return None
        if type(matrix_prep) == str:
            self.alerts.configure(text=matrix_prep, fg_color="red")
            return None
        if matrix_prep==[]:
            self.alerts.configure(text="les temps de preparation \n n'existe pas", fg_color="red")
            return None 
        if matrix==[]:
            self.alerts.configure(text="la matrice n'existe pas", fg_color="red")
            return None 
        if len(matrix[0])>9:
            self.alerts.configure(text="pour plus de 9 jobs cette fonction \n prend un tres long temps", fg_color="red")
            return None 
        DJ = dj_test(self.dj_entry.get())
        if self.checkbox_tardiness.get()==1:
            if type(DJ)==str:
                self.alerts.configure(text=DJ, fg_color="red")
                return None
            elif len(DJ)!=len(matrix[0]):
                self.alerts.configure(text="erreur dans les temps de delai", fg_color="red")
                return None
        result = ""
        if self.checkbox_prep.get() == 0 and self.checkbox_block.get() == 0 and self.checkbox_noidel.get() == 0 and self.checkbox_nowait.get() == 0:
            result+=" sans preparation \n et sans conditions \n"
        elif self.checkbox_prep.get() == 1 and self.checkbox_block.get() == 0 and self.checkbox_noidel.get() == 0 and self.checkbox_nowait.get() == 0:
            result+=" avec preparation \n et sans conditions \n"
        elif self.checkbox_prep.get() == 0 and self.checkbox_block.get() == 1 and self.checkbox_noidel.get() == 0 and self.checkbox_nowait.get() == 0:
            result+=" sans preparation \n et avec blocage \n"
        elif self.checkbox_prep.get() == 1 and self.checkbox_block.get() == 1 and self.checkbox_noidel.get() == 0 and self.checkbox_nowait.get() == 0:
            result+=" avec preparation \n et avec blocage \n"
        elif self.checkbox_prep.get() == 0 and self.checkbox_block.get() == 0 and self.checkbox_noidel.get() == 1 and self.checkbox_nowait.get() == 0:
            result+=" sans preparation \n et avec non arret \n"
        elif self.checkbox_prep.get() == 0 and self.checkbox_block.get() == 0 and self.checkbox_noidel.get() == 0 and self.checkbox_nowait.get() == 1:
            result+=" sans preparation \n et avec non attendre \n"
        Ord = ordonnancement(M=matrix,Mprep=matrix_prep,prep=self.checkbox_prep.get(),block=self.checkbox_block.get(),noidel=self.checkbox_noidel.get(),nowait=self.checkbox_nowait.get(),TT=self.checkbox_tardiness.get(),dj=DJ)
        if self.critere_menu.get()=="Cmax":
            out = Ord.choosed_combinations()
            result+="min(Cmaxs) = "+str(out[0])+"\n"
        elif self.critere_menu.get()=="TT":
            out = Ord.choosed_combinations_by_TT()
            result+="min(TTs) = "+str(out[0])+"\n"
        else:
            out = Ord.choosed_combinations_by_TT_Cmax()
            if type(out)==str:
                self.combinations_result.delete(1.0,ct.END)
                self.combinations_result.insert(1.0,out)
                return None
            else:
                result+="min(TTs) = "+str(out[0][0])+"\n min(Cmaxs) = "+str(out[0][1])+"\n"
        for seq in out[1]:
            char = ""
            for i in range(len(seq)):
                if i!=len(seq)-1:
                    char+=str(seq[i])+","
                else:
                    char+=str(seq[i])
            result = result + char
            result +="\n"
        self.combinations_result.delete(1.0,ct.END)
        self.combinations_result.insert(1.0,result)
    
    def combinations_test_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        matrix = ttm(self.matrix_text.get(1.0,ct.END))
        matrix_prep = char_to_lst(self.prep_text.get(1.0,ct.END))
        if type(matrix) == str:
            self.alerts.configure(text=matrix, fg_color="red")
            return None
        if type(matrix_prep) == str:
            self.alerts.configure(text=matrix_prep, fg_color="red")
            return None
        if matrix_prep==[]:
            self.alerts.configure(text="les temps de preparation \n n'existe pas", fg_color="red")
            return None 
        if matrix==[]:
            self.alerts.configure(text="la matrice n'existe pas", fg_color="red")
            return None
        DJ = dj_test(self.dj_entry.get())
        if self.checkbox_tardiness.get()==1:
            if type(DJ)==str:
                self.alerts.configure(text=DJ, fg_color="red")
                return None
            elif len(DJ)!=len(matrix[0]):
                self.alerts.configure(text="erreur dans les temps de delai", fg_color="red")
                return None
        seqqq= ttm(self.combinations_entry_result.get(1.0,ct.END))
        if type(seqqq) == str:
            self.alerts.configure(text=seqqq, fg_color="red")
            return None
        seq_to_test=[]
        for seq,k in zip(seqqq,range(len(seqqq))):
            seq_to_test.append([])
            for i in range(len(seqqq[0])):
                seq_to_test[k].append(int(seq[i]))
        if seq_to_test ==[]:
            self.alerts.configure(text="entrer les sequences à tester", fg_color="red")
            return None 
        if self.checkbox_prep.get() == 0 and self.checkbox_block.get() == 0 and self.checkbox_noidel.get() == 0 and self.checkbox_nowait.get() == 0:
            result=" sans preparation \n et sans conditions \n"
        elif self.checkbox_prep.get() == 1 and self.checkbox_block.get() == 0 and self.checkbox_noidel.get() == 0 and self.checkbox_nowait.get() == 0:
            result=" avec preparation \n et sans conditions \n"
        elif self.checkbox_prep.get() == 0 and self.checkbox_block.get() == 1 and self.checkbox_noidel.get() == 0 and self.checkbox_nowait.get() == 0:
            result=" sans preparation \n et avec blocage \n"
        elif self.checkbox_prep.get() == 1 and self.checkbox_block.get() == 1 and self.checkbox_noidel.get() == 0 and self.checkbox_nowait.get() == 0:
            result=" avec preparation \n et avec blocage \n"
        elif self.checkbox_prep.get() == 0 and self.checkbox_block.get() == 0 and self.checkbox_noidel.get() == 1 and self.checkbox_nowait.get() == 0:
            result=" sans preparation \n et avec non arret \n"
        elif self.checkbox_prep.get() == 0 and self.checkbox_block.get() == 0 and self.checkbox_noidel.get() == 0 and self.checkbox_nowait.get() == 1:
            result=" sans preparation \n et avec non attendre \n"
        Cmaxs=[]
        TTs=[]
        for seq in seq_to_test:
            Ord= ordonnancement(M=matrix,S=seq,Mprep=matrix_prep,prep=self.checkbox_prep.get(),block=self.checkbox_block.get(),noidel=self.checkbox_noidel.get(),nowait=self.checkbox_nowait.get(),TT=self.checkbox_tardiness.get(),dj=DJ)
            if self.checkbox_tardiness.get()==1:
                CT=Ord.Cmax_TT(seq)
                result+= str(seq)+"-> \n Cmax="+str(CT[0])+" / TT="+ str(CT[1])+"\n"
                Cmaxs.append(CT[0])
                TTs.append(CT[1])
            else:
                C=Ord.Cmax(seq)
                result+= str(seq)+"-> \n Cmax="+str(C)+"\n"
                Cmaxs.append(C)
        if self.checkbox_tardiness.get()==1:
            result= "min(Cmaxs)="+str(min(Cmaxs))+"\n"+"min(TTs)="+str(min(TTs))+"\n"+result
        else:
            result= "min(Cmaxs)="+str(min(Cmaxs))+"\n"+result
        self.combinations_test_result.delete(1.0,ct.END)
        self.combinations_test_result.insert(1.0,result)
        
    def Gantt_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        matrix = ttm(self.matrix_text.get(1.0,ct.END))
        matrix_prep = char_to_lst(self.prep_text.get(1.0,ct.END))
        if type(matrix) == str:
            self.alerts.configure(text=matrix, fg_color="red")
            return None
        if type(matrix_prep) == str:
            self.alerts.configure(text=matrix_prep, fg_color="red")
            return None
        if matrix_prep==[]:
            self.alerts.configure(text="les temps de preparation \n n'existe pas", fg_color="red")
            return None 
        if matrix==[]:
            self.alerts.configure(text="la matrice n'existe pas", fg_color="red")
            return None 
        DJ = dj_test(self.dj_entry.get())
        if self.checkbox_tardiness.get()==1:
            if type(DJ)==str:
                self.alerts.configure(text=DJ, fg_color="red")
                return None
            elif len(DJ)!=len(matrix[0]):
                self.alerts.configure(text="erreur dans les temps de delai", fg_color="red")
                return None
        seq = self.seq_entry.get()
        seq_lst = seq.split(",")
        job_lst = [] 
        for job in seq_lst:
            try:
                job_lst.append(int(job))
            except:
                self.alerts.configure(text="erreur dans la sequence", fg_color="red")
        if type(test_seq(job_lst,len(matrix[0])))==str:
            self.alerts.configure(text=test_seq(job_lst,len(matrix[0])), fg_color="red")
            return None
        Ord = ordonnancement(M=matrix,S=job_lst,Mprep=matrix_prep,prep=self.checkbox_prep.get(),
                             block=self.checkbox_block.get(),noidel=self.checkbox_noidel.get(),
                             nowait=self.checkbox_nowait.get(),dj=DJ,TT=self.checkbox_tardiness.get())
        TFR_TAR = Ord.TFR_TAR()
        TW = [[],[],[]]#Ord.TW()
        first_tabs = Ord.traite()
        """print(first_4_tabs[0])
        print(first_4_tabs[1])
        print(first_4_tabs[2])
        print(first_4_tabs[3])
        print(TFR_TAR)
        print(TW[0])
        print(TW[1])
        print(TW[2])"""



        task=Ord.Gantt()
        if self.checkbox_nowait.get() == 1:
            tables = Tableaux(first_tabs[0],first_tabs[1],[[]],[[]],TFR_TAR,first_tabs[2],[[]],[[]],[[]],task,job_lst,0,0,1,0,first_tabs[3],first_tabs[-1],first_tabs[-2],self.checkbox_tardiness.get())
        elif self.checkbox_noidel.get() == 1:
            tables = Tableaux(first_tabs[0],first_tabs[1],[[]],[[]],TFR_TAR,first_tabs[2],[[]],[[]],[[]],task,job_lst,0,0,0,1,first_tabs[3],first_tabs[-1],first_tabs[-2],self.checkbox_tardiness.get())
        elif self.checkbox_prep.get()==1 and self.checkbox_block.get()==0:
            TW = Ord.TW()
            tables = Tableaux(first_tabs[0],first_tabs[1],first_tabs[2],first_tabs[3],TFR_TAR,TW[0],TW[1],TW[2],[[]],task,job_lst,1,0,0,0,first_tabs[4],first_tabs[-1],first_tabs[-2],self.checkbox_tardiness.get())
        elif self.checkbox_prep.get()==0 and self.checkbox_block.get()==1:
            tables = Tableaux(first_tabs[0],first_tabs[1],[[]],[[]],TFR_TAR,first_tabs[4],[[]],[[]],[[]],task,job_lst,0,1,0,0,first_tabs[5],first_tabs[-1],first_tabs[-2],self.checkbox_tardiness.get())
        elif self.checkbox_prep.get()==0 and self.checkbox_block.get()==0:
            TW = Ord.TW()
            tables = Tableaux(first_tabs[0],first_tabs[1],[[]],[[]],TFR_TAR,TW[0],[[]],[[]],[[]],task,job_lst,0,0,0,0,first_tabs[2],first_tabs[-1],first_tabs[-2],self.checkbox_tardiness.get())
        elif self.checkbox_prep.get()==1 and self.checkbox_block.get()==1:
            tables = Tableaux(first_tabs[0],first_tabs[1],first_tabs[2],first_tabs[3],TFR_TAR,first_tabs[6],first_tabs[9],first_tabs[8],first_tabs[7],task,job_lst,1,1,0,0,first_tabs[10],first_tabs[-1],first_tabs[-2],self.checkbox_tardiness.get())
        if __name__ == "__main__":
            tables.mainloop()

        """result = "Cmax = " + str(Ord.Cmax(Seq=job_lst)) + "\n"
        for t1 , t2 , i in zip(TFR_TAR[0] , TFR_TAR[1] , range(len(TFR_TAR))):
            result += "TFR[" + str(i) + "] = " + str(round(t1*100,4)) + "%" + "\n"
            result += "TAR[" + str(i) + "] = " + str(round(t2*100,4)) + "%" + "\n"
        self.to_result.delete(1.0,ct.END)
        self.to_result.insert(1.0,result)"""
        #print(Ord.TW())

    def checkbox_prep_fun(self):
        if self.checkbox_prep.get()==1:
            self.checkbox_noidel.deselect()
            self.checkbox_nowait.deselect()
    def checkbox_block_fun(self):
        if self.checkbox_block.get()==1:
            self.checkbox_noidel.deselect()
            self.checkbox_nowait.deselect()
    def checkbox_noidel_fun(self):
        if self.checkbox_noidel.get()==1:
            self.checkbox_prep.deselect()
            self.checkbox_block.deselect()
            self.checkbox_nowait.deselect()
    def checkbox_nowait_fun(self):
        if self.checkbox_nowait.get()==1:
            self.checkbox_prep.deselect()
            self.checkbox_block.deselect()
            self.checkbox_noidel.deselect()
    def checkbox_tardiness_fun(self):
        if self.checkbox_tardiness.get()==1:
            self.critere_menu.destroy()
            self.critere_menu = ct.CTkOptionMenu(self.combinations_frame, values=["Cmax", "TT" , "Cmax & TT"])
            self.critere_menu.grid(row=3, column=1, padx=5, pady=10)
        else:
            self.critere_menu.destroy()
            self.critere_menu = ct.CTkOptionMenu(self.combinations_frame, values=["Cmax"])
            self.critere_menu.grid(row=3, column=1, padx=5, pady=10)
    
    def report_event(self):
        self.alerts.configure(text='Alerts', fg_color="transparent")
        matrix = ttm(self.matrix_text.get(1.0,ct.END))
        matrix_prep = char_to_lst(self.prep_text.get(1.0,ct.END))
        if type(matrix) == str:
            self.alerts.configure(text=matrix, fg_color="red")
            return None
        if type(matrix_prep) == str:
            self.alerts.configure(text=matrix_prep, fg_color="red")
            return None
        if matrix_prep==[]:
            self.alerts.configure(text="les temps de preparation \n n'existe pas", fg_color="red")
            return None 
        if matrix==[]:
            self.alerts.configure(text="la matrice n'existe pas", fg_color="red")
            return None 
        DJ = dj_test(self.dj_entry.get())
        if self.checkbox_tardiness_report.get()==1:
            if type(DJ)==str:
                self.alerts.configure(text=DJ, fg_color="red")
                return None
            elif len(DJ)!=len(matrix[0]):
                self.alerts.configure(text="erreur dans les temps de delai", fg_color="red")
                return None
        else:
            DJ=[]

        if self.checkbox_choosed_seq_report.get()==0:
            print(matrix,matrix_prep,DJ)
            doc = Report(Matrix=matrix, TP=matrix_prep,dj=DJ,regular=self.checkbox_regular_report.get(),prep=self.checkbox_prep_report.get(),block=self.checkbox_block_report.get(),prep_block=self.checkbox_prep_block_report.get(),noidel=self.checkbox_noidel_report.get(),nowait=self.checkbox_nowait_report.get())
        else:
            seq = self.seq_entry.get()
            seq_lst = seq.split(",")
            job_lst = [] 
            for job in seq_lst:
                try:
                    job_lst.append(int(job))
                except:
                    self.alerts.configure(text="erreur dans la sequence", fg_color="red")
            if type(test_seq(job_lst,len(matrix[0])))==str:
                self.alerts.configure(text=test_seq(job_lst,len(matrix[0])), fg_color="red")
                return None
            doc = Report(Seq=job_lst,Matrix=matrix, TP=matrix_prep,dj=DJ,regular=self.checkbox_regular_report.get(),prep=self.checkbox_prep_report.get(),block=self.checkbox_block_report.get(),prep_block=self.checkbox_prep_block_report.get(),noidel=self.checkbox_noidel_report.get(),nowait=self.checkbox_nowait_report.get())
    


if __name__ == "__main__":
    app = App()
    app.mainloop()


