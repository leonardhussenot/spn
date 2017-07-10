
# Developing inference on the SPYN package (https://github.com/arranger1044/spyn)

Initial package has been completed and modified to deal test Maximum-A-Posteriori Inference on different classes of sum Product Network.
To use package normally, see spyn part below.
Goal was to compare the result of the max-product algorithm with an exact algorithm on different class of SPNs:

To do test on inference, see the MAP_inference.pynb jupiter notebook, composed of these parts:

## The Poon Algorithm (or Max-Product Algorithm)
Implementing the max-product approximation for most probable evidence, now integrated in the library itself.

## Branch & Bound Algorithm
Implementing exact inference with different heuristics

## Exact Solver
A link to an Couenne, an exact solver (works only on small problems and require the installation of Couenne, see: https://projects.coin-or.org/Couenne )

## idSPN : Transorm AC in SPN
A translation from an SPN learned thanks to libra library (the idSPN algorithm),  see : http://libra.cs.uoregon.edu/
The SPN was composed of arithmetic circuit and we had to implement a translation from arithmetic circuit to sum-product network. 
Finding the layer structure can be done much faster. TODO : find a better algorithm than looking for all paths from node to leaves.

## From tree to graph
An implementation on the algorithm for merging subtrees to avoid overfitting: Merging Strategies for Sum-Product Networks: From Trees to Graphs. from T. Rahman & V. Gogate 
Need to be finished (TODO).


# spyn

Implementing Sum-Product Networks (SPN) in python and providing
some routines to do inference and learning.



## overview

Implementing [LearnSPN](http://homes.cs.washington.edu/~pedrod/papers/mlc13.pdf)
and SPN-BTB as presented in:  
_A. Vergari, N. Di Mauro, andF. Esposito_   
**Simplifying, Regularizing and Strengthening Sum-Product Network Structure Learning** at ECML-PKDD 2015.


## requirements
spyn is build upon [numpy](http://www.numpy.org/),
[sklearn](http://scikit-learn.org/stable/),
[scipy](http://www.scipy.org/), [numba](http://numba.pydata.org/), [matplotlib](http://matplotlib.org/) and [theano](http://deeplearning.net/software/theano/).

## usage
Several datasets are provided in the `data/` folder.


To run the algorithms and their grid search check the scripts in the `bin/` folder.  
To learn a single SPN from the training set portion of the `nltcs`
data you can call:

    ipython -- bin/learnspn_exp.py nltcs

To get an overview of the possible parameters use `-h`:

    -h, --help            show this help message and exit
    -k [N_ROW_CLUSTERS], --n-row-clusters [N_ROW_CLUSTERS]
                          Number of clusters to split rows into (for DPGMM it is
                          the max num of clusters)
    -c [CLUSTER_METHOD], --cluster-method [CLUSTER_METHOD]
                          Cluster method to apply on rows ["GMM"|"DPGMM"|"HOEM"]
    --seed [SEED]         Seed for the random generator
    -o [OUTPUT], --output [OUTPUT]
                          Output dir path
    -g G_FACTOR [G_FACTOR ...], --g-factor G_FACTOR [G_FACTOR ...]
                          The "p-value like" for G-Test on columns
    -i [N_ITERS], --n-iters [N_ITERS]
                          Number of iterates for the row clustering algo
    -r [N_RESTARTS], --n-restarts [N_RESTARTS]
                          Number of restarts for the row clustering algo (only
                          for GMM)
    -p CLUSTER_PENALTY [CLUSTER_PENALTY ...], --cluster-penalty CLUSTER_PENALTY [CLUSTER_PENALTY ...]
                          Penalty for the cluster number (i.e. alpha in DPGMM
                          and rho in HOEM, not used in GMM)
     -s [SKLEARN_ARGS], --sklearn-args [SKLEARN_ARGS]
                          Additional sklearn parameters in the for of a list
                          "[name1=val1,..,namek=valk]"
    -m MIN_INST_SLICE [MIN_INST_SLICE ...], --min-inst-slice MIN_INST_SLICE [MIN_INST_SLICE ...]
                          Min number of instances in a slice to split by cols
    -a ALPHA [ALPHA ...], --alpha ALPHA [ALPHA ...]
                          Smoothing factor for leaf probability estimation
    --clt-leaves          Whether to use Chow-Liu trees as leaves
    -v [VERBOSE], --verbose [VERBOSE]
                          Verbosity level


To run a grid search you can do:

    ipython -- bin/learnspn_exp.py nltcs -k 2 -c GMM -g 5 10 15 20 -m 10 50 100 500 -a 0.1 0.2 0.5 1.0 2.0 -o exp/learnspn-f/

