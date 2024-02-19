import numpy as np
from fonctions import generate_combinations
from fonctions import find_combinations
from fonctions import combine_lists
import pandas as pd
color_names = ['red', 'green', 'blue', 'navy' , 'orange', 'purple', 'pink', 'brown', 'cyan', 'magenta',
               'teal', 'lime', 'lavender', 'indigo', 'maroon', 'gold', 'olive', 'yellow']
color_names_prep = ['black','red','black', 'green','black', 'blue','black', 'yellow','black', 'orange','black', 'purple','black', 'pink','black', 'brown','black', 'cyan','black', 'magenta','black',
                    'teal','black', 'lime','black', 'lavender','black', 'indigo','black', 'maroon','black', 'gold','black', 'olive','black', 'navy','black', 'silver']


# cas possible de (prep,block,noidel,nowait) = (0,0,0,0)/(1,0,0,0)/(0,1,0,0)/(1,1,0,0)/(0,0,1,0)/(0,0,0,1)
# Définition de la classe d'ordonnancement qui sert à traiter les problemes de flowshop
class ordonnancement () :
    def __init__(self,O=[],F=[],OP=[],FP=[],M=[[]],S=[],Mprep=[[]],prep=0,block=0,noidel=0,nowait=0,dj=[],TT=0,sim=0,do_report=0): 
        self.O = O           # O: dates des fins des jobs (out of job)
        self.M = M           # M: matrice des temps de processus 
        self.S = S           # S: séquence des jobs (indexage début de 0)
        self.F = F           # F: dates des debuts des jobs (first of job)
        self.OP = OP         # OP : dates des fins des temps de préparation (out of preparation time)
        self.FP = FP         # FP : dates des debuts des temps de préparation (firt of preparation time)       
        self.Mprep = Mprep   # Mprep : matrice des temps de preparations
        self.prep = prep     # si = 0 on n'utiluse pas les temps de preparation si non utiluse les
        self.block = block   # si = 0 on n'utiluse pas la condition de blockage si non utiluse la
        self.noidel = noidel # si = 0 on n'utiluse pas la condition de noidel si non utiluse la
        self.nowait = nowait # si = 0 on n'utiluse pas la condition de nowait si non utiluse la
        self.dj = dj         # dj : list des delais des jobs 
        self.TT = TT         # si = 0 on n'utiluse pas les delais si non utiluse les
        self.sim = sim       # si = 0 on return un dataframe dans gatt si on on retourn des listre pour les simule
        self.do_report = do_report 
        self.report = {}
    # Méthode pour traiter le probleme flowshop
    def traite (self):
        # initialisation de variables 
        self.O,self.OP,self.F,self.FP=[],[],[],[]
        # avec condition de non arret
        if self.noidel == 1:
            return noidel_probleme_solving(self.M,self.S,self.dj,self.TT,self.do_report)
        # avec condition de non attendre
        if self.nowait == 1:
            return nowait_probleme_solving(self.M,self.S,self.dj,self.TT,self.do_report)
        # sans preparation et sans blockage 
        if self.prep == 0 and self.block == 0:
            char = "Sans préparation et sans aucune condition \n" 
            # initialisation
            for i in range(len(self.M)):
                self.O.append([0.0]*len(self.M[0]))
                self.F.append([0.0]*len(self.M[0]))
            # equation 1
            self.O[0][0] = self.M[0][self.S[0]]
            char+='équation 1: pour i = 0 et j = 0\n'
            char+='  C[0][J'+str(self.S[0])+'] = P[0][J'+str(self.S[0])+'] = '+str(self.O[0][0])+'\n'
            # equation 2
            char+='équation 2: pour i = 0,...,'+str(len(self.M)-1)+' et j = 0'+'\n'
            for i in range(1,len(self.M)):
                char+='  C['+str(i)+'][J'+str(self.S[0])+'] = C['+str(i-1)+'][J'+str(self.S[0])+'] + P['+str(i)+'][J'+str(self.S[0])+'] = '+str(self.O[i-1][0])+" + "+str(self.M[i][self.S[0]])+" = "+str(self.O[i-1][0]+self.M[i][self.S[0]])+'\n'
                self.O[i][0] = self.O[i-1][0]+self.M[i][self.S[0]]
                self.F[i][0] = self.O[i-1][0]
            # equation 3
            char+='équation 3: pour i = 0 et j = 0,...,'+str(len(self.M[0])-1)+'\n'
            for j in range(1,len(self.S)):
                char+='  C[0][J'+str(self.S[j])+'] = C[0][J'+str(self.S[j-1])+'] + P[0][J'+str(self.S[j])+'] = '+str(self.O[0][j-1])+" + "+str(self.M[0][self.S[j]])+" = "+str(self.O[0][j-1]+self.M[0][self.S[j]])+'\n'
                self.O[0][j] = self.O[0][j-1]+self.M[0][self.S[j]]
                self.F[0][j] = self.O[0][j-1]
            # equation 4
            char+='équation 4: pour i = 1,...,'+str(len(self.M)-1)+' et j = 1,...,'+str(len(self.M[0])-1)+'\n'
            for i in range(1,len(self.M)):
                for j in range(1,len(self.S)):
                    char+='  C['+str(i)+'][J'+str(self.S[j])+'] = max( C['+str(i-1)+'][J'+str(self.S[j])+'] , C['+str(i)+'][J'+str(self.S[j-1])+'] ) + P['+str(i)+'][J'+str(self.S[j])+'] = max('+str(self.O[i-1][j])+','+str(self.O[i][j-1])+')'+' '+str(self.M[i][self.S[j]])+' = '+str(max(self.O[i-1][j],self.O[i][j-1]))+'+'+str(self.M[i][self.S[j]])+' = '+str(max(self.O[i-1][j],self.O[i][j-1])+self.M[i][self.S[j]])+'\n'
                    self.O[i][j] = max(self.O[i-1][j],self.O[i][j-1])+self.M[i][self.S[j]]
                    self.F[i][j] = max(self.O[i-1][j],self.O[i][j-1])
            if self.TT == 1:
                char2=""
                char3="Tardiness T:\n"
                char+="\n"+'Total flow time TFT = '
                TFT,Tm,TT=0.0,[],0.0
                #TFT : total flow time
                #Tm :temps de retard d'un job "tardiness"
                #TT : total tardiness
                for j in range(len(self.M[0])):
                    char+= '  C['+str(len(self.M)-1)+'][J'+str(self.S[j])+']'
                    char2+= str(self.O[-1][j])
                    char3+= '  T[J'+str(self.S[j])+'] = '+'max( C['+str(len(self.M)-1)+'][J'+str(self.S[j])+'] - d[J'+str(self.S[j])+'] , 0 ) = '+'max( '+str(self.O[-1][j])+' - '+str(self.dj[self.S[j]])+' , 0 ) = '+str(max(self.O[-1][j]-self.dj[self.S[j]],0))+'\n'
                    if j!=len(self.M[0])-1:
                        char+=" + "
                        char2+=" + "
                    else:
                        char+=" = "
                        char2+=" = "
                    TFT+=self.O[-1][j]
                    Tm.append(max(self.O[-1][j]-self.dj[self.S[j]],0))
                char+="\n"+char2
                char+=str(TFT)+'\n'
                char3+= "Tardiness TT = ∑ T[S[j]] : j = 0,...,"+str(len(self.M[0])-1)+"\n  TT = "+str(sum(Tm))
                char+="\n"+char3
                TT=sum(Tm)
                # renvoi des dates des fins et des debuts de chaque job
                if self.do_report == 0:
                    return [self.O,self.F,TFT,Tm,TT]
                else:
                    return [self.O,self.F,TFT,Tm,TT,char]
            else:
                char2=""
                char+="\n"+'Total flow time TFT = '
                TFT=0.0
                for j in range(len(self.M[0])):
                    char+= 'C['+str(len(self.M)-1)+'][J'+str(self.S[j])+']'
                    char2+= str(self.O[-1][j])
                    if j!=len(self.M[0])-1:
                        char+=" + "
                        char2+=" + "
                    else:
                        char+=" = "
                        char2+=" = "
                    TFT+=self.O[-1][j]
                char+="\n"+char2
                char+=str(TFT)
                print(char)
                if self.do_report==0:
                    return [self.O,self.F,TFT]
                else:
                    return [self.O,self.F,TFT,char]
        # avec preparaion et sans blockage
        elif self.prep == 1 and self.block == 0:
            char = "Avec préparation et sans aucune condition \n"
            # initialisation
            for i in range(len(self.M)):
                self.O.append([0.0]*len(self.M[0]))
                self.F.append([0.0]*len(self.M[0]))
                self.OP.append([0.0]*len(self.M[0]))
                self.FP.append([0.0]*len(self.M[0]))
            # equation 1
            char+='équation 1: pour i = 0 et j = 0\n'
            char+='  C[0][J'+str(self.S[0])+'] = P[0][J'+str(self.S[0])+'] + M[0][J'+str(self.S[0])+'][J'+str(self.S[0])+'] = '+str(self.M[0][self.S[0]])+'+'+str(self.Mprep[0][self.S[0]][self.S[0]])+' = '+str(self.M[0][self.S[0]]+self.Mprep[0][self.S[0]][self.S[0]])+'\n'
            self.O[0][0] = self.M[0][self.S[0]]+self.Mprep[0][self.S[0]][self.S[0]]
            self.F[0][0] = self.Mprep[0][self.S[0]][self.S[0]]
            self.OP[0][0] = self.F[0][0]
            # equation 2
            char+='équation 2: pour i = 1,...,'+str(len(self.M)-1)+' et j = 0\n'
            for i in range(1,len(self.M)):         
                char+='  C['+str(i)+'][J'+str(self.S[0])+'] = max( C['+str(i-1)+'][J'+str(self.S[0])+'] , M['+str(i)+'][J'+str(self.S[0])+'][J'+str(self.S[0])+'] ) + P['+str(i)+'][J'+str(self.S[0])+'] = max( '+str(self.O[i-1][0])+' , '+str(self.Mprep[0][self.S[0]][self.S[0]])+') + '+str(self.M[i][self.S[0]])+' = '+str(max( self.O[i-1][0] , self.Mprep[i][self.S[0]][self.S[0]] )+self.M[i][self.S[0]])+'\n'
                self.O[i][0] = max( self.O[i-1][0] , self.Mprep[i][self.S[0]][self.S[0]] )+self.M[i][self.S[0]]
                self.F[i][0] = max( self.O[i-1][0] , self.Mprep[i][self.S[0]][self.S[0]] )
                self.OP[i][0] = self.Mprep[i][self.S[0]][self.S[0]]
            # equation 3
            char+='équation 3: pour i = 0 et j = 1,...,'+str(len(self.M[0])-1)+'\n'
            for j in range(1,len(self.S)):
                char+='  C[0][J'+str(self.S[j])+'] = C[0][J'+str(self.S[j-1])+'] + P[0][J'+str(self.S[j-1])+'] + M[0][J'+str(self.S[j-1])+'][J'+str(self.S[j])+'] = '+str(self.O[0][j-1])+'+'+str(self.M[0][self.S[j]])+'+'+str(self.Mprep[0][self.S[j-1]][self.S[j]])+' = '+str(self.O[0][j-1]+self.M[0][self.S[j]]+self.Mprep[0][self.S[j-1]][self.S[j]])+'\n'
                self.O[0][j] = self.O[0][j-1]+self.M[0][self.S[j]]+self.Mprep[0][self.S[j-1]][self.S[j]]
                self.F[0][j] = self.O[0][j-1]+self.Mprep[0][self.S[j-1]][self.S[j]]
                self.OP[0][j] = self.F[0][j]
                self.FP[0][j] = self.O[0][j-1]
            # equation 4
            char+='équation 4: pour i = 1,...,'+str(len(self.M)-1)+'j = 1,...,'+str(len(self.M[0])-1)+'\n'
            for i in range(1,len(self.M)):
                for j in range(1,len(self.S)):
                    char+='  C['+str(i)+'][J'+str(self.S[j])+'] = max( C['+str(i-1)+'][J'+str(self.S[j])+'] , C['+str(i)+'][J'+str(self.S[j-1])+'] + M['+str(i)+'][J'+str(self.S[j-1])+'][J'+str(self.S[j])+'] ) + P['+str(i)+'][J'+str(self.S[j])+'] = max( '+str(self.O[i-1][j])+' , '+str(self.O[i][j-1])+'+'+str(self.Mprep[i][self.S[j-1]][self.S[j]])+') + '+str(self.M[i][self.S[0]])+' = '+str(max(self.O[i-1][j],self.O[i][j-1]+self.Mprep[i][self.S[j-1]][self.S[j]])+self.M[i][self.S[j]])+'\n'
                    self.O[i][j] = max(self.O[i-1][j],self.O[i][j-1]+self.Mprep[i][self.S[j-1]][self.S[j]])+self.M[i][self.S[j]]
                    self.F[i][j] = max(self.O[i-1][j],self.O[i][j-1]+self.Mprep[i][self.S[j-1]][self.S[j]])
                    self.OP[i][j] = self.O[i][j-1]+self.Mprep[i][self.S[j-1]][self.S[j]]
                    self.FP[i][j]= self.O[i][j-1]
            if self.TT == 1:
                char2=""
                char3="Tardiness T:\n"
                char+="\n"+'Total flow time TFT = '
                TFT,Tm,TT=0.0,[],0.0
                #TFT : total flow time
                #Tm :temps de retard d'un job "tardiness"
                #TT : total tardiness
                for j in range(len(self.M[0])):
                    char+= '  C['+str(len(self.M)-1)+'][J'+str(self.S[j])+']'
                    char2+= str(self.O[-1][j])
                    char3+= '  T[J'+str(self.S[j])+'] = '+'max( C['+str(len(self.M)-1)+'][J'+str(self.S[j])+'] - d[J'+str(self.S[j])+'] , 0 ) = '+'max( '+str(self.O[-1][j])+' - '+str(self.dj[self.S[j]])+' , 0 ) = '+str(max(self.O[-1][j]-self.dj[self.S[j]],0))+'\n'
                    if j!=len(self.M[0])-1:
                        char+=" + "
                        char2+=" + "
                    else:
                        char+=" = "
                        char2+=" = "
                    TFT+=self.O[-1][j]
                    Tm.append(max(self.O[-1][j]-self.dj[self.S[j]],0))
                char+="\n"+char2
                char+=str(TFT)+'\n'
                char3+= "Tardiness TT = ∑ T[S[j]] : j = 0,...,"+str(len(self.M[0])-1)+"\n  TT = "+str(sum(Tm))
                char+="\n"+char3
                TT=sum(Tm)
                # renvoi des dates des fins et des debuts de chaque job et temp de preparation
                if self.do_report==0:
                    return [self.O,self.F,self.OP,self.FP,TFT,Tm,TT]
                else:
                    return [self.O,self.F,self.OP,self.FP,TFT,Tm,TT,char]
            else:
                char2=""
                char+="\n"+'Total flow time TFT = '
                TFT=0.0
                for j in range(len(self.M[0])):
                    char+= '  C['+str(len(self.M)-1)+'][J'+str(self.S[j])+']'
                    char2+= str(self.O[-1][j])
                    if j!=len(self.M[0])-1:
                        char+=" + "
                        char2+=" + "
                    else:
                        char+=" = "
                        char2+=" = "
                    TFT+=self.O[-1][j]
                char+="\n"+char2
                char+=str(TFT)
                print(char)
                if self.do_report==0:
                    return [self.O,self.F,self.OP,self.FP,TFT]
                else:
                    return [self.O,self.F,self.OP,self.FP,TFT,char]
        # sans preparation et avec blockage 
        elif self.prep == 0 and self.block == 1:
            # self.D est la matrice des fins des jobs avec leur blockage qui nous donne plusieur donnée 
            # initialisation et equation 1
            char = "Sans préparation et avec blocage \n on Ajout une machine vertuel pour calculer la matrice D\n indéxation des machines réeel de 1 à"+str(len(self.M))+'\n'
            self.D = np.array([[0.0]*len(self.M[0])]*(len(self.M)+1))
            char+='équation 1: pour i = 0 et j = 0\n'
            char+='  D[0][J'+str(self.S[0])+'] = 0\n'
            # equation 2
            char+='équation 2: pour i = 1,...,'+str(len(self.M)-1)+' et j = 0\n'
            for i in range(1,len(self.M)):
                char+='  D['+str(i)+'][J'+str(self.S[0])+'] = D['+str(i-1)+'][J'+str(self.S[0])+'] + P['+str(i-1)+'][J'+str(self.S[0])+'] = '+str(self.D[i-1][0])+' + '+str(self.M[i-1][self.S[0]])+' = '+str(self.D[i-1][0]+self.M[i-1][self.S[0]])+'\n'
                self.D[i][0]=self.D[i-1][0]+self.M[i-1][self.S[0]]
            # equation 5
            char+='équation 5: pour i = '+str(len(self.M)-1)+' et j = 0\n'
            char+='  D['+str(len(self.M))+'][J'+str(self.S[0])+'] = D['+str(len(self.M)-1)+'][J'+str(self.S[0])+'] + P['+str(len(self.M)-1)+'][J'+str(self.S[0])+'] = '+str(self.D[len(self.M)-1][0])+' + '+str(self.M[len(self.M)-1][self.S[0]])+' = '+str(self.D[len(self.M)-1][0]+self.M[len(self.M)-1][self.S[0]])+'\n'
            self.D[len(self.M)][0]=self.D[len(self.M)-1][0]+self.M[len(self.M)-1][self.S[0]]
            # equation 2,3,4
            for j in range(1,len(self.D[0])):
                for i in range(len(self.D)):
                    if i == 0:# equation 3
                        char+='équation 3: pour i = 0 et j = '+str(j)+'\n'
                        char+='  D[0][J'+str(self.S[j])+'] = D[1][J'+str(self.S[j-1])+'] = '+str(self.D[1][j-1])+'\n'
                        self.D[0][j]=self.D[1][j-1]
                    elif i!=0 and i!=len(self.M):# equation 4
                        char+='équation 4: pour i = '+str(i)+' et j = '+str(j)+'\n'
                        char+='  D['+str(i)+'][J'+str(self.S[j])+'] = max( D['+str(i-1)+'][J'+str(self.S[j])+'] + P['+str(i-1)+'][J'+str(max(self.D[i-1][j]+self.M[i-1][self.S[j]],self.D[i+1][j-1]))+'\n'
                        self.D[i][j]=max(self.D[i-1][j]+self.M[i-1][self.S[j]],self.D[i+1][j-1])
                    else:# equation 5
                        char+='équation 5: pour i = '+str(len(self.M)-1)+' et j = '+str(j)+'\n'
                        char+='  D['+str(i)+'][J'+str(self.S[j])+'] = D['+str(len(self.M)-1)+'][J'+str(self.S[j])+'] + P['+str(len(self.M)-1)+'][J'+str(self.S[j])+'] = '+str(self.D[len(self.M)-1][j])+' + '+str(self.M[len(self.M)-1][self.S[j]])+' = '+str(self.D[len(self.M)-1][j]+self.M[len(self.M)-1][self.S[j]])+'\n'
                        self.D[i][j]=self.D[len(self.M)-1][j]+self.M[len(self.M)-1][self.S[j]]
            self.F = np.array([[0.0]*len(self.M[0])]*len(self.M)) # dates de debuts des jobs 
            self.DN= np.array([[0.0]*len(self.M[0])]*len(self.M)) # nouveau matrice D
            self.TB= np.array([[0.0]*len(self.M[0])]*len(self.M)) # temps de blockage
            self.O = np.array([[0.0]*len(self.M[0])]*len(self.M)) # dates des fins des jobs 
            self.TBO = np.array([[0.0]*len(self.M[0])]*len(self.M)) # dates de fins des temps de blockage
            self.TBF = np.array([[0.0]*len(self.M[0])]*len(self.M)) # dates des debuts des temps de blockage
            # extraction des donnée depuis la matrice D
            char+='Calcul des temps de blocage\n'
            for i in range(len(self.D)-1):
                for j in range(len(self.D[0])):
                    char+='  TB['+str(i)+'][J'+str(self.S[j])+'] = D['+str(i+1)+'][J'+str(self.S[j])+'] - D['+str(i)+'][J'+str(self.S[j])+'] - P['+str(i)+'][J'+str(self.S[j])+'] = '+str(self.D[i+1][j])+' - '+str(self.D[i][j])+' - '+str(self.M[i][self.S[j]])+' = '+str(self.D[i+1][j]-self.D[i][j]-self.M[i][self.S[j]])+'\n'
                    self.F[i][j]=self.D[i][j]
                    self.DN[i][j]=self.D[i+1][j]
                    self.TB[i][j]=self.DN[i][j]-self.F[i][j]-self.M[i][self.S[j]]
                    self.O[i][j]=self.DN[i][j]-self.TB[i][j]
                    if self.TB[i][j]!=0:
                        self.TBO[i][j]=self.DN[i][j]
                        self.TBF[i][j]=self.O[i][j]
            if self.TT == 1:
                char2=""
                char3="Tardiness T:\n"
                char+="\n"+'Total flow time TFT = '
                TFT,Tm,TT=0.0,[],0.0
                #TFT : total flow time
                #Tm :temps de retard d'un job "tardiness"
                #TT : total tardiness
                for j in range(len(self.M[0])):
                    char+= '  D['+str(len(self.M))+'][J'+str(self.S[j])+']'
                    char2+= str(self.O[-1][j])
                    char3+= '  T[J'+str(self.S[j])+'] = '+'max( D['+str(len(self.M))+'][J'+str(self.S[j])+'] - d[J'+str(self.S[j])+'] , 0 ) = '+'max( '+str(self.D[-1][j])+' - '+str(self.dj[self.S[j]])+' , 0 ) = '+str(max(self.D[-1][j]-self.dj[self.S[j]],0))+'\n'
                    if j!=len(self.M[0])-1:
                        char+=" + "
                        char2+=" + "
                    else:
                        char+=" = "
                        char2+=" = "
                    TFT+=self.D[-1][j]
                    Tm.append(max(self.D[-1][j]-self.dj[self.S[j]],0))
                char+="\n"+char2
                char+=str(TFT)+'\n'
                char3+= "Tardiness TT = ∑ T[S[j]] : j = 0,...,"+str(len(self.M[0])-1)+"\n  TT = "+str(sum(Tm))
                char+="\n"+char3
                TT=sum(Tm)
                # renvoi des dates des fins et des debuts de chaque job et temp de blockage
                if self.do_report==0:
                    return [self.O,self.F,self.TBO,self.TBF,self.TB,TFT,Tm,TT]
                else:
                    return [self.O,self.F,self.TBO,self.TBF,self.TB,TFT,Tm,TT,self.D,char]
            else:
                char2=""
                char+="\n"+'Total flow time TFT = '
                TFT=0.0
                for j in range(len(self.M[0])):
                    char+= '  C['+str(len(self.M)-1)+'][J'+str(self.S[j])+']'
                    char2+= str(self.O[-1][j])
                    if j!=len(self.M[0])-1:
                        char+=" + "
                        char2+=" + "
                    else:
                        char+=" = "
                        char2+=" = "
                    TFT+=self.O[-1][j]
                char+="\n"+char2
                char+=str(TFT)
                if self.do_report==0:
                    return [self.O,self.F,self.TBO,self.TBF,self.TB,TFT]
                else:
                    return [self.O,self.F,self.TBO,self.TBF,self.TB,TFT,self.D,char]
        # avec preparaion et avec blockage
        elif self.prep == 1 and self.block == 1:
            return block_prep(self.M,list(self.S).copy(),self.Mprep,self.dj,self.TT,self.do_report) 
    # Méthode pour calculer les temps réels de fonctionnement TFR et d'arret TAR
    def TFR_TAR(self):
        TFR , TAR = [] , []
        #extraction de makspane
        Cmax = self.Cmax(self.S)
        # calcul de TFR/TAR pour le cas 1 -> preparation = arret
        for i in range(len(self.M)):
            tfr = 0 
            for j in range(len(self.M[0])):
                tfr += self.M[i][self.S[j]]
            cst = tfr/Cmax
            TFR.append(cst)
            TAR.append(1- cst)
        # calcul de TFR/TAR/TAP pour le cas 2 si on a de ppreparation -> preparation = travail
        if self.prep == 1:
            TFR_2 , TAR_2 , TAP = [] , [] , []
            for i in range(len(self.M)):
                tfr , tap = 0 , 0 
                for j in range(len(self.M[0])):
                    if j != 0:
                        tfr += self.M[i][self.S[j]]+self.Mprep[i][self.S[j-1]][self.S[j]]
                        tap += self.Mprep[i][self.S[j-1]][self.S[j]]
                    else:
                        tfr += self.M[i][self.S[j]]+self.Mprep[i][self.S[j]][self.S[j]]
                        tap += self.Mprep[i][self.S[j]][self.S[j]]
                cst = tfr/Cmax
                cst2 = tap/Cmax
                TFR_2.append(cst)
                TAR_2.append(1- cst)
                TAP.append(cst2)
            # si cas 2 renvoi tous les cas
            return [TFR,TAR,TFR_2,TAR_2,TAP]
        #si non renvoi le cas1
        return [TFR,TAR]
    # Méthode pour calculer les temps d'attente "utilusé dans les cas (0,1,0,0)/(1,1,0,0) "
    def TW(self):
        # TW :  temps d'attendre(time of waiting)
        # TWA :  temps d'attendre en arret (time of waiting arret)
        # TWA :  temps d'attendre en travail (time of waiting non arret)
        TW , TWA , TWNA = [] , [] , [[0.0]]
        traite = self.traite()  # donnée necessaire apres le traitement 
        # équation 0
        for i in range(len(self.M)-1):
            TW.append([])
            for j in range(len(self.M[0])):
                TW[i].append(traite[0][i+1][j]-self.M[i+1][self.S[j]]-traite[0][i][j])
        # équation 1
        for j in range(1,len(self.M[0])):
            TWNA[0].append(max(self.O[1][j-1]-self.O[0][j],0.0))
        # équation 2
        for i in range(1,len(self.M)-1):
            TWNA.append([])
            TWNA[i].append(self.F[i+1][0]-self.O[i][0])
        # équation 3
        for i in range(1,len(self.M)-1):
            TWNA.append([])
            for j in range(1,len(self.M[0])):
                TWNA[i].append(max(0.0,self.O[i+1][j-1]-self.O[i][j]))
        # équation 4
        TWNA.remove(TWNA[len(self.M)-1])
        for i in range(len(self.M)-1):
            TWA.append([])
            for j in range(len(self.M[0])):
                TWA[i].append(TW[i][j]-TWNA[i][j])
        return [TW,TWA,TWNA]
    # Méthode pour extracter le data frame pour tracer le Ganttchart
    def Gantt (self):
        global color_names       # liste des couleur utilusée sans préparaion ou avec noidel ou avec nowait
        global color_names_prep  # liste des couleur utilusée avec préparaion
        Matrix = self.traite()   # données traitées
        Cmax= Matrix[0][len(Matrix[0])-1][-1]
        # s'il y'a une erreur dans le traitement
        if type(Matrix)==str:
            return Matrix
        START , END , Machines , colors , texts= [] , [] , [] , [] , [] 
        # START : list des temps de débuts de chaque block soit temps de processus ou de preparaion ou de blocage
        # END : list des temps de fin de chaque block soit temps de processus ou de preparaion ou de blocage
        # Machines : list des labels de chaque machine
        # colors : list des couleur de chaque block soit temps de processus ou de preparaion ou de blocage
            # noir pour les temps de preparation / gris pour blocage / autres pour les temps de processus
        # text : labels de chaque block
            # Jj pour les jobs / TP pour les préparaion / TB pour les blocages
        Gantt = {'Machines' : None , 'Start' : None,'End' : None , 'Color' : None, 'Label': None }
        # Gantt : dictionnaire des données utilusée pour afficher le gaint
        for i in range(len(self.M)-1,-1,-1):  # remplissage des labels pour les machines 
            Machines.append("Machine "+str(i))
        # sans preparation et sans blockage ou nowait ou noidel
        if (self.prep == 0 and self.block == 0) or self.noidel==1 or self.nowait == 1:
            if len(Matrix[0][0])> len(color_names):
                color_names = color_names*((len(Matrix[0][0])//len(color_names))+1)
            for lst1,lst2,k in zip(Matrix[0],Matrix[1],range(len(self.M))):
                START.append([])
                END.append([])
                colors.append([])
                texts.append([])
                for e1,e2,c,i in zip(lst1,lst2,color_names,range(len(lst1))):
                    START[k].append([e2])
                    END[k].append([e1])
                    colors[k].append(c)
                    texts[k].append("J"+str(self.S[i]))
        # avec preparaion et sans blockage
        elif self.prep == 1 and self.block == 0:
            M1 , M2 = [] , []
            for lst1,lst2,lst3,lst4 in zip(Matrix[0],Matrix[1],Matrix[2],Matrix[3]):
                lst5 , lst6 = lst1+lst3 , lst2+lst4
                lst5.sort()
                lst6.sort()
                M1.append(lst5)
                M2.append(lst6)
            if len(M1[0])> len(color_names_prep):
                color_names_prep = color_names_prep*((len(Matrix[0][0])//len(color_names_prep))+1)
            for lst1,lst2,k in zip(M1,M2,range(len(M1))):
                START.append([])
                END.append([])
                colors.append([])
                texts.append([])
                for e1,e2,c,i in zip(lst1,lst2,color_names_prep,range(len(lst1))):
                    START[k].append([e2])
                    END[k].append([e1])
                    colors[k].append(c)
                    if i%2 == 1:
                        texts[k].append("J"+str(self.S[i//2]))
                    else:
                        texts[k].append("TP")
        # sans preparation et avec blockage 
        elif self.prep == 0 and self.block == 1:
            if len(Matrix[0][0])> len(color_names):
                color_names = color_names*((len(Matrix[0][0])//len(color_names))+1)
            for Jends,Jstarts,TBends,TBstarts,TBs,i in zip(Matrix[0],Matrix[1],Matrix[2],Matrix[3],Matrix[4],range(len(Matrix[0]))):
                START.append([])
                END.append([])
                colors.append([])
                texts.append([])
                for Jend,Jstart,TBend,TBstart in zip(Jends,Jstarts,TBends,TBstarts):
                    START[i].append([float(Jstart)])
                    END[i].append([float(Jend)])
                    if TBstart!=0:
                        START[i].append([float(TBstart)])
                        END[i].append([float(TBend)])
                START[i].sort()
                END[i].sort()
                index_color = 0
                colors[i].append(color_names[index_color])
                texts[i].append("J"+str(self.S[index_color]))
                index_color+=1
                for j in range(1,len(START[i])):
                    if START[i][j] in TBstarts:
                        colors[i].append('silver')
                        texts[i].append("TB")
                    else:
                        colors[i].append(color_names[index_color])
                        texts[i].append("J"+str(self.S[index_color]))
                        index_color+=1
        # avec preparaion et avec blockage            
        elif self.prep == 1 and self.block == 1:
            if len(Matrix[0][0])> len(color_names):
                color_names = color_names*((len(Matrix[0][0])//len(color_names))+1)
            for Jends,Jstarts,Pends,Pstarts,TBends,TBstarts,i in zip(Matrix[0],Matrix[1],Matrix[2],Matrix[3],Matrix[4],Matrix[5],range(len(Matrix[0]))):
                START.append([])
                END.append([])
                colors.append([])
                texts.append([])
                for Jend,Jstart,Pend,Pstart,TBend,TBstart,j in zip(Jends,Jstarts,Pends,Pstarts,TBends,TBstarts,range(len(Matrix[0][0]))):
                    START[i].append([float(Pstart)])
                    texts[i].append("TP")
                    colors[i].append("black")
                    START[i].append([float(Jstart)])
                    texts[i].append("J"+str(self.S[j]))
                    colors[i].append(color_names[j])
                    END[i].append([float(Pend)])
                    END[i].append([float(Jend)])
                    if TBstart!=0:
                        print("added")
                        START[i].append([float(TBstart)])
                        texts[i].append("TB")
                        colors[i].append('silver')
                        END[i].append([float(TBend)])
        START.reverse()
        END.reverse()
        texts.reverse()
        colors.reverse()
        Gantt['Machines'] = Machines
        Gantt['Start'] = START
        Gantt['End'] = END
        Gantt['Color'] = colors
        Gantt['Label'] = texts
        tasks_df = pd.DataFrame(Gantt)
        tasks_df = tasks_df.set_index('Machines')
        if self.sim==0:
            return tasks_df
        else:
            return [Gantt,self.M,self.S,Cmax]
    # Méthode pour extracter le Cmax
    def Cmax(self,Seq):
        self.S = Seq
        return max(self.traite()[0][len(self.M)-1])
    # Méthode pour extracter le Cmax et TT(total tardiness)
    def Cmax_TT(self,Seq):
        self.S = Seq
        donees = self.traite()    
        return [max(donees[0][len(self.M)-1]),donees[-1]] # retourner Cmax et TT
    # Méthode pour calculer les combinaisons possibles
    def combinations (self) :
        n = len(self.M[0])
        combinations = generate_combinations(n)
        Cmaxs = []
        if self.TT ==1:
            TTs = []
            for comb in combinations:
                cmax_tt = self.Cmax_TT(comb)
                Cmaxs.append(cmax_tt[0])
                TTs.append(cmax_tt[1])
            return [Cmaxs,combinations,TTs]
        else:
            for comb in combinations:
                Cmaxs.append(self.Cmax(comb))
            return [Cmaxs,combinations]
    # Méthode pour calculer les combinaisons où Cmax = min(Cmaxs)
    def choosed_combinations(self):
        lst = self.combinations()
        Cmaxs = np.array(lst[0])
        indexs = np.where(Cmaxs == min(Cmaxs))
        choosed = []
        for i in indexs[0]:
            choosed.append(lst[1][i])
        return [min(Cmaxs),choosed]
    # Méthode pour calculer les combinaisons où TT = min(TTs)
    def choosed_combinations_by_TT(self):
        lst = self.combinations()
        TTs = np.array(lst[2])
        indexs = np.where( TTs == min(TTs))
        choosed = []
        for i in indexs[0]:
            choosed.append(lst[1][i])
        return [min(TTs),choosed]
    # Méthode pour calculer les combinaisons où TT = min(TTs) et Cmax = min(Cmaxs)
    def choosed_combinations_by_TT_Cmax(self):
        lst = self.combinations()
        TTs = np.array(lst[2])
        Cmaxs = np.array(lst[0])
        indexs_tt = np.where( TTs == min(TTs))
        indexs_cmax = np.where(Cmaxs == min(Cmaxs))
        choosed_by_cmax = []
        choosed_by_tt = []
        for i in indexs_cmax[0]:
            choosed_by_cmax.append(lst[1][i])
        for i in indexs_tt[0]:
            choosed_by_tt.append(lst[1][i])
        choosed = []
        for comb in choosed_by_tt:
            if comb in choosed_by_tt:
                choosed.append(comb)
        if choosed!=[]:
            return [(min(TTs),min(Cmaxs)),choosed]
        else:
            return "il n'y a pas de séquence vérifiant min(TT) et min(Cmax)"
    # Méthode pour calculer la sequence optimale dans le cas de deux machines
    def Johnson(self): #(Algorithme de jonhson)
        if len(self.M) !=2 :
            print("Jonhson Algorithme ne fonctionne qu'avec deux machines")
            return None
        # etape 1 et 2
        jobs = list(range(len(self.M[0])))
        U,V = [],[]
        for j,t1,t2 in zip(jobs,self.M[0],self.M[1]):
            if t1 < t2:
                U.append(j)
            else:
                V.append(j)
        X,Y = U.copy(),V.copy()
        # etape 3
        SPT,LPT,M1,M2 = [],[],[],[]
        for j in U:
            M1.append(self.M[0][j])
        for j in V:
            M2.append(self.M[1][j])
        x = 0
        n= len (U)
        MA,MB = [],[]
        while 1:
            if len(SPT)==n:
                break
            if M1[x] == min(M1):
                SPT.append(U[x])
                MA.append(M1[x])
                M1.remove(M1[x])
                U.remove(U[x])
                x=0
            else:
                x+=1
        x = 0
        n= len (V)
        while 1:
            if len(LPT)==n:
                break
            if M2[x] == max(M2):
                LPT.append(V[x])
                MB.append(M2[x])
                M2.remove(M2[x])
                V.remove(V[x])
                x=0
            else:
                x+=1
        print(SPT,LPT)
        # etape 4
        A1=find_combinations(SPT, MA)
        A2=find_combinations(LPT, MB)
        RESULT =combine_lists(A1,A2)
        return [X,Y,SPT,LPT,RESULT]
    # Méthode pour calculer la sequence optimale dans le cas de plusieurs machines 
    def CDS(self,k): # (CAMPBELL, DUDEK et SMITH)
        if len(self.M) <= 2 :
            print("CDS ne fonctionne qu'avec plus de deux machines")
            return None
        if len(self.M) == 2 :
            print("on va applique Jonhson car il y'a deux machines ")
            return self.Johnson()
        Matrix = [[],[]]
        for j in range(len(self.M[0])):
            som = 0
            for i in range(k):
                som = som + self.M[i][j]
            Matrix[0].append(som)
        for j in range(len(self.M[0])):
            som = 0
            for i in range(len(self.M)-k,len(self.M)):
                som = som + self.M[i][j]
            Matrix[1].append(som)
        self.M = Matrix
        if self.do_report==0:
            return self.Johnson()
        else:
            return [self.Johnson(),Matrix]
# fonction qui traite les problemes flowshop avec condition de blocage avec les temps de préparation
def block_prep(P,S,TP,dj,T,report):
    #preparation des variables et equation 1 et 2 "adéquation des systèmes d'indexation"
    char = "Avec préparation et avec blocage \n on Ajout une machine vertuel et un job virtuel pour calculer la matrice D\n indéxation des machines réeel de 1 à "+str(len(P))+' ; et des jobs de 1 à '+str(len(P[0]))+'\n'
    char+='équation 1: pour i = 0,...,'+str(len(P))+' et j = 0\n'
    char+='  D[i][J0] = 0\n'
    for i in range(len(S)):
        S[i]=S[i]+1
    S = np.array(S) 
    S = np.hstack(([0], S))
    new_line = [0.0]*len(P[0])
    P = np.vstack((new_line, P))
    new_column = [[0.0]]*len(P)
    P = np.hstack((new_column,P)) 
    D = np.array([[0.0]*(len(P[0]+1))]*(len(P)))
    #equation 2 3 et 4
    for j in range(1,len(D[0])):
        for i in range(len(D)):
            if i == 0:
                # équation 2 et 3
                if j == 1:
                   char+='équation 2: pour i = 0 et j = 1\n'
                   char+='  D[0][J'+str(S[j])+'] = D[1][J0] + M[1][J'+str(S[1])+'][J'+str(S[1])+'] = '+str(D[1][j-1])+' + '+str(TP[0][S[1]-1][S[1]-1] )+' = '+str(D[1][j-1] + TP[0][S[1]-1][S[1]-1] )+'\n'
                   D[0][j] = D[1][j-1] + TP[0][S[1]-1][S[1]-1] 
                else:
                    char+='équation 3: pour i = 0 et j = '+str(j)+'\n'
                    char+='  D[0][J'+str(S[j])+'] = D[1][J'+str(S[j-1])+'] + M[1][J'+str(S[j-1])+'][J'+str(S[j])+'] = '+str(D[1][j-1])+' + '+str(TP[0][S[j-1]-1][S[j]-1])+' = '+str(D[1][j-1] + TP[0][S[j-1]-1][S[j]-1])+'\n'
                    D[0][j] = D[1][j-1] + TP[0][S[j-1]-1][S[j]-1]
            elif i == len(D)-1:
                # équation 6
                char+='équation 6: pour i = '+str(len(D)-1)+' et j = '+str(j)+'\n'
                char+='  D['+str(len(D)-1)+'][J'+str(S[j])+'] = D['+str(len(D)-2)+'][J'+str(S[j])+'] + P['+str(len(P)-1)+'][J'+str(S[j])+'] = '+str(D[-2][j])+' + '+str(P[-1][S[j]])+' = '+str(D[-2][j] + P[-1][S[j]])+'\n'
                D[-1][j] = D[-2][j] + P[-1][S[j]]
            else:
                # équation 4
                if j == 1:
                    char+='équation 4: pour i = '+str(i)+' et j = 1\n'
                    char+='  D['+str(i)+'][J'+str(S[j])+'] = max( D['+str(i-1)+'][J'+str(S[j])+'] + P['+str(i)+'][J'+str(S[j])+'] , D['+str(i+1)+'][J0] + M['+str(i)+'][J'+str(S[j])+'][J'+str(S[j])+'] ) = max( '+str(D[i-1][1])+' + '+str(P[i][S[1]])+' , ' + str(D[i+1][0])+' + '+str(TP[i][S[1]-1][S[1]-1])+' ) = '+str(max(D[i-1][1] + P[i][S[1]] , D[i+1][0] + TP[i][S[1]-1][S[1]-1]))+'\n'
                    D[i][1] = max(D[i-1][1] + P[i][S[1]] , D[i+1][0] + TP[i][S[1]-1][S[1]-1])
                # équation 5
                else:
                    char+='équation 5: pour i = '+str(i)+' et j = '+str(j)+'\n'
                    char+='  D['+str(i)+'][J'+str(S[j])+'] = max( D['+str(i-1)+'][J'+str(S[j])+'] + P['+str(i)+'][J'+str(S[j])+'] , D['+str(i+1)+']['+str(S[j-1])+'] + M['+str(i)+']['+str(S[j-1])+']['+str(S[j])+'] ) = max( '+str(D[i-1][j])+' + '+str(P[i][S[j]])+' , ' + str(D[i+1][j-1])+' + '+str(TP[i][S[j-1]-1][S[j]-1])+' ) = '+str(max(D[i-1][j] + P[i][S[j]] , D[i+1][j-1] + TP[i][S[j-1]-1][S[j]-1]))
                    D[i][j] = max(D[i-1][j] + P[i][S[j]] , D[i+1][j-1] + TP[i][S[j-1]-1][S[j]-1])
    O,F,OP,FP,OB,FB,OOB,TB = [],[],[],[],[],[],[],[]
    # O: dates des fins des jobs (out of job)
    # F: dates des debuts des jobs (first of job)
    # OP : dates des fins des temps de préparation (out of preparation time)
    # FP : dates des debuts des temps de préparation (firt of preparation time)
    # FB : dates des debuts des temps de blocage (first of blocing time)
    # OB : dates des find des temps de blocage (first of job blocking time)
    # OOB : partie supérieur à droite de D
    # TB : temps de blocage (blocking time) 
    #préparation pour le calcul
    for i in range(len(D)):
        Flst,FPlst,OOBlst=[],[],[]
        for j in range(len(D[0])):
            if i != 0 and j != len(D[0])-1:
                FPlst.append(D[i][j])
            if i != len(D)-1 and j != 0:
                Flst.append(D[i][j])
            if i !=0 and j !=0:
                OOBlst.append(D[i][j])
        if i != 0 :
            FP.append(FPlst)
            OOB.append(OOBlst)
        if i != len(D)-1:
            F.append(Flst)
    # calcul des matrices nécessaire pour tracer le gaint
    char+= ' Indexation normale pour TB et C\n'
    charTB='Calcul des temps de blocage\n'
    charC='Calcul de la matrice C\n'
    for i in range(len(F)):
        O.append([])
        OP.append([])
        TB.append([])
        OB.append([])
        FB.append([])
        for j in range(len(F[0])): 
            O[i].append(F[i][j]+P[i+1][S[j+1]])
            charC+='  C['+str(i)+'][J'+str(S[j+1]-1)+'] = D['+str(i+1)+'][J'+str(S[j])+'] + P['+str(i)+'][J'+str(S[j+1]-1)+'] = '+str(F[i][j])+' + '+str(P[i+1][S[j+1]])+' = '+str(F[i][j]+P[i+1][S[j+1]])+'\n'
            if j == 0:
                OP[i].append(FP[i][0]+TP[i][S[1]-1][S[1]-1])
            else:
                OP[i].append(FP[i][j]+TP[i][S[j]-1][S[j+1]-1])
            TB[i].append(OOB[i][j]-O[i][j])
            charTB+='  TB['+str(i)+'][J'+str(S[j+1]-1)+'] = D['+str(i+1)+'][J'+str(S[j])+'] - C['+str(i)+'][J'+str(S[j+1]-1)+'] = '+str(OOB[i][j])+' - '+str(O[i][j])+' = '+str(OOB[i][j]-O[i][j])+'\n'
            if TB[i][j] == 0:
                OB[i].append(0.0)
                FB[i].append(0.0)
            else:
                FB[i].append(O[i][j])
                if j != len(F[0])-1:
                    OB[i].append(FP[i][j+1]) 
                else:
                    OB[i].append(O[i][j]+TB[i][j]) 
    char+=charC
    char+=charTB
    TBP,TBB,TBF = [],[],[]
    # TBB : temps de bolocage à cause d'un autre blocage 
    # TBP : temps de bolocage à cause de préparation
    # TBF : temps de blocage à cause de travail
    # calcul des temps de blocage
    for i in range(len(O)-1):
        TBP.append([])
        TBB.append([0.0])
        TBF.append([0.0])
        if TB[i][0] != 0:
            TBP[i].append(TB[i][0]) 
        else:
            TBP[i].append(0.0) 
    for i in range(len(O)-1):
        for j in range(1,len(O[0])):
            if TB[i][j] != 0:
                if F[i+1][j]-FP[i+1][j] >= TB[i][j]:
                    TBP[i].append(TB[i][j])
                    TBF[i].append(0.0)
                    TBB[i].append(0.0)
                else:
                    TBP[i].append(TP[i+1][S[j]-1][S[j+1]-1])
                    TBF[i].append(O[i+1][j-1] - O[i][j])
                    if TB[i+1][j-1] != 0:
                        TBB[i].append(TB[i+1][j-1])
                    else:
                        TBB[i].append(0.0)
            else:
                TBP[i].append(0.0)
                TBB[i].append(0.0)
                TBF[i].append(0.0)
    if T==1:
        char2=""
        char3="Tardiness T:\n"
        char+="\n"+'Total flow time TFT = '
        TFT,Tm,TT=0.0,[],0.0
        #TFT : total flow time
        #Tm :temps de retard d'un job "tardiness"
        #TT : total tardiness
        for j in range(len(P[0])):
            char+= 'D['+str(len(P))+'][J'+str(S[j])+']'
            char2+= str(D[-1][j])
            char3+= '  T[J'+str(S[j])+'] = '+'max( D['+str(len(P))+'][J'+str(S[j])+'] - d[J'+str(S[j]-1)+'] , 0 ) = '+'max( '+str(D[-1][j])+' - '+str(dj[S[j]-1])+' , 0 ) = '+str(max(D[-1][j]-dj[S[j]-1],0))+'\n'
            if j!=len(P[0])-1:
                char+=" + "
                char2+=" + "
            else:
                char+=" = "
                char2+=" = "
            TFT+=D[-1][j]
            if j!=0:
                Tm.append(max(D[-1][j]-dj[S[j]-1],0))
        char+="\n"+char2
        char+=str(TFT)+'\n'
        char3+= "Tardiness TT = ∑ T[S[j]] : j = 0,...,"+str(len(P[0])-1)+"\n  TT = "+str(sum(Tm))
        char+="\n"+char3
        TT=sum(Tm)
        if report==0:
            return [O,F,OP,FP,OB,FB,TB,TBF,TBB,TBP,TFT,Tm,TT]
        else:
            return [O,F,OP,FP,OB,FB,TB,TBF,TBB,TBP,TFT,Tm,TT,D,char]
    else:
        char2=""
        char+="\n"+'Total flow time TFT = '
        TFT=0.0
        for j in range(len(P[0])):
            char+= '  C['+str(len(P)-1)+'][J'+str(S[j]-1)+']'
            char2+= str(O[-1][j])
            if j!=len(P[0])-1:
                char+=" + "
                char2+=" + "
            else:
                char+=" = "
                char2+=" = "
            TFT+=D[-1][j]
        char+="\n"+char2
        char+=str(TFT)
        if report==0:
            return [O,F,OP,FP,OB,FB,TB,TBF,TBB,TBP,TFT]
        else:
            return [O,F,OP,FP,OB,FB,TB,TBF,TBB,TBP,TFT,D,char]
# fonction qui traite les problemes flowshop avec condition de non arret 
def noidel_probleme_solving(P,S,dj,T,report):
    L,C,F,TW=[0.0],[],[],[] 
    char = 'Sans préparation et dans arrets\n'
    # L list des temps mort dans chaque machine et équation 1
    # C matrice des temps de fin de chaque job
    # F matrice des temps des début de chaque job
    # TW matrice des temps d'attete de chaque job entre machine i et i+1 
    n,m=len(P[0]),len(P) 
    # n est le nombre total des jobs et m et le nombre total des machines
    # application des formules mathématique
    char+='équation 1 : pour i = 0 : \n L[0] = 0\n'
    for i in range(m): 
        C.append([])
        F.append([])
        # équation 2
        if i!=0:
            char+='équation 2: pour i='+str(i)+'\n'
            charmaxs="max( "
            charmaxsnum="max( "
            maxs = []
            for k in range(n):
                char+='  maxs['+str(k)+'] =  '
                mx1,mx2 = 0,0
                sum1,sum11,sum2,sum22='','','',''
                for j in range(n-k):
                    sum1+='P['+str(i-1)+'][J'+str(S[j])+']'
                    sum11+=str(P[i-1][S[j]])
                    mx1+=P[i-1][S[j]]
                    if j != n-k-1:
                        sum1+= ' + '
                        sum11+= ' + ' 
                for j in range(n-k-1):
                    sum2+='P['+str(i)+'][J'+str(S[j])+']'
                    sum22+=str(P[i][S[j]])
                    mx2+=P[i][S[j]]
                    if j != n-k-2:
                        sum2+= ' - '
                        sum22+= ' - ' 
                char+=sum1+' - '+sum2+ ' = '+sum11+' - '+sum22+' = '+str(mx1-mx2)+'\n'
                charmaxs+='maxs['+str(k)+']'
                charmaxsnum+=str(mx1-mx2)
                if k != n-1:
                    charmaxs+= ' , '
                    charmaxsnum+= ' , '
                maxs.append(mx1-mx2)
            char+='  L['+str(i)+'] = L['+str(i-1)+'] + '+charmaxs+' ) = '+str(L[i-1])+' + '+charmaxsnum+' ) = '+str(L[i-1])+' + '+str(max(maxs))+' = '+str(L[i-1]+max(maxs))+'\n'
            L.append(L[i-1]+max(maxs))
        char+='équation 3 et 4 : pour i = '+str(i)+' et j = 0,...,'+str(n-1)+': \n'
        for j in range(n):
            # équation 3
            if j==0:
                char+='  C['+str(i)+'][J'+str(S[j])+'] = L['+str(i)+'] + P['+str(i)+'][J'+str(S[j])+'] = '+str(L[i])+' + '+str(P[i][S[j]])+' = '+str(L[i]+P[i][S[j]])+'\n'
                C[i].append(L[i]+P[i][S[j]])
                F[i].append(L[i])
            # équation 4
            else:
                char+='  C['+str(i)+'][J'+str(S[j])+'] = C['+str(i)+'][J'+str(S[j-1])+'] + P['+str(i)+'][J'+str(S[j])+'] = '+str(C[i][j-1])+' + '+str(P[i][S[j]])+' = '+str(C[i][j-1]+P[i][S[j]])+'\n'
                C[i].append(C[i][j-1]+P[i][S[j]])
                F[i].append(C[i][j-1])
    # calcul des temps d'attendre de chaque job de la machine i à i+1
    char+="Calcul des temps d'attendre :\n"
    for i in range(m-1):
        TW.append([])
        for j in range(n):
            char+='  TA['+str(i)+'/'+str(i+1)+'][J'+str(S[j])+'] = C['+str(i+1)+'][J'+str(S[j])+'] - P['+str(i+1)+'][J'+str(S[j])+'] - C[i][J'+str(S[j])+'] = '+str(C[i+1][j])+' - '+str(P[i+1][j])+' - '+str(C[i][j])+' = '+str(F[i+1][j]-C[i][j])+'\n'
            TW[i].append(F[i+1][j]-C[i][j])
    if T==1:
        char2=""
        char3="Tardiness T:\n"
        char+="\n"+'Total flow time TFT = '
        TFT,Tm,TT=0.0,[],0.0
        #TFT : total flow time
        #Tm :temps de retard d'un job "tardiness"
        #TT : total tardiness
        for j in range(n):
            char+= '  C['+str(m-1)+'][J'+str(S[j])+']'
            char2+= str(C[-1][j])
            char3+= '  T[J'+str(S[j])+'] = '+'max( C['+str(m-1)+'][J'+str(S[j])+'] - d[J'+str(S[j])+'] , 0 ) = '+'max( '+str(C[-1][j])+' - '+str(dj[S[j]])+' , 0 ) = '+str(max(C[-1][j]-dj[S[j]],0))+'\n'
            if j!=n-1:
                char+=" + "
                char2+=" + "
            else:
                char+=" = "
                char2+=" = "
            TFT+=C[-1][j]
            Tm.append(max(C[-1][j]-dj[S[j]],0))
        char+="\n"+char2
        char+=str(TFT)+'\n'
        char3+= "Tardiness TT = ∑ T[S[j]] : j = 0,...,"+str(n-1)+"\n  TT = "+str(sum(Tm))
        char+="\n"+char3
        TT=sum(Tm)
        if report==0:
            return [C,F,TW,TFT,Tm,TT]
        else:
            return [C,F,TW,TFT,Tm,TT,char]
    else:
        char2=""
        char+="\n"+'Total flow time TFT = '
        TFT=0.0
        for j in range(n):
            char+= '  C['+str(m-1)+'][J'+str(S[j])+']'
            char2+= str(C[-1][j])
            if j!=n-1:
                char+=" + "
                char2+=" + "
            else:
                char+=" = "
                char2+=" = "
            TFT+=C[-1][j]
        char+="\n"+char2
        char+=str(TFT)
        if report==0:
            return [C,F,TW,TFT]
        else:
            return [C,F,TW,TFT,char]
# fonction qui traite les problemes flowshop avec condition de non attendre
def nowait_probleme_solving(P,S,dj,T,report):
    char = 'Sans préparation et dans attendre\n'
    n,m=len(P[0]),len(P) # n est le nombre total des jobs et m et le nombre total des machines
    D = np.array([[0.0]*n]*n) # matrice des delais entre deux jobs j1 et j2
    C = [] # C matrice des temps de fin de chaque job "au début elle est seulement la derniere ligne"
    # équation 1 : calcul de la matrice des delais
    char+='équation 1 : Calcul de la matrice des délais D entre chaque deux job tel que j1 = 0,...,'+str(n-1)+' j2 = 0,...,'+str(n-1)+' :\n'
    for j1 in range(n):
        for j2 in range(n):
            mxs = []
            for r in range(m):
                char+='  maxs['+str(r)+'] = '
                mx1,mx2=0,0
                mx1char,mx2char='',''
                mx1charnum,mx2charnum='',''
                for k in range(1,r+1):
                    mx1char+='P['+str(k)+'][J'+str(j1)+']'
                    mx1charnum+=str(P[k][j1])
                    if k != r:
                        mx1char+=' + '
                        mx1charnum+=' + '
                    mx1+=P[k][j1]
                for k in range(r):
                    mx2char+='P['+str(k)+'][J'+str(j2)+']'
                    mx2charnum+=str(P[k][j2])
                    if k != r-1:
                        mx2char+=' - '
                        mx2charnum+=' - '
                    mx2+=P[k][j2]
                if mx1char=='':
                    mx1char='0'
                if mx2char=='':
                    mx2char='0'
                if mx1charnum=='':
                    mx1charnum='0'
                if mx2charnum=='':
                    mx2charnum='0'
                if mx1char==mx1charnum and mx2char==mx2charnum:
                    char+=mx1charnum+' - '+mx2charnum+" = "+str(mx1-mx2)+'\n'
                elif str(mx1)==mx1charnum and str(mx2)==mx2charnum :
                    char+=mx1char+' - '+mx2char+" = "+mx1charnum+' - '+mx2charnum+" = "+str(mx1-mx2)+'\n'
                else:
                    char+=mx1char+' - '+mx2char+" = "+mx1charnum+' - '+mx2charnum+" = "+str(mx1)+' - '+str(mx2)+' = '+str(mx1-mx2)+'\n'
                mxs.append(mx1-mx2)
            char+='  maxs = '+str(mxs)+'\n'
            char+='  D[J'+str(j1)+'][J'+str(j2)+'] = P[0][J'+str(j1)+'] + max(max(maxs),0)'+' = '+str(P[0][j1])+' + '+str(max(max(mxs),0))+' = '+str(P[0][j1] + max(max(mxs),0))+'\n'
            D[j1][j2] = P[0][j1] + max(max(mxs),0)
    # équation 2 : calcul des temps de fins et de début de chaque job dans la dernière machine
    char+='équation 2 : Calcul de la dernière ligne de la matrice C pour i = '+str(m-1)+' et j = 0,...,'+str(n-1)+' :\n'
    for j in range(n):
        v1,v2=0,0
        v1char,v2char="",""
        v1charnum,v2charnum="",""
        for k in range(1,j+1):
            v1char+='D[J'+str(S[k-1])+'][J'+str(S[k])+']'
            v1charnum+=str(D[S[k-1]][S[k]])
            if k!=j:
                v1char+=' + '
                v1charnum+=' + '
            v1+=D[S[k-1]][S[k]]
        for k in range(m):
            v2char+='P['+str(k)+'][J'+str(S[j])+']'
            v2charnum+=str(P[k][S[j]])
            if k!=m-1:
                v2char+=' + '
                v2charnum+=' + '
            v2+=P[k][S[j]]
        if v1char=='':
            char+='C['+str(m-1)+'][J'+str(S[j])+'] = '+v2char+' = '+v2charnum+' = '+str(v2)+" = "+str(v1+v2)+'\n'
        elif v2char=='':
            char+='C['+str(m-1)+'][J'+str(S[j])+'] = '+v1char+' = '+v1charnum+' = '+str(v1)+" = "+str(v1+v2)+'\n'
        else:
            char+='C['+str(m-1)+'][J'+str(S[j])+'] = '+v1char+' + '+v2char+' = '+v1charnum+' + '+v2charnum+' = '+str(v1)+' + '+str(v2)+" = "+str(v1+v2)+'\n'
        C.append(v1+v2)
    C=np.array([[0.0]*n]*(m-1)+[C]) # C devien une matrice
    F=np.array([[0.0]*n]*(m))  # F matrice des temps des début de chaque job
    char+='équation 3 : Calcul de la matrice C pour i = '+str(m-2)+',...,0 et j = 0,...,'+str(n-1)+' :\n'
    for i in range(m-1,-1,-1):
        for j in range(n):
            if i!=m-1:
                char+='C['+str(i)+'][J'+str(S[j])+'] = C['+str(i+1)+'][J'+str(S[j])+'] - P['+str(i+1)+'][J'+str(S[j])+'] = '+str(C[i+1][j])+' - '+str(P[i+1][S[j]])+' = '+str(C[i+1][j]-P[i+1][S[j]])+'\n'
                C[i][j]=C[i+1][j]-P[i+1][S[j]]
            F[i][j] = C[i][j] - P[i][S[j]]
    TW=np.array([[0.0]*(n-1)]*(m)) 
    # TW : matrice des temps d'attente entre deux jobs successif dans chaque machine
    for i in range(m):
        for j in range(n-1):
            TW[i][j] = F[i][j+1]-C[i][j]
    if T ==1:
        char2=""
        char3="Tardiness T:\n"
        char+="\n"+'Total flow time TFT = '
        TFT,Tm,TT=0.0,[],0.0
        #TFT : total flow time
        #Tm :temps de retard d'un job "tardiness"
        #TT : total tardiness
        for j in range(n):
            char+= '  C['+str(m-1)+'][J'+str(S[j])+']'
            char2+= str(C[-1][j])
            char3+= '  T[J'+str(S[j])+'] = '+'max( C['+str(m-1)+'][J'+str(S[j])+'] - d[J'+str(S[j])+'] , 0 ) = '+'max( '+str(C[-1][j])+' - '+str(dj[S[j]])+' , 0 ) = '+str(max(C[-1][j]-dj[S[j]],0))+'\n'
            if j!=n-1:
                char+=" + "
                char2+=" + "
            else:
                char+=" = "
                char2+=" = "
            TFT+=C[-1][j]
            Tm.append(max(C[-1][j]-dj[S[j]],0))
        char+="\n"+char2
        char+=str(TFT)+'\n'
        char3+= "Tardiness TT = ∑ T[S[j]] : j = 0,...,"+str(n-1)+"\n  TT = "+str(sum(Tm))
        char+="\n"+char3
        TT=sum(Tm)
        if report ==0:
            return [C,F,TW,TFT,Tm,TT]
        else:
            return [C,F,TW,TFT,Tm,TT,char]
    else:
        char2=""
        char+="\n"+'Total flow time TFT = '
        TFT=0.0
        for j in range(n):
            char+= '  C['+str(m-1)+'][J'+str(S[j])+']'
            char2+= str(C[-1][j])
            if j!=n-1:
                char+=" + "
                char2+=" + "
            else:
                char+=" = "
                char2+=" = "
            TFT+=C[-1][j]
        char+="\n"+char2
        char+=str(TFT)

        if report==0:
            return [C,F,TW,TFT]
        else:
            return [C,F,TW,TFT,char]


