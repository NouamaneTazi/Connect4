from player import Player
from board import Board
import copy
import random as rd
import math
import logging
import numpy as np

# def seqfinder(seq,list):
#     seq=map(str,seq)
#     for i in range(len(list)):
#         list=copy.deepcopy(list)
#         if list[i]==-1:
#             list[i]=2
#     list=map(str,list)
#     return ','.join(seq) in ','.join(list)
def seqfinder(seq,list):
    for j in range(len(list)-3):
        if list[j:j+4]==seq:
            return True
    return False
def seqfinder2(seq,list,index,etat):
    for j in range(len(list)-4):
        if list[j:j+5]==seq:
            if index>0:
                before_l=etat.getRow(index-1)
                if before_l[j]==0 or before_l[j+4]==0:
                    continue
            return True
    return False
def seqfinder3(seq,list,index,etat,bool):
    for j in range(len(list)-4):
        if list[j:j+5]==seq:
            if bool==False: #descendant
                before_l=etat.getDiagonal(bool,index-1).copy()
                if index>5: # before_l et l ne commencent pas du meme indice
                    before_l.pop(0)
                if before_l[j]==0 and len(before_l)>j+4 and before_l[j+4]==0:
                    continue
            else:
                before_l=etat.getDiagonal(bool,index+1).copy()
                if index>=0:
                    before_l.insert(0,0)
                if before_l[j+4]==0 and j>0 and before_l[j]==0:
                    continue
            return True
    return False
