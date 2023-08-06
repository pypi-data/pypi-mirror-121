# -*- coding: utf-8 -*-

# Copyright (C) 2010-2021 The PyStar project
#
# This file is part of PyStar.
#
# PyStar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyStar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import operator
from typing import List
import numpy as np
import warnings


def dir_init(obj, path: str="") -> str:
    """
    Create folders and
    :param obj: instance
    :return: saving_data_path
    """
    if not path: path = os.path.abspath(os.curdir)
    mpath = path + '/data/' + obj.general_system_name + '/' + obj.system_name + '/'
    if not os.path.exists(mpath): os.makedirs(mpath)
    return mpath


def test_overlap(testposition: np.array, other_positions:np.array, rmin: float) -> bool:
    for other_position in other_positions:
        if np.linalg.norm(testposition - other_position) < rmin: return True
    return False


def random_vector_on_circle() -> np.array:
    """ return a random vector on a circe of unit length in cartesian coordinates.
The output is a numpy array with shape (2,)."""
    theta: float = np.random.random() * 2.0 * np.pi
    return np.array([np.cos(theta), np.sin(theta)])


def random_vector_on_sphere() -> np.array:
    """ return a random vector on a shpere of unit length in cartesian coordinates.
The output is a numpy array with shape (3,).

Algorim from:
(1) Allen, M. P.; Tildesley, D. J. Computer Simulation of Liquids; Oxford University Press, USA,
    1987.
(2) Marsaglia, G. Choosing a Point from the Surface of a Sphere. The Annals of Mathematical
    Statistics 1972, 43 (2), 645–646. https://doi.org/10.1214/aoms/1177692644.
"""
    while True:
        xi  = np.random.random(2)
        zeta = 1 - 2 * xi
        zetas = np.sum(np.power(zeta, 2.0))
        if zetas < 1:
            zetasqrt = np.sqrt(1 - zetas)
            return np.array(
                [2.0 * zeta[0] * zetasqrt, 2.0 * zeta[1] * zetasqrt, 1.0 - 2.0 * zetas]
            )


class PositionError(LookupError):
    """raise this error when you failed to generate a position"""


def adaptive_position_generator(function, value_start: float, value_break: float, key: str = "rmin", factor: float = 0.9, **args):
    """The function takes some initial value (<value_start>) for the parameter with name <key>, and
    tries to generate particle positions with the function <function>. The other parameters for the
    function call can be given as the <**args> keyword arguments. If the generation of the particle
    positions fails, then it will multiply the value with <factor>, and try again. This is repeated,
    untill either the positions are successfully generated, or untill the value used breaches
    <value_break>.

    Factor has to be non-negative and not equal to one.
    """
    if key in args:
        warnings.warn(
            "You passed the parameter {0}, but you specified this {0} to be varied.".format(key) +
            "\n The parameter {} = {} you passed will be ignored.".format(key, args[key]) +
            "\n Instead {} will be varied between {} and {}.".format(key, value_start, value_break),
            Warning
        )
        del args[key]

    if factor <= 0.0:
        raise ValueError(
            "You passed a factor of {}.".format(factor),
            "Factor needs to be non-negative"
            )

    if factor > 1.0:   comp = operator.gt
    elif factor < 1.0: comp = operator.lt
    else:
        raise ValueError(
            "You passed a factor of {}.".format(factor),
            "Factor can not be 1.0"
            )

    if not comp(value_break, value_start):
        raise ValueError(
            "You passed a factor of {}.".format(factor),
            "You passed a value_start of {}.".format(value_start),
            "You passed a value_break of {}.".format(value_break),
            "Can not breach value_break by muliplying value_start with factor repeatedly"
            )
    value = value_start
    while comp(value_break, value):
        try:
            positions = function(**{key: value}, **args)
        except PositionError:
            value *= factor
            print("value {} is set to {}".format(key, value))
        else:
            return positions
    raise PositionError("Failed to set random particles using {}".format(function.__name__))


