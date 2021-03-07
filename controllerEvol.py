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
        self.nb_hiddens = 10
        self.weights = [np.random.normal(0, 1, (self.nb_sensors + 1, self.nb_hiddens)),
                        np.random.normal(0, 1, (self.nb_hiddens, 2))]
        self.tot_weights = np.sum([np.prod(layer.shape) for layer in self.weights])

    def reset(self):
        pass

    def step(self):
        input = self.get_all_distances()
        out = np.clip(evaluate_network(input, self.weights), -1, 1)
        self.set_translation(out[0])
        self.set_rotation(out[1])

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