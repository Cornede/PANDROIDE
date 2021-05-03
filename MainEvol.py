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
import time


from objects import SwitchObject, UWallObject, Feuille

gen_to_track=[0,5,10,15,25]
def main():
    nbgen = 40
    nbiterpergen = 4000
    lambda_=20
    mu=5
    performance_list=[]
    performance_list_ded=[]
    rob: Pyroborobo = Pyroborobo.create(
        "config/test.properties",
        controller_class=EvolController,
        world_observer_class=WorldObserverEvol,
        object_class_dict={'uwall': UWallObject, 'switch': SwitchObject,'feuille': Feuille},
        override_conf_dict={"gBatchMode": True, "gDisplayMode": 2,"gInitialNumberOfRobots":lambda_}
    )

 
    rob.start()
    # un genome : une solution candidate , poids du réseau
    all_genomes=init_random_gen(rob,lambda_)
    debug = []
    for igen in range(nbgen):
        """
        if igen in gen_to_track:
            rob.init_trajectory_monitor()  """# log trajectory for all agents
        print("*" * 10, igen, "*" * 10)
        ## Pour tester une solution candidate(les poids) il faudrait faire
        ## une moyenne sur plusieurs expériences et pas que sur une 
        s = ("génération:",igen)
        debug.append(s)
        performance_gen_ref=[]
        performance_gen_ded=[]
        i = 0
        for genome in all_genomes:
            i = i+1
            s2 = ("genome:",i)
            debug.append(s2)
            print("*" * 10,"genome:",i, "*" * 10)
            apply_weight_clonal(rob,genome)
            tps1 = time.time()
            stop = rob.update(nbiterpergen)
            if stop:
                break
            tps2 = time.time()
            print("temps test genome :",tps2 - tps1)
            #fitness dediee de chaque agent/robot
            fitnesses_ded_list = get_fitnesses_ded(rob)
            #fitness dediee totale pour ce genome
            fitness_ded_genome=np.sum(fitnesses_ded_list)+get_global_fitnesses(rob)
            performance_gen_ded.append(fitness_ded_genome)
            #performance_gen_ref= get_reference_function(rob)
            performance_gen_ref.append(get_reference_function(rob))
            print("debug:",debug)
            tps1 = time.time()
            reset_world_observer(rob)
            tps2 = time.time()
            print("temps reset_world_observer:",tps2 - tps1)
            reset_agent_controllers(rob)
            
        
        performance_list_ded.append(np.mean(performance_gen_ded))
        performance_list.append(np.mean(performance_gen_ref))
   
        #on garde le meilleur genome en memoire
        updateHoF(all_genomes, performance_gen_ref)
   	    #ou utiliser fitprop ici ou tout algo de selection de type ES
        all_genomes = mu_comma_lambda_nextgen(all_genomes, performance_gen_ded,mu,lambda_)
        """
        if igen in gen_to_track:
            rob.save_trajectory_image("all_agents for gen"+str(igen))"""

        plt.plot(np.arange(len(performance_list)),performance_list)
        plt.xlabel("génération")
        plt.ylabel("performance")
        plt.title("graphe_de_performance_ref")
        plt.savefig("graphe_de_performance_ref")
        plt.figure()
        
        
        plt.plot(np.arange(len(performance_list_ded)),performance_list_ded)
        plt.xlabel("génération")
        plt.ylabel("performance")
        plt.title("graphe_de_performance_ded")
        plt.savefig("graphe_de_performance_ded")
        plt.figure()
    plt.show()
    
if __name__ == "__main__":
    main()

