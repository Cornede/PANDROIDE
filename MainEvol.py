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


from objects import SwitchObject, UWallObject, Feuille

gen_to_track=[0,5,10,15,25]
def main():
    nbgen = 20
    nbiterpergen = 200
    lambda_=20
    plt.show()
    performance_list=[]
    rob: Pyroborobo = Pyroborobo.create(
        "config/test.properties",
        controller_class=EvolController,
        world_observer_class=WorldObserverEvol,
        agent_observer_class=EvolObserver,
        object_class_dict={'uwall': UWallObject, 'switch': SwitchObject,'feuille': Feuille},
        override_conf_dict={"gBatchMode": True, "gDisplayMode": 2,"gInitialNumberOfRobots":lambda_}
    )

    all_genomes=init_random_gen(lambda_)
    rob.start()
    for igen in range(nbgen):
        if igen in gen_to_track:
            rob.init_trajectory_monitor()  # log trajectory for all agents
        print("*" * 10, igen, "*" * 10)
        
        performance_gen=0
        for genome in all_genomes:
            apply_weight_clonal(rob,genome)
            stop = rob.update(nbiterpergen)
            if stop:
                break
            #fitness dediee de chaque agent
            fitnesses_ded_list = get_fitnesses_ded(rob)
            #fitness dediee totale pour ce genome
            fitness_ded_genome=np.sum(fitnesses_list)+get_global_fitnesses(rob)
            performance_gen_ded.append(fitness_ded_genome)
            performance_gen_ref=FIT_REF(rob)
        
        performance_list.append(np.mean(performance_gen_ref))
        performance_gen_ref=[]
        print("fit ="+str(performance_list[-1]))
   
   	     #ou utiliser fitprop ici ou tout algo de selection de type ES
        all_genomes = mu_comma_lambda_nextgen(all_genomes, performance_gen_ded,5,20)
        reset_agent_observers(rob)
        performance_gen_ded=[]
        
        if igen in gen_to_track:
            rob.save_trajectory_image("all_agents for gen"+str(igen))

    plt.plot(np.arange(len(performance_list)),performance_list)
    plt.xlabel("génération")
    plt.ylabel("performance")
    plt.show()
    
if __name__ == "__main__":
    main()
