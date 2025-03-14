#
# Copyright 2021 Jan Griesser (U. Freiburg)
#           2021 Lars Pastewka (U. Freiburg)
#
# matscipy - Materials science with Python at the atomic-scale
# https://github.com/libAtoms/matscipy
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
#

"""
Pair potential + Ewald summation
"""

#
# Coding convention
# * All numpy arrays are suffixed with the array dimensions
# * The suffix stands for a certain type of dimension:
#   - n: Atomic index, i.e. array dimension of length nb_atoms
#   - p: Pair index, i.e. array dimension of length nb_pairs
#   - c: Cartesian index, array dimension of length 3
#   - l: Wave vector index, i.e. array of dimension length of k_lc

import numpy as np

from scipy.sparse import bsr_matrix

from scipy.linalg import block_diag

from scipy.sparse.linalg import cg

from scipy.special import erfc

import ase

from ase.calculators.calculator import Calculator

from ...neighbours import neighbour_list, first_neighbours, mic
from ...numpy_tricks import mabincount
from ...elasticity import Voigt_6_to_full_3x3_stress

###

# Charges q are expressed as multiples of the elementary charge e: q = x*e
# e^2/(4*pi*epsilon0) = 14.399645 eV * Angström 
conversion_prefactor = 14.399645

###

class BKSEwald:
    """
    Beest, Kramer, van Santen (BKS) potential.
    Functional form is Buckingham + Coulomb potential

    Buckingham:  
        Energy is shifted to zero at the cutoff.
    Coulomb:   
        Electrostatic interaction is treated using the traditional Ewald summation.
                     
    References
    ----------
    B. W. Van Beest, G. J. Kramer and R. A. Van Santen, Phys. Rev. Lett. 64.16 (1990)
    """

    def __init__(self, A, B, C, alpha, cutoff_r, cutoff_k, nb_kspace, accuracy):
        self.A = A
        self.B = B 
        self.C = C
        self.alpha = alpha
        self.cutoff_r = cutoff_r
        self.cutoff_k = cutoff_k
        self.nb_kspace = nb_kspace
        self.accuracy = accuracy

        # Expression for shifting energy
        self.buck_offset_energy = A * np.exp(-B * cutoff_r) - C / cutoff_r**6

    def get_nb_kspace(self):
        """
        Return triplet of integers defining maximal number of reciprocal points
        """
        return self.nb_kspace

    def get_alpha(self):
        return self.alpha

    def get_cutoff_real(self):
        """
        Cutoff radius for the short range interaction
        """
        return self.cutoff_r

    def get_cutoff_kspace(self):
        """
        Cutoff wave vector in reciprocal space
        """
        return self.cutoff_k

    def get_accuracy(self):
        """
        Accuracy in reciprocal space 
        """
        return self.accuracy
        
    def energy_rspace(self, r, pair_charge, a):
        """
        Potential
        """
        E_buck = self.A * np.exp(-self.B * r) - self.C / r**6 - self.buck_offset_energy 
        E_coul = conversion_prefactor * pair_charge * erfc(a * r) / r

        return E_buck + E_coul

    def first_derivative_rspace(self, r, pair_charge, a):
        """
        First derivative
        """
        f_buck = -self.A * self.B * np.exp(-self.B * r) + 6 * self.C / r**7 
        f_coul = -conversion_prefactor * pair_charge * (erfc(a * r) / r**2
                  + 2 * a * np.exp(-((a * r)**2)) / (np.sqrt(np.pi)*r))

        return f_buck + f_coul

    def second_derivative_rspace(self, r, pair_charge, a):
        """
        Second derivative 
        """
        k_buck = self.A * self.B**2 * np.exp(-self.B * r) - 42 * self.C / r**8
        k_coul = conversion_prefactor * pair_charge * (2 * erfc(a * r) / r**3
                 + 4 * a * np.exp((-(a * r)**2)) / np.sqrt(np.pi) * (1 / r**2 + a**2))

        return k_buck + k_coul

###

