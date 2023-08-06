# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from typing import Sequence, Tuple, Union

import miniball as mnbl
import numpy as nmpy
from scipy.spatial.distance import pdist as PairwiseDistances


array_t = nmpy.ndarray


def Simplex(
    dimension: int,
    /,
    *,
    centered: bool = False,
    around: array_t = None,
    with_a_margin: float = None,
    with_m_margin: float = None,
) -> array_t:
    """
    See: https://codegolf.stackexchange.com/questions/152774/create-an-n-dimensional-simplex-tetrahedron
    Answer by PattuX om Jan 8 '18 at 3:54

    Parameters
    ----------
    dimension
    centered
    around
    with_a_margin
    with_m_margin

    Returns
    -------

    """
    output = nmpy.empty((dimension + 1, dimension), dtype=nmpy.float64)

    output[:dimension, :] = nmpy.eye(dimension)
    output[dimension, :] = (1.0 + nmpy.sqrt(dimension + 1.0)) / dimension

    if around is not None:
        if around.shape[1] != dimension:
            raise ValueError(f"{around.shape[1]}: Invalid dimension of point set \"around\"; Expected={dimension}")

        nmpy.subtract(output, nmpy.mean(output, axis=0, keepdims=True), out=output)
        radius = nmpy.mean(nmpy.linalg.norm(output, axis=1))

        target_center, target_squared_radius = mnbl.get_bounding_ball(around)
        target_radius = nmpy.sqrt(target_squared_radius)

        if with_a_margin is not None:
            radius_scaling = (with_a_margin + target_radius) / radius
        elif with_m_margin is not None:
            radius_scaling = with_m_margin * target_radius / radius
        else:
            radius_scaling = target_radius / radius
        nmpy.multiply(output, radius_scaling, out=output)

        nmpy.add(output, target_center.reshape(1, dimension), out=output)
    elif centered:
        nmpy.subtract(output, nmpy.mean(output, axis=0, keepdims=True), out=output)

    return output


def IsARegularSimplex(
    check: array_t,
    /,
    *,
    tolerance: float = nmpy.finfo(nmpy.float).eps,
    return_issues: bool = False,
) -> Union[bool, Tuple[bool, Sequence[str]]]:
    """"""
    valid = True
    issues = []

    shape = check.shape
    if shape[1] != shape[0] - 1:
        valid = False
        issues.append(
            f"{shape}: Invalid vertex matrix dimension; "
            f"Expected={shape[0]+1}x{shape[0]} or {shape[1]}x{shape[1]-1}"
        )

    distances = PairwiseDistances(check)
    min_distance = nmpy.min(distances)
    max_distance = nmpy.max(distances)
    if max_distance - min_distance > tolerance:
        valid = False
        issues.append(
            f"[{min_distance},{max_distance}]: "
            f"Interval of pairwise distances larger than tolerance ({tolerance})"
        )

    if return_issues and not valid:
        return False, issues

    return valid
