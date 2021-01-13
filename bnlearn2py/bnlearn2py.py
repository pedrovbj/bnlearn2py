# bnlearn2py
#
# Converts bnlearn.com RDS models to pgmpy models
# Copyright (c) 2019-2021 Pedro V. B. Jeronymo

import tempfile
import shutil
import urllib.request
import numpy as np
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
pandas2ri.activate()


def fetch_model(name):
    """
    Fetches model from bnlearn.com

    Parameters
    ----------
    name :
        Model name, e.g. 'asia', 'alarm', 'win95pts', etc.

    Returns
    -------
    model : BayesianModel
        Model converted from RDS to python
    cpds : dict
        The CPDs for the variables in the model
    """
    url = f"https://www.bnlearn.com/bnrepository/{name}/{name}.rds"
    with urllib.request.urlopen(url) as response:
        # Retrive RDS from bnlearn.com and save it in temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as tmpf:
            shutil.copyfileobj(response, tmpf)
        # Load model
        return load_model(tmpf.name)


def load_model(filename):
    """
    Creates a pgmpy's BayesianModel from a bnlearn.com RDS file

    Parameters
    ----------
    filename :
        RDS file path, e.g. './asia.rds'

    Returns
    -------
    model : BayesianModel
        Model converted from RDS to python
    cpds : dict
        The CPDs for the variables in the model
    """
    data = load_data(filename)
    model = get_structure(data)
    cpds = get_cpds(data)
    model.add_cpds(*cpds.values())
    assert(model.check_model())
    return model, cpds


def load_data(filename):
    """
    Loads data for the models in RDS format from bnlearn.com

    Parameters
    ----------
    filename :
        RDS file path, e.g. './asia.rds'

    Returns
    -------
    data : 
        RDS data object
    """
    readRDS = robjects.r['readRDS']
    data = readRDS(filename)
    data = pandas2ri.rpy2py(data)
    return data


def get_structure(data):
    """
    Structure of model from data (Loaded RDS)

    Parameters
    ----------
    data :
        RDS data object
    model : BayesianModel
        Empty network

    Returns
    -------
    model : BayesianModel
        Model converted from RDS to python
    """
    model = BayesianModel()
    for k in range(len(data)):
        node = list(data[k][0])[0]
        children = list(data[k][2])
        model.add_node(node)
        for child in children:
            model.add_edge(node, child)
    return model


def get_cpds(data):
    """
    CPDs from data (Loaded RDS)

    Parameters
    ----------
    data :
        RDS data object

    Returns
    -------
    cpds : dict
        The CPDs for the variables in the model
    """
    cpds = {}
    for k in range(len(data)):
        node = list(data[k][0])[0]
        parents = list(data[k][1])
        prob = data[k][3]
        cpd = None
        aux = list(prob.shape)
        variable_card = aux[0]
        evidence_card = aux[1:]
        if evidence_card:
            values = prob.reshape(variable_card, np.prod(evidence_card))
            cpd = TabularCPD(node, variable_card, values,
                             evidence=parents, evidence_card=evidence_card)
        else:
            values = prob.reshape(variable_card, 1)
            cpd = TabularCPD(node, variable_card, values)
        cpds[node] = cpd
    return cpds