class Ewald(Calculator):
    implemented_properties = ["energy", "free_energy", "stress", "forces", "hessian"]
    default_parameters = {}
    name = 'Ewald'

    def __init__(self, f, cutoff=None):
        Calculator.__init__(self)
        self.f = f
        self.initial_cell = None
        self.kvectors = None
        self.initial_I = None
        self.initial_alpha = None
        self.dict = {x: obj.get_cutoff_real() for x, obj in f.items()}

    def determine_alpha(self, charge, acc, cutoff, cell):
        """
        Determine an estimate for alpha on the basis of the cell, cutoff and desired accuracy
        (Adopted from LAMMPS)
        """

        # The kspace rms error is computed relative to the force that two unit point
        # charges exert on each other at a distance of 1 Angström
        accuracy_relative = acc * conversion_prefactor

        qsqsum = conversion_prefactor * np.sum(charge**2)

        a = accuracy_relative * np.sqrt(len(charge) * cutoff * cell[0,0] * cell[1, 1] * cell[2, 2]) / (2 * qsqsum)
        
        if a >= 1.0:
            return (1.35 - 0.15 * np.log(accuracy_relative)) / cutoff

        else:
            return np.sqrt(-np.log(a)) / cutoff

    def determine_nk(self, charge, c, cell, acc, a, natoms):
        """
        Determine the maximal number of points in reciprocal space for each direction,
        and the cutoff in reciprocal space 
        """

        # The kspace rms error is computed relative to the force that two unit point
        # charges exert on each other at a distance of 1 Angström
        accuracy_relative = acc * conversion_prefactor

        nxmax = 1
        nymax = 1
        nzmax = 1
     
        qsqsum = conversion_prefactor * np.sum(charge**2)

        error = c.rms_kspace(nxmax, cell[0, 0], natoms, a, qsqsum)
        while error > (accuracy_relative):
            nxmax += 1
            error = c.rms_kspace(nxmax, cell[0, 0], natoms, a, qsqsum)

        error = c.rms_kspace(nymax, cell[1, 1], natoms, a, qsqsum)
        while error > (accuracy_relative):
            nymax += 1
            error = c.rms_kspace(nymax, cell[1, 1], natoms, a, qsqsum)

        error = c.rms_kspace(nzmax, cell[2, 2], natoms, a, qsqsum)
        while error > (accuracy_relative):
            nzmax += 1
            error = c.rms_kspace(nzmax, cell[2, 2], natoms, a, qsqsum)

        kxmax = 2 * np.pi / cell[0, 0] * nxmax
        kymax = 2 * np.pi / cell[1, 1] * nymax
        kzmax = 2 * np.pi / cell[2, 2] * nzmax
        
        kmax = max(kxmax, kymax, kzmax)

        # Check if box is triclinic --> Scale lattice vectors for triclinic skew
        if np.count_nonzero(cell - np.diag(np.diagonal(cell))) != 9:
            vector = np.array([nxmax / cell[0, 0], nymax / cell[1, 1], nzmax / cell[2, 2]])
            scaled_nbk = np.dot(np.array(np.abs(cell)), vector)
            nxmax = max(1, np.int(scaled_nbk[0]))
            nymax = max(1, np.int(scaled_nbk[1]))
            nzmax = max(1, np.int(scaled_nbk[2]))

        return kmax, np.array([nxmax, nymax, nzmax])

    def determine_kc(self, cell, nk):
        """
        Determine maximal wave vector based in a given integer triplet
        """
        kxmax = 2 * np.pi / cell[0, 0] * nk[0]
        kymax = 2 * np.pi / cell[1, 1] * nk[1]
        kzmax = 2 * np.pi / cell[2, 2] * nk[2]

        return max(kxmax, kymax, kzmax)

    def rms_kspace(self, km, l, n, a, q2):
        """
        Compute the root mean square error of the force in reciprocal space
        
        Reference
        ------------------
        Henrik G. Petersen, The Journal of chemical physics 103.9 (1995)
        """

        return 2 * q2 * a / l * np.sqrt(1 / (np.pi * km * n)) * np.exp(-(np.pi * km / (a * l))**2) 

    def rms_rspace(self, charge, cell, a, rc):
        """
        Compute the root mean square error of the force in real space
        
        Reference
        ------------------
        Henrik G. Petersen, The Journal of chemical physics 103.9 (1995)
        """

        return 2 * np.sum(charge**2) * np.exp(-(a * rc)**2) / np.sqrt(rc * len(charge) * cell[0,0] * cell[1, 1] * cell[2, 2])
 
    def allowed_wave_vectors(self, cell, km, a, nk):
        """
        Compute allowed wave vectors and the prefactor I 
        """
        nx = np.arange(-nk[0], nk[0]+1, 1)
        ny = np.arange(-nk[1], nk[1]+1, 1)
        nz = np.arange(-nk[2], nk[2]+1, 1) 
   
        n_lc = np.array(np.meshgrid(nx, ny, nz)).T.reshape(-1,3)
        
        k_lc = 2 * np.pi * np.dot(np.linalg.inv(np.array(cell)), n_lc.T).T
        
        k = np.linalg.norm(k_lc, axis=1)
        
        mask = np.logical_and(k <= km, k != 0)

        return np.exp(-(k[mask] / (2 * a))**2) / k[mask]**2, k_lc[mask]

    def self_energy(self, charge, a):
        """
        Return the self energy
        """
        return -conversion_prefactor * a * np.sum(charge**2) / np.sqrt(np.pi)

    def kspace_energy(self, charge, pos, vol, I, k):
        """
        Return the energy from the reciprocal space contribution
        """

        structure_factor_l = np.sum(charge * np.exp(1j * np.tensordot(k, pos, axes=((1),(1)))), axis=1)

        return conversion_prefactor * 2 * np.pi * np.sum(I * np.absolute(structure_factor_l)**2) / vol

    def first_derivative_kspace(self, charge, natoms, vol, pos, I, k):
        """
        Return the kspace part of the force 
        """
        n = len(pos)

        phase_ln = np.tensordot(k, pos, axes=((1),(1)))

        cos_ln = np.cos(phase_ln) 
        sin_ln = np.sin(phase_ln)

        cos_sin_ln = (cos_ln.T * np.sum(charge * sin_ln, axis=1)).T
        sin_cos_ln = (sin_ln.T * np.sum(charge * cos_ln, axis=1)).T

        prefactor_ln = (I * (cos_sin_ln - sin_cos_ln).T).T

        f_nc = np.sum(k.reshape(-1, 1, 3) * prefactor_ln.reshape(-1, n, 1), axis=0)

        return -conversion_prefactor * 4 * np.pi * (charge * f_nc.T).T / vol

    def stress_kspace(self, charge, pos, vol, a, I, k):
        """
        Return the stress contribution of the long-range Coulomb part
        """
        sqk_l = np.sum(k * k, axis=1) 

        structure_factor_l = np.sum(charge * np.exp(1j * np.tensordot(k, pos, axes=((1),(1)))), axis=1)

        wave_vectors_lcc = (k.reshape(-1, 3, 1) * k.reshape(-1, 1, 3)) * (1 / (2 * a**2) + 2 / sqk_l).reshape(-1, 1, 1) - np.identity(3)

        stress_lcc = (I * np.absolute(structure_factor_l)**2).reshape(len(I), 1, 1) * wave_vectors_lcc
        
        stress_cc = np.sum(stress_lcc, axis=0)
        
        stress_cc *= (conversion_prefactor * 2 * np.pi / vol)

        return np.array([stress_cc[0, 0],        # xx
                         stress_cc[1, 1],        # yy
                         stress_cc[2, 2],        # zz
                         stress_cc[1, 2],        # yz
                         stress_cc[0, 2],        # xz
                         stress_cc[0, 1]])       # xy


    def calculate(self, atoms, properties, system_changes):
        Calculator.calculate(self, atoms, properties, system_changes)

        nb_atoms = len(self.atoms)
        atnums = self.atoms.numbers
        atnums_in_system = set(atnums)

        if atoms.has("charge"):
            charge_n = self.atoms.get_array("charge")
        else:
            raise AttributeError(
                "Attribute error: Unable to load atom charges from atoms object!")

        if np.sum(charge_n) > 1e-3:
            print("Net charge: ", np.sum(charge_n))
            raise AttributeError(
                "Attribute error: System is not charge neutral!")      

        if not any(self.atoms.get_pbc()):
            raise AttributeError(
                "Attribute error: This code only works for 3D systems with periodic boundaries!")    

        for index, pairs in enumerate(self.f.values()):
            if index == 0:
                alpha = pairs.get_alpha()
                rc = pairs.get_cutoff_real()
                kc = pairs.get_cutoff_kspace()
                nbk_c = pairs.get_nb_kspace()
                accuracy = pairs.get_accuracy()
            else:
                if ((rc != pairs.get_cutoff_real()) 
                     or (kc != pairs.get_cutoff_kspace()) 
                     or (alpha != pairs.get_alpha()) 
                     or (accuracy != pairs.get_accuracy())):
                    raise AttributeError(
                        "Attribute error: Cannot use different rc, kc, number of wave vectors or accuracy!")     


        # If cell has changed --> Recompute wave vectors, parameters and errors
        if np.all(self.initial_cell == None):

            self.initial_cell = atoms.get_cell()

            if alpha == None:
                alpha = self.determine_alpha(charge_n, accuracy, rc, atoms.get_cell())

            if np.any(nbk_c) == None:
                kc, nbk_c = self.determine_nk(charge_n, atoms.get_calculator(), atoms.get_cell(), accuracy, alpha, nb_atoms)    

            if np.all(nbk_c) != None and kc == None:
                kc = self.determine_kc(atoms.get_cell(), nbk_c)

            self.initial_alpha = alpha 

            I_l, k_lc = self.allowed_wave_vectors(atoms.get_cell(), kc, alpha, nbk_c)

            self.kvectors = k_lc
            self.initial_I = I_l

            # 
            rms_rspace = self.rms_rspace(charge_n, atoms.get_cell(), alpha, rc)
            rms_kspace_x = self.rms_kspace(nbk_c[0], atoms.get_cell()[0, 0], nb_atoms, alpha, conversion_prefactor * np.sum(charge_n**2))
            rms_kspace_y = self.rms_kspace(nbk_c[1], atoms.get_cell()[1, 1], nb_atoms, alpha, conversion_prefactor * np.sum(charge_n**2))
            rms_kspace_z = self.rms_kspace(nbk_c[2], atoms.get_cell()[2, 2], nb_atoms, alpha, conversion_prefactor * np.sum(charge_n**2))

            print("Estimated alpha: ", alpha)
            print("Number of wave vectors: ", k_lc.shape[0])
            print("Cutoff for kspace vectors: ", kc)
            print("Estimated kspace triplets nx/ny/nx: ", nbk_c[0], "/", nbk_c[1], "/", nbk_c[2]) 
            print("Estimated absolute RMS force accuracy (Real space): ", np.absolute(rms_rspace))
            print("Estimated absolute RMS force accuracy (Kspace): ", np.sqrt(rms_kspace_x**2 + rms_kspace_y**2 + rms_kspace_z**2))

        elif np.any(self.initial_cell != atoms.get_cell()):

            self.initial_cell = atoms.get_cell()

            if alpha == None:
                alpha = self.determine_alpha(charge_n, accuracy, rc, atoms.get_cell())

            if np.any(nbk_c) == None:
                kc, nbk_c = self.determine_nk(charge_n, atoms.get_calculator(), atoms.get_cell(), accuracy, alpha, nb_atoms)    

            if np.all(nbk_c) != None and kc == None:
                kc = self.determine_kc(atoms.get_cell(), nbk_c)

            self.initial_alpha = alpha 

            # Prefactor and wave vectors for reciprocal space 
            I_l, k_lc = self.allowed_wave_vectors(atoms.get_cell(), kc, alpha, nbk_c)

            self.kvectors = k_lc
            self.initial_I = I_l

            # Compute and print error estimates and kspace parameters
            rms_rspace = self.rms_rspace(charge_n, atoms.get_cell(), alpha, rc)
            rms_kspace_x = self.rms_kspace(nbk_c[0], atoms.get_cell()[0, 0], nb_atoms, alpha, conversion_prefactor * np.sum(charge_n**2))
            rms_kspace_y = self.rms_kspace(nbk_c[1], atoms.get_cell()[1, 1], nb_atoms, alpha, conversion_prefactor * np.sum(charge_n**2))
            rms_kspace_z = self.rms_kspace(nbk_c[2], atoms.get_cell()[2, 2], nb_atoms, alpha, conversion_prefactor * np.sum(charge_n**2))

            print("Estimated alpha: ", alpha)
            print("Number of wave vectors: ", k_lc.shape[0])
            print("Cutoff for kspace vectors: ", kc)
            print("Estimated kspace triplets nx/ny/nx: ", nbk_c[0], "/", nbk_c[1], "/", nbk_c[2]) 
            print("Estimated absolute RMS force accuracy (Real space): ", np.absolute(rms_rspace))
            print("Estimated absolute RMS force accuracy (Kspace): ", np.sqrt(rms_kspace_x**2 + rms_kspace_y**2 + rms_kspace_z**2))

        elif np.all(self.initial_cell == atoms.get_cell()):
            k_lc = self.kvectors
            I_l = self.initial_I
            alpha = self.initial_alpha

        # Neighbor list for short range interaction
        i_p, j_p, r_p, r_pc = neighbour_list('ijdD', self.atoms, self.dict)
        chargeij = charge_n[i_p] * charge_n[j_p]

        if np.sum(i_p == j_p) > 1e-5:
            print("Atoms can see themselves!")

        # Short-range interaction of Buckingham and Ewald
        e_p = np.zeros_like(r_p)
        de_p = np.zeros_like(r_p)
        for params, pair in enumerate(self.dict):
            if pair[0] == pair[1]:
                mask1 = atnums[i_p] == pair[0]
                mask2 = atnums[j_p] == pair[0]
                mask = np.logical_and(mask1, mask2)

                e_p[mask] = self.f[pair].energy_rspace(r_p[mask], chargeij[mask], alpha)
                de_p[mask] = self.f[pair].first_derivative_rspace(r_p[mask], chargeij[mask], alpha)

            if pair[0] != pair[1]:
                mask1 = np.logical_and(
                    atnums[i_p] == pair[0], atnums[j_p] == pair[1])
                mask2 = np.logical_and(
                    atnums[i_p] == pair[1], atnums[j_p] == pair[0])
                mask = np.logical_or(mask1, mask2)

                e_p[mask] = self.f[pair].energy_rspace(r_p[mask], chargeij[mask], alpha)
                de_p[mask] = self.f[pair].first_derivative_rspace(r_p[mask], chargeij[mask], alpha)


        # Energy 
        e_self = self.self_energy(charge_n, alpha)

        e_long = self.kspace_energy(charge_n, atoms.get_positions(), atoms.get_volume(), I_l, k_lc)

        epot = 0.5 * np.sum(e_p) + e_self + e_long 

        # Forces
        df_pc = -0.5 * de_p.reshape(-1, 1) * r_pc / r_p.reshape(-1, 1) 

        f_nc = mabincount(j_p, df_pc, nb_atoms) - mabincount(i_p, df_pc, nb_atoms)

        f_nc += self.first_derivative_kspace(charge_n, nb_atoms, atoms.get_volume(), atoms.get_positions(), I_l, k_lc)

        # Virial
        virial_v = -np.array([r_pc[:, 0] * df_pc[:, 0],               # xx
                              r_pc[:, 1] * df_pc[:, 1],               # yy
                              r_pc[:, 2] * df_pc[:, 2],               # zz
                              r_pc[:, 1] * df_pc[:, 2],               # yz
                              r_pc[:, 0] * df_pc[:, 2],               # xz
                              r_pc[:, 0] * df_pc[:, 1]]).sum(axis=1)  # xy

        virial_v += self.stress_kspace(charge_n, atoms.get_positions(), atoms.get_volume(), alpha, I_l, k_lc) 

        self.results = {'energy': epot,
                        'free_energy': epot,
                        'stress': virial_v/self.atoms.get_volume(),
                        'forces': f_nc}

    ###

    def hessian_rspace(self, atoms, format='sparse', divide_by_masses=False):
        """
        Calculate the Hessian matrix for the short range part.

        Parameters
        ----------
        atoms: ase.Atoms
            Atomic configuration in a local or global minima.

        format: "dense" or "neighbour-list"
            Output format of the hessian matrix.

        divide_by_masses: bool
            if true return the dynamical matrix else the Hessian matrix 

        Restrictions
        ----------
        This method is currently only implemented for three dimensional systems
        """

        f = self.f
        nb_atoms = len(atoms)
        atnums = atoms.numbers

        if atoms.has("charge"):
            charge_n = atoms.get_array("charge")
        else:
            raise AttributeError(
                "Attribute error: Unable to load atom charges from atoms object!")

        if np.sum(charge_n) > 1e-3:
            print("Net charge: ", np.sum(charge_n))
            raise AttributeError(
                "Attribute error: System is not charge neutral!")      

        if not any(atoms.get_pbc()):
            raise AttributeError(
                "Attribute error: This code only works for 3D systems with periodic boundaries!")    

        for index, pairs in enumerate(self.f.values()):
            if index == 0:
                alpha = pairs.get_alpha()
                rc = pairs.get_cutoff_real()
                accuracy = pairs.get_accuracy()
            else:
                if ((rc != pairs.get_cutoff_real()) 
                     or (alpha != pairs.get_alpha()) 
                     or (accuracy != pairs.get_accuracy())):
                    raise AttributeError(
                         "Attribute error: Cannot use different rc, number of wave vectors or accuracy!")   

        if alpha == None:
            alpha = self.determine_alpha(charge_n, accuracy, rc, atoms.get_cell())

        print("Rspace parameters:")
        print("----------------------------")
        print("Estimated alpha: ", alpha)

        i_p, j_p, r_p, r_pc = neighbour_list('ijdD', atoms, self.dict)
        chargeij = charge_n[i_p] * charge_n[j_p]
        first_i = first_neighbours(nb_atoms, i_p)

        if np.sum(i_p == j_p) > 1e-5:
            print("Atoms can see themselves!")

        de_p = np.zeros_like(r_p)
        dde_p = np.zeros_like(r_p)
        for params, pair in enumerate(self.dict):
            if pair[0] == pair[1]:
                mask1 = atnums[i_p] == pair[0]
                mask2 = atnums[j_p] == pair[0]
                mask = np.logical_and(mask1, mask2)

                de_p[mask] = f[pair].first_derivative_rspace(r_p[mask], chargeij[mask], alpha)
                dde_p[mask] = f[pair].second_derivative_rspace(r_p[mask], chargeij[mask], alpha)

            if pair[0] != pair[1]:
                mask1 = np.logical_and(
                    atnums[i_p] == pair[0], atnums[j_p] == pair[1])
                mask2 = np.logical_and(
                    atnums[i_p] == pair[1], atnums[j_p] == pair[0])
                mask = np.logical_or(mask1, mask2)

                de_p[mask] = f[pair].first_derivative_rspace(r_p[mask], chargeij[mask], alpha)
                dde_p[mask] = f[pair].second_derivative_rspace(r_p[mask], chargeij[mask], alpha)
        
        n_pc = (r_pc.T / r_p).T
        H_pcc = -(dde_p * (n_pc.reshape(-1, 3, 1)
                           * n_pc.reshape(-1, 1, 3)).T).T
        H_pcc += -(de_p / r_p * (np.eye(3, dtype=n_pc.dtype)
                                    - (n_pc.reshape(-1, 3, 1) * n_pc.reshape(-1, 1, 3))).T).T

        # Sparse BSR-matrix
        if format == "sparse":
            if divide_by_masses:
                masses_n = atoms.get_masses()
                geom_mean_mass_p = np.sqrt(masses_n[i_p]*masses_n[j_p])

            if divide_by_masses:
                H = bsr_matrix(((H_pcc.T/geom_mean_mass_p).T, j_p, first_i), shape=(3*nb_atoms, 3*nb_atoms))

            else: 
                H = bsr_matrix((H_pcc, j_p, first_i), shape=(3*nb_atoms, 3*nb_atoms))

            Hdiag_icc = np.empty((nb_atoms, 3, 3))
            for x in range(3):
                for y in range(3):
                    Hdiag_icc[:, x, y] = - \
                        np.bincount(i_p, weights=H_pcc[:, x, y])

            if divide_by_masses:
                H += bsr_matrix(((Hdiag_icc.T/masses_n).T, np.arange(nb_atoms),
                             np.arange(nb_atoms+1)), shape=(3*nb_atoms, 3*nb_atoms))

            else:
                H += bsr_matrix((Hdiag_icc, np.arange(nb_atoms),
                             np.arange(nb_atoms+1)), shape=(3*nb_atoms, 3*nb_atoms))

            return H

        # Neighbour list format
        elif format == "neighbour-list":
            return H_pcc, i_p, j_p, r_pc, r_p

        else:
           raise AttributeError(
                "Attribute error: Can not return a Hessian matrix using the given format!")                

    ###

    def kspace_properties(self, atoms, prop="Hessian", divide_by_masses=False):
        """
        Calculate the recirprocal contributiom to the Hessian, the non-affine forces and the Born elastic constants

        Parameters
        ----------
        atoms: ase.Atoms
            Atomic configuration in a local or global minima.

        prop: "Hessian", "Born" or "Naforces"
            Compute either the Hessian/Dynamical matrix, the Born constants 
            or the non-affine forces.

        divide_by_masses: bool
            if true return the dynamic matrix else Hessian matrix 

        Restrictions
        ----------
        This method is currently only implemented for three dimensional systems
        """
        f = self.f
        nb_atoms = len(atoms)

        if atoms.has("charge"):
            charge_n = atoms.get_array("charge")
        else:
            raise AttributeError(
                "Attribute error: Unable to load atom charges from atoms object!")

        if np.sum(charge_n) > 1e-3:
            print("Net charge: ", np.sum(charge_n))
            raise AttributeError(
                "Attribute error: System is not charge neutral!")      

        if not any(atoms.get_pbc()):
            raise AttributeError(
                "Attribute error: This code only works for 3D systems with periodic boundaries!")    

        for index, pairs in enumerate(self.f.values()):
            if index == 0:
                alpha = pairs.get_alpha()
                rc = pairs.get_cutoff_real()
                kc = pairs.get_cutoff_kspace()
                nbk_c = pairs.get_nb_kspace()
                accuracy = pairs.get_accuracy()
            else:
                if ((rc != pairs.get_cutoff_real()) 
                     or (kc != pairs.get_cutoff_kspace()) 
                     or (alpha != pairs.get_alpha()) 
                     or (accuracy != pairs.get_accuracy())):
                    raise AttributeError(
                        "Attribute error: Cannot use different rc, kc, number of wave vectors or accuracy!")  

        if alpha == None:
            alpha = self.determine_alpha(charge_n, accuracy, rc, atoms.get_cell())

        if np.any(nbk_c) == None:
            kc, nbk_c = self.determine_nk(charge_n, atoms.get_calculator(), atoms.get_cell(), accuracy, alpha, nb_atoms)    

        if np.all(nbk_c) != None and kc == None:
            kc = self.determine_kc(atoms.get_cell(), nbk_c)

        I_l, k_lc = self.allowed_wave_vectors(atoms.get_cell(), kc, alpha, nbk_c)

        # Compute and print error estimates
        rms_rspace = self.rms_rspace(charge_n, atoms.get_cell(), alpha, rc)
        rms_kspace_x = self.rms_kspace(nbk_c[0], atoms.get_cell()[0, 0], nb_atoms, alpha, conversion_prefactor*np.sum(charge_n**2))
        rms_kspace_y = self.rms_kspace(nbk_c[1], atoms.get_cell()[1, 1], nb_atoms, alpha, conversion_prefactor*np.sum(charge_n**2))
        rms_kspace_z = self.rms_kspace(nbk_c[2], atoms.get_cell()[2, 2], nb_atoms, alpha, conversion_prefactor*np.sum(charge_n**2))

        print("Kspace parameters:")
        print("----------------------------")
        print("Estimated alpha: ", alpha)
        print("Number of wave vectors: ", k_lc.shape[0])
        print("Cutoff for kspace vectors: ", kc)
        print("Estimated kspace vectors nx/ny/nx: ", nbk_c[0], "/", nbk_c[1], "/", nbk_c[2]) 
        print("Estimated absolute RMS force accuracy (Real space): ", np.absolute(rms_rspace))
        print("Estimated absolute RMS force accuracy (Kspace): ", np.sqrt(rms_kspace_x**2 + rms_kspace_y**2 + rms_kspace_z**2))

        if prop == "Hessian":  
            H = np.zeros((3*nb_atoms, 3*nb_atoms))

            pos = atoms.get_positions()

            for i, k in enumerate(k_lc):
                phase_l = np.sum(k * pos, axis=1)

                I_sqcos_sqsin = I_l[i] * (np.cos(phase_l).reshape(-1, 1) * np.cos(phase_l).reshape(1, -1) + 
                                          np.sin(phase_l).reshape(-1, 1) * np.sin(phase_l).reshape(1, -1))

                I_sqcos_sqsin[range(nb_atoms), range(nb_atoms)] = 0.0

                H += np.concatenate(np.concatenate(k.reshape(1, 1, 3, 1) * k.reshape(1, 1, 1, 3) * I_sqcos_sqsin.reshape(nb_atoms, nb_atoms, 1, 1), axis=2), axis=0)

            H *= (conversion_prefactor * 4 * np.pi  / atoms.get_volume()) * charge_n.repeat(3).reshape(-1, 1) * charge_n.repeat(3).reshape(1, -1)

            Hdiag = np.zeros((3*nb_atoms, 3))
            for x in range(3):
                Hdiag[:, x] = -np.sum(H[:,x::3], axis=1)
         
            Hdiag = block_diag(*Hdiag.reshape(nb_atoms, 3, 3))

            H += Hdiag

            if divide_by_masses:
                masses_p = (atoms.get_masses()).repeat(3)
                H /= np.sqrt(masses_p.reshape(-1, 1)*masses_p.reshape(1, -1))

            return H 

        elif prop == "Born":
            delta_ab = np.identity(3)
            sqk_l = np.sum(k_lc * k_lc, axis=1) 

            structure_factor_l = np.sum(charge_n * np.exp(1j * np.tensordot(k_lc, atoms.get_positions(), axes=((1),(1)))), axis=1)
            prefactor_l = (I_l * np.absolute(structure_factor_l)**2).reshape(-1, 1, 1, 1, 1)

            # First expression
            first_abab = delta_ab.reshape(1, 3, 3, 1, 1) * delta_ab.reshape(1, 1, 1, 3, 3) + \
                         delta_ab.reshape(1, 1, 3, 3, 1) * delta_ab.reshape(1, 3, 1, 1, 3)

            # Second expression 
            prefactor_second_l = -(1 / (2 * alpha**2) + 2 / sqk_l).reshape(-1, 1, 1, 1, 1)
            second_labab = k_lc.reshape(-1, 1, 1, 3, 1) * k_lc.reshape(-1, 1, 1, 1, 3) * delta_ab.reshape(1, 3, 3, 1, 1) + \
                           k_lc.reshape(-1, 3, 1, 1, 1) * k_lc.reshape(-1, 1, 1, 3, 1) * delta_ab.reshape(1, 1, 3, 1, 3) + \
                           k_lc.reshape(-1, 3, 1, 1, 1) * k_lc.reshape(-1, 1, 3, 1, 1) * delta_ab.reshape(1, 1, 1, 3, 3) + \
                           k_lc.reshape(-1, 1, 3, 1, 1) * k_lc.reshape(-1, 1, 1, 3, 1) * delta_ab.reshape(1, 3, 1, 1, 3) + \
                           k_lc.reshape(-1, 3, 1, 1, 1) * k_lc.reshape(-1, 1, 1, 1, 3) * delta_ab.reshape(1, 1, 3, 3, 1)

            # Third expression
            prefactor_third_l = (1 / (4 * alpha**4) + 2 / (alpha**2 * sqk_l) + 8 / sqk_l**2).reshape(-1, 1, 1, 1, 1)
            third_labab = k_lc.reshape(-1, 3, 1, 1, 1) * k_lc.reshape(-1, 1, 3, 1, 1) * k_lc.reshape(-1, 1, 1, 3, 1) * k_lc.reshape(-1 ,1, 1, 1, 3)

            C_labab = prefactor_l * (first_abab + prefactor_second_l * second_labab + prefactor_third_l * third_labab)

            return conversion_prefactor * 2 * np.pi * np.sum(C_labab, axis=0) / atoms.get_volume()**2

        elif prop == "Naforces":
            delta_ab = np.identity(3)
            sqk_l = np.sum(k_lc * k_lc, axis=1) 

            phase_ln = np.tensordot(k_lc, atoms.get_positions(), axes=((1),(1)))

            cos_ln = np.cos(phase_ln) 
            sin_ln = np.sin(phase_ln)

            cos_sin_ln = (cos_ln.T * np.sum(charge_n * sin_ln, axis=1)).T
            sin_cos_ln = (sin_ln.T * np.sum(charge_n * cos_ln, axis=1)).T

            prefactor_ln = (I_l * (cos_sin_ln - sin_cos_ln).T).T

            # First expression
            first_lccc = (1 / (2 * alpha**2) + 2 / sqk_l).reshape(-1, 1, 1, 1) * \
                         k_lc.reshape(-1, 1, 1, 3) * k_lc.reshape(-1, 3, 1, 1) * k_lc.reshape(-1, 1, 3, 1)
                         
            # Second expression
            second_lccc = -(k_lc.reshape(-1, 3, 1, 1) * delta_ab.reshape(-1, 1, 3, 3) + 
                            k_lc.reshape(-1, 1, 3, 1) * delta_ab.reshape(-1, 3, 1, 3))

            naforces_nccc = np.sum(prefactor_ln.reshape(-1, nb_atoms, 1, 1, 1) * (first_lccc + second_lccc).reshape(-1, 1, 3, 3, 3), axis=0)

            return -conversion_prefactor * 4 * np.pi * (charge_n * naforces_nccc.T).T / atoms.get_volume()

    ###

    def get_hessian(self, atoms):
        """
        Compute the real space + kspace Hessian
        """
        H = self.hessian_rspace(atoms, format="sparse").todense()
        H += self.kspace_properties(atoms, prop="Hessian")

        return H

    ###

    def get_nonaffine_forces(self, atoms):
        """
        Compute the non-affine forces which result from an affine deformation of atoms.

        Parameters
        ----------
        atoms: ase.Atoms
            Atomic configuration in a local or global minima.

        """

        nat = len(atoms)

        # Rspace 
        H_pcc, i_p, j_p, dr_pc, abs_dr_p = self.hessian_rspace(atoms, "neighbour-list")
        naF_pcab = -0.5 * H_pcc.reshape(-1, 3, 3, 1) * dr_pc.reshape(-1, 1, 1, 3)
        naforces_icab = mabincount(i_p, naF_pcab, nat) - mabincount(j_p, naF_pcab, nat)

        # Kspace
        naforces_icab += self.kspace_properties(atoms, prop="Naforces")

        return naforces_icab  

    ###

    def get_born_elastic_constants(self, atoms):
        """
        Compute the Born elastic constants. 

        Parameters
        ----------
        atoms: ase.Atoms
            Atomic configuration in a local or global minima.

        """
        # Contribution from real space 
        H_pcc, i_p, j_p, dr_pc, abs_dr_p = self.hessian_rspace(atoms, "neighbour-list")

        # Real space contribution
        C_pabab = H_pcc.reshape(-1, 3, 1, 3, 1) * dr_pc.reshape(-1, 1, 3, 1, 1) * dr_pc.reshape(-1, 1, 1, 1, 3)
        C_abab = -C_pabab.sum(axis=0) / (2*atoms.get_volume())

        # Reciprocal space contribution
        C_abab += self.kspace_properties(atoms, prop="Born")

        # Symmetrize elastic constant tensor
        C_abab = (C_abab + C_abab.swapaxes(0, 1) + C_abab.swapaxes(2, 3) + C_abab.swapaxes(0, 1).swapaxes(2, 3)) / 4

        return C_abab

    ###

    def get_stress_contribution_to_elastic_constants(self, atoms):
        """
        Compute the correction to the elastic constants due to non-zero stress in the configuration.
        Stress term  results from working with the Cauchy stress.

        Parameters
        ----------
        atoms: ase.Atoms
            Atomic configuration in a local or global minima.

        """
        
        stress_ab = Voigt_6_to_full_3x3_stress(atoms.get_stress())
        delta_ab = np.identity(3)

        # Term 1
        C1_abab = -stress_ab.reshape(3, 3, 1, 1) * delta_ab.reshape(1, 1, 3, 3)
        C1_abab = (C1_abab + C1_abab.swapaxes(0, 1) + C1_abab.swapaxes(2, 3) + C1_abab.swapaxes(0, 1).swapaxes(2, 3)) / 4

        # Term 2
        C2_abab = (stress_ab.reshape(3, 1, 1, 3) * delta_ab.reshape(1, 3, 3, 1) + \
                   stress_ab.reshape(3, 1, 3, 1) * delta_ab.reshape(1, 3, 1, 3) + \
                   stress_ab.reshape(1, 3, 1, 3) * delta_ab.reshape(3, 1, 3, 1) + \
                   stress_ab.reshape(1, 3, 3, 1) * delta_ab.reshape(3, 1, 1, 3))/4

        return C1_abab + C2_abab
    
    ###

    def get_birch_coefficients(self, atoms):
        """
        Compute the Birch coefficients (Effective elastic constants at non-zero stress). 
        
        Parameters
        ----------
        atoms: ase.Atoms
            Atomic configuration in a local or global minima.

        """
        if self.atoms is None:
            self.atoms = atoms

        # Born (affine) elastic constants
        calculator = atoms.get_calculator()
        bornC_abab = calculator.get_born_elastic_constants(atoms)

        # Stress contribution to elastic constants
        stressC_abab = calculator.get_stress_contribution_to_elastic_constants(atoms)

        return bornC_abab + stressC_abab

    ###

    def get_non_affine_contribution_to_elastic_constants(self, atoms, eigenvalues=None, eigenvectors=None, pc_parameters=None, cg_parameters={"x0": None, "tol": 1e-5, "maxiter": None, "M": None, "callback": None, "atol": 1e-5}):
        """
        Compute the correction of non-affine displacements to the elasticity tensor.
        The computation of the occuring inverse of the Hessian matrix is bypassed by using a cg solver.

        If eigenvalues and and eigenvectors are given the inverse of the Hessian can be easily computed.

        Parameters
        ----------
        atoms: ase.Atoms
            Atomic configuration in a local or global minima.

        eigenvalues: array
            Eigenvalues in ascending order obtained by diagonalization of Hessian matrix.
            If given, use eigenvalues and eigenvectors to compute non-affine contribution. 

        eigenvectors: array
            Eigenvectors corresponding to eigenvalues.

        cg_parameters: dict
            Dictonary for the conjugate-gradient solver.

            x0: {array, matrix}
                Starting guess for the solution.

            tol/atol: float, optional
                Tolerances for convergence, norm(residual) <= max(tol*norm(b), atol).

            maxiter: int
                Maximum number of iterations. Iteration will stop after maxiter steps even if the specified tolerance has not been achieved.

            M: {sparse matrix, dense matrix, LinearOperator}
                Preconditioner for A.
                
            callback: function  
                User-supplied function to call after each iteration.

        pc_parameters: dict
            Dictonary for the incomplete LU decomposition of the Hessian.

            A: array_like
                Sparse matrix to factorize.

            drop_tol: float
                Drop tolerance for an incomplete LU decomposition.

            fill_factor: float
                Specifies the fill ratio upper bound.

            drop_rule: str
                Comma-separated string of drop rules to use.

            permc_spec: str
                How to permute the columns of the matrix for sparsity.

            diag_pivot_thresh: float
                Threshold used for a diagonal entry to be an acceptable pivot.

            relax: int
                Expert option for customizing the degree of relaxing supernodes.

            panel_size: int
                Expert option for customizing the panel size.

            options: dict 
                Dictionary containing additional expert options to SuperLU.
        """

        nat = len(atoms)

        calc = atoms.get_calculator()    

        if (eigenvalues is not None) and (eigenvectors is not None):
            naforces_icab = calc.get_nonaffine_forces(atoms)

            G_incc = (eigenvectors.T).reshape(-1, 3*nat, 1, 1) * naforces_icab.reshape(1, 3*nat, 3, 3)
            G_incc = (G_incc.T / np.sqrt(eigenvalues)).T
            G_icc  = np.sum(G_incc, axis=1)
            C_abab = np.sum(G_icc.reshape(-1,3,3,1,1) * G_icc.reshape(-1,1,1,3,3), axis=0)

        else:
            H_nn = calc.get_hessian(atoms)
            naforces_icab = calc.get_nonaffine_forces(atoms)

            if pc_parameters != None:
                # Transform H to csc 
                H_nn = H_nn.tocsc()

                # Compute incomplete LU 
                approx_Hinv = spilu(H_nn, **pc_parameters)
                operator_Hinv = LinearOperator(H_nn.shape, approx_Hinv.solve)
                cg_parameters["M"] = operator_Hinv

            D_iab = np.zeros((3*nat, 3, 3))
            for i in range(3):
                for j in range(3):
                    x, info = cg(H_nn, naforces_icab[:, :, i, j].flatten(), **cg_parameters)
                    if info != 0:
                        print("info: ", info)
                        raise RuntimeError(" info > 0: CG tolerance not achieved, info < 0: Exceeded number of iterations.")
                    D_iab[:,i,j] = x

            C_abab = np.sum(naforces_icab.reshape(3*nat, 3, 3, 1, 1) * D_iab.reshape(3*nat, 1, 1, 3, 3), axis=0)
        
        # Symmetrize 
        C_abab = (C_abab + C_abab.swapaxes(0, 1) + C_abab.swapaxes(2, 3) + C_abab.swapaxes(0, 1).swapaxes(2, 3)) / 4             

        return -C_abab / atoms.get_volume()

    ###

    def get_derivative_volume(self, atoms, d=1e-6):
        """
        Calculate the change of volume with strain using central differences
        """
        nat = len(atoms)
        cell = atoms.cell.copy()
        vol = np.zeros((3,3))

        for i in range(3):
            # Diagonal 
            x = np.eye(3)
            x[i, i] += d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            Vplus = atoms.get_volume()

            x[i, i] -= 2 * d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            Vminus = atoms.get_volume()

            derivative_volume = (Vplus - Vminus) / (2 * d)

            vol[i, i] = derivative_volume

            # Off diagonal
            j = i - 2
            x[i, j] = d
            x[j, i] = d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            Vplus = atoms.get_volume()

            x[i, j] = -d
            x[j, i] = -d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            Vminus = atoms.get_volume()

            derivative_volume = (Vplus - Vminus) / (4 * d)
            vol[i, j] = derivative_volume
            vol[j, i] = derivative_volume


        return vol

    ###

    def get_derivative_wave_vector(self, atoms, d=1e-6):
        """
        Calculate the change of volume with strain using central differences
        """
        nat = len(atoms)
        cell = atoms.cell.copy()
        
        initial_k = 2 * np.pi * np.dot(np.linalg.inv(cell), np.array([1,1,1]))
        print("Wave vector for n=(1,1,1): ", initial_k)

        def_k = np.zeros((3,3,3))

        for i in range(3):
            # Diagonal 
            x = np.eye(3)
            x[i, i] += d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            k_pos = 2 * np.pi * np.dot(np.linalg.inv(atoms.get_cell()), np.array([1,1,1]))

            x[i, i] -= 2 * d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            k_minus = 2 * np.pi * np.dot(np.linalg.inv(atoms.get_cell()), np.array([1,1,1]))
            derivative_k = (k_pos - k_minus) / (2 * d)
            def_k[:, i, i] = derivative_k

            # Off diagonal --> xy, xz, yz
            j = i - 2
            x[i, j] = d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            scaled_nbk = np.dot(np.array(np.abs(cell)), np.array([1,1,1]))
            k_pos = 2 * np.pi * np.dot(np.linalg.inv(atoms.get_cell()), np.array([1,1,1]))

            x[i, j] = -d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            k_minus = 2 * np.pi * np.dot(np.linalg.inv(atoms.get_cell()), np.array([1,1,1]))

            derivative_k = (k_pos - k_minus) / (2 * d)
            def_k[:, i, j] = derivative_k

            # Odd diagonal --> yx, zx, zy
            x[j, i] = d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            k_pos = 2 * np.pi * np.dot(np.linalg.inv(atoms.get_cell()), np.array([1,1,1]))

            x[j, i] = -d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            k_minus = 2 * np.pi * np.dot(np.linalg.inv(atoms.get_cell()), np.array([1,1,1]))

            derivative_k = (k_pos - k_minus) / (2 * d)
            def_k[:, j, i] = derivative_k

        return def_k


    ###

    def get_numerical_non_affine_forces(self, atoms, d=1e-6):
        """

        Calculate numerical non-affine forces using central finite differences.
        This is done by deforming the box, rescaling atoms and measure the force.

        Parameters
        ----------
        atoms: ase.Atoms
            Atomic configuration in a local or global minima.

        """

        nat = len(atoms)
        cell = atoms.cell.copy()
        fna_ncc = np.zeros((nat, 3, 3, 3))

        for i in range(3):
            # Diagonal 
            x = np.eye(3)
            x[i, i] += d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            fplus = atoms.get_forces()

            x[i, i] -= 2 * d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            fminus = atoms.get_forces()

            naForces_ncc = (fplus - fminus) / (2 * d)
            fna_ncc[:, 0, i, i] = naForces_ncc[:, 0]
            fna_ncc[:, 1, i, i] = naForces_ncc[:, 1]
            fna_ncc[:, 2, i, i] = naForces_ncc[:, 2]

            # Off diagonal
            j = i - 2
            x[i, j] = d
            x[j, i] = d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            fplus = atoms.get_forces()

            x[i, j] = -d
            x[j, i] = -d
            atoms.set_cell(np.dot(cell, x), scale_atoms=True)
            fminus = atoms.get_forces()

            naForces_ncc = (fplus - fminus) / (4 * d)
            fna_ncc[:, 0, i, j] = naForces_ncc[:, 0]
            fna_ncc[:, 0, j, i] = naForces_ncc[:, 0]
            fna_ncc[:, 1, i, j] = naForces_ncc[:, 1]
            fna_ncc[:, 1, j, i] = naForces_ncc[:, 1]
            fna_ncc[:, 2, i, j] = naForces_ncc[:, 2]
            fna_ncc[:, 2, j, i] = naForces_ncc[:, 2]

        return fna_ncc
