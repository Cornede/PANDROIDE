#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 13:00:34 2021

@author: Damien
"""

from pyroborobo import  Controller
import numpy as np
from tools import evaluate_network


class EvolController(Controller):

    def __init__(self, wm):
        Controller.__init__(self, wm)
        self.nb_hiddens = 14
        self.nb_zones=6
        
        self.wantDrop=False
        self.setObjCollected(False)
        self.setCanInstantDrop(False)
    

        self.setIsObserved(False)
        
        self.weights = [np.random.normal(0, 1, (self.nb_sensors+ 4, self.nb_hiddens)),
                        np.random.normal(0, 1, (self.nb_hiddens, 3))]
        self.tot_weights = np.sum([np.prod(layer.shape) for layer in self.weights])
        self.zones=np.zeros(self.nb_zones)

    def get_random_weights(self):
        return np.random.normal(0, 1, (self.tot_weights))
    def get_tot_weights(self):
        return self.tot_weights 
    
    def reset(self):
        pass

    def step(self):
        self.lookForFood()

        input = np.concatenate((self.get_all_distances(),[self.getIsObserved(),self.getObjCollected(),self.absolute_orientation]))

        out = np.clip(evaluate_network(input, self.weights), -1, 1)
        self.set_translation(out[0])
        self.set_rotation(out[1])
        self.setWantDrope(out[2])#depot ou non d objet

        
        # Quand le robot est sur la pente 
        maxRampSpeed = 0.3
        p = self.absolute_position
        orientation = self.absolute_orientation
        x = p[0]
        y = p[1]
        if (x > 250 and x < 670 and y > 450 and y < 700 and orientation < 0.0):
            self.set_translation(maxRampSpeed)
        if (x > 250 and x < 670 and y > 450 and y < 700 and orientation > 0.0):
            self.set_translation(maxRampSpeed)
            
        
        



    def get_flat_weights(self):
        all_layers = []
        for layer in self.weights:
            all_layers.append(layer.reshape(-1))
        flat_layers = np.concatenate(all_layers)
        assert (flat_layers.shape == (self.tot_weights,))
        return flat_layers

    
    def set_weights(self, weights):
        j = 0
        for i, elem in enumerate(self.weights):
            shape = elem.shape
            size = elem.size
            #self.weights[i] = np.array(elem).reshape(shape)
            self.weights[i] = np.array(weights[j:(j + size)]).reshape(shape)
            j += size
        # assert that we have consume all the weights needed
        assert (j == self.tot_weights)
        assert (j == len(weights))
        
    def lookForFood(self):
        camera_dist = self.get_all_distances()
        for i in range(len(camera_dist)):
            if camera_dist[i] < 1:  # if we see something
                if self.get_object_at(1) != -1:  # And it is food
                    self.setIsObserved(True)
                    break
        
	# Fonctions de ramassage et dépôt d'objets
    
    def getWantDrope(self):
        return self.wantDrop
    
    def getCanCollect(self):
        return self.canCollect
    
    def getCanDropSlope(self):
        return self.canDropSlope
        
    def getCanDropNest(self):
        return self.canDropNest
      
    def getCanInstantDrop(self):
        return self.instantDrop
    
    def getObjCollected(self):
        return self.objCollected

    def getIsObserved(self):
        return self.objObserved
    
    
    


	# Fonction set
    
    def setWantDrope(self,c):
        self.wantDrop = c
    
    def setCanCollect(self,c):
        self.canCollect = c
    
    def setCanDropSlope(self,c):
        self.canDropSlope = c
        
    def setCanDropNest(self,c):
         self.canDropNest = c
      
    def setCanInstantDrop(self,c):
        self.instantDrop = c
        
    def setIsObserved(self,c):
        self.objObserved = c
    

    def setObjCollected(self,c):
        self.objCollected = c
        if(c == True):
            print("Can not collect anymore")
            self.setCanCollect(False)
            self.setIsObserved(False)
            self.setCanDropSlope(True)
            self.setCanDropNest(True)
            self.setCanInstantDrop(True)
        if (c == False):
            print("Can recollect")
            self.setCanCollect(True)
            self.setCanDropSlope(False)
            self.setCanDropNest(False)
            self.setCanInstantDrop(False)

    
