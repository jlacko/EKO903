"""
Available solvers / for the PuLP modeller

"""

import pulp as pl

solver_list = pl.listSolvers(onlyAvailable=True)
