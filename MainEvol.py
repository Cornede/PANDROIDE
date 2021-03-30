#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:06:11 2021

@author: Damien
"""

from pyroborobo import Pyroborobo
from agentObserverEvol import *
from controllerEvol import *
from WorldObserverEvol import *
from tools import *
import matplotlib
import matplotlib.pyplot as plt

<<<<<<< HEAD
from custom.objects import SwitchObject, GateObject
from objects import SwitchObject, UWallObject, Feuille
=======
from objects import SwitchObject, UWallObject, Feuille

>>>>>>> e2f8a5d661ff1901da8251edcdb5d26ee4096ceb

def main():
    nbgen = 10
    nbiterpergen = 400
    plt.show()
    performance_list=[]
    rob: Pyroborobo = Pyroborobo.create(
        "config/test.properties",
        controller_class=EvolController,
        world_observer_class=WorldObserverEvol,
        agent_observer_class=EvolObserver,
        object_class_dict={'uwall': UWallObject, 'switch': SwitchObject,'feuille': Feuille}
    )

    rob.start()
    for igen in range(nbgen):
        print("*" * 10, igen, "*" * 10)
        ## Pour tester une solution candidate(les poids) il faudrait faire
        ## une moyenne sur plusieurs expériences et pas que sur une 
        stop = rob.update(nbiterpergen)
        if stop:
            break
        weights = get_weights(rob)
        fitnesses = get_fitnesses(rob)
        
        performance_list.append(np.sum(fitnesses))
        print("fit ="+str(performance_list[-1]))

        new_weights = fitprop(weights, fitnesses)
        apply_weights(rob, new_weights)
        reset_agent_observers(rob)

    plt.plot(np.arange(len(performance_list)),performance_list)
    plt.xlabel("génération")
    plt.ylabel("performance")
    plt.show()
    
if __name__ == "__main__":
    main()
