#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 00:57:55 2021

@author: Damien
"""
from pyroborobo import Pyroborobo, Controller, WorldObserver
from controllerEvol import EvolController
import numpy as np
from objects import SwitchObject, UWallObject, Feuille
import random

#Variables globales
#Zone de jeu
zoneCollectMin = 50
depotMin = 400
depotMax = 450
rampeYMin=450
rampeYMax=700
nestX=450
nestY=850
Rayon_nid = 50


class WorldObserverEvol(WorldObserver):

    def __init__(self, world):
        super().__init__(world)
        self.rob = Pyroborobo.get()
        self.global_fit = 0
        self.pointCount = 0
        self.reference_function = 0
        self.next_id_obj = 8
        self.nb_objects = 20
        
    def init_post(self):
        
        for i in range (self.nb_objects):
            obj = Feuille(self.next_id_obj)
            obj.unregister()
            x = random.randint(250, 650)
            y = random.randint(120, 650)
            obj.set_coordinates(x, y)
            obj = self.rob.add_object(obj)
            obj.show()
            obj.register()
            self.next_id_obj += 1

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

                new_obj = Feuille(self.next_id_obj)
                new_obj.unregister()
                x = random.randint(250, 650)
                y = random.randint(120, 450)
                new_obj.set_coordinates(x, y)
                new_obj = self.rob.add_object(new_obj)
                new_obj.show()
                new_obj.register()
                self.next_id_obj += 1


                ori = c.absolute_orientation
                # on est dans la zone du nid
                if(nestX-Rayon_nid <=x<=nestX+Rayon_nid and nestY-Rayon_nid <= y <= nestY+Rayon_nid and c.getWantDrope()):
                        c.setObjCollected(False)
                        c.setCanInstantDrop(False)
                        print("Dropped in nest!")
                        self.reference_function += 1
                        self.addPoint(50000)
                if(y>depotMin and y < rampeYMax):
                        self.addPoint(20000)
                        
    def addPoint(self,p):
        self.global_fit=self.global_fit+p
        self.pointCount+= p
   
        
    def step_post(self):
       # on récupère la liste des robots
       for c in self.rob.controllers:
            if c.getCanCollect():
                self.global_fit+=10
            if c.getObjCollected():
                self.global_fit+=1000
        # et augmenter global_fit ( de bcp ) en fonction du nb d'objet dans le nid