def random_pos(
    N:     int, 
    box_l: float, 
    rmin:  float,
     occ_positions: List = [], maxtry: int = 1000, TwoD: bool = True, fix_z: float = 1.0):
    """generate overlap free random positions"""
    set_pos = []
    for ipos in range(N):
        itry = 0
        while True:
            pos = np.random.rand(1, 3) * box_l
            if TwoD:
                pos[:, 2] = fix_z
            if not test_overlap(pos, set_pos + occ_positions, rmin):
                break
            itry += 1
            if itry >= maxtry:
                raise PositionError("Failed to set random particle {}".format(ipos))
        set_pos += [pos]
    return [pos[0] for pos in set_pos]


def self_avoiding_random_chain(
    N:     int , 
    box_l: float, 
    rmin:  float, 
    bondl: float , 
    occ_positions: List = [], maxtry: int = 1000, TwoD: bool = False, fix_z: float =1.0):
    """ generate a self avoinding walk of N steps in a box of size box_l
* rmin gives the minimum distance between beads in the system
* bondl defines the step length of the self avoiding walk
    * bondl has to be larger than rmin
* pass the positions which are already occupied as a list of vectors in occ_positions (default [])
* define the number of tries to set a particle with maxtry (default = 1000)
* you can generate a chain in 2D (fixed z-coordinate) by setting TwoD = True (default False).
    * Specify the value of the fixed z-coordinate with the parmeter fix_z (default 1.0)
"""
    itry: int = 0
    set_pos = []
    if rmin >= bondl:
        raise ValueError(
            "You passed bondl = {} and rmin = {} to self_avoiding_random_chain.".format(bondl, rmin)
            + "But bondl needs to be larger than rmin"
        )
    while len(set_pos) < N:
        set_pos = random_pos(1, box_l, rmin, occ_positions, maxtry, TwoD, fix_z)
        for ipos in range(1, N):
            set_part = False
            for jtry in range(maxtry):
                if TwoD: pos = np.append(set_pos[ipos - 1][0:2] + random_vector_on_circle()*bondl, fix_z)
                else:    pos = set_pos[ipos - 1] + random_vector_on_sphere() * bondl
                if not np.any(np.asarray(pos) > box_l):
                    if not test_overlap(pos, set_pos + occ_positions, rmin):
                        set_part = True
                        break
            if set_part: set_pos += [pos]
            else:
                print(set_pos, pos)
                raise PositionError("Failed to set random chain at particle {} at try {}".format(ipos, jtry))
        itry += 1
        if itry >= maxtry: raise PositionError("Failed to set random chain at particle")
    return set_pos


def prepare_output_energy(obj, path: str = "") -> None:
    """
    Create header for output file of energy
    :return:
    """
    with open(path + str(obj.system_name) + "_energy.dat", "a") as in_file:
        in_file.write("# (1) System time (2) Total Energy (3) Kinetic Energy (4) Potential Energy" + "\n")


def prepare_output_pressure(obj, path: str = "") -> None:
    """
    Create header for output file of pressure
    :return:
    """
    with open(path + str(obj.system_name) + "_pressure.dat", "a") as in_file:
        in_file.write("# (1) System time (2) Total Pressure" + "\n")


def save_particle_positions(obj, path: str = "") -> None:
    with open(path + str(obj.system_name) + "_particles_positions.xyz", "a") as in_file:
        in_file.write(str(len(obj.particles_info) + 1) + "\n"); in_file.write('')
        for part in obj.particles_info:
            in_file.write(
                '{} {} {} {}\n'.format(
                    part[1],
                    part[2][0],
                    part[2][1],
                    part[2][2])
            )


def save_energy(obj, path: str = "") -> None:
    with open(path + str(obj.system_name) + "_energy.dat", "a") as in_file:
        in_file.write('{} {} {} {} \n'.format(obj.time_simulation,
                                              obj.total_energy, obj.kinetic_energy, obj.total_energy-obj.kinetic_energy))


def save_pressure(obj, path: str = "") -> None:
    with open(path + str(obj.system_name) + "_pressure.dat", "a") as in_file:
        in_file.write('{} {} \n'.format(obj.time_simulation, obj.pressure))
