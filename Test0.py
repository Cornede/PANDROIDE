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
        object_class_dict={'_default': Feuille,'uwall': UWallObject, 'switch': SwitchObject},
        override_conf_dict={"gBatchMode": False, "gDisplayMode": 0}
    )

    rob.start()
    rob.update(1000)
    rob.close()
    
if __name__ == "__main__":
    main()