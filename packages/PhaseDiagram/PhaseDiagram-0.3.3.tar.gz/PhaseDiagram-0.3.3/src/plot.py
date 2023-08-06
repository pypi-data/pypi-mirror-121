# PhaseDiagram main file
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from matplotlib import colors
import warnings

# @param init_points: a numpy array of shape (N, 2). Initial set of points to define the grid.
# @param func:        the phase function. This should accept vectors in the same format as init_points
#                     and return a 1D vector of integers, of size (N,).
# @param num_refinements: The leve lof detail to go to.
# @param ax:         Plotting axes from matplotlib.
# ----------
# Returns: a Delaunay triangulation object, values for each point and and the boundary coordinates
def phase_optimise(init_points, func, num_refinements=4):
    assert init_points.shape[1] == 2
    vals = func(init_points)
    assert vals.shape[0] == init_points.shape[0]
    tri = Delaunay(init_points, incremental=True)
    boundary = []
    for n in range(num_refinements):
        print("Optimising: n=%d" % (n+1))
        vals, boundary = d_phase_optimise(tri, vals, func)
        if len(boundary) == 0:
            print('No phase boundaries found.')
            break
    
    return tri, vals, boundary
    


def d_phase_optimise(tri, vals, func):
    boundary = []
    for simplex in tri.simplices:
        x = vals[simplex]
        if not np.all(x == x[0]):
            boundary.append(np.mean(tri.points[simplex],axis=0))
#         if x[0] != x[1]:
#             boundary.append(0.5*(tri.points[simplex][0] + tri.points[simplex][1]))
#         if x[0] != x[2]:
#             boundary.append(0.5*(tri.points[simplex][0] + tri.points[simplex][2]))
#         if x[1] != x[2]:
#             boundary.append(0.5*(tri.points[simplex][1] + tri.points[simplex][2]))

    vals = np.append(vals, func(np.array(boundary)))

    tri.add_points(boundary)

    return vals, boundary
    


def genradgrid(n_radii, n_angles, max_radius=1, min_radius=None):
    if min_radius is None:
        min_radius = max_radius/100
        
    radii = np.linspace(min_radius, max_radius, n_radii)

    angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
    angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
    angles[:, 1::2] += np.pi / n_angles

    return np.vstack(((radii * np.cos(angles)).flatten(), (radii * np.sin(angles)).flatten())).T
    
# Deneral purpose phase diagram plotting
# @param phase_func - accepts 1 vectorised inputs e.g. F([[x1,y1],[x2,y2],...]) and returns an integer between 0 and N-1, where N is the number of named phases
# @param phase_names - a list of length N for labelling the phases
# @param init_points - an initial list of [ [J1,J2], ... ] 
# @param num_refinements - number of subtriangulations to calculate
# @param cmap - matplotlib colormap
# @param show_boundary - one of:
#                        + dict of keyword arguments for the call to plt.plot() on how to style the phase boundary
#                        + True to show default style
#                        + None or False to hide phase boundary plotting
# @param show_triangulation - one of:
#                        + dict of keyword arguments for the call to plt.plot() on how to style the traingulation
#                        + True to show default style
#                        + None or False to hide traingulation
    
def plot_phasedia(phase_func, phase_names, init_points, num_refinements=6, cmap='Pastel2',
                  show_boundary=True, show_triangulation=None):
    t,v,b = phase_optimise(init_points, phase_func, num_refinements=num_refinements)
    d_plot_phasedia(t,v,b, phase_names, cmap, show_boundary, show_triangulation)



def d_plot_phasedia(tri, vals, boundary, phase_names, cmap='Pastel2',
                  show_boundary=True,
                  show_triangulation=None):
    # define boundaries for the colormap
    bounds = np.arange(len(phase_names)+1,dtype=np.float64)-0.5
    norm = colors.BoundaryNorm(bounds, len(bounds))

    fig, ax= plt.subplots()

    
    c = ax.tripcolor(tri.points[:,0], tri.points[:,1], tri.simplices, vals, cmap=cmap, norm=norm)
    
    ##########################
    # Format the triangulation (good intellectual honesty to show this, it removes ambiguity as to which points were evaluated)
    if show_triangulation is not None:
        if type(show_triangulation) is not dict:
            ax.triplot(tri.points[:,0], tri.points[:,1], tri.simplices, color='w',lw=0.2)
        elif show_triangulation is not False:
            ax.triplot(tri.points[:,0], tri.points[:,1], tri.simplices, **show_triangulation)
    
#     #######################
    # format the colorbar
    cbar = fig.colorbar(c, location='right',aspect=14)
    cbar.ax.get_yaxis().set_ticks([])
    bounds = cbar.ax.get_ylim()
    x = 0.5*(cbar.ax.get_xlim()[0] + cbar.ax.get_xlim()[1])
    
    for j, name in enumerate(phase_names):
        cbar.ax.text(x, j , name, ha='center', va='center')

    # Plot the phase boundaries in another colour to hide the ugly interpolated colouring
    if show_boundary is not None:
        if len(boundary)==0:
            warnings.warn('There is no boundary to show!')
        elif type(show_boundary) is dict:
            X, Y = np.array(boundary).T
            ax.plot(X, Y, **show_boundary)
        elif show_boundary is not False:
            sb = {'color':'white', 'ms':3, 'marker': '.', 'linestyle':'None'}
            X, Y = np.array(boundary).T
            ax.plot(X, Y, **sb)
    
    return fig, ax
    
        

        
