#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 00:57:55 2021

@author: Damien
"""
from pyroborobo import WorldObserver
from controllerEvol import EvolController

class WorldObserverEvol(WorldObserver):
    def __init__(self):
        WorldObserver.__init__(self)
        self.C = EvolController()
        self.global_fit = 0
        
    def step_post(self):
        r = self.C.rob# on récupère la liste des robots
        for c in r.controllers:
            if c.is_holding_obj:
                self.global_fit+=100
        # et augmenter global_fit ( de bcp ) en fonction du nb d'objet dans le nid