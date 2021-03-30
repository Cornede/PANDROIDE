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
<<<<<<< HEAD
        Controller.__init__(self, wm)
        self.nb_hiddens = 14
        self.nb_zones=6
        
        self.is_holding_obj=False
        self.setObjCollected(False);
        self.setCanInstantDrop(False);
        self.setIsObserved(False)
        
        self.weights = [np.random.normal(0, 1, (self.nb_sensors+ 3, self.nb_hiddens)),
                        np.random.normal(0, 1, (self.nb_hiddens, 3))]
        self.tot_weights = np.sum([np.prod(layer.shape) for layer in self.weights])
        self.zones=np.zeros(self.nb_zones)
=======
        	Controller.__init__(self, wm)
        	self.nb_hiddens = 14
        	self.is_holding_obj=False
        	self.weights = [np.random.normal(0, 1, (self.nb_sensors + 5, self.nb_hiddens)),
        			np.random.normal(0, 1, (self.nb_hiddens, 3))]
        	self.tot_weights = np.sum([np.prod(layer.shape) for layer in self.weights])
        	self.setObjCollected(False)
        	self.setCanInstantDrop(False)
        	self.setIsObserved(False)
>>>>>>> e2f8a5d661ff1901da8251edcdb5d26ee4096ceb
        
    def reset(self):
        pass

    def step(self):
<<<<<<< HEAD
    
        self.zones=self.get_current_zone()
        input = np.concatenate((self.get_all_distances(),[self.is_holding_obj],[self.absolute_orientation],))
=======
        input = np.concatenate((self.get_all_distances(),[self.is_holding_obj,self.getIsObserved(),self.getObjCollected(),self.absolute_orientation]))
>>>>>>> e2f8a5d661ff1901da8251edcdb5d26ee4096ceb
        out = np.clip(evaluate_network(input, self.weights), -1, 1)
        self.set_translation(out[0])
        self.set_rotation(out[1])
        self.is_holding_obj=out[2] #depot ou non d objet
        
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


        camera_dist = self.get_all_distances()
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
            self.weights[i] = np.array(weights[j:(j + size)]).reshape(shape)
            j += size
        # assert that we have consume all the weights needed
        assert (j == self.tot_weights)
        assert (j == len(weights))


	# Fonctions de ramassage et dépôt d'objets
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
    
<<<<<<< HEAD
    def get_current_zone(self):
            res = np.zeros(self.nb_zones)
            x,y=self.absolute_position
            
            # a modifier!faire avec des if en fonction de la position de l'agent
            if 0<=x<=100: #exemple bete
                res[1]=1
            else:
                res[0]=1 
            assert(np.sum(res)==1)
            return res
            
# Fonctions de ramassage et dépôt d'objets

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

    def getIsObserved(self,c):
        return self.objObserved

# Fonction set
    
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
    
=======
>>>>>>> e2f8a5d661ff1901da8251edcdb5d26ee4096ceb
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
<<<<<<< HEAD
    
            

=======
>>>>>>> e2f8a5d661ff1901da8251edcdb5d26ee4096ceb
    
