# -*- coding: utf-8 -*-
"""
Code modifiable.
"""

from automate import Automate
from state import State
from transition import Transition
from parser import *

### EXERCICE 2

## Q1 et Q4 et Q5

# s0 : State
s0 = State(0, True, False)
# s1 : State
s1 = State(1,False,False)
# s2 : State
s2 = State(2, False, True)
# s3 : State
s3 = State(0,True, False)

# t1 : Transition
t1 = Transition(s0,"a",s0)
# t2 : Transition
t2 = Transition(s0,"b",s1)
# t3 : Transition
t3 = Transition(s1,"a",s2)
# t4 : Transition
t4 = Transition(s1,"b",s2)
# t5 : Transition
t5 = Transition(s2,"a",s0)
# t6 : Transition
t6 = Transition(s2,"b",s1)
# t : Transition 
t = Transition(s0,"a",s1)

# liste_t : list[Transition]
liste_t = [t1,t2,t3,t4,t5,t6]

# liste_e : list[State]
liste_e = [s0,s1,s2]

# auto : Automate
auto = Automate(liste_t)
print(auto.removeTransition(t))
print(auto.removeTransition(t1))
print(auto.addTransition(t1))
print(auto.removeState(s1))
print(auto.addState(s1))
print(auto.addState(s3))
print(auto)
auto.show("A_ListeTrans")

## Q2 et Q6

# auto1 : Automate
auto1 = Automate(liste_t,liste_e)
print(auto1.getListTransitionsFrom(s1))
print(auto1)
auto1.show("A_ListeTransEtEtats")

## Q3

# auto2 : Automate
auto2 = Automate.creationAutomate("automate.txt")
print(auto2)
auto2.show("A_CreationFichier")


### EXERCICE 3

## Q1
print(Automate.succ(auto,[s0,s1,s2],"a"))

## Q2
print(Automate.accepte(auto2,"aba"))

## Q3 
print(Automate.estComplet(auto2,["a", "b"]))

## Q4
print(Automate.estDeterministe(auto2))

## Q5 
auto2.removeTransition(t1)
Automate.completeAutomate(auto2,["a", "b"]).show("Complet")

### EXERCICE 4

#auto3 : Automate
auto3 = Automate.creationAutomate("testDeter.txt")
# autod : Automate
autod = Automate.determinisation(auto3)
autod.show("Determinisation")

### EXERCICE 5 

## Complementaire
#auto4 : Automate
auto4 = Automate.creationAutomate("testCompl.txt")
#autocompl : Automate
autocompl = Automate.complementaire(auto4, ["a","b"])
autocompl.show("Complementaire")

## Intersection
#auto5 : Automate
auto5 = Automate.creationAutomate("testInter1.txt")
#auto6 : Automate
auto6 = Automate.creationAutomate("testInter2.txt")
#autointer : Automate
autointer = Automate.intersection(auto5,auto6)
autointer.show("Intersection")


## Concatenation
#auto7 : Automate
auto7 = Automate.creationAutomate("testconc1.txt")
#auto8 : Automate
auto8 = Automate.creationAutomate("testconc2.txt")
#autoconc : Automate
autoconc = Automate.concatenation(auto7,auto8)
autoconc.show("Concatenation")

## Etoile 
#auto9 : Automate
auto9 = Automate.creationAutomate("testetoile.txt")
#autoetoile : Automate
autoetoile = Automate.etoile(auto9)
autoetoile.show("Etoile")
