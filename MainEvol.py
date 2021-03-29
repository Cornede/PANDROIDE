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
import matplotlib.pyplot as plt

from objects import SwitchObject, UWallObject, Feuille


def main():
    nbgen = 1000
    nbiterpergen = 400
    plt.show()
    performance_list=[]
    rob: Pyroborobo = Pyroborobo.create(
        "config/test.properties",
        #world_observer_class=WorldObserverEvol,
        controller_class=EvolController,
        agent_observer_class=EvolObserver,
        object_class_dict={'uwall': UWallObject, 'switch': SwitchObject,'feuille': Feuille}
    )

    rob.start()
    for igen in range(nbgen):
        print("*" * 10, igen, "*" * 10)
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
    plt.show()
    
if __name__ == "__main__":
    main()
