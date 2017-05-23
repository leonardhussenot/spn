from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory

from spn.factory import SpnFactory

from spn.linked.spn import Spn as SpnLinked

from spn.linked.layers import SumLayer as SumLayerLinked
from spn.linked.layers import ProductLayer as ProductLayerLinked
from spn.linked.layers import CategoricalIndicatorLayer
from spn.linked.layers import CategoricalSmoothedLayer

from spn.linked.nodes import SumNode
from spn.linked.nodes import ProductNode
from spn.linked.nodes import CategoricalIndicatorNode
from spn.linked.nodes import CategoricalSmoothedNode
from spn.linked.nodes import CLTreeNode

from spn import MARG_IND
from spn import LOG_ZERO

import numpy
from math import log
import dataset


import logging
import dataset
import algo.learnspn
from algo.dataslice import DataSlice
from pyomo.opt import ProblemFormat


seed = 1337
numpy.random.seed(seed)
rand_gen = numpy.random.RandomState(seed)

def test_learnspn_oneshot():

    logging.basicConfig(level=logging.INFO)
    #
    # loading a very simple dataset
    dataset_name = 'dna'
    train, valid, test = dataset.load_train_val_test_csvs(dataset_name)
    train_feature_vals = [2 for i in range(train.shape[1])]
    print('Loaded dataset', dataset_name)

    #
    # initing the algo
    learnSPN = algo.learnspn.LearnSPN(rand_gen=rand_gen)

    #
    # start learning
    spn = learnSPN.fit_structure(train,
                                 train_feature_vals)
    return spn

a = test_learnspn_oneshot()

var_node,var_indic,constraints = a.get_variables_and_constraints()



model = ConcreteModel()
model.x = Var(var_node, domain=NonNegativeReals, bounds=(0,1))
model.l = Var(var_indic, domain=Boolean, bounds=(0,1))

model.I = RangeSet(0, len(constraints)-1)
def constraint_rule(model, i):
    return eval(constraints[i])
model.super_constraint = Constraint(model.I, rule=constraint_rule)

k = a._root_layer._nodes[0].id
model.obj = Objective(expr=model.x[k], sense=maximize)

model.write("concrete_to_nl.nl", format=ProblemFormat.nl)