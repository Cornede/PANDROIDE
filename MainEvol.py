#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:06:11 2021

@author: Damien
"""

from pyroborobo import Pyroborobo
from agentObserverEvol import *
from controllerEvol import *
from tools import *

from custom.objects import SwitchObject, GateObject

def main():
    nbgen = 10000
    nbiterpergen = 400
    rob: Pyroborobo = Pyroborobo.create(
        "config/test.properties",
        controller_class=EvolController,
        agent_observer_class=EvolObserver,
        object_class_dict={'gate': GateObject, 'switch': SwitchObject}
    )

    rob.start()
    for igen in range(nbgen):
        print("*" * 10, igen, "*" * 10)
        stop = rob.update(nbiterpergen)
        if stop:
            break
        weights = get_weights(rob)
        fitnesses = get_fitnesses(rob)
        print("fit ="+str(np.sum(fitnesses)))

        new_weights = fitprop(weights, fitnesses)
        apply_weights(rob, new_weights)
        reset_agent_observers(rob)


if __name__ == "__main__":
    main()
