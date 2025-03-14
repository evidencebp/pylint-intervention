# ======================================================================
# matscipy - Python materials science tools
# https://github.com/libAtoms/matscipy
#
# Copyright (2014-2018) James Kermode, King's College London
#                       Lars Pastewka, University of Freiburg
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ======================================================================

"""
Simple pair potential.
"""

from __future__ import division

import os

import sys

import time

import numpy as np

import ase
from ase.calculators.calculator import Calculator

from matscipy.neighbours import neighbour_list, first_neighbours


### 

class LennardJonesCut():
    """
    Functional form for a 12-6 Lennard-Jones potential with a hard cutoff.
    Energy is shifted to zero at cutoff.
    """

    def __init__(self, epsilon, sigma, cutoff):
        self.epsilon = epsilon
        self.sigma = sigma 
        self.cutoff = cutoff
        self.offset = (sigma/cutoff)**12 -(sigma/cutoff)**6

    def __call__(self, r):
        """
        Return function value (potential energy).
        """
        r6 = (self.sigma / r)**6
        return 4 * self.epsilon * ((r6 - 1) * r6 - self.offset)

    def get_cutoff(self):
        return self.cutoff

    def first_derivative(self, r):
        r = (self.sigma / r)
        r6 = r**6
        return -24 * self.epsilon / self.sigma * (2 * r6 - 1) * r6 * r

    def second_derivative(self, r):
        r2 = (self.sigma / r)**2
        r6 = r2**3
        return 24 * self.epsilon/self.sigma**2 * (26 * r6 - 7) * r6 * r2

    def derivative(self, n=1):
        if n == 1:
            return self.first_derivative
        elif n == 2:
            return self.second_derivative
        else:
            raise ValueError("Don't know how to compute {}-th derivative.".format(n))

###

class LennardJonesQuadratic():
    """
    Functional form for a 12-6 Lennard-Jones potential with a soft cutoff.
    Energy, its first and second derivative are shifted to zero at cutoff.
    """

    def __init__(self, epsilon, sigma, cutoff):
        self.epsilon = epsilon
        self.sigma = sigma 
        self.cutoff = cutoff 
        self.offset_energy = (sigma/cutoff)**12 -(sigma/cutoff)**6
        self.offset_force = 6/cutoff * (-2 * (sigma/cutoff)**12 + (sigma/cutoff)**6)
        self.offset_dforce = (1/cutoff**2) * (156 * (sigma/cutoff)**12 - 42 * (sigma/cutoff)**6)
    
    def get_cutoff(self):
        return self.cutoff

    def __call__(self, r):
        """
        Return function value (potential energy).
        """
        r6 = (self.sigma / r)**6
        return 4 * self.epsilon * ((r6 - 1) * r6 - self.offset_energy - (r - self.cutoff) * self.offset_force - ((r - self.cutoff)**2 /2) * self.offset_dforce)

    def first_derivative(self, r):
        r6 = (self.sigma / r)**6
        return 4 * self.epsilon * ((6/r) * (-2 * r6 + 1 ) * r6 - self.offset_force - (r - self.cutoff) * self.offset_dforce)

    def second_derivative(self, r):
        r6 = (self.sigma / r)**6
        return 4 * self.epsilon * ((1/r**2) * (156 * r6 - 42) * r6 - self.offset_dforce)

    def derivative(self, n=1):
        if n == 1:
            return self.first_derivative
        elif n == 2:
            return self.second_derivative
        else:
            raise ValueError("Don't know how to compute {}-th derivative.".format(n))

