#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 00:57:55 2021

@author: Damien
"""
from pyroborobo import Pyroborobo, Controller, WorldObserver
from controllerEvol import EvolController
import numpy as np


#Variables globales
#Zone de jeu
zoneCollectMin = 50
depotMin = 400
depotMax = 450
rampeYMin=450
rampeYMax=700
nestX=450
nestY=850


class WorldObserverEvol(WorldObserver):

    def __init__(self, world):
        super().__init__(world)
        self.rob = Pyroborobo.get()
        self.global_fit = 0
        
    def init_post(self):
        
        arena_size = np.asarray(self.rob.arena_size)
        landmark = self.rob.add_landmark()
        landmark.radius = 20
        landmark.set_coordinates(450,850)
        landmark.show()
        
    def step_pre(self):
        super().step_pre()
        for c in self.rob.controllers:
            p = c.absolute_position
            x = p[0]
            y = p[1]
            if(c.getCanInstantDrop()==True):
                ori = c.absolute_orientation
                if(x==nestX and y == nestY): # on est dans le nid
                        c.setObjCollected(False)
                        print("Dropped in nest!")
                        self.addPoint(50000)
                if(y>depotMin and y < rampeYMax):
                        self.addPoint(20000)
                        
    def addPoint(self,p):
        self.global_fit=self.global_fit+p
   
        
    def step_post(self):
       # on récupère la liste des robots
       for c in self.rob.controllers:
            if c.is_holding_obj:
                self.global_fit+=100
        # et augmenter global_fit ( de bcp ) en fonction du nb d'objet dans le nid
