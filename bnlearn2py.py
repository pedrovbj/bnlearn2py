# bnlearn2py
#
# Description: Converts bnlearn.com RDS models to pgmpy models
# Author: Pedro V. B. Jeronymo (pedrovbj@gmail.com)
# Date: 21/08/2019

import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import numpy as np
pandas2ri.activate()

def load_model(filename):
    '''
    Creates a pgmpy's Bayesian Model from a bnlearn.com RDS file.
    '''
    model = BayesianModel()
    data = load_data(filename)
    add_structure(data, model)
    cpds = add_cpds(data, model)
    return model, cpds

def load_data(filename):
    '''
    Loads data for the models in RDS format from bnlearn.com
    '''
    readRDS = robjects.r['readRDS']
    data  = readRDS(filename)
    data = pandas2ri.rpy2py(data)
    return data

def add_structure(data, model):
    '''
    Adds structure to Bayesian Model (pgmpy) from data (Loaded RDS)
    '''
    for k in range(len(data)):
        node = list(data[k][0])[0]
        parents = list(data[k][1])
        children = list(data[k][2])

        model.add_node(node)
        for child in children:
            model.add_edge(node, child)

def add_cpds(data, model):
    '''
    Adds Bayesian Model's (pgmpy) cpds from data (Loaded RDS)
    '''
    cpds = {}

    for k in range(len(data)):
        node = list(data[k][0])[0]
        parents = list(data[k][1])
        children = list(data[k][2])
        prob = data[k][3]

        cpd = None
        aux = list(prob.shape)
        variable_card = aux[0]
        evidence_card = aux[1:]
        if evidence_card:
            values = prob.reshape(variable_card, np.prod(evidence_card))
            cpd = TabularCPD(node, variable_card, values, evidence = parents,\
                evidence_card = evidence_card)
        else:
            values = prob.reshape(variable_card, 1)
            cpd = TabularCPD(node, variable_card, values)
        cpds[node] = cpd

    model.add_cpds(*cpds.values())
    assert(model.check_model())
    return cpds


if __name__ == '__main__':
    from bnlearn2py import load_model

    model, cpds = load_model('asia.rds')
    print(model.nodes())
    print(model.edges())