###
class LennardJonesLinear()
    """
    Function form of a 12-6 Lennard-Jones potential with a soft cutoff
    The energy and the force are shifted at the cutoff.
    """

    def __init__(self, epsilon, sigma, cutoff):
        self.epsilon = epsilon
        self.sigma = sigma 
        self.cutoff = cutoff 
        self.offset_energy = (sigma/cutoff)**12 -(sigma/cutoff)**6
        self.offset_force = 6/cutoff * (-2 * (sigma/cutoff)**12 + (sigma/cutoff)**6)

    def get_cutoff():
        return self.cutoff

    def __call__(self, r):
        """
        Return function value (potential energy).
        """
        r6 = (self.sigma / r)**6
        return 4 * self.epsilon * ((r6 - 1) * r6 - self.offset_energy - (r - self.cutoff) * self.offset_force)

    def first_derivative(self, r):
        r6 = (self.sigma / r)**6
        return 4 * self.epsilon * ((6/r) * (-2 * r6 + 1 ) * r6 - self.offset_force)

    def second_derivative(self, r):
        r6 = (self.sigma / r)**6
        return 4 * self.epsilon * ((1/r**2) * (156 * r6 - 42) * r6)

    def derivative(self, n=1):
        if n == 1:
            return self.first_derivative
        elif n == 2:
            return self.second_derivative
        else:
            raise ValueError("Don't know how to compute {}-th derivative.".format(n))


###

class LennardJones


###


