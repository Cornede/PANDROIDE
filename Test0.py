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
import random
import numpy as np


from objects import SwitchObject, UWallObject, Feuille

gen_to_track=[0,5,10,15,25]

def main():
    nbgen = 30
    mu = 5
    lambda_ = 20
    nbiterpergen = 200
    plt.show()
    performance_list=[]
    rob: Pyroborobo = Pyroborobo.create(
        "config/test.properties",
        controller_class=EvolController,
        world_observer_class=WorldObserverEvol,
        agent_observer_class=EvolObserver,
        object_class_dict={'uwall': UWallObject, 'switch': SwitchObject,'feuille': Feuille},
        override_conf_dict={"gBatchMode": True, "gDisplayMode": 2}
    )

    rob.start()
    
    # on initialise les parents
  
    for k in range(lambda_):
        stop = rob.update(nbiterpergen)
        if stop :
            break
        
    weights = [[get_weights(rob)] for i in range(lambda_)]
    fitnesses = [[np.sum(get_fitnesses(rob))] for i in range(lambda_)]
    bestFit = np.max(fitnesses)
    
    
    for igen in range(nbgen):
        
        print("*" * 10, igen, "*" * 10)
        
        ## Pour tester une solution candidate(les poids) il faudrait faire
        ## une moyenne sur plusieurs expériences et pas que sur une 
 	#on pourra utiliser la global fit pour faire varier la variance sigma de fitprop en fonction de si la génération s'est améliorer ou non.
        global_fitnesses = get_global_fitnesses(rob)
        
        performance_list.append(bestFit)
        print("fit ="+str(performance_list[-1]))
        
        new_weights = mu_comma_lambda_nextgen(weights, fitnesses,5,20)
        for k in range(lambda_):
            apply_weights(rob, new_weights[k])
            reset_agent_observers(rob)
            stop = rob.update(nbiterpergen)
            if stop :
                break
            fitnesses[k] = np.sum(get_fitnesses(rob))
            
        if bestFit <= np.max(fitnesses):
                bestFit = np.max(fitnesses)
        
        
    
    plt.plot(np.arange(len(performance_list)),performance_list)
    plt.xlabel("génération")
    plt.ylabel("performance")
    plt.show()
    
if __name__ == "__main__":
    main()