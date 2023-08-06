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

import matplotlib.pyplot as pypl
import miniball as mnbl
import numpy as nmpy
from matplotlib.patches import Circle as circle_t
from scipy.spatial import ConvexHull as convex_hull_t
from scipy.spatial import convex_hull_plot_2d as Plot2DConvexHull

import rn_simplex.simplex as smpx


print("--- Simplices")
for dimension in (2, 3, 4):
    simplex = smpx.Simplex(dimension)
    assert smpx.IsARegularSimplex(simplex)
    print(simplex)

print("--- Not a Simplex")
not_a_simplex = nmpy.random.random((3, 3))
_, issues = smpx.IsARegularSimplex(not_a_simplex, return_issues=True)
print(not_a_simplex)
for issue in issues:
    print(issue)

print("--- Simplex around point set")
half_n_points = 100
side = 100
margin = 10
min_stddev = int(side / 10)

point_sets = []
for _ in range(2):
    point_sets.append(
        nmpy.random.normal(
            loc=nmpy.random.randint(margin, high=side - margin, size=2),
            scale=nmpy.random.randint(min_stddev, high=2 * min_stddev),
            size=(half_n_points, 2),
        )
    )
point_set = nmpy.vstack(point_sets)

simplex = smpx.Simplex(2, around=point_set, with_m_margin=0.2)

hull = convex_hull_t(points=simplex)
center, squared_radius = mnbl.get_bounding_ball(point_set)
radius = nmpy.sqrt(squared_radius)

print(simplex)
print(center, radius)

_, axes = pypl.subplots()
axes.scatter(point_set[:, 0], point_set[:, 1], c="r", marker="x", s=25)

circle = circle_t(center, radius=radius, facecolor="none", edgecolor="blue")
axes.add_artist(circle)

Plot2DConvexHull(hull, ax=axes)

simplex_bounds_min = nmpy.min(simplex, axis=0)
simplex_bounds_max = nmpy.max(simplex, axis=0)
axes.set_xlim(
    min(center[0] - radius, simplex_bounds_min[0]),
    max(center[0] + radius, simplex_bounds_max[0]),
)
axes.set_ylim(
    min(center[1] - radius, simplex_bounds_min[1]),
    max(center[1] + radius, simplex_bounds_max[1]),
)
axes.set_aspect("equal")

pypl.show()