class PairPotential(Calculator):
    implemented_properties = ['energy', 'stress', 'forces', "hessian"]
    default_parameters = {}
    name = 'PairPotential'

    def __init__(self, f, cutoff=None):
        Calculator.__init__(self)
        self.f = f

        self.dict = {x: obj.get_cutoff() for x,obj in f.items()}
        self.df = {x: obj.derivative(1) for x,obj in f.items()}
        self.df2 = {x: obj.derivative(2) for x,obj in f.items()}

    def calculate(self, atoms, properties, system_changes):
        Calculator.calculate(self, atoms, properties, system_changes)

        nat = len(self.atoms)
        atnums = self.atoms.numbers
        atnums_in_system = set(atnums)

        i_n, j_n, dr_nc, abs_dr_n = neighbour_list('ijDd', self.atoms, self.dict)

        e_n = np.zeros_like(abs_dr_n)
        de_n = np.zeros_like(abs_dr_n)
        for params, pair in enumerate(self.dict):
            if pair[0] == pair[1]:
                mask1 = atnums[i_n] == pair[0]
                mask2 = atnums[j_n] == pair[0]
                mask = np.logical_and(mask1, mask2)

                e_n[mask] = self.f[pair](abs_dr_n[mask])
                de_n[mask] = self.df[pair](abs_dr_n[mask])

            if pair[0] != pair[1]:
                mask1 = np.logical_and(atnums[i_n] == pair[0], atnums[j_n] == pair[1])
                mask2 = np.logical_and(atnums[i_n] == pair[1], atnums[j_n] == pair[0])
                mask = np.logical_or(mask1, mask2)

                e_n[mask] = self.f[pair](abs_dr_n[mask])
                de_n[mask] = self.df[pair](abs_dr_n[mask]) 

        epot = 0.5*np.sum(e_n)

        # Forces
        df_nc = -0.5*de_n.reshape(-1,1)*dr_nc/abs_dr_n.reshape(-1,1)

        # Sum for each atom
        fx_i = np.bincount(j_n, weights=df_nc[:,0], minlength=nat) - \
            np.bincount(i_n, weights=df_nc[:,0], minlength=nat)
        fy_i = np.bincount(j_n, weights=df_nc[:,1], minlength=nat) - \
            np.bincount(i_n, weights=df_nc[:,1], minlength=nat)
        fz_i = np.bincount(j_n, weights=df_nc[:,2], minlength=nat) - \
            np.bincount(i_n, weights=df_nc[:,2], minlength=nat)

        # Virial
        virial_v = -np.array([dr_nc[:,0]*df_nc[:,0],               # xx
                              dr_nc[:,1]*df_nc[:,1],               # yy
                              dr_nc[:,2]*df_nc[:,2],               # zz
                              dr_nc[:,1]*df_nc[:,2],               # yz
                              dr_nc[:,0]*df_nc[:,2],               # xz
                              dr_nc[:,0]*df_nc[:,1]]).sum(axis=1)  # xy


        self.results = {'energy': epot,
                        'stress': virial_v/self.atoms.get_volume(),
                        'forces': np.transpose([fx_i, fy_i, fz_i])}

    ###

    def hessian_matrix(f, atoms, H_format="dense"):
        """
        Calculate the Hessian matrix for a pair potential

        Parameters
        ----------
        atoms: ase.Atoms
            Atomic configuration in a local minima 
        H_format: "dense" or "sparse"
            Output format of the hessian matrix      
        """

        if H_format == "sparse":
            try:
                from scipy.sparse import bsr_matrix
            except:
                print("Changing format to dense since scipy.sparse could not be loaded!")
                H_format = "dense"


        dict = {x: obj.get_cutoff() for x,obj in f.items()}
        df = {x: obj.derivative(1) for x,obj in f.items()}
        df2 = {x: obj.derivative(2) for x,obj in f.items()}

        nat = len(atoms)
        atnums = atoms.numbers

        i_n, j_n, dr_nc, abs_dr_n = neighbour_list('ijDd', atoms, dict)
        first_i = first_neighbours(nat, i_n)

        e_n = np.zeros_like(abs_dr_n)
        de_n = np.zeros_like(abs_dr_n)
        dde_n = np.zeros_like(abs_dr_n)
        for params, pair in enumerate(dict):
            if pair[0] == pair[1]:
                mask1 = atnums[i_n] == pair[0]
                mask2 = atnums[j_n] == pair[0]
                mask = np.logical_and(mask1, mask2)

                e_n[mask] = f[pair](abs_dr_n[mask])
                de_n[mask] = df[pair](abs_dr_n[mask])
                dde_n[mask] = df2[pair](abs_dr_n[mask])

            if pair[0] != pair[1]:
                mask1 = np.logical_and(atnums[i_n] == pair[0], atnums[j_n] == pair[1])
                mask2 = np.logical_and(atnums[i_n] == pair[1], atnums[j_n] == pair[0])
                mask = np.logical_or(mask1, mask2)

                e_n[mask] = f[pair](abs_dr_n[mask])
                de_n[mask] = df[pair](abs_dr_n[mask]) 
                dde_n[mask] = df2[pair](abs_dr_n[mask])

        # Sparse BSR-matrix
        if H_format == "sparse":
            e_nc = (dr_nc.T/abs_dr_n).T
            H_ncc = -(dde_n * (e_nc.reshape(-1,3,1) * e_nc.reshape(-1,1,3)).T).T
            H_ncc += -(de_n/abs_dr_n * (np.eye(3, dtype=e_nc.dtype) - (e_nc.reshape(-1,3,1) * e_nc.reshape(-1,1,3))).T).T

            H = bsr_matrix((H_ncc, j_n, first_i), shape=(3*nat,3*nat))

            Hdiag_icc = np.empty((nat,3,3))
            for x in range(3):
                for y in range(3):
                    Hdiag_icc[:,x,y] = -np.bincount(i_n, weights = H_ncc[:,x,y])

            H += bsr_matrix((Hdiag_icc,np.arange(nat),np.arange(nat+1)), shape=(3*nat,3*nat))
            return H


        # Dense matrix format 
        if H_format == "dense":
            e_nc = (dr_nc.T/abs_dr_n).T
            H_ncc = -(dde_n * (e_nc.reshape(-1,3,1) * e_nc.reshape(-1,1,3)).T).T
            H_ncc += -(de_n/abs_dr_n * (np.eye(3, dtype=e_nc.dtype) - (e_nc.reshape(-1,3,1) * e_nc.reshape(-1,1,3))).T).T

            H = np.zeros((3*nat,3*nat))
            for atom in range(len(i_n)):
                H[H_ncc.shape[1]*i_n[atom]:H_ncc.shape[1]*i_n[atom]+H_ncc.shape[1],H_ncc.shape[2]*j_n[atom]:H_ncc.shape[2]*j_n[atom]+H_ncc.shape[2]] = H_ncc[atom]

            Hdiag_icc = np.empty((nat,3,3))
            for x in range(3):
                for y in range(3):
                    Hdiag_icc[:,x,y] = -np.bincount(i_n, weights = H_ncc[:,x,y])

            Hdiag_ncc = np.zeros((3*nat,3*nat))
            for atom in range(nat):
                Hdiag_ncc[Hdiag_icc.shape[1]*atom:Hdiag_icc.shape[1]*atom+Hdiag_icc.shape[1],Hdiag_icc.shape[2]*atom:Hdiag_icc.shape[2]*atom+Hdiag_icc.shape[2]] = Hdiag_icc[atom]

            H += Hdiag_ncc

            return H