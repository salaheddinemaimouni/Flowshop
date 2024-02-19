import numpy as np
from itertools import permutations
from tkinter import filedialog

# Fonction pour transformer une chaîne de texte en une matrice
def ttm(txt):
    # Divise le texte en lignes
    L = txt.split("\n")
    l, m = [], []

    # Parcourt chaque ligne
    for i in range(len(L)):
        # Ignore les lignes vides ou avec des espaces multiples
        if L[i] == "" or L[i] == " " or L[i] == "  " or L[i] == "   " or L[i] == "    ":
            pass
        else:
            # Ajoute les éléments de la ligne à la liste l
            l.append(L[i].split(","))

    # Convertit les éléments en nombres flottants et construit la matrice
    for e, i in zip(l, range(len(l))):
        m.append([])
        for f, j in zip(e, range(len(e))):
            try:
                m[i].append(float(f))
            except:
                print("erreur de syntaxe")
                return "erreur de syntaxe"

    # Tente de créer un tableau NumPy à partir de la matrice
    try:
        test = np.array(m)
    except:
        return "erreur dans la matrice"

    return m

# Fonction pour tester la validité d'une séquence
def test_seq(SQ, n):
    seq = SQ.copy()

    # Vérifie si la longueur de la séquence est correcte
    if len(seq) != n:
        return "le nombre des jobs n'est pas exacte"

    # Trie la séquence et la compare avec une séquence ordonnée
    seq.sort()
    lst = list(range(n))
    if lst != seq:
        return 'la sequence est erronée'

    return SQ

# Fonction pour convertir une chaîne en liste
def char_to_lst(char):
    if char == "":
        print("le champ des temps de préparation est vide")
        return "le champ des temps de préparation est vide"

    lst1 = char.split("-")
    lst2 = []

    # Divise la chaîne en listes
    for e in lst1:
        lst2.append(e.split("\n"))

    lst3 = []
    lst22 = lst2.copy()

    # Construit une liste de listes de nombres entiers
    for i in range(len(lst22)):
        lst3.append([])
        for j in range(len(lst22[0])):
            if lst2[i][j] == "" or lst2[i][j] == " " or lst2[i][j] == " " or lst2[i][j] == " ":
                pass
            else:
                lst3[i].append(lst2[i][j].split(","))

    lst4 = []

    # Convertit les éléments en nombres entiers
    for i in range(len(lst3)):
        lst4.append([])
        for j in range(len(lst3[i])):
            lst4[i].append([])
            for k in range(len(lst3[i][j])):
                try:
                    lst4[i][j].append(float(lst3[i][j][k]))
                except:
                    print("erreur de syntaxe dans champ des temps de préparation")
                    return "erreur de syntaxe dans champ des temps de préparation"

    try:
        for i in range(len(lst4)):
            np.array(lst4[i])
    except:
        print("erreur de syntaxe dans champ des temps de préparation")
        return "erreur de syntaxe dans champ des temps de préparation"

    return lst4

# Fonction pour générer toutes les combinaisons possibles
def generate_combinations(n):
    numbers = list(range(n))
    combinations = list(permutations(numbers))
    return combinations

# Fonction pour obtenir le chemin d'un fichier via une boîte de dialogue
def get_file_path():
    file_path1 = filedialog.askopenfilename(title="Sélectionner un fichier", filetypes=(("Fichiers Python", "*.txt"), ("python", "*.py")))
    return file_path1

# Fonction pour combiner deux listes
def combine_lists(A, B):
    combined_list = []
    for a in A:
        for b in B:
            combined_list.append(a + b)
    return combined_list

# Fonction pour trouver les combinaisons valides de deux listes
def find_combinations(A, B):
    n = len(A)
    valid_combinations = []

    def generate_combinations(current_combination, a_index):
        if a_index == n:
            valid_combinations.append(current_combination[:])
            return

        value = A[a_index]
        for b_index in range(n):
            if B[b_index] == B[a_index] and b_index not in current_combination:
                current_combination[a_index] = b_index
                generate_combinations(current_combination, a_index + 1)
                current_combination[a_index] = -1

    # Initialise la liste de combinaisons
    current_combination = [-1] * n
    generate_combinations(current_combination, 0)
    R = []
    for combination in valid_combinations:
        result = [A[i] for i in combination]
        R.append(result)
    return R

# Fonction pour transposer une matrice
def transpose_matrix(matrix):
    transposed_matrix = [[0] * len(matrix) for _ in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            transposed_matrix[j][i] = matrix[i][j]
    return transposed_matrix

#fonction pour tester le syntaxt dans l'entrée des temps de delais
def dj_test(dj):
    if dj == '':
        return "chaps des delais vide"
    L  = dj.split(",")
    DJ = []
    try: 
        for i in range(len(L)):
            DJ.append(float(L[i]))
    except:
        return "erreur dans les temps de delai"
    return DJ