def evalue(num_j,etat,inf=False):
    ind=0
    logging.error(etat)
    for i in range(6):
        l=etat.getRow(i)
        #logging.error(l)
        for j in range(7):
            if l[j]==-num_j: ind-=Tab[i,j]
            elif l[j]==num_j: ind+=Tab[i,j]
        if seqfinder2([0,num_j,num_j,num_j,0],l,i,etat):
            ind += 9999999999
        if seqfinder([num_j,num_j,num_j,num_j],l):
            logging.error("1 hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            if inf:
                return math.inf
            else: return 999999999999999999999999
        elif seqfinder([-num_j,-num_j,-num_j,-num_j],l) or seqfinder2([0,-num_j,-num_j,-num_j,0],l,i,etat):
            logging.error("1 nooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            if inf:
                return -math.inf
            else: return -999999999999999999999999
    for j in range(7):
        c=etat.getCol(j)
        if seqfinder([num_j,num_j,num_j,num_j],c):
            logging.error("2 hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            if inf:
                return math.inf
            else: return 999999999999999999999999
        elif seqfinder([-num_j,-num_j,-num_j,-num_j],c):
            logging.error("2 noooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            if inf:
                return -math.inf
            else: return -999999999999999999999999
    for j in range(3,9):
        ldown=etat.getDiagonal(False,j)
        if seqfinder3([0,num_j,num_j,num_j,0],ldown,j,etat,False):
            ind += 9999999999
        if seqfinder([num_j,num_j,num_j,num_j],ldown):
            logging.error("3 hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            if inf:
                return math.inf
            else: return 999999999999999999999999
        elif seqfinder([-num_j,-num_j,-num_j,-num_j],ldown)or seqfinder3([0,-num_j,-num_j,-num_j,0],ldown,j,etat,False):
            logging.error("3 nooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            if inf:
                return -math.inf
            else: return -999999999999999999999999
    for j in range(-2,4):
        lup=etat.getDiagonal(True,j)
        if seqfinder3([0,num_j,num_j,num_j,0],lup,j,etat,True):
            ind += 9999999999
        if seqfinder([num_j,num_j,num_j,num_j],lup):
            logging.error("4 hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            if inf:
                return math.inf
            else: return 999999999999999999999999
        elif seqfinder([-num_j,-num_j,-num_j,-num_j],lup)or seqfinder3([0,-num_j,-num_j,-num_j,0],lup,j,etat,True):
            logging.error("4 nooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            ind= -math.inf
    logging.error("ind= "+str(ind))
    return ind
def successeur(num_joueur,etat):
    l=[]
    for col in etat.getPossibleColumns(): # returns [0,1,3,4]
        copie_etat=copy.deepcopy(etat)
        copie_etat.play(num_joueur,col)
        l.append((copie_etat,col))
    return l
def num_tour(etat):
    global numtour
    #logging.error(sum([etat.getHeight(i) for i in range(7)]))
    return sum([etat.getHeight(i) for i in range(7)]) - numtour

def Estfeuille(num_joueur,etat):
    return etat.getPossibleColumns()==[]

flag=False
def MaxValue(etat,alpha,beta):
    global flag , profondeur, num_joueur
    if flag==False:
        flag=True
        for copie_etat,c in successeur(num_joueur,etat):
            logging.error("###############################################")
            logging.error("   Si IA joue à "+str(c))
            candidat=MinValue(copie_etat,alpha,beta)
            logging.error("candidat="+str(candidat))
            if candidat>alpha:
                # logging.error("MaxValue: candidat>alpha donc alpha="+str(candidat))
                alpha=candidat
                col=c
            if alpha>=beta:
                logging.error("col "+str(col))
                return col #retourne nimporte tant que cette sous arbre ne sera pas prise
        logging.error("alpha="+str(alpha))
        logging.error("col "+str(col))
        return col
    else:
        # logging.error("MaxValue debut: ]"+str(alpha)+" , "+str(beta)+"[")
        #logging.error("MaxValue num_tour: "+str(num_tour(etat)))
        if num_tour(etat) > profondeur:
            x=evalue(num_joueur,etat)
            return x
        eval=evalue(num_joueur,etat,True)
        if eval==math.inf:
            logging.error("GAGNé")
            return math.inf
        if eval==-math.inf:
            logging.error("PERDU")
            return -math.inf
        if Estfeuille(num_joueur,etat) :
            return eval

        for copie_etat,c in successeur(num_joueur,etat):
            logging.error("         Si IA joue à "+str(c))
            alpha0=alpha
            alpha=max(alpha,MinValue(copie_etat,alpha,beta))
            # if alpha!=alpha0: logging.error(str(alpha)+">alpha0 donc alpha0= "+str(alpha))
            # else: logging.error("MaxValue: "+str(alpha)+"=alpha n'a pas changé")
            if beta<=alpha:
                # logging.error("MaxValue: "+str(beta)+"<="+str(alpha)+" alors je retourne "+str(alpha))
                return alpha
        # logging.error("MaxValue alpha = "+str(alpha))
        return alpha
def MinValue(etat,alpha,beta):
    global profondeur, num_joueur
    #logging.error("MinValue num_tour: "+str(num_tour(etat)))
    if num_tour(etat) > profondeur:
        logging.error("ON DOIT PAS ETRE LA")
        x=evalue(num_joueur,etat)
        # logging.error("MinValue evalue donne: "+str(x))
        return x
    if num_tour(etat)==profondeur-2:
        eval=evalue(num_joueur,etat,inf=True)
        if eval==math.inf:
            logging.error("GAGNé")
            return math.inf
        if eval==-math.inf:
            logging.error("PERDU")
            return -math.inf
        if Estfeuille(num_joueur,etat) :
            return eval
    if num_tour(etat)==profondeur:
        eval=evalue(num_joueur,etat,inf=False)
        if eval==math.inf:
            logging.error("GAGNé")
            return math.inf
        if eval==-math.inf:
            logging.error("PERDU")
            return -math.inf
        if Estfeuille(num_joueur,etat) :
            return eval
    logging.error("MinValue debut: ]"+str(alpha)+" , "+str(beta)+"[")
    for copie_etat,c in successeur(-num_joueur,etat):
        if num_tour(etat)==profondeur-2: logging.error("     Si joueur joue à "+str(c))
        if num_tour(etat)==profondeur: logging.error("              Si joueur joue à "+str(c))
        x=MaxValue(copie_etat,alpha,beta)
        # if x<=beta: logging.error("beta a changé de "+str(beta)+" a "+str(x))
        # else: logging.error("MinValue: beta="+ str(beta)+" n'a pas changé")
        beta=min(beta,x)
        if beta<=alpha:
            logging.error("MinValue: "+str(beta)+"<="+str(alpha)+" alors je retourne "+str(beta))
            return beta
    logging.error("MinValue: beta = "+str(beta))
    return beta

numtour=0
profondeur=3
flag2=False
class AIPlayer(Player):
    """This player should implement a heuristic along with a min-max and alpha
    beta search to """

    def __init__(self):
        self.name = "NouaMarah"


    def getColumn(self, board):
        #TODO(student): implement this!
        global flag , numtour,Tab,flag2, num_joueur
        Tab=np.array([[3,4,5,7,5,4,3],[4,6,8,10,8,6,4],[5,8,11,13,11,8,5],[5,8,11,13,11,8,5],[4,6,8,10,8,6,4],[3,4,5,7,5,4,3]])
        flag=False
        numtour=sum([board.getHeight(i) for i in range(7)])
        if not flag2:
            if numtour==0: num_joueur=1
            else: num_joueur=-1
            flag2=True
        logging.error(numtour)
        logging.error("*************************************************************")
        x=MaxValue(board,- math.inf, math.inf)
        return x
