"""START[i].sort()
                END[i].sort()
                index_color = 0
                colors[i].append(color_names[index_color])
                texts[i].append("J"+str(self.S[index_color]))
                index_color+=1
                for j in range(1,len(START[i])):
                    print(START)
                    print(colors,texts)
                    if START[i][j] in TBstarts:
                        colors[i].append('silver')
                        texts[i].append("TB")
                    else:
                        colors[i].append(color_names[index_color])
                        texts[i].append("J"+str(self.S[index_color]))
                        index_color+=1"""
Q = [[2,4,5,3],[5,6,7,8],[3,2,3,2]]
H = [[9,3,5,6,4,8,6,2],[7,7,4,8,7,5,9,5]]
P = [[5,2,3,6,8,4,5,7],[2,4,4,5,3,9,6,3],[3,2,5,4,2,7,8,2]]
s = [2, 5, 6, 3, 0, 1, 4, 7]
""""


list_prep = [[[2, 2, 3, 2, 1], 
              [2, 3, 2, 3, 3], 
              [3, 2, 3, 4, 2], 
              [1, 3, 2, 3, 2], 
              [3, 4, 2, 3, 1]], 
             [[3, 1, 3, 2, 1], 
              [3, 3, 2, 3, 3], 
              [3, 2, 3, 4, 2], 
              [2, 1, 2, 4, 2], 
              [2, 3, 2, 3, 2]], 
             [[2, 3, 1, 2, 3], 
              [1, 2, 3, 3, 3], 
              [4, 3, 2, 3, 1], 
              [3, 2, 2, 1, 2], 
              [3, 2, 3, 4, 2]]] 
matrice = [[5,5,3,6,7],
           [2,4,5,5,3],
           [3,2,5,4,2]]

list_prep2= [[[3,2,3,2,3,2],
             [2,2,2,3,2,3],
             [4,2,2,3,2,4],
             [3,3,3,5,4,3],
             [3,2,3,2,4,3],
             [2,4,3,4,3,2]],
            [[4,3,3,2,3,4],
             [2,3,2,4,2,3],
             [2,2,2,5,3,2],
             [3,2,3,3,5,4],
             [2,4,3,4,5,2],
             [3,2,3,4,5,3]],
            [[5,4,3,3,2,3],
             [3,2,2,4,2,4],
             [2,2,3,2,3,3],
             [3,2,3,3,2,3],
             [3,2,3,3,4,4],
             [2,2,3,2,3,3]]]
matrice2=[[7,9,5,9,8,4],
         [3,8,4,5,4,9],
         [5,5,8,7,6,7]]
S=[4,2,0,3,1]
S2=[2, 5, 1, 3, 4, 0]
#Test = ordonnancement(M=matrice,S=[4,2,0,3,1],Mprep=list_prep,prep=1)
#print(Test.traite())
Test2 = ordonnancement(M=matrice2,S=S2,Mprep=list_prep2,prep=1)
print(Test2.Gantt())


"""


"""
class MatrixEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Editor")

        # Demander le nombre de lignes et de colonnes au démarrage
        self.num_rows = simpledialog.askinteger("Input", "Enter the number of rows:")
        self.num_cols = simpledialog.askinteger("Input", "Enter the number of columns:")

        # Créer la matrice (une liste de listes)
        self.matrix = [['' for _ in range(self.num_cols)] for _ in range(self.num_rows)]

        # Créer une grille de boutons pour éditer la matrice
        self.buttons = []
        for i in range(self.num_rows):
            row_buttons = []
            for j in range(self.num_cols):
                btn = tk.Button(root, text='', width=5, height=2, command=lambda i=i, j=j: self.edit_cell(i, j))
                btn.grid(row=i, column=j)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Bouton de sauvegarde
        self.save_button = tk.Button(root, text="Save Matrix", command=self.save_matrix)
        self.save_button.grid(row=self.num_rows, column=0, columnspan=self.num_cols)

    def edit_cell(self, i, j):
        value = simpledialog.askstring("Input", f"Enter value for cell ({i+1}, {j+1}):")
        if value is not None:
            self.matrix[i][j] = value
            self.buttons[i][j].config(text=value)

    def save_matrix(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                for row in self.matrix:
                    file.write(','.join(row) + '\n')
"""

"""P=[[3,9,5,3,3],
   [2,5,2,2,4],
   [5,4,7,4,7],
   [3,6,2,3,9]]

def noidel_probleme_solving(P,S):
    text='L[0] = 0 \n pour i = 0:\n'
    L,C=[0.0],[]
    n,m=len(P),len(P)
    for i in range(n):
        C.append([])
        if i!=0:
            text='L['+str(i)+'] = L['+str(i-1)+'] + max[k=0,...,'+str(n)+'](sum[j=0,...k](P['+str(i-1)+']-sum[j=0,...k](P[)) \n pour i = 0:\n'
            maxs = []
            for k in range(n):
                mx1,mx2 = 0,0
                for j in range(n-k):
                    mx1+=P[i-1][S[j]]
                for j in range(n-k-1):
                    mx2+=P[i][S[j]]
                maxs.append(mx1-mx2)
            L.append(L[i-1]+max(maxs))
        for j in range(m):
            text+="    pour j = "+str(j)+":\n"
            if j==0:
                C[i].append(L[i]+P[i][S[j]])
                text+="        C["+str(i)+"]["+str(j)+'] = L['+str(i)+"] + P["+str(i)+"][S["+str(j)+"] = "+str(C[i].append(L[i]+P[i][S[j]]))
            else:
                C[i].append(C[i][j-1]+P[i][S[j]])
                text+="        C["+str(i)+"]["+str(j)+'] = C['+str(i)+"]["+str(j-1)+"] + P["+str(i)+"][S["+str(j)+"] = "+str(C[i][j-1]+P[i][S[j]])+'\n'
            
    print(C,L)
    print(text)
    return C,L
S=[0,1,2,3,4]
noidel_probleme_solving(P,S)"""

"""def nowait_probleme_solving(P,S):
    C=[[P[0][S[0]]]]
    n,m=len(P[0]),len(P)
    for i in range(1,m):
        C.append([])
        C[i].append(C[i-1][0]+P[i][S[0]])
    for j in range(n):
        for i in range(m):
            k=0
            while 1:
                if k!=m-1:
                    if C[k][j-1]+P[k][S[j]]<=C[k+1]:
                        C[k].append(C[k+1][j-1])
                        for l in range(k,-1,-1):
                            try:
                                C[l][j]=C[l+-1][j-1]"""