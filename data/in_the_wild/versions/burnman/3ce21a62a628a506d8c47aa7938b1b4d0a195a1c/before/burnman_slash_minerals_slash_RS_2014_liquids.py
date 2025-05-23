# BurnMan - a lower mantle toolkit
# Copyright (C) 2012, 2013, Heister, T., Unterborn, C., Rose, I. and Cottaar, S.
# Released under GPL v2 or later.

"""
RS_2014
Liquids from Ramo and Stixrude (2014) FPMD simulations
There are some typos in the article which have been corrected where marked
with the help of David Munoz Ramo.
"""

from burnman import constants
from burnman.mineral import Mineral
from burnman.solidsolution import SolidSolution
from burnman.solutionmodel import *

from ..processchemistry import read_masses, dictionarize_formula, formula_mass
atomic_masses = read_masses()

class Fe2SiO4_liquid(Mineral):
    def __init__(self):
        formula = 'Fe2SiO4'
        formula = dictionarize_formula(formula)
        self.params = {
            'name': 'Fe2SiO4_liquid',
            'formula': formula,
            'equation_of_state': 'rs_l',
            'V_0':  59.7717e-6, # modified for T_0
            'T_0':  1900., # corrected
            'O_theta': 1 ,
            'O_f': 4 ,
            'm': 0.6 ,
            'a': np.array([[-4252948.0, 997810.188],
                           [-599315.125, 12032.8936], 
                           [12572739., 7299239.5],
                           [53442800.0, -26791676.0],
                           [52981912.0, 0.]]), # corrected order
            'zeta_0': 0.0161350928 , # 0.0166734, # the comment is a refit to David's dataset
            'xi': 0.34431043 , # 0.34431053, # the comment is a refit to David's dataset
            'Tel_0': 1919.3553 , # 1921.6813, # the comment is a refit to David's dataset
            'eta': 0.0127067110 , # 0.0127067, # the comment is a refit to David's dataset
            'spin_a': [-0.00011134, 0.00010863],
            'spin_b': [3.53793, -3.81421, 2.83703, -0.676241],
            'n': sum(formula.values()),
            'molar_mass': formula_mass(formula, atomic_masses)}
        Mineral.__init__(self)

