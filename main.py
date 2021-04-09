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
    
    mu = 5
    lambdA = 20
    nbgen = 30
    nbiterpergen = 200
    sigma = 0.1
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
    
    n = len(get_weights(rob))
    
    # on initialise les parents
    parents = []
    parentsFit = []
    for k in np.arange(lambdA):
        stop = rob.update(nbiterpergen)
        if stop :
            break
        parents.append(get_weights(rob))
        parentsFit.append(np.sum(get_fitnesses(rob)))
    
    bestFit = np.max(parentsFit)
    
    for igen in range(nbgen):
        """
        if igen in gen_to_track:
            rob.init_trajectory_monitor()  # log trajectory for all agents"""
        print("*" * 10, igen, "*" * 10)
        childs = np.zeros((lambdA,len(parents[0])))
        childsFit = np.zeros(lambdA)
        for z in np.arange(lambdA):
            w = random.randint(0,mu-1)
            parent = parents[w]
            print("poids")
            print(parent[0])
            print(len(parent[0]))
            childs[z] = parent[0]+sigma*np.random.normal(0,sigma,len(parent[0]))
            apply_weights(rob,childs[z])
            stop = rob.update(nbiterpergen)
            if stop :
                break
            childsFit[z] = np.sum(get_fitnesses(rob))
        childsFitId = np.argsort(childsFit)
        parents = childs[childsFitId[0:mu]]
        parentsFit = []
        for z in np.arange(mu):
            apply_weights(rob,parents[z])        
            stop = rob.update(nbiterpergen)
            if stop :
                break
            parentsFit.append(np.sum(get_fitnesses(rob)))
            global_fitnesses = get_global_fitnesses(rob)
            
        bestFit = np.max(parentsFit)
        performance_list.append(bestFit)
        """
        if igen in gen_to_track:
            rob.save_trajectory_image("all_agents for gen"+str(igen))"""
            
            
    plt.plot(np.arange(len(performance_list)),performance_list)
    plt.xlabel("génération")
    plt.ylabel("performance")
    plt.show()
         
        
        
    
if __name__ == "__main__":
    main()

