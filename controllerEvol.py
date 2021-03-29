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
        self.is_holding_obj=False
        self.weights = [np.random.normal(0, 1, (self.nb_sensors+ self.nb_zones + 3, self.nb_hiddens)),
                        np.random.normal(0, 1, (self.nb_hiddens, 3))]
        self.tot_weights = np.sum([np.prod(layer.shape) for layer in self.weights])
        self.zones=np.zeros(self.nb_zones)
        
    def reset(self):
        pass

    def step(self):
        self.zones=self.get_current_zone()
        input = np.concatenate((self.get_all_distances(),self.zones,[self.is_holding_obj],[self.absolute_orientation]))
        out = np.clip(evaluate_network(input, self.weights), -1, 1)
        self.set_translation(out[0])
        self.set_rotation(out[1])
        self.is_holding_obj=out[2] #depot ou non d objet

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
    
