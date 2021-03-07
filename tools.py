#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 13:02:00 2021

@author: Damien
"""
#set of methods used for learning with neuron networks

import numpy as np
from pyroborobo import Pyroborobo
from scipy.stats import rankdata

def evaluate_network(input_, network):
    out = np.concatenate([[1], input_])
    for elem in network[:-1]:
        out = np.tanh(out @ elem)
    out = out @ network[-1]  # linear output for last layer
    return out


def get_weights(rob: Pyroborobo):
    weights = []
    for ctl in rob.controllers:
        weights.append(ctl.get_flat_weights())
    return weights


def get_fitnesses(rob: Pyroborobo):
    fitnesses = []
    for observer in rob.agent_observers:
        fitnesses.append(observer.fitness)
    return fitnesses


def fitprop(weights, fitnesses):
    adjust_fit = rankdata(fitnesses)
    # adjust_fit = np.clip(fitnesses, 0.00001, None)
    normfit = adjust_fit / np.sum(adjust_fit)
    # select
    new_weights_i = np.random.choice(len(weights), len(weights), replace=True, p=normfit)
    new_weights = np.asarray(weights)[new_weights_i]
    # mutate
    new_weights_mutate = np.random.normal(new_weights, 0.01)
    return new_weights_mutate


def apply_weights(rob, weights):
    for ctl, weight in zip(rob.controllers, weights):
        ctl.set_weights(weight)


def reset_agent_observers(rob):
    for obs in rob.agent_observers:
        obs.reset()
