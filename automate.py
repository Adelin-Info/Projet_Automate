# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from sp import *
from parser import *
from itertools import product
from automateBase import AutomateBase


class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        successeurs = []
        # s : State
        for s in listStates:
            # l : State
            for l in self.succElem(s, lettre):
                if l not in successeurs:
                        successeurs.append(l)
        return successeurs 




    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """
    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        # s : State
        # t : Transition
        # c : str
        for c in mot:
            for t in auto.listTransitions:
                if t.etiquette == c :
                    s = t.stateDest
        if s.fin == True :
            return True
        else :
            return False


    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """
        # etiquette : list[str]
        etiquette = [] 
        # s : State
        for s in auto.listStates:
            # c : char
            for c in alphabet:
                # t : Transition
                for t in auto.getListTransitionsFrom(s):
                    etiquette.append(t.etiquette)
                if not c in etiquette :
                    return False
                    etiquette = []
        return True 


        
    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        # etiquette : list[str]
        etiquette = [] 
        # s : State
        for s in auto.listStates:
            # t : Transition
            for t in auto.getListTransitionsFrom(s):
                if not t.etiquette in etiquette:
                    etiquette.append(t.etiquette)
                else : 
                    return False
            etiquette = []
        return True
        

       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        # autocomp : AutomateBase
        autocomp = copy.deepcopy(auto)
        # scomp : State 
        scomp = State("T", False, False)
        autocomp.addState(scomp)
        # etiquette : list[str]
        etiquette = []
        # s : State
        for s in auto.listStates:
            # c : str
            for c in alphabet:
                # t : Transition
                for t in auto.getListTransitionsFrom(s):
                    etiquette.append(t.etiquette)
                if not c in etiquette :
                    # t1 : Transition
                    t1 = Transition(s, c, scomp)
                    autocomp.addTransition(t1)
                # t2 : Transition
                t2 = Transition(scomp, c, scomp)
                autocomp.addTransition(t2)
                etiquette = []
            
        return autocomp 

       

    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
    
        if auto.estDeterministe(auto):
            return auto
            
        # autoDeter : Automate
        autoDeter = Automate([],[])
        autoDeter.listStates.append(State(0,True,False))
        
        # alphabet : list[str]
        alphabet=auto.getAlphabetFromTransitions()
        # Ls : list[set[State]]
        Lstate=[]
        Lstate.append(set(auto.getListInitialStates()))
        # e : set[State]
        for e in Lstate :
            # l : str
            for l in alphabet :
                # nv : set[State]
                nv = set(auto.succ(list(e),l))
                if nv not in Lstate :
                    Lstate.append(nv)
        
        #i : int 
        for i in range(1,len(Lstate)) :
            # Ef : set[State]
            Ef=set(auto.getListFinalStates())
            if Lstate[i].isdisjoint(Ef)==False:
                autoDeter.listStates.append(State(i,False,True))
            else :
                autoDeter.listStates.append(State(i, False, False))

        for i in range(0,len(Lstate)):
            for l in alphabet:
                # Es : set[State]
                Es=set(auto.succ(list(Lstate[i]),l))
                # iSucc : int
                iSucc=Lstate.index(Es)
                # Ltransition : list[Transition]
                Ltransition=Transition(autoDeter.listStates[i],l,autoDeter.listStates[iSucc])
                autoDeter.addTransition(Ltransition)

        return autoDeter
        
        
    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        
        # autoComp : Automate
        autoComp=copy.deepcopy(auto)

        if (Automate.estComplet(autoComp,alphabet)==False):
            autoComp=Automate.completeAutomate(autoComp,alphabet)
        
        if (Automate.estDeterministe(autoComp)==False):
            autoComp=Automate.determinisation(auto)
        
        # s : State
        for s in autoComp.listStates:
            if s.fin==False:
                s.fin=True
            else :
                s.fin=False
        return autoComp      
   
   
    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        import itertools
        
        # autoA : Automate
        # autoB : Automate
        # autoInter : Automate
        autoA=auto0
        autoB=auto1

        autoA=Automate.determinisation(auto0)
        autoB=Automate.determinisation(auto1)
        autoInter=Automate([],[])
        
        #listeA0 : list[str]
        #listeA1 : list[str]
        #listeA : list[str]
        listeA0=autoA.getAlphabetFromTransitions()
        listeA1=autoB.getAlphabetFromTransitions()
        listeA=[]
        
        # val : str 
        for val in listeA0:
            if val in listeA1:
                listeA.append(val)
        
        #listeIs0 : list[State]
        #listeIs1 : list[State]
        #listeProduit : list[tuple[alpha,beta]]
        listeIs0=autoA.getListInitialStates()
        listeIs1=autoB.getListInitialStates()
        listeProduit=list(itertools.product(listeIs0,listeIs1))

        ##CREATION DE LA LISTE DES ETATS DU NOUVEAU AUTOMATE
        
        # couple : tuple[alpha,beta]
        # l : str  
        for couple in listeProduit:
            for l in listeA:
                # Ls : list[State]
                Ls=autoA.succElem(couple[0],l)
                Ls+=autoB.succElem(couple[1],l)
                if (len(Ls)!=2):
                    continue
                if tuple(Ls) not in listeProduit:
                    listeProduit.append(tuple(Ls))

        ## CREATION DES ETATS 
        
        #i : int 
        for i in range(0,len(listeProduit)):
            if (i==0):
                autoInter.listStates.append(State(i, True, False))
            else :
                autoInter.listStates.append(State(i,False,False))

        ## CREATION DES TRANSITIONS 
        
        for couple in listeProduit:
            for l in listeA:
                # Ls : list[State]
                Ls = autoA.succElem(couple[0],l)
                Ls+= autoB.succElem(couple[1],l)
                iCouple=autoInter.listStates[listeProduit.index(couple)]
                iSucc=autoInter.listStates[listeProduit.index(tuple(Ls))]
                autoInter.addTransition(Transition(iCouple,l,iSucc))

        ## CREATION DES ETATS FINAUX 
        
        #listeFs0 : list[State]
        #listeFs1 : list[State]
        #listeProduitfin : list[tuple[alpha,beta]]
        listeFs0=autoA.getListFinalStates()
        listeFs1=autoB.getListFinalStates()
        listeProduitFin = list(itertools.product(listeFs0, listeFs1))

        for couple in listeProduitFin:
            if couple in listeProduit:
                autoInter.listStates[listeProduit.index(couple)].fin=True
        return autoInter
        

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        return
        

   
       

    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        
        #autoA : Automate
        #autoB : Automate
        autoA=copy.deepcopy(auto1)
        autoB=copy.deepcopy(auto2)
        
        #listeFsA : list[State]
        #listeFsB : list[State]
        #listeIsA : list[State]
        #listeIsB : list[State]
        listeFsA=autoA.getListFinalStates()
        listeFsB=autoB.getListFinalStates()
        listeIsA=autoA.getListInitialStates()
        listeIsB=autoB.getListInitialStates()
        
        #listeStateB : list[State]
        #listeTransitionB : list[Transition]
        listeStateB = autoB.listStates
        listeTransitionB = autoB.listTransitions
        
        #eA : bool
        #eB : bool
        eA=False
        eB=False

        # i : State
        for i in listeFsA:
            if i in listeIsA:
                eA=True
                break
        for i in listeFsB:
            if i in listeIsB:
                eB=True
                break
        if eA==False:
            for i in listeIsB:
                i.init=False
        if eB==False:
            for i in listeFsA:
                i.fin=False  
        
        # autoConc : Automate
        autoConc = copy.deepcopy(autoA) 
        
        # s : State
        for s in listeStateB:
            autoConc.addState(s)
        
        #tconc : Transition
        # sf : State
        # si : State
        for tconc in autoConc.listTransitions :
            for sf in listeFsA:
                for si in listeIsB :
                    if tconc.stateDest == sf :
                        autoConc.addTransition(Transition(tconc.stateSrc,tconc.etiquette,si)) 
        
        # t : Transition
        for t in listeTransitionB :
            autoConc.addTransition(t)          

        return autoConc
        
       
    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        
        #autoEtoile : Automate
        autoEtoile = copy.deepcopy(auto)
        
        # t : Transition
        # s : State
        for t in autoEtoile.listTransitions :
                for s in autoEtoile.getListInitialStates():
                    if t.stateDest.fin == True : 
                        autoEtoile.addTransition(Transition(t.stateSrc, t.etiquette,s))
                        
        autoEtoile.addState(State("T", True, True))
        return autoEtoile
